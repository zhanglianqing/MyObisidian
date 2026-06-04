# 第 2 篇 · ResearchTrack + 工作台汇总

这一模块对应小红书第 2 篇：不是讲小助理，而是讲多项目 workflow 的基础骨架。

## 解决什么问题

当你同时有多个科研、审稿、基金、会议或长期任务时，需要两条线互相配合：

```text
项目文件线 = 正式资料、记录、数据说明、ResearchTrack 留在项目内
工作台汇总线 = 每个项目抽出 1 个当前下一节点，汇总到统一视图
```

日常使用时，不需要逐个翻项目文件夹；先看工作台和下一节点，需要深挖时再点回项目自己的 `ResearchTrack`。

## 文件

| 文件 | 用途 |
|------|------|
| `examples/00_ResearchTrack.example.md` | 脱敏 ResearchTrack 示例 |
| `prompts/迁移口令.md` | 可直接复制给 Cursor / Codex 的迁移 prompt |

## 推荐迁移步骤

1. 把 `examples/00_ResearchTrack.example.md` 放到你的 vault，例如 `examples/`。
2. 让 Cursor / Codex 先读示例，不要立即改文件。
3. 选一个最典型的项目，建立第一个 `00_ResearchTrack.md`。
4. 从这个项目抽出 1 条当前下一节点。
5. 再做统一的 `同期项目-下一节点` 和 `本周工作台`。

## 关键原则

- 项目资料保留在项目文件夹内。
- `ResearchTrack` 负责项目上下文，不负责装所有本周细则。
- 每条项目线只抽 1 条当前下一节点到统一页面。
- 工作台只汇总当前视图，不变成完整 todo list。
- 写入正式任务系统前，让 AI 先列建议并等你确认。
