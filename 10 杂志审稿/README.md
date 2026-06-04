# 杂志审稿

> 期刊邀稿、在审、二轮修订的**工作区**。简历条目见 [[张帘青-简历#担任审稿]]；任务总览 → [[00_ReviewTrack]]；下一节点 → [[同期项目-下一节点#10 · 杂志审稿]]。

## 目录结构

| 路径 | 用途 |
|------|------|
| `active/` | 进行中：已接受、撰写中、尚未提交 EM |
| `archive/` | 首轮已提交、待编辑决定，或已完结（决定已出、无待办修订） |
| [[00_ReviewTrack]] | Tasks 总览；按 `manuscript_id` 检索 |

每篇稿一个子文件夹，**文件夹名以稿件号开头**（如 `IMAG-26-0219 …`）。**二轮修订不新建文件夹**——仍在原目录下更新 `round` 与「二轮修订」小节（可能在 `archive/`）。

## 生命周期与归档

单篇笔记 frontmatter 字段：

- `manuscript_id`：期刊稿号（不变）
- `round`：`1` / `2` / …
- `status`：`invited` → `accepted` → `drafting` → `submitted` → `decision_pending` → `closed`；若收到修订稿 → `r2_pending` → …
- `submitted` / `archived`：提交 EM 日与移入 `archive/` 日（YYYY-MM-DD）

| 阶段 | 位置 | `status` | 动作 |
|------|------|----------|------|
| 接受邀稿 ~ 撰写中 | `active/` | `accepted` / `drafting` | 建文件夹 + 更新 [[00_ReviewTrack]]、[[同期项目-下一节点#10 · 杂志审稿]] |
| **提交 EM 后** | **`archive/`** | **`decision_pending`** | 整夹移入 `archive/`；笔记保留 Review comments；Track 移入「已提交 · 待编辑决定」 |
| 编辑决定已出 | `archive/` | `closed` | 在 Track「已完结」记一行摘要 |
| 编辑部送二轮 | 原文件夹（多在 `archive/`） | `r2_pending` | 更新 `round`；若需再写意见，可暂移回 `active/` 或仍在 `archive/` 写 |

**归档清单（提交后）**

1. 笔记 frontmatter：`status: decision_pending`，填 `submitted`、`archived`
2. 进度勾选、日程补「提交审稿」「归档」
3. `active/稿号…/` → `archive/稿号…/`（含 PDF）
4. 更新 [[00_ReviewTrack]]、[[archive/README]]、[[同期项目-下一节点#10 · 杂志审稿]]

## 二轮修订

在原目录下更新 `round`，在笔记「二轮修订」小节追加日期与作者回复对照；**不另建文件夹**。

## 定期清理（建议每季度或每半年）

1. `archive/` 中 `status: closed` 超过 **12 个月**、且无 revisit 价值 → 删除文件夹（保留 `00_ReviewTrack` 里一行摘要即可）
2. 勿删：`status: decision_pending` / `r2_pending`，或仍需跟进的条目

## 给 Cursor

```text
维护杂志审稿：新邀稿在 active/ 建 IMAG-xxxxx 文件夹 + 更新 00_ReviewTrack 与同期项目-下一节点；提交 EM 后按「归档清单」移入 archive/；二轮在同一文件夹追加 round。
```

## 给 Codex：审稿协作习惯

> 用途：后续与 Codex 一起审稿时，按此风格记录 working comments。

### 基本原则

- 用户在审稿过程中会随时提问、吐槽、标记疑点或给出半成品 comment。
- Codex 的主要任务是把用户的 comment 补成可提交、可定位、不过度扩展的审稿句子。
- 默认写入当前稿件笔记的 `Review comments (working)` 或对应审稿笔记区。
- 不主动把每个想法扩展成完整审稿意见，除非用户明确要求。
- **未经用户明确说「合并」「删减」「精简」，不要合并条目、不要大幅改写或删改 comment 含义。**
- 用户明确说“不写进 comment”时，只对话回应，不记录。
- 审稿协作要保持审慎：用户不一定一直是对的。若用户的 comment 可能忽略了稿件中已说明的内容，或可能源于对论文所属领域常规做法、常见术语不熟悉，Codex 应及时提示并提供相关信息，供用户二次确认后再决定是否记录。

### Comment 记录风格

- 每条 comment 要能让作者找到具体位置。
- 优先带上章节、段落、原句片段，必要时带页码或行号。
- 可以引用原句的一部分，用省略号即可，不需要整段复制。
- 句子要直接、可执行，避免泛泛批评。
- 对不确定之处保持审稿语气，例如使用 `appears to`、`may`、`would benefit from`。
- 如果用户已经判断很明确，可以用更直接的语气，例如 `should be removed`。

### 用户偏好的审稿重点

- 关注摘要、Key Points、Introduction、Methods 中是否存在句子结构问题、未完成编辑、语义不清。
- 关注 hypothesis 是否清楚，因为它会影响后续实验设计和结果解读。
- 关注研究 aim 是否过大、问题是否泛化。
- 关注 literature review 是否引用过载、背景堆叠、迟迟不进入研究 gap。
- 关注 key points 是否过度机制化或超过数据能证明的范围。
- 关注 Methods 是否说明本研究实际怎么做，而不是堆 prior studies 或数据库字段细节。
- 对 custom pipeline、control cost、controllability、thresholding、parcellation resolution 等方法细节，要求作者给出足够的操作化定义和理由。

### 推荐写法

```text
Abstract, Results: The sentence "..." is incomplete. Please clarify the comparison or association.
```

```text
Introduction, final paragraph: The hypothesis sentence beginning "..." is hard to read and seems unfinished. Please revise it so the main hypothesis is clear.
```

```text
Methods, Section 2.2.1: Please state more directly how anxiety was measured, who completed the measure, and whether raw scores, t-scores, or both were analyzed.
```

### 避免事项

- 不把用户的即时吐槽自动写成正式 comment，除非用户同意或语境明显是在要求记录。
- 不替用户大幅发挥成新的 major concern。
- 不把一个简单语言问题扩展成方法学批评。
- 不写无定位的 comment，例如只说 `The writing is unclear`。
- 不在用户边读边审时频繁总结整篇文章，除非用户要求。

### 当前协作口令

- 用户说“写进 comment / 记一下 / comment”：补全句子并写入稿件笔记。
- 用户说“不写进 comment”：只回应，不记录。
- 用户问“这句话什么意思”：先解释作者可能想表达什么，再判断是否需要记录。
- 用户问“有什么 comment”：给 1-3 条短 comment，不展开长篇。
- 用户说“已提交 / 归档”：按 [[README#归档清单（提交后）]] 移入 `archive/` 并更新 Track。

### Review comments 排版（提交 EM）

- Overall comment 单独一段。
- Specific comments 按 section 编号：**1. Abstract …**、**2. Introduction …** 等。
- 每个 section 内条目再编号 1、2、3…
- 粘贴 EM 时去掉 Markdown 加粗（`**`）即可。
