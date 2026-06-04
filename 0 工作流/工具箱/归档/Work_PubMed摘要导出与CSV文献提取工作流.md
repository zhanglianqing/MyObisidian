# PubMed 摘要导出 → 结构化 CSV 文献提取工作流

本工作流用于：**在 PubMed 完成检索后，将摘要批量导出为 Markdown（`*.md`，推荐）或纯文本（`*.txt`），再在 Cursor 中由 AI 按统一表头抽取、分级、合并为一张可筛选的 CSV**，便于综述、立项依据或后续导入 Zotero/表格软件。表内 **`DOI` / `PMID` 与「优先 DOI」规则**用于与 Zotero「通过标识符添加」衔接（见 **§5**）。

> 实践验证：已在「肺癌 / CRCI」主题下多轮合并（`abstract-LungCancer-set1`～`set4` → `literature-review-LungCRCI.csv`），可原样复用到其他检索式。

---

## 1. 流程总览

| 步骤 | 操作 | 产出 |
| :--- | :--- | :--- |
| ① | **PubMed** 构建检索式，运行检索，按需筛选（年份、Article type 等） | 检索结果列表 |
| ② | **推荐**：运行仓库内脚本 `0 工作流/scripts/Fetch-PubMedJournalPages.ps1`（NCBI E-utilities，见 **§2**）；**备选**：PubMed **Send to → File → Abstract** | `*.md`（每页一个，含 `## Article` 与 DOI/PMID）或 `*.txt` |
| ③ | 将 md/txt 放入项目目录（建议命名：`<主题>-abstracts-pageNN.md` 或 `abstract-<主题>-setN.txt`） | 原始摘要库 |
| ④ | 在 Cursor 中 `@` 引用该 md/txt，说明**分级规则**、**表头含义**、是否与已有 CSV **合并去重** | AI 生成/追加行 |
| ⑤ | 合并结果保存为 **UTF-8（推荐带 BOM）** **CSV**（见 §3「输出」与 §4.1，便于 Windows 下 **Excel 双击**不乱码）；表内含 **`DOI`、`PMID`**（抽取规则见 §3、§4） | `literature-review-<主题>.csv` |
| ⑥ | 个人备注在 **`comment`** 列填写，不依赖 AI 长期记忆 | 可持续维护的表 |
| ⑦ | 对重要条目：按 **§5** 用 **DOI（无则 PMID）** 批量粘贴进 Zotero「通过标识符添加」 | Zotero 题录（全文获取见 §5） |

**要点：** 导出格式选 **Abstract**，而非仅题录；这样 AI 才能抽取目的、方法、样本量、结局等字段。

---

## 2. PubMed 端操作建议

### 2.1 检索式（网页与脚本共用）

