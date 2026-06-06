# 第 3 篇 · 小助理捕获模块

对应小红书第 3 篇：`小助理：xxxx` 只捕获、不擅自执行；整理时迁往 track / 下一节点 / 工作台。

与 [03-email-peer-review](../03-email-peer-review/) 并列，可单独或一起迁移：

```text
临时碎片
  ↓
小助理收件箱
  ↓
整理确认
  ↓
项目 track / 下一节点 / 工作台
```

```text
临时碎片
  ↓
小助理收件箱
  ↓
整理确认
  ↓
项目 track / 下一节点 / 工作台
```

## 适合什么时候启用

- 你已经有项目文件夹和 ResearchTrack。
- 你已经有统一的下一节点 / 工作台。
- 你经常有临时碎片，不想直接污染正式任务系统。

## 包含内容

| 路径 | 用途 |
|------|------|
| `prompts/迁移口令.md` | 复制给 Cursor / Codex 的落地 prompt |
| `shared/AGENTS.md`（仓库根） | 捕获与整理边界参考 |
| `.cursor/rules/assistant-inbox.mdc` | 小助理触发词与禁止项 |
| `.cursor/hooks.json` + `.cursor/hooks/` | 可选：打开 Cursor 时合并手机 drop |
| `0 工作流/小助理收件箱.md` | 收件箱模板 |
| `0 工作流/_assistant_drop/` | 手机 drop 目录（含 `_done/`、`_failed/`） |
| `0 工作流/scripts/` | `Merge-AssistantDrop.ps1` 与说明 |
| `reference/3.6 Workflow …` | 完整 workflow 定稿 |

## 验证口令

```text
小助理：安装验证条目
```

预期：只写入 `小助理收件箱.md`，不改工作台、不展开方案。
