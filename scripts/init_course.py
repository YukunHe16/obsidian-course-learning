#!/usr/bin/env python3
"""Create an idempotent course Obsidian vault from the bundled template."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
import urllib.parse
from pathlib import Path


COURSE_ID_RE = re.compile(r"^[A-Z][A-Z0-9-]{1,31}$")
TEXT_SUFFIXES = {".md", ".base", ".json", ".yaml", ".yml", ".txt", ".tpl"}


def yaml_list(values: list[str], indent: int = 2) -> str:
    if not values:
        return "  []"
    prefix = " " * indent
    return "\n".join(f"{prefix}- {value}" for value in values)


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_if_missing(path: Path, content: str, created: list[Path], skipped: list[Path]) -> None:
    if path.exists():
        skipped.append(path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(path)


def copy_template(template_root: Path, destination: Path, values: dict[str, str], created: list[Path], skipped: list[Path]) -> None:
    for source in sorted(template_root.rglob("*")):
        if source.name == "__pycache__" or ".pre-" in source.name or source.suffix in {".bak", ".tmp"}:
            continue
        relative = source.relative_to(template_root)
        target_name = relative.name[:-4] if relative.name.endswith(".tpl") else relative.name
        target = destination / relative.parent / target_name
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists():
            skipped.append(target)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix in TEXT_SUFFIXES:
            target.write_text(render(source.read_text(encoding="utf-8"), values), encoding="utf-8")
        else:
            shutil.copy2(source, target)
        created.append(target)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--semester-root", required=True, type=Path)
    parser.add_argument("--course-id", required=True)
    parser.add_argument("--title")
    parser.add_argument("--term", help="Defaults to the term property in semester.md")
    parser.add_argument("--language", default="Chinese-primary prose; English technical terms and English citations")
    parser.add_argument("--lecture-days", nargs="*", default=[])
    parser.add_argument("--exam-dates", nargs="*", default=[])
    parser.add_argument("--source-types", nargs="*", default=["lecture-slides"])
    parser.add_argument("--review-weight", type=float, default=1.0)
    parser.add_argument(
        "--ai-policy",
        default="Course concepts and original practice only; no submit-ready assessed work unless explicitly permitted.",
    )
    return parser.parse_args()


def semester_term(semester_root: Path) -> str | None:
    profile = semester_root / "semester.md"
    if not profile.is_file():
        return None
    for line in profile.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"term:\s*['\"]?([^'\"]+)['\"]?", line.strip())
        if match:
            return match.group(1).strip()
    return None


def main() -> int:
    args = parse_args()
    course_id = args.course_id.upper()
    if not COURSE_ID_RE.fullmatch(course_id):
        print(f"error: invalid course id: {args.course_id}", file=sys.stderr)
        return 2
    if args.review_weight <= 0:
        print("error: review weight must be positive", file=sys.stderr)
        return 2

    semester_root = args.semester_root.expanduser().resolve()
    term = args.term or semester_term(semester_root)
    if not term:
        print("error: --term is required when semester.md has no term property", file=sys.stderr)
        return 2
    title = args.title or course_id
    course_root = semester_root / "Courses" / course_id
    overview_root = semester_root / "Overview"
    today = dt.date.today().isoformat()
    home_path = course_root / "Home.md"
    obsidian_uri = "obsidian://open?path=" + urllib.parse.quote(str(home_path), safe="")

    values = {
        "COURSE_ID": course_id,
        "COURSE_TITLE": title,
        "TERM": term,
        "VAULT_NAME": course_id,
        "LANGUAGE": args.language,
        "LECTURE_DAYS": yaml_list(args.lecture_days),
        "EXAM_DATES": yaml_list(args.exam_dates),
        "SOURCE_TYPES": yaml_list(args.source_types),
        "REVIEW_WEIGHT": str(args.review_weight),
        "AI_POLICY": args.ai_policy.replace("\n", " ").strip(),
        "CREATED_DATE": today,
        "COURSE_PATH": str(course_root),
        "OBSIDIAN_URI": obsidian_uri,
    }

    template_root = Path(__file__).resolve().parent.parent / "assets" / "course-template"
    summary_template = Path(__file__).resolve().parent.parent / "assets" / "overview-course-summary.md.tpl"
    if not template_root.is_dir() or not summary_template.is_file():
        print("error: bundled templates are missing", file=sys.stderr)
        return 2

    required_dirs = [
        course_root / ".obsidian",
        course_root / "inbox",
        course_root / "raw" / "lectures",
        course_root / "wiki" / "lectures",
        course_root / "wiki" / "concepts",
        course_root / "wiki" / "course-policies",
        course_root / "wiki" / "pending",
        course_root / "learning" / "questions",
        course_root / "learning" / "sessions",
        course_root / "views",
        course_root / "templates",
        overview_root / "courses",
    ]
    for directory in required_dirs:
        directory.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    skipped: list[Path] = []
    copy_template(template_root, course_root, values, created, skipped)
    summary_path = overview_root / "courses" / f"{course_id}.md"
    write_if_missing(
        summary_path,
        render(summary_template.read_text(encoding="utf-8"), values),
        created,
        skipped,
    )

    print(f"course={course_id}")
    print(f"course_root={course_root}")
    print(f"created={len(created)}")
    for path in created:
        print(f"  + {path}")
    print(f"skipped={len(skipped)}")
    for path in skipped:
        print(f"  = {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
