# Codex / Claude Code + Obsidian Course Learning

项目导航见 [INDEX.md](INDEX.md)。

A reusable, local-first course-learning system maintained by a coding agent — **Codex or Claude Code** — and browsed in Obsidian.

**第一次使用？** 把 [GETTING_STARTED_PROMPT.md](GETTING_STARTED_PROMPT.md) 中的完整提示词复制给你的 agent。它会检查并从官方来源安装 Obsidian，再完成 Vault 注册和界面验证。

It turns lecture PDFs and other course sources into:

- source-grounded lecture notes and concept pages;
- Obsidian Bases, Graph, Backlinks, and dashboards;
- source-grounded homework, quiz, lab, project, and exam deadline tracking;
- learner-initiated Socratic quizzes and on-demand review;
- a semester Overview across independent course vaults;
- optional, explicitly requested source maintenance.

The repository contains only the reusable framework. It does **not** contain course slides, answers, grades, or personal study data.

## Architecture

```text
<semester>/                  # agent project; not an Obsidian vault
├── AGENTS.md                # shared agent contract (Codex reads it directly)
├── CLAUDE.md                # Claude Code entry point; defers to AGENTS.md
├── Index.md                 # 学期级稳定入口
├── semester.md
├── Overview/                # independent Obsidian vault; has Index.md
└── Courses/
    ├── COURSE101/           # independent Obsidian vault; has Index.md
    └── COURSE202/           # independent Obsidian vault; has Index.md
```

Course vaults are authoritative. Overview stores only regenerable summaries. Vaults are siblings, never nested.

## Requirements

- One of: **Codex** (or ChatGPT desktop) with local file access, or **Claude Code** (CLI, desktop, or IDE extension)
- Obsidian with the core Bases plugin (tested with Obsidian 1.13)
- Python 3.10+
- Poppler (`pdfinfo`, `pdftotext`, `pdftoppm`) for full PDF ingestion

No OpenAI or Anthropic API key, backend, database, or community Obsidian plugin is required.

## Agent compatibility

The workflows, schemas, and scripts are shared. Only five things differ per agent, and all of them are documented in [`references/agent-compatibility.md`](references/agent-compatibility.md):

| | Codex | Claude Code |
| --- | --- | --- |
| Skill directory | `~/.agents/skills/course-learning/` | `~/.claude/skills/course-learning/` |
| Invocation | `$course-learning` | `/course-learning` |
| Project instruction file | `AGENTS.md` | `CLAUDE.md` (defers to `AGENTS.md`) |
| App automation | Computer Use | `obsidian` CLI + screenshots, or a computer-use MCP server |
| Scheduling | Codex Scheduled | scheduled tasks, or `cron`/`launchd` with `claude -p` |

`init_semester.py` writes both `AGENTS.md` and `CLAUDE.md`, so one semester workspace can be driven by either agent. The validator accepts a workspace that has only one of them and warns instead of failing.

## Install and Configure Obsidian

