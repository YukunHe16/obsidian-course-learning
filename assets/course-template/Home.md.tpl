---
type: course-dashboard
course: {{COURSE_ID}}
term: {{TERM}}
---

# {{COURSE_ID}} 学习主页

完整导航：[[Index|课程 Wiki 总索引]]

> [!info] 课程配置
> [[Course|{{COURSE_ID}} - {{COURSE_TITLE}}]] · [[wiki/index|知识索引]] · [[raw/manifest|来源清单]] · [[wiki/log|维护日志]]

## 今日课程截止

![[views/Course.base#今日截止]]

## 未来 14 天课程截止

![[views/Course.base#未来 14 天截止日期]]

## 待核验课程节点

![[views/Course.base#待核验截止日期]]

## 今日复习 (Spaced review)

![[views/Course.base#今日复习]]

## 薄弱概念 (Weak concepts)

![[views/Course.base#薄弱概念]]

## 待审核 (Pending review)

![[views/Course.base#待审核]]

## 最近学习 (Recent study)

![[views/Course.base#最近学习]]

## 探索方式

- 打开全局 Graph 查看整门课的知识结构。
- 打开概念的 local Graph 查看 lecture、prerequisite 与 misconception 关系。
- 从 [[views/Course.base#全部截止日期|全部截止日期]] 检查作业、quiz、lab、exam 与 administrative milestones。
- 让 agent 复习这门课：Codex `使用 $course-learning 复习这门课`，Claude Code `/course-learning 复习这门课`。
