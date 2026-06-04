# Research TODO 总控

本页依赖社区插件 **Tasks**（Obsidian 内搜索安装）。

| 层级 | 写在哪 | 粒度 |
|------|--------|------|
| **下一节点** | [[同期项目-下一节点]] | 每项目标题下 **1 条** open；工作台 §二 同款查询 |
| **本周细则** | [[本周科研推进]] | 本周可勾选的多条任务 |
| **长期 track** | 各 `00_ResearchTrack.md` / `RESEARCH_TRACKER.md` | 项目内完整待办 |
| **排班** | [[本周工作台]] §一 | 时段 |

**本周主题（2026-06-01 周）**：RTNF 瑞士会征文（**06-03 注册** · **06-10 截止**）+ **Eur Radiol 全包** + 指南 topic + RTNF 改稿 + 3.8；06-08 → 华西/邮件/眉彡；06-15 → 省自然伦理。维护顺序：[[本周工作台]] §一 → §二 → [[本周科研推进]]。

---

## 下一节点（里程碑，非本页维护）

编辑 [[同期项目-下一节点]]；[[本周工作台]] §二 已嵌入相同查询。此处便于从总控页跳转。

```tasks
not done
filename includes 同期项目-下一节点
group by heading
sort by happens
```

---

## 下周计划（请每周一改日期）

将下面查询里的起止日期改成你的「下周一～下周日」或任意一周窗口。

```tasks
not done
(filename includes ResearchTrack) OR (filename includes RESEARCH_TRACKER) OR (filename includes 本周科研推进)
happens after 2026-05-31
happens before 2026-06-08
sort by happens
```

---

## 未完成：按项目路径分组

同文件名（如多个 `00_ResearchTrack.md`）会按**完整路径**分开显示。

```tasks
not done
(filename includes ResearchTrack) OR (filename includes RESEARCH_TRACKER) OR (filename includes 本周科研推进)
group by path
sort by priority
```

---

## 未完成：按优先级（全列表）

```tasks
not done
(filename includes ResearchTrack) OR (filename includes RESEARCH_TRACKER) OR (filename includes 本周科研推进)
sort by priority
```

---

## 高优先级且未完成

```tasks
not done
(filename includes ResearchTrack) OR (filename includes RESEARCH_TRACKER) OR (filename includes 本周科研推进)
priority is high
sort by happens
```

---

## 已过期或今天到期（需尽快处理）

含「今天及以前」的 `📅` / `⏳`。

```tasks
not done
(filename includes ResearchTrack) OR (filename includes RESEARCH_TRACKER) OR (filename includes 本周科研推进)
happens before tomorrow
sort by happens
```

---

## 尚未标日期（建议补上 ⏳ 或 📅）

便于在周视图里出现；否则容易只在「按路径分组」里被看到。

```tasks
not done
(filename includes ResearchTrack) OR (filename includes RESEARCH_TRACKER) OR (filename includes 本周科研推进)
no due date
no scheduled date
sort by path
```



## 写法约定（写在项目跟踪笔记里）

- 普通任务：`- [ ] 描述`
- **计划日**（打算哪天做）：`⏳ YYYY-MM-DD`
- **截止日**（必须哪天前）：`📅 YYYY-MM-DD`
- **优先级**：高 `🔼`、低 `🔽`（中间可不加符号）
- 在任务行用 Tasks 命令「Create or edit task」可图形化补全上述字段。

示例：

```markdown
- [ ] 给出数据表头 ⏳ 2026-05-19 🔼
```

---
