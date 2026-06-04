# _assistant_drop

手机快捷指令 / 自动化写入的**待合并**条目。PC 开 Cursor 时由 `sessionStart` Hook 调用 `Merge-AssistantDrop.ps1` 合并进 [[0 工作流/小助理收件箱]]。

## 目录约定

| 路径 | 用途 |
|------|------|
| 本目录根 | 待合并的 `.md` / `.txt` |
| `_done/` | 已成功合并的 drop |
| `_failed/` | 解析失败 + 同名 `.log` |

## 单条 drop 文件格式

文件名：`yyyyMMdd-HHmmss.md`（快捷指令生成）

```markdown
---
type: idea
captured_at: 2026-05-24T15:30
source: ios-shortcut
---

明天交伦理材料
```

- **type**（脚本用英文码，收件箱行内显示中文区名）：`todo` | `idea` | `notice` | `misc`（缺省 → misc）
- 对应收件箱 `##` 顺序：第 1～4 区（待办 / 想法 / 通知 / 杂项）
- **正文**：首段非空行为一条捕获内容（单行或多行均可，合并时压成一行摘要）

## 合并后行格式

写入收件箱对应 `##` 区：

```markdown
- [ ] 2026-05-24 15:30 | 待办 | 明天交伦理材料
```

## 手动合并

```powershell
cd "c:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
.\Merge-AssistantDrop.ps1
```

主文档：[[0 工作流/workflows/3.6 Workflow ：小助理收件箱（捕获与整理）]]
