# 1a-2a 海马疗效预测稿 · 定稿文件区

> 项目总控：[[1a-2a 海马宏观微观分割与抗抑郁疗效预测]]

库内副本（2026-05-22，方案甲）。**可编辑主稿** = `manuscript_RadAdv.docx`（源自 `Hip-manuscript-RadAdv-blinded-clean-plain.docx`）。

## 库内文件

| 文件 | 说明 |
|------|------|
| `manuscript_RadAdv.docx` | 主稿 Word（最新） |
| `manuscript_RadAdv.pdf` | 主稿 PDF（投稿/审阅用） |
| `figures_main.pdf` | 主文图 |
| `supplementary.pdf` | 补充材料 |
| `tables.docx` | 主文表 |
| `cover_letter.docx` | Cover letter |
| `response_transfer.pdf` | 转投说明 |
| `title_page.docx` | Title page |
| `manuscript_digest.md` | **瘦身版** md（~10 KB，日常 @） |
| `manuscript_digest_full.md` | 全文备份（Pandoc 直出，~80 KB） |

## 更新 digest（docx → md）

已安装 **Pandoc** 时：

```powershell
cd "C:\Users\41516\Nutstore\1\MyObisidian\0 工作流\scripts"
.\Update-ManuscriptDigest.ps1
```

产出 **slim + full** 两个文件。改 `manuscript_RadAdv.docx` 后 rerun。**投稿与改格式仍以 docx/pdf 为准。** 流程见 [[0 工作流/workflows/3.5 Workflow ：Legacy 前期项目入库]]。

## 源路径（坚果云原稿，勿删）

| 用途 | 路径 |
|------|------|
| 母目录 | `C:\Users\41516\Nutstore\1\我的坚果云\2025-4季度\MDD.hippo.JAD投稿版本` |
| Advance 投稿包 | `...\Radiology-Adv 最新` |
| 图/表/补充（较全） | `...\Radiology投稿版本 较全` |

## 未复制（留在原处）

- `Figuers/`、`csv/`、多版 Rad2/3/4、track 修订 docx、`拼圖.pptx` 等过程与探索文件

## AI 阅读

- **优先**：`manuscript_digest.md`（Title/Abstract + Intro·Results·Discussion 摘录 + 全文 Conclusions）
- **逐句核对**：`manuscript_digest_full.md`
- **改稿 / 投稿**：`manuscript_RadAdv.docx`、`manuscript_RadAdv.pdf`
