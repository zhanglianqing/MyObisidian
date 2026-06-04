# 周度整理脚本

主文档：[[0 工作流/workflows/3.4 Workflow ：长周期项目与每日规划（试点）#定稿摘要（调用入口）]]  
Cursor 规则：`.cursor/rules/weekly-prep.mdc`

## 一键 Step 0（邮件 + 队列 + 小助理 drop）

```powershell
cd "c:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
powershell -NoProfile -ExecutionPolicy Bypass -File .\Invoke-WeeklyPrep.ps1
```

| 参数 | 默认 | 说明 |
|------|------|------|
| `-MaxCount` | 30 | 单次 IMAP 上限（周度略大于日常 20） |
| `-SinceDays` | 14 | 时间窗 |
| `-AllMail` | 关 | 加上则拉全部未限制未读（慎用） |

## Cursor 口令

```text
小助理整理下周工作
```

Agent 顺序：本脚本 → `邮件整理` 卡片（确认后落地）→ 小助理 open 清单 → 3.4 新周清单。

## 与 sessionStart Hook 分工

| 时机 | 行为 |
|------|------|
| 每次开 Cursor | Hook 仅 `Merge-EmailDrop`（刷新索引，不拉 IMAP） |
| 周度整理 | `Invoke-WeeklyPrep` 含 **IMAP 拉取** |

可选：Windows 计划任务工作日跑 `Invoke-QQEmailFetch.ps1`，周度整理时 drop 更新更及时（见 3.7 §七）。