- 在 [PubMed Advanced](https://pubmed.ncbi.nlm.nih.gov/advanced/) 写好 Boolean，确认命中量可管理（分批时可按年份、Article type 等切分）。
- **脚本用的 `-Term` 必须与网页检索式一致**（含 `[jour]`、`[tiab]`、AND/OR 等）。示例：`"Invest Radiol"[jour]` 对应网页 URL 中的 `term=%22Invest+Radiol%22%5Bjour%5D`。
- 网页 **Sort by: Date** 对应脚本 **`-Sort pub_date`**（默认）。

### 2.2 推荐：复用脚本批量导出（Markdown，勿重写代码）

**固定脚本路径（库内已写好，只改参数）：**

`0 工作流/scripts/Fetch-PubMedJournalPages.ps1`

- 走 **NCBI E-utilities**（`esearch` + `efetch`），不依赖浏览器，可避免 PubMed 网页 **reCAPTCHA**。
- **产出**：UTF-8（带 BOM）**`*.md`**，**每页一个文件**；每文件约 **`-PerPage` 条**（默认 10）；每条为 `## Article N` + PubMed Abstract 原文（含 **DOI / PMID**），条目间 `---`。
- **命名**：`<FilePrefix>-page01.md` … `pageNN.md`；未指定 `-OutDir` 时输出到 `0 工作流/PubMed_export_<检索式缩写>_<时间戳>/`。

**复制即用（PowerShell，只改 `-Term` / `-Pages` / `-OutDir` / `-FilePrefix`）：**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "e:\Obisidian\MyObisidian\0 工作流\scripts\Fetch-PubMedJournalPages.ps1" `
  -Term '"Invest Radiol"[jour]' `
  -Pages 5 `
  -PerPage 10 `
  -Sort pub_date `
  -OutDir "e:\Obisidian\MyObisidian\0 工作流\PubMed_export_InvestRadiol_5pages" `
  -FilePrefix "InvestRadiol-abstracts" `
  -Email "你的邮箱"
```

| 参数 | 默认 | 说明 |
| :--- | :--- | :--- |
| `-Term` | `"Invest Radiol"[jour]` | PubMed 检索式（与 Advanced 一致） |
| `-Pages` | `5` | 下载页数 |
| `-PerPage` | `10` | 每页条数（对应 PubMed 每页显示数） |
| `-Sort` | `pub_date` | `pub_date` / `relevance` / `author` / `journal` |
| `-OutDir` | 自动 | 输出文件夹；建议按课题固定路径便于 `@` |
| `-FilePrefix` | `InvestRadiol-abstracts` | 文件名与一级标题前缀 |
| `-Email` | 占位邮箱 | NCBI 建议填写真实邮箱 |

**高频批量**（数百页以上）：在 [NCBI 账户](https://www.ncbi.nlm.nih.gov/account/settings/) 申请 API Key，并在脚本内 `esearch`/`efetch` URL 追加 `&api_key=...`（当前脚本未内置该参数；需要时再改脚本一行即可）。

**在 Cursor 里省 token 的用法（不要每次让 AI 重写脚本）：**

1. `@` 本工作流 + `@0 工作流/scripts/Fetch-PubMedJournalPages.ps1`
2. 只说明要改的参数，例如：「`-Term '"Radiology"[jour]'`，`-Pages 3`，`-OutDir` 放到 `5 分支项目/5.1 xxx/`」
3. 请 AI **直接运行上述脚本**，或把 §2.2 代码块里的路径与参数替换后粘贴到终端执行

**已验证示例输出目录：** `0 工作流/PubMed_export_InvestRadiol_5pages/`（5 个 `InvestRadiol-abstracts-page01.md`～`page05.md`）。

### 2.3 备选：PubMed 网页手动导出

- `Send to` → `File` → **Format: Abstract (text)** → `Create file`。
- 适合无法跑 PowerShell、或需网页端额外筛选后再导出的情况；产出为 **`.txt`**，后续 AI 提取规则与 md **相同**（见 §3）。
- 多次检索可保存为 `set1`、`set2`… 避免单文件过大。

### 2.4 目录与命名

- 同一主题的 **md/txt** 与最终 **CSV** 放在同一项目子文件夹（例如 `5 分支项目/5.1 xxx/`），便于版本管理与 `@` 引用。
- 分批追加时保持前缀一致：`<主题>-abstracts-pageNN.md` 或 `abstract-<主题>-setN.txt`。

---

## 3. Cursor / AI 提取时的约定（推荐每次说明）

以下内容建议在每条新任务里复制或简述，减少偏差：

1. **文献层级**（可按课题修改）：例如  
   - `1-NSCLC脑结构功能`：原始研究 + NSCLC + 脑结构/功能影像等  
   - `2-肺癌原始研究`：原始研究 + 肺癌 CRCI 任意层面  
   - `3-肺癌综述`：综述/Meta/范围综述且主题含肺癌 CRCI  
   - `其他癌症/混合/非肺癌主题`：非主线但可保留作背景  
   - `其他（…）`：噪声或极弱相关，便于 `comment` 标剔除  

2. **字段分工**  
   - **样本量及样本特征**：癌种、分期、n、人群、时间地点等；**不要**塞进「暴露因素」。  
   - **暴露因素**：化疗 / 放疗 / 靶向 / ICI / 手术或「未在摘要中分层」等。  
   - **影像方法**：序列、模态；摘要未写则写「摘要未报告层厚/序列」。  

3. **`DOI` / `PMID`（与 Zotero 衔接；优先 DOI）**  
   - 从 Abstract **md/txt** 每条记录中抽取：**`DOI`**（常见形如 `10.xxxx/...`，填标准形式，不要带 `https://doi.org/` 前缀亦可，全表统一即可）；**`PMID`**（纯数字，PubMed 记录末尾常见 `PMID: 12345678` 等）。  
   - **优先 DOI**：摘要或题录中**同时**出现 DOI 与 PMID 时，两列都填；向 Zotero 批量粘贴标识符时，**优先复制 `DOI` 列**（Zotero 对 DOI 解析出版社元数据往往更利于后续「查找可用 PDF」）。  
   - **仅 PMID**：无 DOI 时 `DOI` 列留空，仅用 `PMID` 建条目。  
   - **皆无**：两列均留空，并在 `comment` 注明「无 DOI/PMID，需手工检索」，避免误当成可批量导入行。

4. **合并策略**：新 set 追加到已有 CSV 时，勘误（Erratum）、与正文重复的条目单独一行或跳过；会议摘要汇编等非文献可整批排除。

5. **输出（编码与 Excel）**  
   - 保存为 **UTF-8**带 BOM。**逗号分隔**；字段内如有英文逗号需按 RFC 4180 用双引号包裹。  


---

## 4. CSV 表头模板（下次直接复制首行）

以下为**固定表头**（列名与顺序勿随意改，便于纵向合并多批检索；**`DOI` 在 `PMID` 前**，表示标识符优先级与粘贴 Zotero 时的推荐顺序）：

```csv
文献层级,文献信息,DOI,PMID,样本量及样本特征,暴露因素,影像方法,主要研究目的及相应的结果,其他测量/结局,comment
```

### 各列含义（写进模板供对照）

| 列名               | 填写说明                                                                         |
| :--------------- | :--------------------------------------------------------------------------- |
| **文献层级**         | 分级标签，用于筛选与排序（见上节，可按课题改名但建议保持可排序前缀）。                                          |
| **文献信息**         | **作者（第一作者或 et al.）+ 年份 + 期刊** 合一列，例：`Hu L 等 (2025). Quant Imaging Med Surg`。 |
| **DOI**          | 数字对象标识符，标准 `10.xxxx/...` 形式；无则留空。**向 Zotero 批量添加时优先使用本列**（见 §5）。             |
| **PMID**         | PubMed 唯一号，仅数字；无则留空。无 DOI 时用本列配合 Zotero「通过标识符添加」。                            |
| **样本量及样本特征**     | n、癌种/病理、设计（前瞻/回顾/RCT）、关键人口学或临床特征；摘要未写则注明。                                    |
| **暴露因素**         | 抗肿瘤治疗或研究设计中的暴露；非治疗因素（如仅性别）一般不写在此列。                                           |
| **影像方法**         | MRI/fMRI/PET/序列或替代指标（如 DTI-ALPS）；无影像写「未使用神经影像」等。                             |
| **主要研究目的及相应的结果** | 建议格式：`目的：…。结果：…。` 一段内写完。                                                     |
| **其他测量/结局**      | 量表、血检、生物标志物、协变量等补充结局。                                                        |
| **comment**      | **留空给人工**：剔除原因、全文待补、与某条重复、临床备注等。                                             |

**占位示例行（复制后删除）：**

```csv
2-肺癌原始研究,示例 等 (20XX). 期刊缩写,10.1234/example.2025,12345678,n=…；…。,化疗/放疗/…,…,目的：…。结果：…。,MoCA；FACT-Cog；…,
```


---

## 5. Zotero 衔接（批量题录：**优先 DOI**）

1. 在表格软件或 Cursor 中按 **`文献层级` / `comment`** 筛出要进库的条目。  
2. **优先复制 `DOI` 列**：只选**非空**单元格，多行复制（一行一条标识符）。  
3. 若某些行无 DOI：对剩余条目再复制 **`PMID` 列**非空单元格（勿与 DOI 混在同一批重复建同文，一般「有 DOI 就不必再贴 PMID」）。  
4. 打开 Zotero → 工具栏 **「通过标识符添加」**（魔棒图标）→ 将剪贴板粘贴进输入框 → 确认。Zotero 会按标识符拉取题录。  
5. **全文（PDF）**：与「建条目」分开；开放获取可全选题录后使用 **「查找可用 PDF」**；订阅文献需在浏览器打开出版社页面并用 **Zotero Connector** 或本地下载后拖入对应条目。本表不保证一键全文，仅保证标识符驱动的题录批量入口。

> **与旧表兼容**：若已有仅 8 列的历史 CSV（无 `DOI`/`PMID`），合并时可在表头插入 `DOI,PMID` 两列并补抽，或单独维护「待进 Zotero」子表；新主题建议自始采用本节与 §4 的 **10 列表头**。

---

