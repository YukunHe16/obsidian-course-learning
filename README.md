# Codex + Obsidian Course Learning

A reusable, local-first course-learning system maintained by Codex and browsed in Obsidian.

**第一次使用？** 把 [GETTING_STARTED_PROMPT.md](GETTING_STARTED_PROMPT.md) 中的完整提示词复制给 Codex。它会检查并从官方来源安装 Obsidian，再通过 Computer Use 完成 Vault 注册和界面验证。

It turns lecture PDFs and other course sources into:

- source-grounded lecture notes and concept pages;
- Obsidian Bases, Graph, Backlinks, and dashboards;
- Socratic quizzes and 1/3/7/14-day spaced review;
- a semester Overview across independent course vaults;
- optional Codex Scheduled workflows for intake, review, and weekly checks.

The repository contains only the reusable framework. It does **not** contain course slides, answers, grades, or personal study data.

## Architecture

```text
<semester>/                  # Codex project; not an Obsidian vault
├── AGENTS.md
├── semester.md
├── Overview/                # independent Obsidian vault
└── Courses/
    ├── COURSE101/           # independent Obsidian vault
    └── COURSE202/           # independent Obsidian vault
```

Course vaults are authoritative. Overview stores only regenerable summaries. Vaults are siblings, never nested.

## Requirements

- Codex or ChatGPT desktop with local file access
- Obsidian with the core Bases plugin (tested with Obsidian 1.13)
- Python 3.10+
- Poppler (`pdfinfo`, `pdftotext`, `pdftoppm`) for full PDF ingestion

No OpenAI API key, backend, database, or community Obsidian plugin is required.

Automated Obsidian setup currently targets Codex desktop on macOS with Computer Use. If Computer Use is unavailable, file initialization can still run, but the UI setup is not considered complete.

## Install and Configure Obsidian

The full getting-started prompt explicitly authorizes Codex to download the current macOS app from the [official Obsidian download page](https://obsidian.md/download) when it is missing. Codex then uses Computer Use to:

- launch Obsidian and register each sibling folder with **Open folder as vault**;
- enable the Bases, Backlinks, Graph view, Properties view, Templates, and File recovery core plugins;
- open and visibly verify `Home.md`, Base views, and Graph view;
- leave the most useful Home or requested study page open.

CLI commands and `obsidian://` links may assist navigation, but they do not replace the live UI check. Codex must pause for any EULA, administrator credential, login, security-sensitive permission, or unexpected authorization screen. See [`references/obsidian-setup.md`](references/obsidian-setup.md).

## Install the Skill

In Codex, ask:

```text
Use $skill-installer to install https://github.com/YukunHe16/codex-obsidian-course-learning
```

Manual alternative:

```bash
git clone https://github.com/YukunHe16/codex-obsidian-course-learning.git \
  ~/.agents/skills/course-learning
```

Restart Codex if the skill does not appear immediately.

## Create a Semester

```bash
python3 ~/.agents/skills/course-learning/scripts/init_semester.py \
  --root ~/Documents/Study/FA26 \
  --term FA26 \
  --timezone America/Chicago
```

The command is idempotent: existing files are skipped, not overwritten.

## Add a Course

```bash
python3 ~/.agents/skills/course-learning/scripts/init_course.py \
  --semester-root ~/Documents/Study/FA26 \
  --course-id CS425 \
  --title "Distributed Systems" \
  --lecture-days Tuesday Thursday \
  --source-types lecture-slides syllabus textbook
```

Or simply tell Codex:

```text
Use $course-learning to initialize CS425 in my FA26 semester.
```

Open `<semester>/Overview` and each `<semester>/Courses/<COURSE_ID>` folder as separate Obsidian vaults.

## Daily Use

```text
Use $course-learning to ingest the new PDF in this course inbox.
Use $course-learning to teach Lecture 3 in Chinese with English technical terms.
Use $course-learning to quiz me one question at a time.
Use $course-learning to review everything due today.
Use $course-learning to validate the semester workspace.
```

The default writing contract is Chinese-primary prose, precise English technical terms, and English source citations. Edit `Course.md` to change it per course.

## Scheduled Workflows

Ask Codex to create three project-scoped Scheduled tasks for the semester root:

1. Daily material intake at 18:00.
2. Adaptive cross-course review every two days at 20:00.
3. Weekly Overview rebuild and checkpoint on Saturday at 11:00.

The prompts and mixed-autonomy boundaries are in [`references/scheduled-workflows.md`](references/scheduled-workflows.md). Keep reasoning effort at or below the level appropriate for your plan and usage limits.

## Validate

```bash
python3 ~/.agents/skills/course-learning/scripts/validate_vault.py \
  --semester-root ~/Documents/Study/FA26
```

The validator checks required structure, source hashes referenced by lecture notes, concept IDs and mastery ranges, Wikilinks, and Overview/course consistency.

## Privacy and Academic Integrity

- Do not publish copyrighted course materials unless you have permission.
- Generated semester workspaces ignore common raw binary formats by default.
- Keep graded-work policies in each `Course.md`.
- The Skill teaches concepts and creates independent practice; it must not produce prohibited submit-ready work.

## License

MIT. See [LICENSE](LICENSE).
