# 专题外置 AI · 临时 PDF 包

> **归属**：[[0 工作流/workflows/3.8 Workflow ：文献库组织架构]] §7  
> **定稿**：2026-05-29

本目录存放 **Gemini AI Studio / NotebookLM** 等网页端工具用的 **临时 PDF 副本**，不是文献权威库。

---

## 何时使用

| 场景 | 工具 | 本目录 |
|------|------|--------|
| 日常改稿、单篇核对 | Cursor · Copilot · Zotero LLM | **不用** |
| 跨多篇原文对照、专题综述式对话 | Gemini · NotebookLM | **用** |

---

## 命名与生命周期

```
0 工作流/工具箱/ai专题/
└── <topic>-<YYYYMMDD>/     # 例：hippocampus-parcellation-20260529
    ├── paper1.pdf          # 从 Zotero 链接路径复制，非移动原件
    └── ...
```

1. **建夹**：专题开始前创建；topic 用英文或拼音短名即可。  
2. **装填**：Zotero 按 tag 筛选 → 在资源管理器中打开 PDF → **复制**到本夹（保留 S0 原路径不动）。  
3. **使用**：上传 Gemini / 或复制到 Drive `NotebookLM-drop/<topic>/`（仅当连续数周用 NL）。  
4. **收尾**：专题结束 → **整夹删除** 或移出 vault 冷备份；勿回写 Zotero Collection。

---

## 硬规则

- **禁止**在 `1 主线项目/` 下为外置 AI 长期存放 PDF。  
- **禁止**把 `_ai_sessions` 当作第二套 Zotero 分类树。  
- canonical PDF 仅在坚果云 `zotero/literature/{Cornerstone|My Papers|Everything}/`。  
- 本目录内容 **可不进 Cursor Index**（大 PDF 拖慢检索）。

---

## 可选：脚本（未实现）

日后可由 Cursor 根据「tag 列表」批量复制 PDF 到指定子夹；当前 **手动复制** 即可。
