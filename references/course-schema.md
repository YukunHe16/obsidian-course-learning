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
- `deadline_sources`: official URLs or local source classes checked for homework, quiz, lab, project, and exam dates.

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

### Deadline

```yaml
type: deadline
course: CS425
deadline_id: CS425/deadline/hw1
title: HW1
deadline_kind: homework
date_status: exact
due_date: 2026-09-20
due_time: "23:59"
timezone: America/Chicago
status: pending
verification_status: verified
applicable_to:
  - on-campus-3-credit-undergraduate
submission_platform: Gradescope
official_url: https://courses.example.edu/course/assignments
source_locator: "Assignments > HW1"
verified_at: 2026-08-25
```

`deadline_id` 必须使用课程 namespace。课程截止记录保存在 `learning/deadlines/`。状态为 `pending / completed / missed / waived / cancelled`；核验状态为 `candidate / verified / stale / conflict`。

`date_status` 固定为：

- `exact`：官方来源明确给出日期；必须填写 `due_date`。
- `recurring`：来源只给每周或相对规则，不把它展开成猜测日期。
- `unpublished`：项目已知但日期未公布。
- `section-dependent`：日期或时间依赖学生注册的 discussion/lab/exam section。

只有来源明确给出 clock time 时才填写 `due_time`；填写后必须同时给出 `timezone`。动态日期标为 `verified` 时必须带 `verified_at`、`source_locator`，以及 `source_path` 或 `official_url` 至少一项。
若来源给出 clock time 但未写 timezone，把原文放入 `due_time_text`，保持 `due_time` 为空，禁止自行补全时区。
若官网只发布一个 section-dependent 日期范围，把原文放入 `date_window`，不要把窗口起点伪装成个人截止日期。
