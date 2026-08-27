# Codex / Claude Code + Obsidian Course Learning

项目导航见 [INDEX.md](INDEX.md)。

A reusable, local-first course-learning system maintained by a coding agent — **Codex or Claude Code** — and browsed in Obsidian.

**第一次使用？** 把 [GETTING_STARTED_PROMPT.md](GETTING_STARTED_PROMPT.md) 中的完整提示词复制给你的 agent。它会检查并从官方来源安装 Obsidian，再完成 Vault 注册和界面验证。

It turns lecture PDFs and other course sources into:

- source-grounded lecture notes and concept pages;
- Obsidian Bases, Graph, Backlinks, and dashboards;
- source-grounded homework, quiz, lab, project, and exam deadline tracking;
- Socratic quizzes and 1/3/7/14-day spaced review;
- a semester Overview across independent course vaults;
- optional scheduled workflows for intake, review, and weekly checks.

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
Use $skill-installer to install https://github.com/YukunHe16/codex-obsidian-course-learning
```

Manual alternative:

```bash
git clone https://github.com/YukunHe16/codex-obsidian-course-learning.git ~/.agents/skills/course-learning
```

Restart Codex if the skill does not appear immediately.

### Claude Code

```bash
git clone https://github.com/YukunHe16/codex-obsidian-course-learning.git ~/.claude/skills/course-learning
```

For a single project instead of your whole account, clone into `<project>/.claude/skills/course-learning` — project skills are shared with anyone who works in that repository. Run `/skills` to confirm `course-learning` is listed.

## Create a Semester

```bash
python3 ~/.claude/skills/course-learning/scripts/init_semester.py \
  --root ~/Documents/Study/FA26 \
  --term FA26 \
  --timezone America/Chicago
```

Use `~/.agents/skills/course-learning/...` instead if you installed the Skill for Codex. The command is idempotent: existing files are skipped, not overwritten. Running it again on an older workspace adds the missing `CLAUDE.md` without touching anything else.

## Add a Course

```bash
python3 ~/.claude/skills/course-learning/scripts/init_course.py \
  --semester-root ~/Documents/Study/FA26 \
  --course-id CS425 \
  --title "Distributed Systems" \
  --lecture-days Tuesday Thursday \
  --source-types lecture-slides syllabus textbook
```

Or simply ask the agent:

```text
/course-learning initialize CS425 in my FA26 semester.
Use $course-learning to initialize CS425 in my FA26 semester.
```

Open `<semester>/Overview` and each `<semester>/Courses/<COURSE_ID>` folder as separate Obsidian vaults.
每个学期 project、Overview Vault 和课程 Vault 都必须有根级 `Index.md`；`Home.md` 展示当前状态，`Index.md` 负责长期稳定导航。

## Daily Use

Prefix with `/course-learning` in Claude Code or `Use $course-learning to` in Codex:

```text
ingest the new PDF in this course inbox.
teach Lecture 3 in Chinese with English technical terms.
quiz me one question at a time.
review everything due today.
show all course deadlines in the next 14 days.
validate the semester workspace.
```

The default writing contract is Chinese-primary prose, precise English technical terms, and English source citations. Edit `Course.md` to change it per course.

## Scheduled Workflows

Ask the agent to create three semester-scoped scheduled runs:

1. Daily material intake at 18:00.
2. Adaptive cross-course review every two days at 20:00.
3. Weekly Overview rebuild and checkpoint on Saturday at 11:00.

Codex uses project-scoped Scheduled tasks. Claude Code uses its scheduled tasks where available, otherwise `cron` or `launchd` calling `claude -p` from the semester root. The prompts and mixed-autonomy boundaries are in [`references/scheduled-workflows.md`](references/scheduled-workflows.md). Keep reasoning effort at or below the level appropriate for your plan and usage limits.

## Validate

```bash
python3 ~/.claude/skills/course-learning/scripts/validate_vault.py \
  --semester-root ~/Documents/Study/FA26
```

The validator checks required structure, the agent contract files, source hashes referenced by lecture notes, concept IDs and mastery ranges, deadline IDs/dates/evidence/timezones, Wikilinks, and Overview/course consistency.

## Privacy and Academic Integrity

- Do not publish copyrighted course materials unless you have permission.
- Generated semester workspaces ignore common raw binary formats by default.
- Keep graded-work policies in each `Course.md`.
- The Skill teaches concepts and creates independent practice; it must not produce prohibited submit-ready work.

## License

MIT. See [LICENSE](LICENSE).

## Related project

For programme research, application materials, deadlines, and a private admissions
tracker, see [Codex + Obsidian Graduate Admissions](https://github.com/YukunHe16/codex-obsidian-graduate-admissions).
