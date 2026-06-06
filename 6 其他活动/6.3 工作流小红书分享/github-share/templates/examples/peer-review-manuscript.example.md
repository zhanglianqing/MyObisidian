---
type: peer-review
manuscript_id: JOURNAL-26-xxxx
journal: Example Journal
title: "Example Manuscript Title (from invitation email)"
authors: Author A; Author B
editor: Editor Name
status: accepted
round: 1
deadline: 2026-06-22
planned_work: 2026-06-10
em_username: your-em-username
tags:
  - peer-review
source: email
---

# JOURNAL-26-xxxx · 短题目

> 每篇稿：`10 杂志审稿/active/稿号 短题目/` 文件夹 + 同名笔记 + PDF（下载后放同目录）。

## 日程

| 项 | 日期 |
|----|------|
| 邀稿 | YYYY-MM-DD |
| 接受审稿 | YYYY-MM-DD |
| **计划撰写** | **YYYY-MM-DD 起** |
| **编辑部截止** | **YYYY-MM-DD** |

## 进度

- [x] 接受审稿邀请
- [x] 邮件捕获：稿号 / 题目 / 截止 / EM 链接
- [ ] 下载 PDF，通读全文
- [ ] 撰写审稿意见
- [ ] 提交 Editorial Manager（建议截止前 1 天）

## Editorial Manager

- 查看稿件：（邮件里的 view / download 链接，原样粘贴）
- 提交审稿：（邮件里的 submit 链接）
- 登录：<https://www.editorialmanager.com/…/> · 用户名 `…`

## 摘要要点（邀稿邮件）

- **主题**：（1 行）
- **方法**：（1 行）
- **主要结论**：（2～3 条）
- **审稿注意**：（期刊特殊要求，如 Highlights / Graphical Abstract）

## 审稿笔记

（读稿时的方法学备忘、待查文献，不必写进 EM comment）

## Review comments (working)

（边读边记；AI 只在你明确说「写进 comment」时补全英文句子）

## 二轮修订

> 编辑部送修后：在同一文件夹更新 `round`，在此追加日期与作者回复对照；**不另建文件夹**。

| 轮次 | 收到日 | 新截止 | 状态 |
|------|--------|--------|------|
| 1 | — | — | — |

## 邮件来源

- 邀稿 drop：`_email_drop/…`
- 接受后 drop：`_email_drop/…`（如有）

## 生命周期（简）

```text
邮件整理确认 → active/ 建夹 + 笔记
撰写中 → status: accepted / drafting
提交 EM → 整夹移 archive/，status: decision_pending
编辑决定 → closed；二轮仍在原夹更新 round
```

总览页：`00_ReviewTrack` · 下一节点：`同期项目-下一节点#10 · 杂志审稿`
