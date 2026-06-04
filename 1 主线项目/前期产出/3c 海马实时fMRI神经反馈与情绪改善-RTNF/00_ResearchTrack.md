---
project: "3c 海马实时fMRI神经反馈与情绪改善"
type: research-track
updated: 2026-05-26
sy7_script: 2026-05-23
manuscript_working: yao202605修改/zlq0523
send_to_yao: 2026-05-24
tags: [rtnf, data-management]
---

# RTNF · Research Track

> **运营跟踪**（Dashboard 抓取本文件名）。科学总控 → [[3c 海马实时fMRI神经反馈与情绪改善]]  
> **印象笔记存量** → [[RTNF_MOC]]（2026-05-23 自 HTML 导入，正文未改）

## 当前焦点（2026-05-24）

| 项 | 状态 |
|----|------|
| **进度** | 姚老师批注 **大多数已处理**；工作稿 `finalManu\yao202605修改\2026-ZhangLQ-hipp-RTNF-shuxia0521-zlq0523.docx` |
| **下一步** | 叙事框架已定 → [[改稿记录/202605-Storyline-ABD-定稿框架]]；**06-01 周**处理 §3 → [[2026-06-01 科研推进#3.2 · RTNF]] |
| **改稿台账** | [[改稿记录/202605-姚老师-R01-批注处理清单]] |
| 主稿入库 | vault `定稿/manuscript_RTNF.docx` 仍为 0522 快照；**发回定稿后**再覆盖 + rerun digest |
| 版本 | 坚果云留档 + Word 比较；不建 Git → [[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/定稿/README#改稿版本约定（坚果云 · 不建 Git）]] |
| 投稿 | 已试 BS、Psych Med；转投待定 → [[RTNF 投稿思路与期刊备忘]] |

### 姚老师 2026-05-24 回复 · 分类摘要（06-01 周处理）

| 类 | 要点 |
|----|------|
| **功能连接** | PPI 看 NF 期间连通变化；可加 dPPI；写作交代 NF 调控局限 |
| **建模/对比** | Rest 作基线、Condition−Rest；连续减法 = active control |
| **rest1** | 删 rest1；删不净则放弃该线 |
| **呈现** | 对比减法结果好 → 可作摘要主结果 |
| **预期** | 深挖或能出东西，难冲高分刊 |

明细与待办 → 改稿台账 **§3**。叙事定稿框架 → [[改稿记录/202605-Storyline-ABD-定稿框架]]。

### 待办

- [ ] RTNF：A+B+D 叙事框架下处理姚老师 §3 改稿 → [[2026-06-01 科研推进#3.2 · RTNF]] ⏳ 2026-06-06 🔼
- [ ] `05_文献阅读/` 中有 DOI 的条目迁入 Zotero（可先列清单）
- [ ] **RTNF 数据盘规整** 🔽：多盘路径索引与归拢（非阻塞改稿）
- [x] **[SY7]** 敏感性分析脚本入库并跑通 → `SY7_sensitivity_exclude_run1.py` + TSV（**结论是否进稿** 仍待姚老师）

## 分析脚本索引（库外 · finalManu）

| 批注 / 用途 | 脚本 | 定稿母本 | 主要输入 |
|-------------|------|----------|----------|
| 脑–行为相关（Figure 2C） | `...\3.2 Analysis of the Target Hippocampal ROI\散点图\Brain-Behavior Correlation Analysis.py` | — | `J:\RTNF\test2-bids\fmriprep\ROI_aal\nilearn_AllRois\roi_signals_results.csv`；临床 `AllData-before/after.csv` |
| **[SY7] 排除 Run1 敏感性** | `...\3.2 Analysis of the Target Hippocampal ROI\SY7_sensitivity_exclude_run1.py` | 同上散点图脚本 | 同上；**新增** `mean_feedback_no_run1` = mean(Hipp2, Hipp4) |
| SY7 输出 | 同目录 `SY7_correlation_results.tsv`、`SY7_subject_level_metrics.tsv` | — | 由 SY7 脚本生成 |

坚果云根（本机）：`C:\Users\HMRRC\Nutstore\1\我的坚果云\RTNF\finalManu\`

**SY7 运行**（在脚本所在目录或任意 cwd）：

```bash
python "C:\Users\HMRRC\Nutstore\1\我的坚果云\RTNF\finalManu\3.2 Analysis of the Target Hippocampal ROI\SY7_sensitivity_exclude_run1.py"
```

**相对定稿脚本的改动摘要**：未改 `Brain-Behavior Correlation Analysis.py`；SY7 脚本仅复用其 complete-case 定义与 `mean_feedback_activity`，额外计算 `(Hipp2+Hipp4)/2` 及相关矩阵并写 TSV。

## 子线导航

| 子线 | 入口 |
|------|------|
| SMA（toy / 并行） | [[印象笔记归档/notes/01_SMA/SMA study|SMA study]] · [[印象笔记归档/notes/01_SMA/SMA Second-level analysis|SMA Second-level]] |
| 海马 NF 主分析 | [[印象笔记归档/notes/02_海马fMRI分析/Hipp1-4 结合分析 Updated version|Hipp1-4 分析]] · [[印象笔记归档/notes/02_海马fMRI分析/数据分析笔记：探索海马调节效率与行为改善的关联|调节效率×行为]] |
| 行为 / 量表 | [[印象笔记归档/notes/03_行为与统计/探索SDSSAS improvement与其他量表的相关|SDS/SAS 探索]] |
| 实验日志 | [[印象笔记归档/notes/04_实验与工作笔记/ResearchPlan rt-fMRI-NF 工作安排|ResearchPlan]] · `2025.* 工作笔记` |
| 文献 | [[RTNF_MOC#按主题分类]] → `05_文献阅读/` |
| 基建 | [[印象笔记归档/notes/06_方案与基建/OpenNFT|OpenNFT]] |

## 工作安排时间轴（摘自 ResearchPlan）

→ 完整勾选与文献树见 [[ResearchPlan rt-fMRI-NF 工作安排|ResearchPlan: rt-fMRI-NF 工作安排]]

- **一期预实验**（2023–2024）：联影实时传输、ROI（SMA/杏仁核→海马）、block 设计
- **二期 / towards paper**（2024.04+）：SMA toy + 海马 feasibility；首被试 2024/4/13–14
- **数据分析阶段**（2025）：ROI 组间、学习效应、SDS/SAS、gPPI 探索 → 对应 `02_` `03_` 笔记

## 库外资源（不迁入 vault）

> ⚠️ **数据分散在多盘**，整理前以本表为准；完整归拢见待办「RTNF 数据盘规整」。

| 资源 | 路径 | 备注 |
|------|------|------|
| CONN / gPPI 工程 | `F:\RTNF_CONN` | 2026-05 确认；旧笔记写 `K:\CONN_gPPI` |
| fMRI 主工程（BIDS/SPM） | `J:\RTNF`（如 `test2-bids`） | |
| 坚果云 RTNF（主力机） | `C:\Users\41516\Nutstore\1\我的坚果云\RTNF` | 稿件、行为表 |
| 坚果云 RTNF（笔记本，同步） | `C:\Users\HMRRC\Nutstore\1\我的坚果云\RTNF` | |
| 行为主表 | `汇总-总分及配对.xlsx` → `原始表` | 坚果云 |
| 定稿稿件 | [[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/定稿/README]] | |
| finalManu 分析脚本 | `...\RTNF\finalManu\3.2 Analysis of the Target Hippocampal ROI\` | 含 SY7、Figure 2C 散点图脚本 |
| **姚老师改稿轮（2026-05）** | `...\finalManu\yao202605修改\2026-ZhangLQ-hipp-RTNF-shuxia0521-zlq0523.docx` | 命名见定稿 README |
| SMA 统计表 | 见 [[3c 海马实时fMRI神经反馈与情绪改善#SMA 子线 · 数据与分析索引]] | |

## 链接

- [[3c 海马实时fMRI神经反馈与情绪改善]]
- [[RTNF_MOC]]
- [[1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善-RTNF/定稿/README]]
- [[01 RESEARCH_TODO_DASHBOARD]]
