#!/usr/bin/env python3
"""Move selected notes from 印象笔记存档 to 计划1 海马-PPC 印象笔记归档."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
KB = VAULT / "7 可复用知识库/印象笔记存档"
KB_NOTES = KB / "notes"
KB_ATTACH = KB / "attachments"

PROJECT = VAULT / "1 主线项目/计划1：海马-PPC个体化靶点环路的基础病理研究"
ARCHIVE = PROJECT / "印象笔记归档"
PROJ_NOTES = ARCHIVE / "notes" / "00_核心"
PROJ_ATTACH = ARCHIVE / "attachments"
OLD_ATTACH_PREFIX = "7 可复用知识库/印象笔记存档/attachments"
NEW_ATTACH_PREFIX = (
    "1 主线项目/计划1：海马-PPC个体化靶点环路的基础病理研究/印象笔记归档/attachments"
)

EXTRACT_STEMS = [
    "TMS 海马-PPC项目的拓展与变体",
    "基于多模态影像的海马-PPC通路完整性及其在抑郁症认知损伤中的作用",
    "同步TMS-fMRI技术精准调控抑郁症记忆损伤 2510-省面上",
    "7T数据分析笔记2.0",
    "22-25青基评价意见",
    "青基参考",
    "rTMS + hippocampus PNAS文章",
    "TMS+MDD",
]


def regenerate_kb_moc(moved_count: int) -> None:
    remaining = sorted(KB_NOTES.glob("*.md"), key=lambda p: p.stem.lower())
    lines = [
        "---",
        "title: 印象笔记存档目录",
        "type: moc",
        "imported: 2026-05-23",
        "updated: 2026-05-23",
        "---",
        "",
        "# 印象笔记存档",
        "",
        "> 控制台笔记本组剩余笔记；正文未改写。Cursor 默认不索引（见 vault `.cursorignore`）。",
        "",
        f"> 2026-05-23 已迁出 {moved_count} 篇至 "
        f"[[1 主线项目/计划1：海马-PPC个体化靶点环路的基础病理研究/印象笔记归档/PPC_MOC|PPC 项目归档]]。",
        "",
        "## 按标题（A–Z）",
        "",
    ]
    for p in remaining:
        lines.append(f"- [[印象笔记存档/notes/{p.stem}|{p.stem}]]")
    lines.append("")
    (KB / "MOC.md").write_text("\n".join(lines), encoding="utf-8")

    readme = KB / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        text = re.sub(r"\*\*\d+\*\* 篇", f"**{len(remaining)}** 篇", text)
        readme.write_text(text, encoding="utf-8")


def write_ppc_moc(moved: list[str]) -> None:
    moc_lines = [
        "---",
        "title: 海马-PPC 印象笔记归档",
        "type: moc",
        "imported: 2026-05-23",
        "---",
        "",
        "# 海马-PPC · 印象笔记归档",
        "",
        "> 自 [[7 可复用知识库/印象笔记存档/MOC|印象笔记存档]] 按 topic 迁出（TMS/PPC/省自然/7T 分析）。",
        "> 总控：[[海马-PPC 通路研究]]",
        "",
        "## 核心笔记",
        "",
    ]
    for stem in moved:
        moc_lines.append(f"- [[印象笔记归档/notes/00_核心/{stem}|{stem}]]")
    moc_lines.extend(["", "## 说明", "", "- 正文未人工改写；附件在 `attachments/`。", ""])
    (ARCHIVE / "PPC_MOC.md").write_text("\n".join(moc_lines), encoding="utf-8")
    (ARCHIVE / "README.md").write_text(
        f"""# 海马-PPC 印象笔记归档

> 2026-05-23 · **{len(moved)}** 篇自垃圾场迁出  
> 入口：[[PPC_MOC]] · 总控 [[海马-PPC 通路研究]]

## 目录

| 路径 | 内容 |
|------|------|
| `notes/00_核心/` | TMS-PPC 方案、省自然、7T 分析笔记 |
| `attachments/` | 各笔记 `*_files` 资源 |
""",
        encoding="utf-8",
    )


def main() -> None:
    PROJ_NOTES.mkdir(parents=True, exist_ok=True)
    PROJ_ATTACH.mkdir(parents=True, exist_ok=True)

    moved: list[str] = []
    for stem in EXTRACT_STEMS:
        src_md = KB_NOTES / f"{stem}.md"
        if not src_md.exists():
            print(f"MISSING: {stem}")
            continue
        text = src_md.read_text(encoding="utf-8")
        text = text.replace(f"![[{OLD_ATTACH_PREFIX}/", f"![[{NEW_ATTACH_PREFIX}/")
        (PROJ_NOTES / f"{stem}.md").write_text(text, encoding="utf-8")
        src_md.unlink()

        src_attach = KB_ATTACH / f"{stem}_files"
        if src_attach.is_dir():
            dst_attach = PROJ_ATTACH / f"{stem}_files"
            if dst_attach.exists():
                shutil.rmtree(dst_attach)
            shutil.move(str(src_attach), str(dst_attach))
        moved.append(stem)
        print(f"Moved: {stem}")

    regenerate_kb_moc(len(moved))
    write_ppc_moc(moved)
    remaining = len(list(KB_NOTES.glob("*.md")))
    print(f"\nDone: moved {len(moved)}, KB remaining {remaining}")


if __name__ == "__main__":
    main()
