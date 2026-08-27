---
type: semester-index
term: "{{TERM}}"
language: "{{LANGUAGE}}"
---

# {{TERM}} 学期学习系统索引

> 学期根目录是 agent project（Codex 或 Claude Code），不是 Obsidian Vault。Overview 与每门课程是独立的 sibling Vaults。

## 核心入口

- `semester.md`：学期配置与默认策略
- `Overview/Index.md`：跨课程总索引
- `Overview/Home.md`：当前学习状态
- `Courses/`：各课程独立 Vault
- `AGENTS.md`：共享 agent 约定（Codex 直接读取）
- `CLAUDE.md`：Claude Code 入口，指向 `AGENTS.md`

## 工作流

Codex 使用 `$course-learning`，Claude Code 使用 `/course-learning`，后面接同样的指令：

- 资料摄取：`整理所有 active 课程 inbox 中的新资料`
- 跨课程复习：`复习今天到期的内容`
- 系统检查：`检查整个 semester`

## 语言

Wiki 正文以中文为主；English 用于专业术语、proper nouns、官方 source titles 与 citations。
