# 小助理收件箱脚本

主文档：[[0 工作流/workflows/3.6 Workflow ：小助理收件箱（捕获与整理）]]  
Cursor 规则：`.cursor/rules/assistant-inbox.mdc`

## 合并手机 drop

```powershell
cd "c:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
.\Merge-AssistantDrop.ps1
```

- 输入：`0 工作流/_assistant_drop/*.md`（排除 README）
- 输出：追加到 `0 工作流/小助理收件箱.md`；成功 → `_done/`；失败 → `_failed/` + `.log`
- Cursor 打开工程时由 `.cursor/hooks.json` 的 `sessionStart` 自动调用

| 脚本 | 用途 |
|------|------|
| `Merge-AssistantDrop.ps1` | 合并 drop → 收件箱 |
| `.cursor/hooks/merge-assistant-drop.ps1` | Hook 薄包装（fail open） |
