#!/usr/bin/env python3
"""Validate a multi-course semester workspace and its Obsidian vaults."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


LINK_RE = re.compile(r"\[\[([^\]#|]+)")
REQUIRED_ROOT = ["AGENTS.md", "Index.md", "semester.md", "Overview/Index.md", "Overview/Home.md", "Overview/views/Semester.base", "Courses"]
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
    "learning/questions",
    "learning/sessions",
    "templates",
]


def scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if value == "[]":
        return []
    return value


def frontmatter(path: Path) -> dict[str, Any]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return {}
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, Any] = {}
    current: str | None = None
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if line.startswith("  - ") and current:
            if not isinstance(data.get(current), list):
                data[current] = []
            data[current].append(scalar(line[4:]))
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            current = match.group(1)
            data[current] = scalar(match.group(2))
    return data


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add(issues: list[dict[str, str]], level: str, code: str, path: Path, message: str) -> None:
    issues.append({"level": level, "code": code, "path": str(path), "message": message})


def resolve_links(vault: Path, issues: list[dict[str, str]]) -> None:
    notes = list(vault.rglob("*.md"))
    by_stem: dict[str, list[Path]] = defaultdict(list)
    relative_set = {str(note.relative_to(vault).with_suffix("")) for note in notes}
    for note in notes:
        by_stem[note.stem].append(note)
    for note in notes:
        if "templates" in note.relative_to(vault).parts:
            continue
        text = note.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            target = target.strip()
            if not target or target.startswith("http"):
                continue
            normalized = target[:-3] if target.endswith(".md") else target
            if "/" in normalized:
                if normalized not in relative_set and not (vault / target).exists():
                    add(issues, "warning", "broken-link", note, f"Unresolved Wikilink: {target}")
            elif normalized not in by_stem:
                add(issues, "warning", "broken-link", note, f"Unresolved Wikilink: {target}")
            elif len(by_stem[normalized]) > 1:
                add(issues, "warning", "ambiguous-link", note, f"Ambiguous Wikilink: {target}")


def validate_course(course_root: Path, issues: list[dict[str, str]], concept_ids: dict[str, Path]) -> str | None:
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

    for note in (course_root / "wiki" / "concepts").glob("*.md"):
        data = frontmatter(note)
        required = {"type", "course", "concept_id", "mastery", "review_stage", "status"}
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
        if not isinstance(data.get("mastery"), int) or not 0 <= data["mastery"] <= 4:
            add(issues, "error", "mastery-range", note, "mastery must be an integer from 0 to 4")
        if not isinstance(data.get("review_stage"), int) or not 0 <= data["review_stage"] <= 4:
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

    concept_ids: dict[str, Path] = {}
    course_ids: set[str] = set()
    courses_dir = root / "Courses"
    if courses_dir.is_dir():
        for course_root in sorted(path for path in courses_dir.iterdir() if path.is_dir()):
            course_id = validate_course(course_root, issues, concept_ids)
            if course_id:
                course_ids.add(course_id)

    summaries_dir = root / "Overview" / "courses"
    summaries = {path.stem for path in summaries_dir.glob("*.md")} if summaries_dir.is_dir() else set()
    for course_id in sorted(course_ids - summaries):
        add(issues, "error", "missing-summary", summaries_dir / f"{course_id}.md", "Course summary is missing")
    for course_id in sorted(summaries - course_ids):
        add(issues, "warning", "orphan-summary", summaries_dir / f"{course_id}.md", "No matching course vault")

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
