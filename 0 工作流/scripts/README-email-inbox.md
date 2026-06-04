# QQ 邮件筛选脚本

主文档：[[0 工作流/workflows/3.7 Workflow ：QQ 邮件筛选入库]]  
Cursor 规则：`.cursor/rules/email-inbox.mdc`

## 刷新待整理队列（Phase 1 / 2 共用）

```powershell
cd "c:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
.\Merge-EmailDrop.ps1
```

含 pilot 样例索引：

```powershell
.\Merge-EmailDrop.ps1 -IncludePilot
```

- 输入：`0 工作流/_email_drop/*.md`（根目录，不含 `_pilot/` 除非 `-IncludePilot`）
- 输出：更新 `0 工作流/邮件待整理队列.md`
- **不**解析正文、**不**写入 10/11/12

| 脚本 | 用途 |
|------|------|
| `merge_email_drop.py` | 刷新队列索引（主实现） |
| `Merge-EmailDrop.ps1` | 调用上述 Python |
| `.cursor/hooks/merge-email-drop.ps1` | sessionStart 薄包装（fail open） |
| `fetch_qq_email.py` | IMAP 拉取（主实现） |
| `Fetch-QQEmail.ps1` | 调用上述 Python |

## IMAP 拉取（Phase 2 · 需凭证）

1. QQ 邮箱 → 设置 → 账户 → 开启 IMAP → 生成**独立密码**
2. 凭证二选一（**不要**写入 vault）：
   - **A** 用户环境变量：`QQ_MAIL_USER`、`QQ_MAIL_IMAP_PASSWORD`
   - **B** 用户主目录文件：`%USERPROFILE%\.qq_mail_imap.env`（Cursor 内置终端推荐，见 `Setup-QQMailCredentials.ps1`）

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Setup-QQMailCredentials.ps1
```

（若直接 `.\xxx.ps1` 报「禁止运行脚本」，一律加 `-ExecutionPolicy Bypass`。）

```powershell
cd "c:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
.\Fetch-QQEmail.ps1 -UnreadOnly -MaxCount 20
```

| 参数 | 默认 | 说明 |
|------|------|------|
| `-MaxCount` | 20 | 单次上限 |
| `-SinceDays` | 7 | 时间窗 |
| `-UnreadOnly` | 开 | 仅未读 |
| `-All` | 关 | 含已读 |

- 实现：`fetch_qq_email.py`（stdlib `imaplib`）
- 输出：`_email_drop/yyyyMMdd-HHmmss-主题.md`，`source: qq-imap`
- 拉取后建议再跑 `Merge-EmailDrop.ps1`
- **默认**拉取后在 QQ 服务器标已读（`--no-mark-seen` 可关）；已入库的用 `message_id` + `_imported_message_ids.txt` 去重
- 不必在 QQ 网页手动标已读

### 已有 drop 登记（避免第二次拉取重复 20 封）

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Register-EmailDrops.ps1
```

### 邮件整理后清理（默认）

整理确认并写入目标页后，**删除** `_email_drop/` 中对应 `.md`，再跑 `Merge-EmailDrop.ps1`。不要移入 `_done/`。

### `_done` 历史清理（仅当旧数据残留时）


```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Purge-EmailDropDone.ps1 -Days 14
# 预览：加 -DryRun
```

## Windows 计划任务（可选）

每 2～4 小时：

```powershell
Fetch-QQEmail.ps1 -UnreadOnly -MaxCount 20; Merge-EmailDrop.ps1
```

## 故障

| 现象 | 处理 |
|------|------|
| `QQ_MAIL_*` 未设置 | 设用户级环境变量后重开终端 |
| IMAP 登录失败 | 确认已开 IMAP、使用独立密码非 QQ 登录密码 |
| 队列不更新 | 手动 `Merge-EmailDrop.ps1`；查 drop 是否在根目录 |
