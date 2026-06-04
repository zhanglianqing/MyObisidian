---
title: "直接检验“间接靶点调节”假说 (gPPI功能连接分析)"
source: evernote_html
source_html: "直接检验“间接靶点调节”假说 (gPPI功能连接分析).html"
category: "02_海马fMRI分析"
imported: 2026-05-23
---

# 直接检验“间接靶点调节”假说 (gPPI功能连接分析)

#### 

###   


项目位置：

**`F:\RTNF_CONN`**（2026-05 更新；原笔记 `K:\CONN_gPPI`）

**  
**

#### 1\. 分析目的与核心假设 (Aims & Hypotheses)

  * 出发点: 本分析旨在检验“间接靶点调节 (Indirect Target Modulation)”假说。

  * 核心假设: 即使左侧海马的局部激活强度未见预期上调，但其作为记忆中枢的功能连接模式可能在神经反馈训练中被系统性地重塑。我们预期，与执行外部认知任务相比，进行内部积极回忆会增强左侧海马与前额叶控制区域或在激活分析中发现的**“非靶点”网络**之间的功能连接。




#### 2\. 分析方法与流程 (Methods & Pipeline)

  1. 分析工具: CONN Connectivity Toolbox

  2. 数据输入: 采用fMRIPrep (v. X.X.X) 预处理后的数据。通过CONN的Import fMRIPrep dataset功能，将位于MNI152NLin2009cAsym标准空间的预处理功能/结构像、分割图及混淆变量（confounds.tsv）导入项目。

  3. 补充预处理: 在CONN中，仅对fMRIPrep输出的功能像额外执行了8mm FWHM空间平滑。

  4. 去噪 (Denoising): 采用了CONN的默认去噪流程

  5. 一级模型 (1st-level Model):

     * 分析类型: task-modulation (gPPI)

     * 种子点 (Seed): 左侧海马 (从CONN内置atlas.nii或AAL图谱中提取)。

     * 心理学变量: 选择了UpRegulate, SerialSubtraction, Rest三个任务条件进行建模。

     * 模型选项: 采用total-connectivity during each task condition，以计算每个任务条件下的“总连接强度”，为二级分析提供最大的灵活性。




#### 3\. 核心分析结果 (Key Results)

  1. 静态平均连接效应 (Upregulate vs. Serial Subtraction):

     * 结果: 对所有4个训练轮次进行合并分析，未能发现左侧海马与全脑任何区域在UpRegulate和Serial Subtraction两个条件间存在显著的功能连接差异（调整显著性阈值依旧如此）。

     * 结论: 这是一个统计学上的阴性结果 (Null Result)，表明两个任务条件诱导的宏观功能连接差异不够显著。

     * UpRegulate vs Rest 也没有显著差异。Serial Substraction vs Rest有差异，但这个contrast本身不关心，因此未细看

  2. 单独条件的连接模式分析: #这部分我对看单独条件是否有意义存疑

     * UpRegulate 条件: 该任务诱导了左侧海马与一个极其广泛、显著的脑网络的正功能连接。该网络清晰地包含了默认模式网络（DMN）的核心节点（楔前叶、后扣带回、内侧前额叶等）、边缘系统（双侧杏仁核、海马旁回等）以及感觉运动网络。

     * Serial Subtraction 条件: 惊人地，该任务同样诱导了左侧海马与一个在空间分布上高度相似的、以DMN和感觉运动网络为主的脑网络的强正功能连接。




#### 4\. 当前的解读、困惑与待办事项 (Current Interpretation, Puzzles & To-Do)

  1. 对阴性结果的初步解释: Upregulate vs. Subtraction对比的阴性结果，很可能是因为这两个任务在宏观功能连接层面诱导了过于相似的网络模式，导致两者间的差异被掩盖。

  2. 核心困惑 (The Core Puzzle):

     * 激活与连接的“脱节”: 如何调和以下两个看似矛盾的发现？

       * 激活分析显示: Upregulate > Serial Subtraction，表明两个任务的**信号强度（工作强度）**存在显著差异。

       * 连接分析显示: FC(Upregulate) ≈ FC(Serial Subtraction)，表明两个任务的**协同模式（工作模式）**高度相似。

     * 对Serial Subtraction任务本质的疑问: 该任务在我们的实验中，可能并非一个纯粹的“DMN抑制”任务。它可能因为认知负荷相对较低，诱发了强烈的**“思绪漫游 (Mind-Wandering)”**，从而也激活了DMN。

  3. 后续重新拾起此分支时的探索方向 (#ToDo for Future Pick-up):

     * 文献深挖: 深入调研关于“思绪漫游”、“认知负荷与DMN抑制关系”以及“激活与功能连接脱节现象”的文献，为当前的困惑寻找理论支持或反驳证据。

     * 精细化分析:

       * 检验动态学习效应: 按原计划完成连接的线性/U型学习趋势分析。也许连接的变化趋势（而非平均值）存在差异。

       * 大脑-行为关联: 检验在某个特定条件下（如Upregulate）的连接强度，是否与行为改善显著相关。这可以绕开任务对比的复杂性。

       * 探索负连接: 更仔细地审视两个条件下的**负连接/反相关网络（蓝色区域）**是否存在差异。




* * *

关于gPPI，用Gemini生成了一份报告：

[Google Gemini](https://gemini.google.com/app/0d44c0c6961da5f9?utm_source=gemini&utm_medium=referral&utm_campaign=gemini_deep_research_landing_page&redirect=home&hl=zh-CN&_gl=1*y8x4xx*_gcl_au*NjI1MDExMzIyLjE3NTQ5NjYzNTM.*_ga*ODc5NDYyMTkzLjE3NTQ5NjYzNTQ.*_ga_WC57KJ50ZZ*czE3NTQ5NjYzNTQkbzEkZzEkdDE3NTQ5NjY3NTkkajYwJGwwJGgw)
