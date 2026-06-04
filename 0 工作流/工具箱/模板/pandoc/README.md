# Pandoc Word 参考模板（手搓）

本目录只放 **`reference.docx`**（在 Word 里手工调好样式后的 Pandoc 参考文件）。

生成空壳：

```powershell
pandoc -o "0 工作流/工具箱/模板/pandoc/reference.docx" --print-default-data-file=reference.docx
```

导出：

```powershell
pandoc "input.md" -o "output.docx" --reference-doc="0 工作流/工具箱/模板/pandoc/reference.docx" --wrap=none
```

流程说明见 [[3.1 Workflow ：Zotero+Obsidian 文献由进到出全流程]] §3.3。
