# 3c RTNF 稿 · 定稿文件区

> 项目总控：[[3c 海马实时fMRI神经反馈与情绪改善]]

库内副本（2026-05-22）。**可编辑主稿** = `manuscript_RTNF.docx`（源自 `2026-ZhangLQ-Manu-hipp-RTNF-ForSub-final-shuxia0521.docx`，已交黄/姚老师审阅）。

> **改稿进行中（2026-05）**：工作稿 `finalManu\yao202605修改\2026-ZhangLQ-hipp-RTNF-shuxia0521-zlq0523.docx`；**2026-05-24 计划发回姚老师**（大多数批注已改；gPPI、SY7 两处待确认后再动稿）。vault 内 `manuscript_RTNF.docx` 仍为 0522 快照；定稿后再覆盖 + rerun digest。

## 库内文件

| 文件 | 说明 |
|------|------|
| `manuscript_RTNF.docx` | 主稿 Word（2026-05-22 最新） |
| `manuscript_RTNF.pdf` | 投稿 PDF（Brain Stimulation 包 `BRS-S-25-01793.pdf`，与 0521 稿可能略有版本差，改稿后以 docx 为准） |
| `supplementary.docx` | 补充材料（BS 投稿包） |
| `cover_letter.docx` | Cover letter（BS） |
| `highlights.docx` | Highlights（BS） |
| `declaration_COI.docx` | 利益冲突声明（BS） |
| `manuscript_digest.md` | **瘦身版** md（日常 @） |
| `manuscript_digest_full.md` | 全文备份（Pandoc 直出） |

> **主文图**：BS 包无独立 figure PDF；图版在 `manuscript_RTNF.pdf` 内。若需单幅 JPG → 见源路径 `finalManu\sub-PM\Fig1–4.jpg`。

## 更新 digest

```powershell
cd "C:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
.\Update-ManuscriptDigest.ps1 -Docx "…\定稿\manuscript_RTNF.docx" -OutDir "…\定稿"
```

流程见 [[0 工作流/workflows/3.5 Workflow ：Legacy 前期项目入库]]。

## 源路径（坚果云，勿删）

| 用途 | 路径 |
|------|------|
| **母目录（主力机）** | `C:\Users\41516\Nutstore\1\我的坚果云\RTNF` |
| **母目录（笔记本，坚果云同步）** | `C:\Users\HMRRC\Nutstore\1\我的坚果云\RTNF` |
| **行为 N=19 主表** | `汇总-总分及配对.xlsx` → sheet `原始表` |
| 最新主稿（交审底稿） | `...\2026-ZhangLQ-Manu-hipp-RTNF-ForSub-final-shuxia0521.docx` |
| **姚老师改稿轮（2026-05）** | `...\finalManu\yao202605修改\2026-ZhangLQ-hipp-RTNF-shuxia0521-zlq0523.docx` |
| **批注处理清单（vault）** | [[改稿记录/202605-姚老师-R01-批注处理清单]] · 模板 [[改稿记录/_template-批注处理清单]] |
| BS 投稿包 | `...\finalManu\sub-BrianStimulation\` |
| JAD / PM 历史包 | `...\finalManu\sub-JAD\`、`...\sub-PM\` |
| 多版过程稿 | `...\finalManu\Manu-hipp-RTNF*.docx` |

## 改稿版本约定（坚果云 · 不建 Git）

**策略（2026-05 定）**：改稿次数多、极少回滚 → **每版留档 + Word「比较文档」** 即可；**不为 RTNF 稿单独建 Git**。坚果云双机同步 + 文件夹分轮。

| 要素 | 约定 | 本篇范例 |
|------|------|----------|
| 文件夹 | `finalManu\<导师姓><YYYYMM>修改\` | `yao202605修改\` |
| 文件名 | `2026-ZhangLQ-hipp-RTNF-<上游版本>-<本步修订者MMDD>.docx` | `…-shuxia0521-zlq0523.docx`（底稿 shuxia0521，zlq 0523 改） |
| 比对 | Word → 审阅 → 比较；选文件夹内相邻两版 | — |
| 入库 vault | 仅当某轮 clean 稿稳定 → 覆盖 `manuscript_RTNF.docx` → `Update-ManuscriptDigest.ps1` | 本轮尚未覆盖 |

**本机完整路径（笔记本）**：

`C:\Users\HMRRC\Nutstore\1\我的坚果云\RTNF\finalManu\yao202605修改\2026-ZhangLQ-hipp-RTNF-shuxia0521-zlq0523.docx`

## 未复制（留在原处）

- 根目录 `AllData*.xlsx`、`*.sav`、预实验 pptx、`PaperToRead/`、Google 转换副本（`.gsheet` / `.gdoc`）等 → 见总控笔记 **SMA / 数据 / 会议** 索引

## AI 阅读

- **优先**：`manuscript_digest.md`
- **逐句核对**：`manuscript_digest_full.md`
- **改稿 / 投稿**：`manuscript_RTNF.docx`
