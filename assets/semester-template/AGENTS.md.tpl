# {{TERM}} Learning System

## Mission

Maintain a source-grounded learning system across all courses in this semester. Use the `course-learning` Skill (`$course-learning` in Codex, `/course-learning` in Claude Code) for course initialization, ingestion, teaching, quizzes, on-demand review, Overview rebuilds, and validation.

This file is the shared contract for every agent working in this semester. Codex reads it directly; Claude Code reaches it through `CLAUDE.md`. Change the rules here, not in a per-agent copy.

## Project boundaries

- This root is an agent project, not an Obsidian vault. Never create `.obsidian` here or directly under `Courses/`.
- `Overview/` and every `Courses/<COURSE_ID>/` are independent sibling Obsidian vaults. Never nest vaults or join them with symlinks.
- A course vault owns lectures, concepts, questions, raw sources, and mastery state.
- Overview contains only reproducible summaries and cross-course sessions. Use encoded `obsidian://open?path=...` links across vaults.

## Sources and writes

- Raw files are immutable. Record SHA-256, size, source type, and ingest date.
- Course claims cite the source file and page/section. Label external enrichment separately.
- Scheduled or headless runs may create drafts, candidate questions, manifests, logs, and derived summaries.
- Ordinary notes may become active after source verification. Require confirmation for unresolved conflicts, course-policy changes or destructive overwrites of human contributions.

## Reading organization

Default to lecture-first navigation and topic-cluster concepts. Keep each primary lecture readable as a whole, with a recap, examples, assumptions, and closed-book self-check. Place concept catalogues and revisions behind secondary links. Preserve concept IDs and review state when reorganizing. Follow the Skill's `references/reading-workflow.md`.

## Learning behavior

- Follow each `Course.md` for language, source authority, assessment style, schedule, and AI policy.
- Ask Socratic quiz questions one at a time and never reveal the rubric before an answer.
- Learning and review are on demand. Do not create daily tests, recurring review, weekly checkpoints or automatic study schedules. Record only concise actual interaction evidence.
- Cross-course sessions begin only when requested and follow the learner's chosen scope.

## Verification

Run the Skill's validator after structural changes. Inspect every PDF page visually and textually. Check Obsidian state through the live app — the `obsidian` CLI against the running app, plus a screenshot or Computer Use — before reporting that a vault, Base, or Graph is working. Stop unattended retry loops after one failure.

## Checked notes and study records

Ordinary learning notes may become active after source verification, with checked_at and citations. Active means readable, not learned. Student approval is needed for actual source conflicts or policy changes, not every note. Preserve human contributions. Progress keeps a learner-confirmed bookmark and concise evidence-backed questions; old scores are not a basis for weak labels. Do not migrate another existing course implicitly.
