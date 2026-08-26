# Course profile schema

Read `Course.md` before any course-scoped operation. YAML Properties are the machine-readable contract; prose below them gives human context.

## Required properties

```yaml
type: course
course_id: CS425
title: Distributed Systems
term: FA26
vault_name: CS425
language: Chinese-primary prose; English technical terms and English citations
lecture_days:
  - Tuesday
  - Thursday
exam_dates:
  - 2026-10-08
source_types:
  - lecture-slides
review_weight: 1.0
ai_policy: Course concepts and original practice only; no submit-ready HW or MP answers.
scheduled_draft_ingest: true
status: active
```

`course_id` is uppercase and stable. Use it in every concept ID. `status` is `active` or `archived`. Dates use ISO `YYYY-MM-DD`. `review_weight` is a positive number; use `1.0` by default.

The profile may add:

- `source_priority`: ordered source classes, highest authority first.
- `assessment_focus`: concept, calculation, proof, design, code-reading, or other course-specific emphasis.
- `known_exam_dates`: labels paired with dates in the prose section when YAML lists alone are insufficient.
- `academic_integrity_notes`: stricter course-specific boundaries.

Do not infer permission to solve assessed work from a missing policy. Ask before helping with material that appears submit-ready.

## Standard note properties

### Lecture

```yaml
type: lecture
course: CS425
lecture_no: 1
lecture_date: 2026-08-25
source_pdf: raw/lectures/L1.FA26.pdf
source_hash: <sha256>
status: draft
concepts:
  - "[[Distributed System]]"
```

### Concept

```yaml
type: concept
course: CS425
concept_id: CS425/distributed-system
aliases:
  - distributed systems
mastery: 0
review_stage: 0
last_reviewed:
next_review: 2026-08-26
source_lectures:
  - "[[L01 - Welcome and Introduction]]"
status: active
```

Mastery is an integer from 0 through 4. Review stage is an integer from 0 through 4. Status is `active`, `draft`, or `superseded` as appropriate.

### Study session

```yaml
type: study-session
course:
  - CS425
date: 2026-08-25
mode: due-review
concepts:
  - CS425/distributed-system
score: 0
misconceptions: []
next_actions: []
```
