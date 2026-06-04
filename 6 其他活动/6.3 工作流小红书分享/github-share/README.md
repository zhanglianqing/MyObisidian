---
type: share-tooling
project: "[[00 工作流小红书分享 setup]]"
updated: 2026-06-04
---

# GitHub 分享包 · 维护说明

> **与日常 vault 分离**：定稿在 `0 工作流/`；本目录仅负责导出、脱敏、push 到 GitHub。  
> **Git 与已发篇目对齐**：小红书发了哪篇，Git 上才出现对应 `notes/xx-.../`；未发内容留在 `export-manifest.pending.*.json`。

## 原则

| 规则 | 说明 |
|------|------|
| 一篇一模块 | 第 2 篇 → `notes/02-researchtrack-workbench/` |
| 未发不上 Git | 小助理捕获等草稿在 `export-manifest.pending.ep03-assistant-capture.json` |
| 发布后再 push | 成稿发布 → 把 pending 并入 manifest → 导出 → commit → push |

## 一键导出（仅已发布篇目）

```powershell
cd "e:\Obisidian\MyObisidian\6 其他活动\6.3 工作流小红书分享\github-share"
.\Export-WorkflowShare.ps1
```

输出：`github-share/obsidian-cursor-workflow-starter/`（保留已有 `.git`）

## 目录

| 路径 | 用途 |
|------|------|
| `export-manifest.json` | **当前 Git 应含**的文件（`publishedEpisodes`） |
| `export-manifest.pending.*.json` | 待发模块草稿，不进 Git |
| `templates/` | GitHub README、SETUP、各篇模板 |
| `obsidian-cursor-workflow-starter/` | **Git 仓库根** |

## 远程仓库

https://github.com/zhanglianqing/obsidian-cursor-workflow-starter

## 新篇发布后的流程

1. 在 `export-manifest.json` 的 `publishedEpisodes` 追加篇号
2. 从对应 `export-manifest.pending.*.json` 把 `copies` / `templates` 并入 manifest
3. 重跑 `Export-WorkflowShare.ps1`
4. starter 目录 `git add .` → `commit` → `push`
5. 浏览器打开成稿里的 GitHub 链接，确认非 404

```powershell
cd "...\github-share"
.\Export-WorkflowShare.ps1
cd obsidian-cursor-workflow-starter
git add .
git commit -m "Add notes/0X-... for article X"
git push
```

## Cursor 索引

将 `obsidian-cursor-workflow-starter/` 加入 vault 根 `.cursorignore`（见 `.cursorignore-snippet.md`）。
