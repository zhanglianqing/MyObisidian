# Literature · 文献内化库

> [[0 工作流/workflows/3.8 Workflow ：文献库组织架构]] · [[3.1 Workflow ：Zotero+Obsidian 文献由进到出全流程]]  
> **定稿**：2026-06-04

## 路径

| 路径 | 内容 |
|------|------|
| `{citekey}.md` | **S1 定稿**（你已认可的内化；多 project 复用） |
| `_drafts/{citekey}.md` | 晋升前草稿（Agent 从原料抽稿） |
| `_templates/` | `literature-note` · `literature-draft` |
| `_views/MOC-*.md` | 主题索引，只链定稿 |

不按项目分子目录。项目侧只 `[[citekey]]` / `[@citekey]`。

## 流程

1. **S0**：Zotero + `My Library.bib`（不打 tag）。  
2. **原料**：`…/印象笔记归档/` 等。  
3. **草稿**：`_drafts/{citekey}.md`（模板 `literature-draft`）。  
4. **定稿**：你审改后 → `{citekey}.md`（模板 `literature-note`），删草稿。  
5. **项目**：track / 文献队列加链。  
6. **MOC**（可选）：定稿后进 `_views/`。

## Agent

- 改稿、综合 → `@literature/{citekey}.md`（定稿）  
- 起草 → `_drafts/`；勿未确认覆盖定稿  
- 原料考古 → `@…/印象笔记归档/…`

## 迁移队列（过渡）

进行中的引文/内化对照表 → [[7 可复用知识库/_migration/README]]（**不在**项目文件夹；验收后删）。

## 变更

| 日期 | 说明 |
|------|------|
| 2026-06-04 | `_drafts/`；`_migration/` 过渡队列 |
| 2026-05-29 | 平面 citekey + MOC |
