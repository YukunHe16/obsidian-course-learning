#!/usr/bin/env python3
"""Validate a multi-course semester workspace and its Obsidian vaults."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any
from vault_model import frontmatter, scalar, sha256, links, resolve_link, progress_questions, course_fingerprint


LINK_RE = re.compile(r"\[\[([^\]#|]+)")
REQUIRED_ROOT = ["Index.md", "semester.md", "Overview/Index.md", "Overview/Home.md", "Overview/views/Semester.base", "Courses"]
# The semester root carries one contract in two entry points: AGENTS.md for Codex, CLAUDE.md for
# Claude Code. A workspace created before dual-agent support has only AGENTS.md, so a single file
# is a warning rather than a blocking error.
AGENT_CONTRACT_FILES = ["AGENTS.md", "CLAUDE.md"]
REQUIRED_COURSE = [
    "Course.md",
    "Index.md",
    "Home.md",
    "raw/manifest.md",
    "wiki/index.md",
    "wiki/log.md",
    "views/Course.base",
    "inbox",
    "raw/lectures",
    "wiki/lectures",
    "wiki/concepts",
    "wiki/course-policies",
    "wiki/pending",
    "learning/deadlines",
    "learning/questions",
    "learning/sessions",
    "templates",
]
DEADLINE_STATUSES = {"pending", "completed", "missed", "waived", "cancelled"}
DEADLINE_VERIFICATION_STATUSES = {"candidate", "verified", "stale", "conflict"}
DEADLINE_DATE_STATUSES = {"exact", "recurring", "unpublished", "section-dependent"}
DEADLINE_KINDS = {
    "homework",
    "assignment",
    "quiz",
    "exam",
    "lab",
    "discussion",
    "project",
    "reading",
    "administrative",
    "recurring",
    "other",
}


def add(issues: list[dict[str, str]], level: str, code: str, path: Path, message: str) -> None:
    issues.append({"level": level, "code": code, "path": str(path), "message": message})


def valid_iso_date(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        dt.date.fromisoformat(value[:10])
    except ValueError:
        return False
    return True


def validate_deadlines(
    course_root: Path,
    course_id: str,
    issues: list[dict[str, str]],
    deadline_ids: dict[str, Path],
) -> None:
    deadline_root = course_root / "learning" / "deadlines"
    if not deadline_root.is_dir():
        return
    for note in deadline_root.glob("*.md"):
        data = frontmatter(note)
        required = {
            "type",
            "course",
            "deadline_id",
            "title",
            "deadline_kind",
            "date_status",
            "status",
            "verification_status",
        }
        missing = sorted(required - data.keys())
        if missing:
            add(issues, "error", "deadline-schema", note, f"Missing properties: {', '.join(missing)}")
            continue
        if data.get("type") != "deadline" or data.get("course") != course_id:
            add(issues, "error", "deadline-schema", note, "Deadline type/course does not match the vault")

        deadline_id = data.get("deadline_id")
        if not isinstance(deadline_id, str) or not deadline_id.startswith(course_id + "/deadline/"):
            add(issues, "error", "deadline-id", note, "deadline_id must use the course/deadline namespace")
        elif deadline_id in deadline_ids:
            add(issues, "error", "duplicate-deadline-id", note, f"Also defined in {deadline_ids[deadline_id]}")
        else:
            deadline_ids[deadline_id] = note

        if data.get("deadline_kind") not in DEADLINE_KINDS:
            add(issues, "error", "deadline-kind", note, f"Invalid deadline_kind: {data.get('deadline_kind')!r}")
        if data.get("date_status") not in DEADLINE_DATE_STATUSES:
            add(issues, "error", "deadline-date-status", note, f"Invalid date_status: {data.get('date_status')!r}")
        if data.get("status") not in DEADLINE_STATUSES:
            add(issues, "error", "deadline-status", note, f"Invalid status: {data.get('status')!r}")
        if data.get("verification_status") not in DEADLINE_VERIFICATION_STATUSES:
            add(
                issues,
                "error",
                "deadline-verification-status",
                note,
                f"Invalid verification_status: {data.get('verification_status')!r}",
            )

        due_date = data.get("due_date")
        if data.get("date_status") == "exact" and not valid_iso_date(due_date):
            add(issues, "error", "deadline-date", note, "An exact deadline requires an ISO due_date")
        elif due_date is not None and not valid_iso_date(due_date):
            add(issues, "error", "deadline-date", note, "due_date must be an ISO date or empty")

        release_date = data.get("release_date")
        if release_date is not None and not valid_iso_date(release_date):
            add(issues, "error", "deadline-date", note, "release_date must be an ISO date or empty")

        due_time = data.get("due_time")
        if due_time is not None:
            if not isinstance(due_time, str) or not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", due_time):
                add(issues, "error", "deadline-time", note, "due_time must use 24-hour HH:MM or be empty")
            if not valid_iso_date(due_date):
                add(issues, "error", "deadline-time", note, "due_time requires due_date")
            if not isinstance(data.get("timezone"), str) or not data["timezone"].strip():
                add(issues, "error", "deadline-timezone", note, "due_time requires an explicit timezone")

        source_path = data.get("source_path")
        official_url = data.get("official_url")
        if source_path is not None:
            if not isinstance(source_path, str) or not source_path.strip():
                add(issues, "error", "deadline-source", note, "source_path must be a non-empty relative path")
            else:
                source = (course_root / source_path).resolve()
                try:
                    source.relative_to(course_root.resolve())
                except ValueError:
                    add(issues, "error", "deadline-source", note, "source_path must stay inside the course vault")
                else:
                    if not source.is_file():
                        add(issues, "error", "deadline-source", note, f"Source file does not exist: {source_path}")
        if official_url is not None and (
            not isinstance(official_url, str) or not re.match(r"^https?://", official_url)
        ):
            add(issues, "error", "deadline-source", note, "official_url must be HTTP(S) or empty")

        if data.get("verification_status") == "verified":
            missing_evidence: list[str] = []
            if not source_path and not official_url:
                missing_evidence.append("source_path or official_url")
            if not isinstance(data.get("source_locator"), str) or not data["source_locator"].strip():
                missing_evidence.append("source_locator")
            if not valid_iso_date(data.get("verified_at")):
                missing_evidence.append("verified_at")
            if missing_evidence:
                add(
                    issues,
                    "error",
                    "deadline-evidence",
                    note,
                    f"Verified deadline needs: {', '.join(missing_evidence)}",
                )


def resolve_links(vault: Path, issues: list[dict[str, str]]) -> None:
    for note in vault.rglob("*.md"):
        if any(part in {"templates", "raw"} or part.startswith(".") for part in note.relative_to(vault).parts):
            continue
        for target in links(note.read_text(encoding="utf-8")):
            if target.startswith(("http:", "https:", "obsidian:")):
                continue
            _, problem = resolve_link(vault, note, target)
            if problem:
                add(issues, "warning", problem, note, f"Unresolved reference: {target}")


def validate_reading(vault: Path, issues: list[dict[str, str]]) -> None:
    profile = frontmatter(vault / "Course.md")
    version = profile.get("schema_version", 1)
    if type(version) is not int or version not in {1, 2}:
        add(issues, "error", "schema-version", vault / "Course.md", "Supported schema versions: 1, 2")
        return
    if version < 2:
        return
    progress = vault / "learning" / "Progress.md"
    if not progress.exists():
        add(issues, "error", "missing-progress", progress, "Schema v2 requires the progress page")
    else:
        data = frontmatter(progress)
        if data.get("type") != "learning-progress" or data.get("course") not in {None, profile.get("course_id")}:
            add(issues, "error", "progress-schema", progress, "Progress must belong to this course")
        resume = data.get("resume_link")
        if resume:
            targets = links(str(resume))
            if len(targets) != 1 or resolve_link(vault, progress, targets[0])[1]:
                add(issues, "error", "progress-link", progress, "Resume link must resolve to one lecture/section")
            else:
                dest, _ = resolve_link(vault, progress, targets[0])
                if not dest or frontmatter(dest).get("type") != "lecture":
                    add(issues, "error", "progress-link", progress, "Resume target must be a lecture")
            if not valid_iso_date(data.get("updated_at")):
                add(issues, "error", "progress-date", progress, "A saved position requires updated_at")
        for _, body in progress_questions(progress):
            refs = links(body)
            evidence = [resolve_link(vault, progress, ref)[0] for ref in refs]
            if not any(p and p.suffix == ".md" and frontmatter(p).get("type") == "study-session" for p in evidence):
                add(issues, "error", "progress-evidence", progress, "Each question needs session evidence")
    route = vault / "wiki" / "index.md"
    route_links = links(route.read_text()) if route.exists() else []
    destinations = {dest for ref in route_links if (dest := resolve_link(vault, route, ref)[0])}
    primaries = {}
    for note in vault.rglob("*.md"):
        if any(x in {"templates", "raw", ".obsidian"} for x in note.relative_to(vault).parts):
            continue
        data = frontmatter(note)
        kind = data.get("type")
        if kind == "lecture" and data.get("reading_role") == "primary":
            key = (data.get("lecture_no"), data.get("lecture_part"))
            if key in primaries:
                add(issues, "error", "duplicate-primary", note, f"Also primary: {primaries[key]}")
            primaries[key] = note
            if note not in destinations:
                add(issues, "error", "missing-reading-entry", note, "Primary lecture is missing from wiki/index")
        if kind in {"lecture", "concept", "question-set"} and data.get("status") == "active":
            if not valid_iso_date(data.get("checked_at")):
                add(issues, "error", "checked-date", note, "Active v2 learning notes need checked_at")
            raw_refs = [ref for ref in links(note.read_text()) if ref.startswith("raw/") and "#page=" in ref]
            if kind in {"lecture", "concept"} and not any(resolve_link(vault, note, ref)[1] is None for ref in raw_refs):
                add(issues, "error", "checked-source", note, "Checked note needs a valid local source/page citation")
        if kind in {"concept", "question-set"} and data.get("status") != "superseded":
            returns = data.get("return_to", [])
            if isinstance(returns, str):
                returns = [returns]
            valid_return = False
            for item in returns:
                for ref in links(str(item)):
                    dest, problem = resolve_link(vault, note, ref)
                    if not problem and dest and frontmatter(dest).get("reading_role") == "primary":
                        valid_return = True
            if not valid_return:
                add(issues, "error", "missing-return-link", note, "Reference notes need return_to pointing to a primary lecture")
        if kind == "study-session":
            if not valid_iso_date(data.get("date")):
                add(issues, "error", "session-date", note, "Session needs an actual date")
            if not data.get("evidence_summary"):
                add(issues, "error", "session-evidence", note, "Session needs a brief actual interaction summary")
            refs = links(str(data.get("source_lecture", "")))
            if len(refs) != 1 or resolve_link(vault, note, refs[0])[1]:
                add(issues, "error", "session-lecture", note, "Session lecture reference must resolve")


def validate_course(
    course_root: Path,
    issues: list[dict[str, str]],
    concept_ids: dict[str, Path],
    deadline_ids: dict[str, Path],
) -> str | None:
    for relative in REQUIRED_COURSE:
        path = course_root / relative
        if not path.exists():
            add(issues, "error", "missing-course-item", path, "Required course item is missing")

    profile = frontmatter(course_root / "Course.md") if (course_root / "Course.md").is_file() else {}
    course_id = profile.get("course_id")
    if not isinstance(course_id, str):
        add(issues, "error", "course-profile", course_root / "Course.md", "course_id is missing")
        return None
    if course_id != course_root.name:
        add(issues, "error", "course-profile", course_root / "Course.md", "course_id must match directory name")

    validate_deadlines(course_root, course_id, issues, deadline_ids)

    for note in (course_root / "wiki" / "concepts").glob("*.md"):
        data = frontmatter(note)
        required = {"type", "course", "concept_id", "status"}
        missing = sorted(required - data.keys())
        if missing:
            add(issues, "error", "concept-schema", note, f"Missing properties: {', '.join(missing)}")
            continue
        if data.get("type") != "concept" or data.get("course") != course_id:
            add(issues, "error", "concept-schema", note, "Concept type/course does not match the vault")
        concept_id = data.get("concept_id")
        if not isinstance(concept_id, str) or not concept_id.startswith(course_id + "/"):
            add(issues, "error", "concept-id", note, "concept_id must be namespaced by course_id")
        elif concept_id in concept_ids:
            add(issues, "error", "duplicate-concept-id", note, f"Also defined in {concept_ids[concept_id]}")
        else:
            concept_ids[concept_id] = note
        if "mastery" in data and (type(data["mastery"]) is not int or not 0 <= data["mastery"] <= 4):
            add(issues, "error", "mastery-range", note, "mastery must be an integer from 0 to 4")
        if "review_stage" in data and (type(data["review_stage"]) is not int or not 0 <= data["review_stage"] <= 4):
            add(issues, "error", "review-stage-range", note, "review_stage must be an integer from 0 to 4")

    for note in (course_root / "wiki" / "lectures").glob("*.md"):
        data = frontmatter(note)
        for key in ("type", "course", "lecture_no", "source_pdf", "source_hash", "status"):
            if key not in data:
                add(issues, "error", "lecture-schema", note, f"Missing property: {key}")
        source_value = data.get("source_pdf")
        expected_hash = data.get("source_hash")
        if isinstance(source_value, str):
            source = course_root / source_value
            if not source.is_file():
                add(issues, "error", "missing-source", note, f"Source file does not exist: {source_value}")
            elif isinstance(expected_hash, str) and expected_hash != sha256(source):
                add(issues, "error", "source-hash", note, "Source hash does not match the immutable file")

    validate_reading(course_root, issues)
    resolve_links(course_root, issues)
    return course_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--semester-root", required=True, type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.semester_root.expanduser().resolve()
    issues: list[dict[str, str]] = []
    for relative in REQUIRED_ROOT:
        path = root / relative
        if not path.exists():
            add(issues, "error", "missing-root-item", path, "Required semester item is missing")

    missing_contracts = [name for name in AGENT_CONTRACT_FILES if not (root / name).is_file()]
    if len(missing_contracts) == len(AGENT_CONTRACT_FILES):
        add(
            issues,
            "error",
            "missing-agent-contract",
            root / AGENT_CONTRACT_FILES[0],
            f"The semester root needs {' and '.join(AGENT_CONTRACT_FILES)}",
        )
    else:
        for name in missing_contracts:
            add(
                issues,
                "warning",
                "missing-agent-contract",
                root / name,
                f"{name} is missing; rerun init_semester.py to add it without touching existing files",
            )

    concept_ids: dict[str, Path] = {}
    deadline_ids: dict[str, Path] = {}
    course_ids: set[str] = set()
    courses_dir = root / "Courses"
    if courses_dir.is_dir():
        for course_root in sorted(path for path in courses_dir.iterdir() if path.is_dir()):
            course_id = validate_course(course_root, issues, concept_ids, deadline_ids)
            if course_id:
                course_ids.add(course_id)

    summaries_dir = root / "Overview" / "courses"
    summaries = {path.stem for path in summaries_dir.glob("*.md")} if summaries_dir.is_dir() else set()
    for course_id in sorted(course_ids - summaries):
        add(issues, "error", "missing-summary", summaries_dir / f"{course_id}.md", "Course summary is missing")
    for course_id in sorted(summaries - course_ids):
        add(issues, "warning", "orphan-summary", summaries_dir / f"{course_id}.md", "No matching course vault")

    if summaries_dir.is_dir():
        for course_id in sorted(course_ids & summaries):
            summary = summaries_dir / (course_id + ".md")
            data = frontmatter(summary)
            if data.get("source_fingerprint_method") == "sha256-relative-path-nul-bytes-nul-v2":
                if data.get("source_fingerprint") != course_fingerprint(courses_dir / course_id):
                    add(issues, "warning", "overview-drift", summary, "Rebuild derived summary after course changes")
    resolve_links(root / "Overview", issues)

    errors = sum(issue["level"] == "error" for issue in issues)
    warnings = sum(issue["level"] == "warning" for issue in issues)
    result = {"semester_root": str(root), "courses": sorted(course_ids), "errors": errors, "warnings": warnings, "issues": issues}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"semester_root={root}")
        print(f"courses={','.join(sorted(course_ids)) or '-'}")
        print(f"errors={errors} warnings={warnings}")
        for issue in issues:
            print(f"{issue['level'].upper()} {issue['code']} {issue['path']}: {issue['message']}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
