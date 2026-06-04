# 总安装说明

本仓库按**已发布**的小红书篇目拆模块。不要整包覆盖 vault；按篇迁移。

## 第 2 篇（当前唯一模块）

入口：[notes/02-researchtrack-workbench/](notes/02-researchtrack-workbench/)

建议顺序：

1. 读该文件夹 `README.md` 与 `examples/00_ResearchTrack.example.md`
2. 用 `prompts/迁移口令.md` 对 Cursor / Codex 说明你的 vault 结构
3. 先在一个项目上试点 ResearchTrack + 下一节点 + 工作台汇总

## 通用边界（可选）

[shared/AGENTS.md](../shared/AGENTS.md) 可合并进 vault 根。核心原则：

```text
AI 可以先读、先列建议、先给迁移方案；
写入项目页、下一节点、工作台前，先等用户确认。
```

## 不建议

- 直接覆盖已有 `AGENTS.md` 或 `0 工作流/`
- 一口气让 AI 重构全库

更稳：选一个模块、一个项目、小范围试点，跑通后再扩展。
