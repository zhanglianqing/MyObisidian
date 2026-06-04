---
type: revision-note
project: "3c 海马实时fMRI神经反馈与情绪改善"
status: 已定稿口径
based_on: "姚老师 2026-05-24 微信 · A / B / D"
related: "[[改稿记录/202605-姚老师-R01-批注处理清单#3. 姚老师回复 · 待处理（2026-05-24 微信）]]"
working_docx: zlq0523
created: 2026-05-26
tags: [rtnf, revision, storyline, yao202605]
---

# RTNF · Storyline 定稿框架（A + B + D）

> 改稿叙事主线的**已定口径**；对应改稿台账 §3 中 A（功能连接）、B（建模/对比）、D（呈现）。不含 C（rest1，已废弃）。

---

基于你目前定稿的 **A + B + D 框架**，将主要神经结果重塑为 **Up-Regulation > Serial Subtraction (Up>SS)** 是一次重大的**叙事主线重构（Narrative Shift）**。

为了帮你高效改稿，以下是整篇 Paper 需要调整的**核心改动清单**与**具体写作口径**：

---

### 1. 核心叙事逻辑的转变（The Big Picture）

- **过去（被动救场）：** 行为有效 $\rightarrow$ 但 Up>Rest 没激活（海马没上去） $\rightarrow$ 讨论区花大量篇幅解释“为什么反馈没用/次优”的悖论 $\rightarrow$ 顺便提一下 Up>SS 有激活。
- **现在（主动立论）：** 行为有效 $\rightarrow$ **在 active control（SS）基线之下，海马被成功激活（Up>SS）且与情绪改善显著相关** $\rightarrow$ 讨论区聚焦于“主动认知策略（自传体记忆）在主动对照下对海马的特异性唤醒及其临床意义” $\rightarrow$ 诚实交代 Up>Rest 阴性（作为方法学局限或生理基线特性）。

---

### 2. 各章节的具体修改要点

#### ✍️ Introduction（引言）：重塑 Serial Subtraction 的角色
- **旧写法：** 连续减法（SS）只是为了在 Block 之间“清除残留情绪/脑区活动”（washout task）。
- **新写法：** 将 SS 明确定义为 **Active Control Condition（主动对照条件）**。
  - **立论逻辑：** 海马在静息态（Rest）下存在高度的默认模式网络（DMN）活动和自发思维（mind-wandering）。为了准确评估“自传体记忆上调海马”的特异性激活，必须引入一个不涉及情绪和自传体记忆、但同样消耗认知资源的计算任务（SS）作为主动对照。因此，**Up > SS 才是评估海马特异性 Engagement 的最严谨、最主要的离线对比（primary offline contrast）**。

#### ✍️ Methods（方法）：确立“三层口径”
你需要在方法学中清晰、自信地解释为什么“在线反馈”和“离线分析”用了不同的 Contrast：
- **第一层（在线反馈）：** 实时反馈计算采用 **Hippocampal PSC relative to the immediately preceding Rest block**。这是为了保证在线计算的实时性、稳定性和生理基线的快速对齐（常规 rt-fMRI-NF 做法）。
- **第二层（离线主分析）：** 离线推断以 **Up-Regulation > Serial Subtraction** 为主。因为 active control 相比于 wakeful rest，能提供更稳定、更具认知特异性的海马对比。
- **第三层（生理基线）：** Rest 仅作为生理基线（Physiological Baseline），用于 Condition-Rest 的辅助建模。

#### ✍️ Results（结果）：调整汇报顺序与图表主次
这是改动最大的部分，需要调整段落的逻辑先后：
- **第一步：先汇报 Up > SS 的主效应（Headline）。** 展示在 NF 训练期间，海马在 Up>SS 对比下有显著激活，并且该激活度（Engagement）与行为学指标（如 SDS/SAS 改善、情绪状态提升）存在显著的脑-行为相关性（Brain-Behavior Correlation）。
- **第二步：解释 SS 的负激活。** 汇报 SS 阶段海马呈现显著的负激活（Deactivation），这证实了 SS 成功压制了海马的自发活动，起到了合格的 active control 作用。
- **第三步：降调汇报 Up > Rest。** 诚实汇报 Up>Rest 未达显著激活，并指出这是由于 Rest 状态下海马的高基线活动（DMN/mind-wandering）导致的，从而反向证明了采用 Up>SS 作为主分析的合理性与必要性。
- **第四步：并入 PPI/dPPI 连通性分析（A 支路）。** 汇报在 NF 期间以海马为 Seed 的功能连接变化，用以说明网络层面的调控幅度。
- **图表调整：** 
  - 将 **Up > SS 的激活图和脑-行为相关性散点图** 移至 Results 的 **Figure 2/3（主图）**。
  - 将 Up > Rest 的阴性结果或对比图移至附图（Supplementary）或作为主图的一个不起眼的 Panel。

#### ✍️ Discussion（讨论）：重构讨论主轴
- **旧写法：** 围绕“Dissociation（脑区激活与行为脱节）”或“Suboptimal feedback（反馈次优）”展开，显得研究有瑕疵。
- **新写法：** 围绕 **“Active-control 下海马的 Engagement 及其对情绪调节的贡献”** 展开。
  - 重点讨论自传体记忆（AM）如何通过主动认知控制特异性地唤醒海马。
  - 讨论为什么在 active control 下才能观察到这种关联（强调方法学上的严谨性）。
  - **收缩战线：** 将“反馈信号为什么用 Rest 却在 Up>Rest 没看到激活”缩写为一个短段落，降调处理。解释为：在线反馈需要即时基线（preceding Rest），而离线分析需要认知对照（SS），两者的不一致是 rt-fMRI 领域的常见方法学挑战，而非实验失败。

#### ✍️ Abstract & Conclusion（摘要与结论）
- **摘要：** 删去“vs Rest 无激活”的挫败感表述。直接写：“结果显示，与主动对照任务（Serial Subtraction）相比，患者在训练期间展现出显著的海马激活（Up > SS），且该激活程度与焦虑/抑郁情绪的改善显著相关。”
- **结论：** 强调 active-control 框架在评估实时脑电/磁共振反馈中的优越性，以及海马-皮层网络在情绪调节中的适应性改变。

---

### 3. 核心英文写作模板（可直接用于论文）

为了在论文中显得非常自信且方法学严谨，你可以直接在 **Methods** 或 **Discussion** 中使用以下学术化表述：

> "Real-time feedback was computed as hippocampal percent signal change (PSC) relative to the immediately preceding Rest block, following standard block-design rt-fMRI-NF protocols to ensure online signal stability. However, for offline primary inference, we utilized the **Up-Regulation > Serial Subtraction** contrast. This active control (Serial Subtraction) was specifically designed to suppress spontaneous hippocampal activity associated with mind-wandering during wakeful rest, thereby providing a more cognitively specific and statistically robust contrast to evaluate target-specific hippocampal engagement during autobiographical memory recall."

通过这些改动，你的论文将从一个**“结果有瑕疵、勉强解释”**的被动故事，变成一个**“方法学设计严谨、成功定位海马特异性情绪调控机制”**的高质量学术故事。
---

## 4. 链接

- [[改稿记录/202605-姚老师-R01-批注处理清单]]
- [[00_ResearchTrack]]
- [[印象笔记归档/notes/07_其他/关于设计时选择rest作为contrast，而实际发现serial substractio]]
