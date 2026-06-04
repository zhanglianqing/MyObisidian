---
type: revision-log-template
---

# 批注处理清单 · 模板

> **范例（已填）**：[[202605-姚老师-R01-批注处理清单]]  
> **用法**：复制本文件 → 改名 `YYYYMMDD-<审阅者>-R<轮>-批注处理清单.md` → 改 frontmatter → 填 §1–§2。

---

```markdown
---
type: revision-log
project: "<项目名>"
reviewer: "<审阅者>"
round: R01
source: gemini
source_verified: false
source_docx: "<收到批注的底稿后缀>"
working_docx: "<本步工作稿后缀>"
nutstore_dir: "finalManu/<文件夹名>"
nutstore_working: "<工作稿完整路径>"
received: 
started: YYYY-MM-DD
sent_to_reviewer: 
created: YYYY-MM-DD
tags: []
---

# <审阅者> R<轮> · 批注处理清单

> **运营摘要** → [[00_ResearchTrack#…]]  
> **定稿 / 版本约定** → [[定稿/README#改稿版本约定（坚果云 · 不建 Git）]]  
> **工作稿**：`<文件名>.docx`（坚果云 `<文件夹>`）

---

## 1. 本轮概况

| 项 | 内容 |
|----|------|
| 收到带批注稿 | |
| 开始修改 | |
| 计划发回 | |
| 本轮小结 | |

---

## 2. 具体修改

（按主题分块；每条用 **[批注ID]** + 批注意见 / 实际操作 / #ToDo 待确认）

**1. 文本与格式修改**

*   **[SY?]** …

**2. 结果部分的描述调整**

*   **[SY?]** …

**3. …（按本轮实际主题增删小节标题）**

*   **[SY?]** …

**4. …**

*   **[SY?]** …
```

## 命名与存放

| 项 | 约定 |
|----|------|
| 目录 | 项目下 `改稿记录/`（与 `定稿/` 并列，不进 `定稿/`） |
| 文件名 | `YYYYMMDD-<审阅者>-R<轮>-批注处理清单.md` |
| Word | 坚果云 `finalManu\<导师><YYYYMM>修改\`；vault 只链路径 |
| 挂接 | `00_ResearchTrack` 当前焦点 + `定稿/README` 各加一行 wikilink |

## 稿内状态（写在「实际操作」或 #ToDo 里即可）

- 已写入工作稿
- `#ToDo` / 待审阅者确认后再改
- 本轮不改
