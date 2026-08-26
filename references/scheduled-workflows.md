# Scheduled workflows

All schedules use the semester timezone. Scheduled runs use mixed autonomy: drafts and reproducible summaries may be written unattended; canonical knowledge promotion requires confirmation.

## Material intake

- Run against the semester project each day at 18:00.
- Scan every active course `inbox/` for hashes absent from its manifest.
- Follow the ingest workflow for each new source.
- If no source is new, make no file changes and return no routine report.
- If a course expects a lecture that day but has no source, send one concise upload reminder.

## Adaptive review

- Return to the ongoing learning thread every two days at 20:00.
- Read due concepts across active courses and select at most three courses using the assessment priority.
- Ask only the first question, then wait for the learner. Do not mutate mastery before an answer.
- If nothing is due, report the next date briefly.

## Weekly checkpoint

- Return to the ongoing learning thread every Saturday at 11:00.
- Rebuild Overview summaries, run structural validation, and perform a semantic read-only lint.
- Start a cumulative mixed assessment and produce the next-week allocation after the learner completes it.
- Report at most three high-value maintenance issues.

## Failure handling

Do not retry an unattended failure more than once. Do not modify raw files. If permissions, app availability, or a malformed source block safe completion, leave existing canonical notes unchanged and report the exact blocker.
