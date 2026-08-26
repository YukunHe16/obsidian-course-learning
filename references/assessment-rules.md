# Quiz, mastery, and spaced review

## Interaction

- Ask one question at a time.
- Do not show the answer, rubric, key terms, or leading multiple-choice options before the learner commits.
- Prefer short-answer generation, explanation, scenario analysis, comparison, derivation, and transfer over recognition-only questions.
- After an answer, first diagnose the reasoning, then score, correct, and ask a targeted follow-up when useful.

## Mastery scale

- `0`: unseen or no usable evidence.
- `1`: recognizes the term but cannot explain it reliably.
- `2`: explains the core idea with support.
- `3`: applies it correctly to a new course-level scenario.
- `4`: transfers it, compares alternatives, and reasons about changed assumptions.

Do not raise mastery solely because the learner says they understand.

## Review ladder

The intervals are 1, 3, 7, and 14 days.

- Correct with sound reasoning: advance one review stage, capped at 4.
- Partially correct: keep the stage and schedule the same interval again.
- Incorrect, guessed, or unable to explain: reset to stage 0 and schedule in 1 day.

Write `last_reviewed`, `next_review`, `mastery`, and `review_stage` to the owning concept note only after learner evidence. Append a study-session note; never rewrite prior sessions.

## Cross-course selection

Select no more than three courses per session. Prioritize in order:

1. an exam within 14 days;
2. overdue concepts;
3. mastery of 2 or below;
4. a course underrepresented in recent sessions.

Within three days of an exam, that course may dominate but should still include at least one older retrieval item when time permits. If nothing is due, report the next due date instead of inventing busywork.
