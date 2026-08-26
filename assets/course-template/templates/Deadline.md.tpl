---
type: deadline
course: "{{COURSE_ID}}"
deadline_id: "{{COURSE_ID}}/deadline/{{DEADLINE_SLUG}}"
title: "{{DEADLINE_TITLE}}"
deadline_kind: homework
date_status: unpublished
due_date:
date_window:
due_time:
due_time_text:
timezone: "{{TIMEZONE}}"
status: pending
verification_status: candidate
applicable_to: []
submission_platform:
submission_url:
release_date:
source_path:
official_url:
source_locator:
verified_at:
last_checked:
---

# {{DEADLINE_TITLE}}

## 要做什么

{{ACTION}}

## 日期边界

- 只有官方 assignment、syllabus、course website 或 staff announcement 明确给出的日期才能使用 `date_status: exact`。
- 若日期依赖本人 discussion/lab section，使用 `section-dependent`；尚未公布则使用 `unpublished`。

## 来源

{{SOURCE_CITATION}}
