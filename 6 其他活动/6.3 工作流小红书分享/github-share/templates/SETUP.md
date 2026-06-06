# 总安装说明

本仓库按**已发布**的小红书篇目拆模块。不要整包覆盖 vault；按篇迁移。

## 第 2 篇 · ResearchTrack + 工作台

入口：[notes/02-researchtrack-workbench/](notes/02-researchtrack-workbench/)

建议顺序：

1. 读该文件夹 `README.md` 与 `examples/00_ResearchTrack.example.md`
2. 用 `prompts/迁移口令.md` 对 Cursor / Codex 说明你的 vault 结构
3. 先在一个项目上试点 ResearchTrack + 下一节点 + 工作台汇总

## 第 3 篇 · 邮件 + 审稿

入口：[notes/03-email-peer-review/](notes/03-email-peer-review/)

建议顺序：

1. 读 `README.md` 与 `examples/` 下三个示例
2. 复制 `prompts/迁移口令.md` 给 Cursor，先列迁移步骤、等你确认再改文件
3. 可选 IMAP：QQ 开启 POP3/IMAP → 本机 `%USERPROFILE%\.qq_mail_imap.env`（见 `0 工作流/scripts/.qq_mail_imap.env.example`）→ 运行 `Setup-QQMailCredentials.ps1` / `Fetch-QQEmail.ps1` / `Merge-EmailDrop.ps1`
4. 手动试跑：`邮件：` 粘贴 → `邮件整理` → 确认后建 `10 杂志审稿/active/`

## 第 3 篇 · 小助理捕获

入口：[notes/03-assistant-capture/](notes/03-assistant-capture/)

建议顺序：

1. 读 `README.md` 与 `reference/3.6 Workflow …`
2. 复制 `prompts/迁移口令.md` 给 Cursor，先列步骤、等你确认再改文件
3. 复制 `0 工作流/小助理收件箱.md` 模板到 vault；可选合并 `.cursor/hooks.json`（开 Cursor 时自动合并手机 drop）
4. 验证：`小助理：安装验证条目` → 只写入收件箱，不改工作台

与邮件模块联用时，`小助理整理下周工作` 会先拉邮件再整理（见邮件模块 + vault 内 `weekly-prep` 定稿）。

## 通用边界（可选）

[shared/AGENTS.md](../shared/AGENTS.md) 可合并进 vault 根。核心原则：

```text
AI 可以先读、先列建议、先给迁移方案；
写入项目页、下一节点、工作台前，先等用户确认。
```

## 不建议

- 直接覆盖已有 `AGENTS.md` 或 `0 工作流/`
- 一口气让 AI 重构全库

更稳：选一个模块、一个项目、小范围试点，跑通后再扩展。