The full getting-started prompt explicitly authorizes the agent to install the current macOS app from official sources — the [official Obsidian download page](https://obsidian.md/download), or `brew install --cask obsidian` — when it is missing. The agent then:

- launches Obsidian and registers each sibling folder with **Open folder as vault**;
- enables the Bases, Backlinks, Graph view, Properties view, Templates, and File recovery core plugins;
- opens and visibly verifies `Home.md`, Base views, and Graph view;
- leaves the most useful Home or requested study page open.

Obsidian 1.13 ships an official `obsidian` CLI that drives the running app (`obsidian vaults verbose`, `plugin:enable`, `open`, `base:query`, `command id=graph:open`, `dev:screenshot`). It is disabled by default — turn it on once at **Settings → General → Advanced**. It makes most of this deterministic under either agent, but it does not replace looking at the result: a Base that answers a query still has to be seen rendering. The agent must pause for any EULA, administrator credential, login, security-sensitive permission, or unexpected authorization screen. See [`references/obsidian-setup.md`](references/obsidian-setup.md).

## Install the Skill

### Codex

```text
Use $skill-installer to install https://github.com/YukunHe16/obsidian-course-learning
```

Manual alternative:

```bash
git clone https://github.com/YukunHe16/obsidian-course-learning.git ~/.agents/skills/course-learning
```

Restart Codex if the skill does not appear immediately.

### Claude Code

```bash
git clone https://github.com/YukunHe16/obsidian-course-learning.git ~/.claude/skills/course-learning
```

For a single project instead of your whole account, clone into `<project>/.claude/skills/course-learning` — project skills are shared with anyone who works in that repository. Run `/skills` to confirm `course-learning` is listed.

## Create a Semester

Point `SKILL` at wherever you installed it, then the commands below are identical for both agents:

```bash
SKILL=~/.claude/skills/course-learning      # Codex: SKILL=~/.agents/skills/course-learning

python3 $SKILL/scripts/init_semester.py \
  --root ~/Documents/Study/FA26 \
  --term FA26 \
  --timezone America/Chicago
```

The command is idempotent: existing files are skipped, not overwritten. Running it again on a semester created before Claude Code support adds the missing `CLAUDE.md` and touches nothing else.

## Add a Course

```bash
python3 $SKILL/scripts/init_course.py \
  --semester-root ~/Documents/Study/FA26 \
  --course-id CS425 \
  --title "Distributed Systems" \
  --lecture-days Tuesday Thursday \
  --source-types lecture-slides syllabus textbook
```

Or simply ask the agent. In Claude Code:

```text
/course-learning initialize CS425 in my FA26 semester.
```

In Codex:

```text
Use $course-learning to initialize CS425 in my FA26 semester.
```

Open `<semester>/Overview` and each `<semester>/Courses/<COURSE_ID>` folder as separate Obsidian vaults.
每个学期 project、Overview Vault 和课程 Vault 都必须有根级 `Index.md`；`Home.md` 展示当前状态，`Index.md` 负责长期稳定导航。

## On-demand Use

In Claude Code, from the semester root:

```text
/course-learning ingest the new PDF in this course inbox
/course-learning teach Lecture 3 in Chinese with English technical terms
/course-learning quiz me one question at a time
/course-learning review the lecture or topic I choose
/course-learning show all course deadlines in the next 14 days
/course-learning validate the semester workspace
```

In Codex:

```text
Use $course-learning to ingest the new PDF in this course inbox.
Use $course-learning to teach Lecture 3 in Chinese with English technical terms.
Use $course-learning to quiz me one question at a time.
Use $course-learning to review the lecture or topic I choose.
Use $course-learning to show all course deadlines in the next 14 days.
Use $course-learning to validate the semester workspace.
```

中文同样可用，例如 `/course-learning 讲解 Lecture 3` 或 `使用 $course-learning 逐题考我`。

The default writing contract is Chinese-primary prose, precise English technical terms, and English source citations. Edit `Course.md` to change it per course.

## Learning on demand

Open a lecture when you want to learn; ask for a quiz or review when useful. The system has no daily tests, recurring review, weekly checkpoints, or study quotas. Ingestion does not schedule future reviews.

Source intake can be automated only on explicit request. It organizes materials without initiating tests or learning reports. See [material maintenance](references/scheduled-workflows.md).

## Reading, return navigation and progress

Pin the primary lecture tab and open references with Cmd/Ctrl-click. Switch back to keep the exact scroll position, or use Back after same-tab navigation. Concept/question pages also link to their primary lecture sections.

The default layout is reading mode, hidden in-document Properties and Outline; Graph is optional. Progress stores only an explicitly selected learning position and evidence-backed questions. New records need no scores. Ordinary notes become readable after the agent checks sources; conflicts and policy changes are reviewed separately.

Rebuild only derived summaries:

~~~bash
python3 scripts/rebuild_overview.py --semester-root <semester> --course-id <COURSE_ID>
~~~

Upgrading an existing vault: back up notes/settings, add Progress, set schema_version: 2 only after return links and checked-source metadata validate. Preserve old paths, raw hashes and human contributions; do not invent sessions from old numeric scores. Other existing courses need not be migrated.

## Validate

```bash
python3 $SKILL/scripts/validate_vault.py \
  --semester-root ~/Documents/Study/FA26
```

The validator checks required structure, the agent contract files, source hashes referenced by lecture notes, concept IDs, optional legacy score ranges, reading/return links and evidence records, deadline IDs/dates/evidence/timezones, Wikilinks, and Overview/course consistency.

## Privacy and Academic Integrity

- Do not publish copyrighted course materials unless you have permission.
- Generated semester workspaces ignore common raw binary formats by default.
- Keep graded-work policies in each `Course.md`.
- The Skill teaches concepts and creates independent practice; it must not produce prohibited submit-ready work.

## License

MIT. See [LICENSE](LICENSE).

## Related project

For programme research, application materials, deadlines, and a private admissions
tracker, see [Obsidian Graduate Admissions](https://github.com/YukunHe16/obsidian-graduate-admissions),
which supports the same two agents.
