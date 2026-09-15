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
Index.md
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
learning/Progress.md       # schema v2: bookmark + evidence-backed questions
learning/deadlines/
learning/sessions/
views/Course.base
templates/
```

Raw sources are immutable. `raw/manifest.md` records source path, SHA-256, byte size, ingest time, source type, lecture number, and whether it supersedes another source.

## Reading organization

Follow [reading-workflow.md](reading-workflow.md). `wiki/index.md` is the reading route, not a flat concept catalogue. Each lecture has one primary reading page; revision records and the concept catalogue are secondary. Existing concept IDs and review state remain authoritative. A reference catalogue may be added when the number of cards makes the main route difficult to scan.

## Semester Overview

Overview contains only derived `course-summary` notes and cross-course session summaries. One summary exists at `Overview/courses/<COURSE_ID>.md` per active course.

```yaml
type: course-summary
course_id: CS425
status: active
open_question_count: 0
lecture_count: 0
pending_count: 0
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

- Questions: link to Progress; only actual unresolved misconceptions are counted.
- Pending: draft lectures or pending proposals.
- Recent sessions: existing sessions, newest first, without a periodic review requirement.
- Deadlines: today, next 14 days, pending verification, overdue, and all course milestones.

Semester views filter `type == "course-summary"` and expose course status, open-question/pending counts, exam dates, and deep links.
Derived summaries additionally expose `upcoming_deadline_count`, `overdue_deadline_count`, `next_deadline`, and `next_deadline_title`; they never copy deadline prose from a course Vault.

Old due_count / next_review fields are historical compatibility data, not active study queues. Home and Bases do not display daily review loads. Review is learner-initiated.

## Validation

Run:

```bash
python3 <skill>/scripts/validate_vault.py --semester-root <semester>
```

Treat structural failures as blocking. Semantic warnings such as possible contradictions require review but do not automatically rewrite canonical notes.

## Rebuild derived summaries

Run scripts/rebuild_overview.py --semester-root <semester> [--course-id <id>]. The optional course filter confines migration to one course. Same day and unchanged source content leave summary bytes and timestamps unchanged; calendar-derived deadlines refresh on a new day. Summary regeneration writes only Overview/courses; it never creates a study session or changes a course.
