# 剪藏库 Clippings MOC

> 非 PDF 外部信息。文献仍走 Zotero → [[0 工作流/workflows/3.1 Workflow ：Zotero+Obsidian 文献由进到出全流程]]  
> **操作**：[[0 工作流/workflows/3.2 Workflow ：社交内容剪藏（公众号与小红书）]]

## 日常（小红书）

在 **Cursor** 粘贴 App「分享→复制链接」全文即可剪藏并归类。

## 目录

| 路径 | 用途 |
|------|------|
| `Xiaohongshu/_Inbox/` | 小红书（主路径） |
| `Xiaohongshu/<博主名>/` | 博主系列汇总 + 已归类单篇（如 [[Clippings/Xiaohongshu/小狗不是狗/00索引 小狗不是狗 Obsidian实战系列汇总]]） |
| `WeChat/_Inbox/` | 公众号（待接入） |
| `Web/_Inbox/` | 网页 |
| `_Processed/` | 已沉淀归档（可选） |

## 待处理

```dataview
TABLE source, author, tags, captured_at
FROM "Clippings"
WHERE status = "inbox" AND file.name != "00_Clippings_MOC"
SORT captured_at DESC
```

## 已归类

```dataview
TABLE source, author, tags, project, captured_at
FROM "Clippings"
WHERE status = "classified" AND file.name != "00_Clippings_MOC"
SORT captured_at DESC
```
