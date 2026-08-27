# Vault and Overview schema

## Semester root

The semester root is an agent project (Codex or Claude Code), not an Obsidian vault:

```text
<semester>/
|-- AGENTS.md              # shared agent contract; Codex reads it directly
|-- CLAUDE.md              # Claude Code entry point; defers to AGENTS.md
|-- Index.md
|-- semester.md
|-- Overview/              # independent Obsidian vault
`-- Courses/
    `-- <COURSE_ID>/       # independent Obsidian vault
```

`AGENTS.md` owns the contract and `CLAUDE.md` stays thin. Both are written by `init_semester.py`; see [agent-compatibility.md](agent-compatibility.md).

Never add a `.obsidian` directory to the semester root. Never nest a course under `Overview` and never symlink course files into it.

Create a new semester workspace with:

```bash
python3 <skill>/scripts/init_semester.py --root <path> --term <TERM> --timezone <IANA timezone>
```

## Course vault

Required top-level items:

```text
Course.md
Home.md
inbox/
raw/lectures/
raw/manifest.md
wiki/index.md
wiki/log.md
wiki/lectures/
wiki/concepts/
wiki/course-policies/
wiki/pending/
learning/questions/
learning/deadlines/
learning/sessions/
views/Course.base
templates/
```

Raw sources are immutable. `raw/manifest.md` records source path, SHA-256, byte size, ingest time, source type, lecture number, and whether it supersedes another source.

## Semester Overview

Overview contains only derived `course-summary` notes and cross-course session summaries. One summary exists at `Overview/courses/<COURSE_ID>.md` per active course.

```yaml
type: course-summary
course_id: CS425
status: active
due_count: 0
weak_count: 0
pending_count: 0
average_mastery: 0
next_exam: 2026-10-08
last_ingested: 2026-08-25
last_studied:
generated_at: 2026-08-25T18:00:00-05:00
source_fingerprint: <sha256>
vault_path: /absolute/course/path
obsidian_uri: obsidian://open?path=<percent-encoded-absolute-Home.md>
```

Overview summaries may be overwritten because they are reproducible. They must not contain copied lecture or concept prose.

## Obsidian Bases

Course views filter canonical course notes:

- Due: `type == "concept"`, active, with `next_review <= today()`.
- Weak: `type == "concept"` and `mastery <= 2`.
- Pending: draft lectures or pending proposals.
- Recent sessions: study sessions in the last 14 days.
- Deadlines: today, next 14 days, pending verification, overdue, and all course milestones.

Semester views filter `type == "course-summary"` and expose course status, due/weak/pending counts, exam dates, and deep links.
Derived summaries additionally expose `upcoming_deadline_count`, `overdue_deadline_count`, `next_deadline`, and `next_deadline_title`; they never copy deadline prose from a course Vault.

## Validation

Run:

```bash
python3 <skill>/scripts/validate_vault.py --semester-root <semester>
```

Treat structural failures as blocking. Semantic warnings such as possible contradictions require review but do not automatically rewrite canonical notes.
