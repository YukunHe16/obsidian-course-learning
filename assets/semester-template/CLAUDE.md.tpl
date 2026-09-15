# {{TERM}} Learning System (Claude Code)

## Read the shared contract first

The semester contract lives in `AGENTS.md` in this directory. It is shared by every agent and it is authoritative: project boundaries, source rules, write permissions, learning behavior, and verification all live there. Read it before acting, and do not duplicate its rules here.

@AGENTS.md

## Claude Code specifics

- Invoke the Skill as `/course-learning`, or let the skill description trigger it. Confirm it is installed with `/skills`; the expected location is `~/.claude/skills/course-learning/`.
- This root is an agent project, not an Obsidian vault. `Overview/` and every `Courses/<COURSE_ID>/` are independent sibling vaults.
- `CLAUDE.md` and `AGENTS.md` must stay consistent. Edit `AGENTS.md`; keep this file thin.
- Obsidian work uses the `obsidian` CLI against the running app. It is opt-in: if `obsidian version` reports the command line interface is not enabled, turn it on once at **Settings > General > Advanced**. Useful commands (`obsidian vaults verbose`, `plugins:enabled filter=core`, `open path=Home.md`, `base:query`, `command id=graph:open`, `dev:screenshot path=<file>.png`). Read the screenshot back before reporting that a page, Base, or Graph is fine. If no visual check is possible, report the UI portion as unverified instead of assuming it.
- Unattended source maintenance follows AGENTS.md and Course.md: ordinary notes may become active after source checking; unresolved conflicts, policy changes and destructive overwrites require confirmation. Maintenance never initiates a learning session.

## Daily entry points

```text
/course-learning 整理所有 active 课程 inbox 中的新资料
/course-learning 讲解 Lecture 1
/course-learning 逐题考我
/course-learning 复习我指定的讲次或主题
/course-learning 查看未来 14 天的 deadlines
/course-learning 检查整个 semester
```
