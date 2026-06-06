# 迁移口令

## 小助理：先读示例，不改文件

```text
请先阅读 notes/03-assistant-capture/ 下的 README、reference/3.6 Workflow … 和 shared/AGENTS.md 中小助理小节。
我想在现有 vault 里接上小助理捕获 workflow。
请先不要改文件，先列出：
1. 是否已有 小助理收件箱.md、_assistant_drop/ 等；
2. 捕获 / 整理两层分别缺什么规则或页面；
3. 与本周工作台、下一节点的边界说明；
4. 迁移步骤和哪些写入需要我确认。
```

## 试跑捕获

```text
小助理：安装验证条目
```

要求：只追加 `0 工作流/小助理收件箱.md`，回复新增行 +「已记入，未执行」；不改工作台、下一节点、项目页。

## 试跑整理

```text
小助理整理

要求：
1. 先运行 Merge-AssistantDrop.ps1 合并 _assistant_drop（如有）。
2. 读收件箱全部 open 项，列出建议去向（track / 下一节点 / 日常随想 / 勾选完成）。
3. 等我确认后再迁移或勾选。
```

## 周度（与邮件模块联用 · 可选）

```text
小助理整理下周工作
```

若已接邮件模块：先拉 QQ 邮件 + 邮件整理，再小助理 + 新周工作台。见 `notes/03-email-peer-review/` 与 `.cursor/rules/weekly-prep.mdc`（vault 内定稿）。

## Hooks（可选）

将 `notes/03-assistant-capture/.cursor/hooks.json` 合并进 vault 根 `.cursor/hooks.json` 的 `sessionStart`（与邮件 hook 可并存）。复制 `hooks/` 下 ps1 到 vault 根 `.cursor/hooks/`。
