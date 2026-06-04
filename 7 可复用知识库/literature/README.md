# Literature · 文献内化库（S1）

> **架构总述**：[[0 工作流/workflows/3.8 Workflow ：文献库组织架构]]  
> **Zotero 插件与同步**：[[0 工作流/workflows/3.1 Workflow ：Zotero+Obsidian 文献由进到出全流程]]  
> **定稿**：2026-05-29

本目录是 Obsidian 侧 **唯一** 的正式 Literature Note 存放处（平面结构，不按项目分子文件夹）。

---

## 目录约定

| 路径 | 用途 |
|------|------|
| `{citekey}.md` | 单篇内化笔记（与 Zotero BBT citekey 一致） |
| `_templates/literature-note.md` | 新建笔记时复制 frontmatter 与章节标题 |
| `_views/MOC-*.md` | 主题索引（S2），只放链接，不复制全文 |

**不要**在此建 `1a-2a/`、`海马/` 等子目录。项目归属写在 frontmatter 的 `zotero_tags` / `slots` / `projects` 中。

---

## 新建一篇 S1（晋升流程）

1. **S0**：Zotero 用 DOI 添加 → 打 tag → 默认 Collection **`Everything`**；基石 → **`Cornerstone`**；自有论文 → **`My Papers`**。  
2. **阅读**：Zotero LLM 或读 PDF；结论写入 S1，而非在项目文件夹里开长文摘要。  
3. **S1**：复制 `_templates/literature-note.md` → 重命名为 `{citekey}.md` → 填写四段正文。  
4. **S2**：若 `scope/core`，加入 `_views/MOC-全局基石.md`（或相应主题 MOC）。  
5. **项目**：在相关 `00_ResearchTrack` 或 `文献-阅读队列.md` 增加 `[[{citekey}]]` 或 `[@citekey]`。

**何时可以不建 S1**：仅备查、未引用、未进任何 MOC 的文献——留在 Zotero 即可。

---

## 与项目笔记的关系

| 位置 | 放什么 |
|------|--------|
| 本目录 `literature/` | 跨项目可复用的文献内化 |
| `1 主线项目/…/定稿/` | 主稿 digest、投稿包（见 [[3.5 Workflow ：Legacy 前期项目入库]]） |
| `1 主线项目/…/印象笔记归档/` | **仅**项目私有历史实验笔记（Legacy Step 6）；迁移完成后随印象笔记整库删除，**不**与 S1 混用 |

---

## 专题深读（外置 AI）

需要 Gemini / NotebookLM 批量读 PDF 时，见 [[0 工作流/工具箱/ai专题/README]]。  
**不要**为外置 AI 在本目录下再建 PDF 子文件夹。

---

## 变更记录

| 日期 | 说明 |
|------|------|
| 2026-05-29 | 初建；平面 citekey 笔记 + `_views` |
