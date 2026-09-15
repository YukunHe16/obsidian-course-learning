#!/usr/bin/env python3
"""Rebuild derived summaries only; never write course source vaults."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo
from vault_model import course_fingerprint, frontmatter, progress_questions


def date_value(value):
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def build_summary(vault: Path, timezone: str, now: dt.datetime | None = None) -> str:
    now = now or dt.datetime.now(ZoneInfo(timezone))
    today = now.date()
    profile = frontmatter(vault / "Course.md")
    notes = [(p, frontmatter(p)) for p in sorted(vault.rglob("*.md"))
             if "templates" not in p.relative_to(vault).parts and "raw" not in p.relative_to(vault).parts]
    deadlines = [d for _, d in notes if d.get("type") == "deadline" and d.get("status") == "pending"]
    exact = [(date_value(d.get("due_date")), d) for d in deadlines
             if d.get("date_status") == "exact" and date_value(d.get("due_date"))]
    future = sorted([(date, d) for date, d in exact if date >= today], key=lambda x: x[0])
    upcoming = sum(today <= date <= today + dt.timedelta(days=14) for date, _ in exact)
    overdue = sum(date < today for date, _ in exact)
    last_session = max((date_value(d.get("date")) for _, d in notes
                        if d.get("type") == "study-session" and date_value(d.get("date"))), default=None)
    lectures = [d for _, d in notes if d.get("type") == "lecture" and d.get("reading_role") == "primary"]
    pending = sum(d.get("status") in {"draft", "pending"} and
                  (d.get("type") in {"lecture", "concept", "question-set"}
                   or "pending" in p.relative_to(vault).parts) for p, d in notes)
    ingest_dates = [date_value(d.get("ingested_at")) for d in lectures]
    manifest = vault / "raw" / "manifest.md"
    if manifest.exists():
        ingest_dates += [date_value(m) for m in
                         re.findall(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|", manifest.read_text())]
    exams = [date for date, d in future if d.get("deadline_kind") == "exam"]
    exams += [date for x in (profile.get("exam_dates") or []) if
              (date := date_value(x)) and date >= today]
    course_id = profile["course_id"]
    uri = "obsidian://open?path=" + quote(str(vault / "Home.md"), safe="")
    fields = {
        "type": "course-summary", "course_id": course_id, "title": profile.get("title", course_id),
        "term": profile.get("term"), "status": profile.get("status", "active"), "review_mode": "on-demand",
        "lecture_count": len(lectures), "pending_count": pending,
        "open_question_count": sum(not done for done, _ in progress_questions(vault / "learning" / "Progress.md")),
        "upcoming_deadline_count": upcoming, "overdue_deadline_count": overdue,
        "next_deadline": future[0][0] if future else None,
        "next_deadline_title": future[0][1].get("title") if future else None,
        "next_exam": min(exams) if exams else None,
        "last_ingested": max((d for d in ingest_dates if d), default=None),
        "last_studied": last_session, "source_fingerprint": course_fingerprint(vault),
        "source_fingerprint_method": "sha256-relative-path-nul-bytes-nul-v2",
        "as_of_date": today.isoformat(), "timezone": timezone,
        "generated_at": now.isoformat(timespec="seconds"), "vault_path": str(vault), "obsidian_uri": uri,
    }
    out = "---\n"
    for key, value in fields.items():
        if isinstance(value, dt.date):
            value = value.isoformat()
        out += f"{key}: " + ("" if value is None else json.dumps(value, ensure_ascii=False)) + "\n"
    out += f"---\n\n# {course_id} · 课程总览\n\n"
    out += f"主讲义 {len(lectures)} 篇，资料待核验 {pending} 项。待澄清问题来自真实学习记录，不由旧分数推算。\n\n"
    out += f"按本地记录，截至 {today.isoformat()}，未来 14 天有 {upcoming} 个定日节点，{overdue} 个过去日期仍为 pending；不代表已确认未完成。未刷新官网。\n\n"
    out += f"[打开课程]({uri}) · [阅读路线](obsidian://open?path={quote(str(vault / 'wiki' / 'index.md'), safe='')})"
    if (vault / "learning" / "Progress.md").exists():
        out += f" · [学习位置与疑问](obsidian://open?path={quote(str(vault / 'learning' / 'Progress.md'), safe='')})"
    return out + "\n"


def write_summary(path: Path, content: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    normalize = lambda s: re.sub(r"^generated_at:.*\n", "", s, flags=re.M)
    if normalize(old) == normalize(content):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError(f"Refusing symlink output: {path}")
    fd, name = tempfile.mkstemp(prefix=".summary-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--semester-root", type=Path, required=True)
    parser.add_argument("--course-id")
    args = parser.parse_args()
    root = args.semester_root.expanduser().resolve()
    if args.course_id and not re.fullmatch(r"[A-Z][A-Z0-9-]{1,31}", args.course_id):
        parser.error("Invalid course id")
    timezone = frontmatter(root / "semester.md").get("timezone", "America/Chicago")
    if any(p.is_symlink() for p in [root / "Overview", root / "Overview" / "courses"]):
        parser.error("Overview output directories must not be symlinks")
    courses = sorted(p for p in (root / "Courses").iterdir()
                     if p.is_dir() and (p / "Course.md").is_file())
    if args.course_id:
        courses = [p for p in courses if p.name == args.course_id]
        if not courses:
            parser.error("Course not found")
    outputs = []
    for vault in courses:
        if vault.is_symlink() or frontmatter(vault / "Course.md").get("course_id") != vault.name:
            parser.error(f"Invalid course vault: {vault}")
        outputs.append((root / "Overview" / "courses" / (vault.name + ".md"),
                        build_summary(vault, timezone)))
    changed = sum(write_summary(path, text) for path, text in outputs)
    print(f"courses={len(outputs)} updated={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
