# 印象笔记 HTML 导入脚本

主文档：[[0 工作流/workflows/3.5 Workflow ：Legacy 前期项目入库]]（Step 6）

## 脚本

| 文件 | 用途 |
|------|------|
| `import_rtnf_evernote_html.py` | 将「多个 HTML」导出包写入 `3c …/印象笔记归档/` |
| `import_1a2a_evernote_html.py` | **白名单**导入 → `1a-2a …/印象笔记归档/notes/00_核心/` |
| `cleanup_evernote_export_desktop.py` | 从桌面导出目录删除已入库 / 确定不要项（保留待讨论笔记） |
| `import_evernote_kb_archive.py` | 剩余 HTML → `7 可复用知识库/印象笔记存档/`（扁平 notes + MOC）；`--append` 追加不 wipe |
| `extract_kb_to_ppc.py` | 从垃圾场迁出 TMS/PPC/省自然 → 计划1 `印象笔记归档/` |

## 依赖

```powershell
pip install html2text beautifulsoup4 lxml
```

## 常用命令

```powershell
cd "e:\Obisidian\MyObisidian\0 工作流\scripts"
python import_rtnf_evernote_html.py --export-dir "F:\SYSTEM\DESKTOP\RTNF-印象笔记导出"
```

复用到其他项目：编辑脚本内 `PROJECT`、`ARCHIVE`（或复制脚本后改名），并调整 `categorize()` 规则。

## 分线：项目归档 vs 垃圾场

| 脚本 | 落点 | 索引 |
|------|------|------|
| `import_rtnf_evernote_html.py` / `import_1a2a_evernote_html.py` | 项目内 `印象笔记归档/` | 默认 |
| `import_evernote_kb_archive.py` | `7 可复用知识库/印象笔记存档/` | **不索引**（`.cursorignore`） |

混合控制台导出：**先全量迁入垃圾场**，桌面删垃圾；项目已确认的用白名单单独入 `前期产出/`。

> **TODO**：从 [[7 可复用知识库/印象笔记存档/MOC]] 按 topic 提取有用笔记 → 项目 / 可复用知识库 / Zotero。检索见 [[0 工作流/workflows/3.5 Workflow ：Legacy 前期项目入库#Step 6 · 印象笔记 HTML 迁入（可选）]]。
