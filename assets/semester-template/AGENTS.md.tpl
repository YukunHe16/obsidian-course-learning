# {{TERM}} Learning System

## Mission

Maintain a source-grounded learning system across all courses in this semester. Use `$course-learning` for course initialization, ingestion, teaching, quizzes, spaced review, Overview rebuilds, and validation.

## Project boundaries

- This root is a Codex project, not an Obsidian vault. Never create `.obsidian` here or directly under `Courses/`.
- `Overview/` and every `Courses/<COURSE_ID>/` are independent sibling Obsidian vaults. Never nest vaults or join them with symlinks.
- A course vault owns lectures, concepts, questions, raw sources, and mastery state.
- Overview contains only reproducible summaries and cross-course sessions. Use encoded `obsidian://open?path=...` links across vaults.

## Sources and writes

- Raw files are immutable. Record SHA-256, size, source type, and ingest date.
- Course claims cite the source file and page/section. Label external enrichment separately.
- Scheduled may create drafts, candidate questions, manifests, logs, and derived summaries.
- Require confirmation before promoting drafts, changing course policy, or overwriting human-authored canonical notes.

## Learning behavior

- Follow each `Course.md` for language, source authority, assessment style, schedule, and AI policy.
- Ask Socratic quiz questions one at a time and never reveal the rubric before an answer.
- Review intervals are 1, 3, 7, and 14 days. Update mastery only from learner evidence.
- Cross-course sessions use at most three courses, prioritized by exam proximity, overdue state, weak mastery, and recent under-coverage.

## Verification

Run the `$course-learning` validator after structural changes. Inspect every PDF page visually and textually. Stop unattended retry loops after one failure.
