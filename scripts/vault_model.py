"""Shared helpers for the documented flat Markdown Properties schema."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from typing import Any

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")


def scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith(('"', "[")):
        try:
            return json.loads(value)
        except ValueError:
            pass
    if len(value) >= 2 and value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}
    data: dict[str, Any] = {}
    current = None
    for line in lines[1:]:
        if line == "---":
            break
        if line.strip() == "[]" and current:
            data[current] = []
            continue
        if line.startswith("  - ") and current:
            if not isinstance(data.get(current), list):
                data[current] = []
            data[current].append(scalar(line[4:]))
        elif match := re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line):
            current = match[1]
            data[current] = scalar(match[2])
    return data


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def visible_markdown(text: str) -> str:
    """Ignore fenced examples, retain HTML details and Properties links."""
    output, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s*(\x60{3,}|~{3,})", line)
        if match:
            token = match[1][0]
            if fence is None:
                fence = token
            elif fence == token:
                fence = None
            continue
        if fence is None:
            output.append(line)
    return "\n".join(output)


def links(text: str) -> list[str]:
    return [m[1].split("|", 1)[0].strip()
            for m in WIKILINK.finditer(visible_markdown(text).replace(r"\|", "|"))]


def resolve_link(vault: Path, origin: Path, link: str) -> tuple[Path | None, str | None]:
    target, _, fragment = link.partition("#")
    if target:
        relative = Path(target)
        if relative.is_absolute() or ".." in relative.parts:
            return None, "outside-vault"
        candidates = [vault / target, origin.parent / target]
        if not relative.suffix:
            candidates += [vault / (target + ".md"), origin.parent / (target + ".md")]
        found = next((p for p in candidates if p.is_file()), None)
        if found is None and "/" not in target:
            matches = [p for p in vault.rglob("*") if p.is_file()
                       and (p.name == target or p.stem == target)]
            if len(matches) > 1:
                return None, "ambiguous-link"
            found = matches[0] if matches else None
        if found is None:
            return None, "broken-link"
    else:
        found = origin
    try:
        found.resolve().relative_to(vault.resolve())
    except ValueError:
        return None, "outside-vault"
    if fragment:
        if found.suffix == ".pdf":
            if not re.fullmatch(r"page=[1-9]\d*(?:&.*)?", fragment):
                return found, "broken-fragment"
        elif found.suffix == ".base":
            names = re.findall(r"^\s+name:\s*(.+)$", found.read_text(), re.M)
            if fragment not in [str(scalar(n)) for n in names]:
                return found, "broken-fragment"
        elif found.suffix == ".md":
            text = visible_markdown(found.read_text(encoding="utf-8"))
            if fragment.startswith("^"):
                if not re.search(r"(?:^|\s)\^" + re.escape(fragment[1:]) + r"\s*$", text, re.M):
                    return found, "broken-fragment"
            else:
                headings = re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M)
                if any(h not in headings for h in fragment.split("#")):
                    return found, "broken-fragment"
    return found, None


def progress_questions(path: Path) -> list[tuple[bool, str]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    section = re.search(r"^## 待澄清问题\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not section:
        return []
    return [(mark.lower() == "x", body) for mark, body in
            re.findall(r"^- \[([ xX])\] (.+)$", section[1], re.M)]


def course_fingerprint(vault: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(vault.rglob("*")):
        if not path.is_file() or any(x.startswith(".") or x == "__pycache__"
                                    for x in path.relative_to(vault).parts):
            continue
        digest.update(path.relative_to(vault).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()
