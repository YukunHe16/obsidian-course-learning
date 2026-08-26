---
name: course-learning
description: Build and maintain reusable Obsidian course-learning vaults from lecture PDFs and other course materials. Use for initializing courses, ingesting sources, teaching concepts, Socratic quizzes, spaced review, semester dashboards, or vault health checks. Do not use to produce submit-ready work when a course forbids AI assistance.
---

# Course Learning

Maintain a source-grounded learning system in which each course Obsidian vault is authoritative and the semester Overview is derived.

## Find the learning context

1. Locate the nearest `Course.md`. If present, work only in that course unless the user asks for cross-course work.
2. Otherwise locate `semester.md` and `Courses/`. Treat that directory as the semester root.
3. Read the relevant profile before acting. Course-specific language, source priority, exam style, schedule, and AI policy override defaults.
4. If neither profile exists, use `init-course`; do not invent a vault layout ad hoc.

## Route the request

- **Initialize a semester:** Read [vault-schema.md](references/vault-schema.md), then run `scripts/init_semester.py`.
- **Initialize a course:** Read [course-schema.md](references/course-schema.md) and [vault-schema.md](references/vault-schema.md), then run `scripts/init_course.py`.
- **Ingest new material:** Read [ingest-workflow.md](references/ingest-workflow.md). For PDFs, also use the available PDF-specific skill and inspect every page visually as well as textually.
- **Teach or answer:** Read [teaching-workflow.md](references/teaching-workflow.md).
- **Quiz or review:** Read [assessment-rules.md](references/assessment-rules.md).
- **Scheduled run:** Read [scheduled-workflows.md](references/scheduled-workflows.md) plus only the mode reference needed by that run.
- **Lint or audit:** Read [vault-schema.md](references/vault-schema.md), then run `scripts/validate_vault.py` before semantic review.
- **Rebuild Overview:** Read [vault-schema.md](references/vault-schema.md). Recompute only derived course-summary notes; never copy concept prose into Overview.

## Invariants

- Preserve every raw source byte-for-byte. Record a SHA-256 hash before marking a source ingested.
- Cite course claims to a source file and page/section. Label external enrichment separately; it cannot silently override course material.
- Unless `Course.md` explicitly overrides it, write Wiki prose primarily in Chinese, preserve English technical terms at first use and wherever precision matters, and format citation labels, source titles, and slide/page markers in English.
- Write drafts and derived state automatically when authorized. Require user confirmation before promoting drafts, changing course policy, or overwriting human-authored canonical notes.
- Course vaults own lecture, concept, question, and review state. Overview owns only regenerated summaries and cross-course session records.
- Namespace stable identifiers with `course_id`, for example `CS425/asynchrony`.
- Use Obsidian Properties, Wikilinks, Bases, Graph, Backlinks, Templates, and File Recovery. Do not require community plugins.
- Do not create nested vaults or symlink course content into Overview.
- Respect the course AI policy. Explain concepts and create original practice, but do not generate prohibited submit-ready homework, exam, or programming-assignment answers.
- For multi-source analysis, subagents may inspect independent sources read-only. The primary agent alone performs canonical writes.
- Stop after one failed unattended attempt and report the failure; do not loop indefinitely.

## Completion standard

Finish with the affected course, files created or updated, source coverage, pending approvals, next review date, and any validation warnings. Keep interactive quizzes one question at a time and do not reveal a rubric before the learner answers.
