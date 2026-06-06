# 第 3 篇 · 邮件入库 + 杂志审稿

对应小红书第 3 篇：QQ 邮件（或手动粘贴）怎么进 vault，审稿邀请怎么落地，隔几天怎么 locate 续审。

## 解决什么问题

- 基金 / 审稿 / 征稿通知散在邮箱正文里，deadline 容易漏。
- 审稿接完就忘，再打开不知道文件在哪、EM 链接在哪、comment 记什么格式。
- 需要 AI 帮忙补 comment，但不能替你做审稿判断。

## 两层邮件流程

```text
捕获：原文 → _email_drop/（不猜截止日、不建 active）
整理：邮件整理 → 摘要卡片 → 你确认 → 10/11/12
```

可选 Phase 2：QQ IMAP 脚本拉未读邮件（凭证在本机，不进仓库）。

## 文件

| 路径 | 用途 |
|------|------|
| `examples/email-card.example.md` | 审稿邀请摘要卡片（脱敏） |
| `examples/peer-review-README.example.md` | **`10 杂志审稿/README` 完整脱敏版**（同内容亦在 `10 杂志审稿/README.example.md`） |
| `examples/peer-review-manuscript.example.md` | 单篇稿件 active 笔记结构 |
| `prompts/迁移口令.md` | 复制给 Cursor / Codex 的落地 prompt |
| `0 工作流/scripts/` | IMAP 拉取、Merge 队列（见 `README-email-inbox.md`） |
| `.cursor/rules/email-inbox.mdc` | 捕获 / 整理 Cursor 规则 |
| `reference/3.7 Workflow …` | 完整 workflow 定稿 |

## 推荐步骤

1. 建 `0 工作流/_email_drop/` 和 `0 工作流/邮件待整理队列.md`（或等价页面）。
2. 复制 `.cursor/rules/email-inbox.mdc`（或让 AI 按 examples 生成规则）。
3. 建 `10 杂志审稿/active/`，每篇稿一个子文件夹 + 笔记模板。
4. 把 `10 杂志审稿/README.example.md`（或 `examples/peer-review-README.example.md`）复制为 vault 内 `10 杂志审稿/README.md`。
5. 试跑：`邮件：` 粘贴一封 → `邮件整理` → 看卡片 → 确认后建 active。

## 关键原则

- 捕获和整理分开；整理前不写入正式任务系统。
- 审稿邀请卡片须含 Agree / Decline 原文链接。
- 每条 working comment 可定位到章节和原句。
- AI 补句子，不替你做 major/minor 裁决。
- 写入 active、Track、下一节点前，先列建议并等你确认。
