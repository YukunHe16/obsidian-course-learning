# Agent compatibility (Codex and Claude Code)

This Skill is agent-neutral. It is supported on **Codex** and on **Claude Code**. Only five things differ: install path, invocation syntax, project instruction file, GUI/app automation mechanism, and scheduling. Every workflow reference is shared; read this file to translate the agent-specific step, then follow the shared reference unchanged.

Never fork workflow content per agent.

## Install and invoke

| | Codex | Claude Code |
| --- | --- | --- |
| Skill directory | `~/.agents/skills/course-learning/` | `~/.claude/skills/course-learning/` (personal) or `<project>/.claude/skills/course-learning/` (project-scoped) |
| Invocation | `$course-learning` | `/course-learning`, or automatic when the request matches the skill description |
| Discovery check | restart Codex and list skills | run `/skills` and confirm `course-learning` is listed |
| Extra metadata | `agents/openai.yaml` | none; the `SKILL.md` frontmatter is the whole contract |

The `SKILL.md` frontmatter (`name`, `description`) satisfies both agents. `agents/openai.yaml` is Codex-only interface metadata and is ignored by Claude Code.

Paths inside `SKILL.md` (`references/...`, `scripts/...`) resolve relative to the installed skill directory under both agents.

## Project instruction file

`scripts/init_semester.py` writes **both** files into the semester root:

- `AGENTS.md` — the full semester contract. Codex reads it automatically.
- `CLAUDE.md` — what Claude Code reads. It defers to `AGENTS.md` and adds only Claude-Code-specific notes.

Keep the contract in `AGENTS.md`. When it changes, do not copy prose into `CLAUDE.md`; a second copy will drift. `scripts/validate_vault.py` requires at least one of the two and warns when the other is missing, so semesters created before this layer existed keep validating.

## Obsidian automation (both agents)

Obsidian 1.13 ships an official `obsidian` CLI (`/usr/local/bin/obsidian` on macOS, symlinked into `Obsidian.app`). Two prerequisites:

- **It is opt-in.** If a command answers `Command line interface is not enabled. Please turn it on in Settings > General > Advanced.`, or `obsidian` is not on `PATH`, that toggle is off. Enabling it is a one-time GUI action — do it with a GUI capability or ask the user; do not treat the CLI as unavailable without checking.
- **It talks to the running app.** Launch Obsidian first (`open -a Obsidian`) and confirm `obsidian version` answers.

Once both hold, prefer the CLI over ad-hoc GUI clicking under either agent, because it is deterministic and its output is checkable:

```bash
obsidian version
obsidian vaults verbose                                   # registered vaults and paths
obsidian vault=<VAULT> plugins:enabled filter=core        # confirm bases/graph/backlink/file-recovery
obsidian vault=<VAULT> plugin:enable id=bases filter=core
obsidian vault=<VAULT> open path=Home.md
obsidian vault=<VAULT> bases                              # base files in the vault
obsidian vault=<VAULT> base:query path=views/Course.base view="<view name>" format=md
obsidian vault=<VAULT> command id=graph:open
obsidian vault=<VAULT> dev:screenshot path=/tmp/vault.png
```

A successful `base:query` is real evidence that a Base parses and returns rows; a rendered `dev:screenshot` is real evidence about the live window. Neither is a substitute for the other: query proves the data layer, the screenshot proves the UI.

### The one step the CLI cannot do

Registering a new folder as a vault (**Open folder as vault**) has no CLI command.

1. Preferred: perform it in the GUI — Codex Computer Use, a computer-use MCP server under Claude Code, or the user. `obsidian command id=app:open-vault` opens the vault switcher to speed this up.
2. Fallback, only with the user's agreement: quit Obsidian, add an entry under `vaults` in `~/Library/Application Support/obsidian/obsidian.json` (key = a fresh 16-hex id, value = `{"path": "<absolute path>", "ts": <epoch milliseconds>}`), relaunch, and verify with `obsidian vaults verbose`.
3. If neither works, report the UI portion as blocked and give the exact manual clicks. Do not describe file initialization as completed setup.

## Visible verification per agent

The invariant is identical for both agents: never claim a vault, Base, or Graph works from generated files alone, and never present CLI output as UI verification when no UI was observed.

- **Codex:** Computer Use drives installation, the Vault switcher, Settings, navigation, and visual checks. Re-read the screen after each action.
- **Claude Code:** there is no built-in desktop Computer Use. Use, in order of preference: (a) `obsidian dev:screenshot path=<file>.png` and then read the PNG with the Read tool; (b) a computer-use MCP server if the user has one connected; (c) `screencapture -x <file>.png`, which needs macOS Screen Recording permission for the terminal app. If none is available, say the UI verification is unavailable and list the manual checks.

## Installing Obsidian when it is missing

Both agents may install from official sources only. Check `/Applications/Obsidian.app`, `$HOME/Applications/Obsidian.app`, and `command -v obsidian` before deciding it is absent.

- **Codex:** Computer Use on <https://obsidian.md/download>.
- **Claude Code:** `brew install --cask obsidian`, or download the macOS release linked from <https://obsidian.md/download> with `curl`, then mount and copy it. Never an advertisement link, mirror, or unofficial build.

Under both agents, pause at any EULA, administrator credential, login, security-sensitive permission, or unexpected authorization screen. Never type the user's password.

## Optional material maintenance

Learning is on demand. Do not schedule quizzes or periodic learning reports. Only explicit requests for source intake or source maintenance may use the current agent's available scheduling mechanism; no default cadence or setup-time scheduling prompt is required. Preserve paused status of existing tasks. Follow [scheduled-workflows.md](scheduled-workflows.md).

## What does not change

Vault schema, deadline schema, ingestion, teaching, assessment, validation, and the academic-integrity boundary are identical under both agents. If a workflow reference and this file disagree about anything other than the five items above, the workflow reference wins.
