# Scheduled workflows

All schedules use the semester timezone. Scheduled runs use mixed autonomy: drafts and reproducible summaries may be written unattended; canonical knowledge promotion requires confirmation.

## How to schedule

The three workflows below are agent-neutral prompts scoped to the semester root. Only the trigger differs; see [agent-compatibility.md](agent-compatibility.md).

- **Codex:** project-scoped Scheduled tasks on the semester root.
- **Claude Code:** a scheduled-task feature when the build exposes one, otherwise `cron` or `launchd` running headless mode from the semester root:

  ```bash
  cd <semester-root> && claude -p "Use the course-learning skill: <workflow prompt>"
  ```

Create them only after the user confirms. A headless or unattended run has no one to answer a question, so it must end at the approval boundary rather than guessing.

## Material intake

- Run against the semester project each day at 18:00.
- Scan every active course `inbox/` for hashes absent from its manifest.
- Check configured `deadline_sources` and newly ingested assignment/announcement files for changed dates. Create candidate deadline drafts for new or conflicting information; never overwrite a verified or human-edited deadline unattended.
- Follow the ingest workflow for each new source.
- If no source is new, make no file changes and return no routine report.
- If a course expects a lecture that day but has no source, send one concise upload reminder.
- If a verified deadline is within seven days, surface it once in the relevant report; no-change runs remain silent.

## Adaptive review

- Return to the ongoing learning thread every two days at 20:00.
- Read due concepts across active courses and select at most three courses using the assessment priority.
- Ask only the first question, then wait for the learner. Do not mutate mastery before an answer.
- If nothing is due, report the next date briefly.

## Weekly checkpoint

- Return to the ongoing learning thread every Saturday at 11:00.
- Rebuild Overview summaries, run structural validation, and perform a semantic read-only lint.
- Include upcoming/overdue deadline counts and the next deadline per course; flag exact dates without a source, time without a timezone, and stale or conflicting deadline claims.
- Start a cumulative mixed assessment and produce the next-week allocation after the learner completes it.
- Report at most three high-value maintenance issues.

## Failure handling

Do not retry an unattended failure more than once. Do not modify raw files. If permissions, app availability, or a malformed source block safe completion, leave existing canonical notes unchanged and report the exact blocker.
