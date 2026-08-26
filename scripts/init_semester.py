#!/usr/bin/env python3
"""Create an idempotent semester workspace from the bundled template."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


TERM_RE = re.compile(r"^[A-Za-z0-9_-]{2,24}$")
TEXT_SUFFIXES = {".md", ".base", ".json", ".yaml", ".yml", ".txt", ".tpl"}


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def copy_template(template_root: Path, destination: Path, values: dict[str, str]) -> tuple[list[Path], list[Path]]:
    created: list[Path] = []
    skipped: list[Path] = []
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
    return created, skipped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--term", required=True)
    parser.add_argument("--timezone", default="America/Chicago")
    parser.add_argument("--language", default="Chinese-primary prose; English technical terms and English citations")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not TERM_RE.fullmatch(args.term):
        print(f"error: invalid term: {args.term}", file=sys.stderr)
        return 2

    root = args.root.expanduser().resolve()
    template_root = Path(__file__).resolve().parent.parent / "assets" / "semester-template"
    if not template_root.is_dir():
        print("error: bundled semester template is missing", file=sys.stderr)
        return 2

    for directory in (
        root / "Courses",
        root / "Overview" / ".obsidian",
        root / "Overview" / "assets",
        root / "Overview" / "courses",
        root / "Overview" / "sessions",
        root / "Overview" / "views",
    ):
        directory.mkdir(parents=True, exist_ok=True)

    created, skipped = copy_template(
        template_root,
        root,
        {"TERM": args.term, "TIMEZONE": args.timezone, "LANGUAGE": args.language},
    )
    print(f"semester_root={root}")
    print(f"created={len(created)}")
    for path in created:
        print(f"  + {path}")
    print(f"skipped={len(skipped)}")
    for path in skipped:
        print(f"  = {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
