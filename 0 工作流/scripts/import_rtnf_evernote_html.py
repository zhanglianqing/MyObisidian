#!/usr/bin/env python3
"""Import Yinxiang/Evernote HTML export into 3c RTNF vault folder.

Workflow: 0 工作流/workflows/3.5 Workflow ：Legacy 前期项目入库.md (Step 6)
README:   0 工作流/scripts/README-evernote-html.md
"""

from __future__ import annotations

import argparse
import html as html_lib
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup

try:
    import html2text
except ImportError:
    html2text = None  # type: ignore

# --- paths (defaults) ---
VAULT = Path(__file__).resolve().parents[2]
PROJECT = VAULT / "1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善"
ARCHIVE = PROJECT / "印象笔记归档"
NOTES = ARCHIVE / "notes"
ATTACHMENTS = ARCHIVE / "attachments"
# Obsidian resolves ![[...]] from vault root; relative ../attachments/ often fails.
VAULT_ATTACH_PREFIX = "1 主线项目/前期产出/3c 海马实时fMRI神经反馈与情绪改善/印象笔记归档/attachments"

INDEX_NAMES = {"1 RTNF_index.html", "1 RTNF_index.HTML"}


def find_export_dir(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
        if p.is_dir():
            return p
        raise SystemExit(f"Export dir not found: {p}")
    desktop = Path(r"F:\SYSTEM\DESKTOP")
    for d in desktop.iterdir():
        if d.is_dir() and d.name.startswith("RTNF"):
            return d
    raise SystemExit("Could not find RTNF export folder on Desktop")


def safe_filename(stem: str, max_len: int = 120) -> str:
    stem = stem.strip().strip(".")
    stem = re.sub(r'[<>:"/\\|?*]', "-", stem)
    stem = re.sub(r"\s+", " ", stem)
    if len(stem) > max_len:
        stem = stem[:max_len].rstrip()
    return stem or "untitled"


def categorize(stem: str, title: str) -> str:
    s = f"{stem} {title}".lower()
    if re.search(r"\bsma\b|first-level|数据处理", s) and "hipp" not in stem.lower():
        return "01_SMA"
    if re.search(
        r"hipp|海马|roi_results|学习效应|activation map|gppi|间接靶点|数据分析笔记|"
        r"feasibility.*utility|emotion regulation of hippocampus",
        s,
        re.I,
    ):
        return "02_海马fMRI分析"
    if re.search(r"sds|sas|tidier|探索sd", s, re.I):
        return "03_行为与统计"
    if re.search(
        r"paper|review|meta|阅读|neurofeed|depression|\.pdf|sciencedirect|"
        r"literature|bodurka|mindfulness|rtnf in|advances in fMRI",
        s,
        re.I,
    ):
        return "05_文献阅读"
    if re.search(
        r"2024|2025|实验记录|工作笔记|researchplan|合并笔记|2024927|预实验",
        s,
        re.I,
    ):
        return "04_实验与工作笔记"
    if re.search(
        r"opennft|installation|联影|扫描序列|tr及|优化数据|实验设计|mci ",
        s,
        re.I,
    ):
        return "06_方案与基建"
    return "07_其他"


def parse_index(export_dir: Path) -> list[tuple[str, str]]:
    """Return [(title, html_filename), ...] from RTNF index."""
    index_path = None
    for name in INDEX_NAMES:
        p = export_dir / name
        if p.exists():
            index_path = p
            break
    if not index_path:
        for p in export_dir.glob("*index*.html"):
            index_path = p
            break
    if not index_path:
        return []

    soup = BeautifulSoup(index_path.read_text(encoding="utf-8", errors="replace"), "html.parser")
    items: list[tuple[str, str]] = []
    for a in soup.select("ul li a[href]"):
        href = unquote(a["href"].split("#")[0])
        if not href.endswith(".html"):
            continue
        title = a.get_text(strip=True) or href
        items.append((title, href))
    return items


def extract_note_body(soup: BeautifulSoup) -> tuple[str, str]:
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else ""
    if h1:
        h1.decompose()
    container = soup.find("div")
    if container:
        inner = container.find("div") or container
        html_fragment = "".join(str(x) for x in inner.children)
    else:
        html_fragment = soup.body.decode_contents() if soup.body else ""
    return title, html_fragment


def html_to_markdown(fragment: str, h2t) -> str:
    if not fragment.strip():
        return ""
    if h2t is None:
        return fragment
    return h2t.handle(fragment).strip()


def _strip_path_wrapper(src: str) -> str:
    src = src.strip()
    if src.startswith("<") and src.endswith(">"):
        return src[1:-1]
    return src


def to_vault_embed(rel_under_attachments: str) -> str:
    rel = _strip_path_wrapper(rel_under_attachments).lstrip("/")
    return f"![[{VAULT_ATTACH_PREFIX}/{rel}]]"


def rewrite_asset_paths(md: str, note_stem: str) -> str:
    """Point images to vault-root wikilink embeds under 印象笔记归档/attachments/."""

    def repl(m: re.Match) -> str:
        src = _strip_path_wrapper(m.group(2))
        if src.startswith(("http://", "https://", "evernote://")):
            return m.group(0)
        fname = Path(src).name
        folder = f"{note_stem}_files"
        return to_vault_embed(f"{folder}/{fname}")

    md = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, md)
    return md


def fix_existing_image_links(notes_root: Path) -> int:
    """Convert ../attachments/ markdown images to Obsidian ![[vault/path]] embeds."""
    count = 0
    img_pat = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    linked_pat = re.compile(r"\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)")

    def fix_img(m: re.Match) -> str:
        src = _strip_path_wrapper(m.group(2))
        if src.startswith("../attachments/"):
            return to_vault_embed(src[len("../attachments/") :])
        return m.group(0)

    def fix_linked(m: re.Match) -> str:
        alt, img_src, href = m.group(1), _strip_path_wrapper(m.group(2)), m.group(3).strip()
        if not img_src.startswith("../attachments/"):
            return m.group(0)
        rel = img_src[len("../attachments/") :]
        folder = rel.split("/", 1)[0]
        out = to_vault_embed(rel)
        if href.startswith("../attachments/"):
            pdf_rel = href[len("../attachments/") :]
        elif "_files/" in href:
            pdf_rel = href if "/" in href else f"{folder}/{Path(href).name}"
        else:
            pdf_rel = f"{folder}/{Path(href).name}"
        label = alt or Path(href).name
        out += f"\n\n[[{VAULT_ATTACH_PREFIX}/{pdf_rel}|{label}]]"
        return out

    for md_path in notes_root.rglob("*.md"):
        text = md_path.read_text(encoding="utf-8")
        new_text = linked_pat.sub(fix_linked, text)
        new_text = img_pat.sub(fix_img, new_text)
        if new_text != text:
            md_path.write_text(new_text, encoding="utf-8")
            count += 1
    return count


def rewrite_internal_links(md: str, html_to_wikilink: dict[str, str]) -> str:
    def repl(m: re.Match) -> str:
        text, href = m.group(1), unquote(m.group(2))
        if href.startswith(("http://", "https://", "evernote://")):
            return m.group(0)
        key = Path(href).name
        if key in html_to_wikilink:
            return f"[[{html_to_wikilink[key]}|{text}]]"
        return m.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, md)


def copy_assets(export_dir: Path, note_stem: str) -> None:
    src = export_dir / f"{note_stem}_files"
    if not src.is_dir():
        return
    dst = ATTACHMENTS / f"{note_stem}_files"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def build_html_map(export_dir: Path) -> dict[str, tuple[str, str, str]]:
    """html_filename -> (category, md_stem, title)"""
    mapping: dict[str, tuple[str, str, str]] = {}
    for html_path in sorted(export_dir.glob("*.html")):
        if html_path.name in INDEX_NAMES:
            continue
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        title, _ = extract_note_body(soup)
        if not title:
            title = html_lib.unescape(html_path.stem)
        cat = categorize(html_path.stem, title)
        md_stem = safe_filename(html_path.stem)
        mapping[html_path.name] = (cat, md_stem, title)
    return mapping


def import_notes(export_dir: Path, dry_run: bool = False) -> dict[str, str]:
    if html2text is None:
        raise SystemExit("pip install html2text beautifulsoup4 lxml")

    h2t = html2text.HTML2Text()
    h2t.body_width = 0
    h2t.ignore_links = False
    h2t.ignore_images = False
    h2t.unicode_snob = True

    html_map = build_html_map(export_dir)
    html_to_wikilink: dict[str, str] = {}
    for html_name, (cat, md_stem, _title) in html_map.items():
        rel = f"印象笔记归档/notes/{cat}/{md_stem}"
        html_to_wikilink[html_name] = rel

    if not dry_run:
        if ARCHIVE.exists():
            shutil.rmtree(ARCHIVE)
        NOTES.mkdir(parents=True, exist_ok=True)
        ATTACHMENTS.mkdir(parents=True, exist_ok=True)

    imported = 0
    for html_path in sorted(export_dir.glob("*.html")):
        if html_path.name in INDEX_NAMES:
            continue
        if html_path.name not in html_map:
            continue
        cat, md_stem, title_from_map = html_map[html_path.name]
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        title, fragment = extract_note_body(soup)
        if not title:
            title = title_from_map

        md_body = html_to_markdown(fragment, h2t)
        md_body = rewrite_asset_paths(md_body, html_path.stem)
        md_body = rewrite_internal_links(md_body, html_to_wikilink)

        fm = (
            "---\n"
            f'title: "{title.replace(chr(34), chr(39))}"\n'
            "source: evernote_html\n"
            f'source_html: "{html_path.name}"\n'
            f'category: "{cat}"\n'
            "imported: 2026-05-23\n"
            "---\n\n"
        )
        out_path = NOTES / cat / f"{md_stem}.md"
        if not dry_run:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(fm + f"# {title}\n\n{md_body}\n", encoding="utf-8")
            copy_assets(export_dir, html_path.stem)
        imported += 1

    return html_to_wikilink


def write_moc(export_dir: Path, html_to_wikilink: dict[str, str]) -> None:
    index_items = parse_index(export_dir)
    lines = [
        "---",
        "title: RTNF 印象笔记目录",
        "type: moc",
        "imported: 2026-05-23",
        "---",
        "",
        "# RTNF 印象笔记目录",
        "",
        "> 由 `1 RTNF_index.html` 整理；笔记正文未改写，仅自 HTML 转为 Markdown。",
        "> 总控：[[3c 海马实时fMRI神经反馈与情绪改善]] · 运营：[[00_ResearchTrack]]",
        "",
    ]

    if index_items:
        lines.append("## 原笔记本目录（印象笔记顺序）")
        lines.append("")
        for title, href in index_items:
            key = Path(href).name
            if key in html_to_wikilink:
                link = html_to_wikilink[key]
                lines.append(f"- [[{link}|{title}]]")
            else:
                lines.append(f"- {title} *(未导入: {href})*")
        lines.append("")

    # by category
    by_cat: dict[str, list[str]] = {}
    for html_name, wlink in sorted(html_to_wikilink.items(), key=lambda x: x[1]):
        parts = wlink.split("/")
        cat = parts[2] if len(parts) > 2 else "07_其他"
        by_cat.setdefault(cat, []).append(wlink)

    lines.append("## 按主题分类")
    lines.append("")
    cat_labels = {
        "01_SMA": "SMA 子线",
        "02_海马fMRI分析": "海马 fMRI / ROI / 全脑",
        "03_行为与统计": "行为量表与统计",
        "04_实验与工作笔记": "实验记录与工作笔记",
        "05_文献阅读": "文献阅读（待入 Zotero）",
        "06_方案与基建": "方案、OpenNFT、扫描",
        "07_其他": "其他",
    }
    for cat in sorted(by_cat.keys()):
        label = cat_labels.get(cat, cat)
        lines.append(f"### {label}")
        lines.append("")
        for wlink in sorted(by_cat[cat]):
            name = wlink.split("/")[-1]
            lines.append(f"- [[{wlink}|{name}]]")
        lines.append("")

    lines.append("## Zotero 待整理")
    lines.append("")
    lines.append("以下目录内文献笔记可先批量浏览，有 DOI 的用 Zotero「通过标识符添加」：")
    lines.append("")
    lines.append("- `notes/05_文献阅读/`")
    lines.append("")
    (ARCHIVE / "RTNF_MOC.md").write_text("\n".join(lines), encoding="utf-8")


def write_research_track() -> None:
    text = """---
project: "3c 海马实时fMRI神经反馈与情绪改善"
type: research-track
updated: 2026-05-23
---

# RTNF · Research Track

> **运营跟踪**（Dashboard 抓取本文件名）。科学总控 → [[3c 海马实时fMRI神经反馈与情绪改善]]  
> **印象笔记存量** → [[印象笔记归档/RTNF_MOC]]（2026-05-23 自 HTML 导入，正文未改）

## 当前焦点（2026-05）

| 项 | 状态 |
|----|------|
| 主稿 | 已定稿入库 `定稿/manuscript_RTNF.docx`；交黄老师 → **姚老师** 再审 |
| 批注 | [SY3] 3.1 Behavioral：ΔSDS/ΔSAS 报告需补 **±SD**（变化量标准差，非 Table 1 前后 SD） |
| 投稿 | 已试 BS、Psych Med；转投待定 → [[RTNF 投稿思路与期刊备忘]] |

### 待办

- [ ] 姚老师意见返回 → 改稿或定投递 📅 跟进 [[同期项目-下一节点#3.2 · RTNF]]
- [ ] [SY3] 从印象笔记/坚果云定位 paired t-test 原始输出，补 `4.58 ± ?`、`4.11 ± ?` → 见 [[印象笔记归档/notes/03_行为与统计/探索SDSSAS improvement与其他量表的相关|探索SDS/SAS]] 及统计脚本
- [ ] `05_文献阅读/` 中有 DOI 的条目迁入 Zotero（可先列清单）

## 子线导航

| 子线 | 入口 |
|------|------|
| SMA（toy / 并行） | [[印象笔记归档/notes/01_SMA/SMA study|SMA study]] · [[印象笔记归档/notes/01_SMA/SMA Second-level analysis|SMA Second-level]] |
| 海马 NF 主分析 | [[印象笔记归档/notes/02_海马fMRI分析/Hipp1-4 结合分析 Updated version|Hipp1-4 分析]] · [[印象笔记归档/notes/02_海马fMRI分析/数据分析笔记：探索海马调节效率与行为改善的关联|调节效率×行为]] |
| 行为 / 量表 | [[印象笔记归档/notes/03_行为与统计/探索SDSSAS improvement与其他量表的相关|SDS/SAS 探索]] |
| 实验日志 | [[印象笔记归档/notes/04_实验与工作笔记/ResearchPlan rt-fMRI-NF 工作安排|ResearchPlan]] · `2025.* 工作笔记` |
| 文献 | [[印象笔记归档/RTNF_MOC#按主题分类]] → `05_文献阅读/` |
| 基建 | [[印象笔记归档/notes/06_方案与基建/OpenNFT|OpenNFT]] |

## 工作安排时间轴（摘自 ResearchPlan）

→ 完整勾选与文献树见 [[印象笔记归档/notes/04_实验与工作笔记/ResearchPlan rt-fMRI-NF 工作安排|ResearchPlan: rt-fMRI-NF 工作安排]]

- **一期预实验**（2023–2024）：联影实时传输、ROI（SMA/杏仁核→海马）、block 设计
- **二期 / towards paper**（2024.04+）：SMA toy + 海马 feasibility；首被试 2024/4/13–14
- **数据分析阶段**（2025）：ROI 组间、学习效应、SDS/SAS、gPPI 探索 → 对应 `02_` `03_` 笔记

## 库外资源（不迁入 vault）

| 资源 | 路径 |
|------|------|
| 坚果云 RTNF | `C:\\Users\\41516\\Nutstore\\1\\我的坚果云\\RTNF` |
| 定稿稿件 | [[定稿/README]] |
| SMA 统计表 | 见 [[3c 海马实时fMRI神经反馈与情绪改善#SMA 子线 · 数据与分析索引]] |

## 链接

- [[3c 海马实时fMRI神经反馈与情绪改善]]
- [[印象笔记归档/RTNF_MOC]]
- [[定稿/README]]
- [[01 RESEARCH_TODO_DASHBOARD]]
"""
    (PROJECT / "00_ResearchTrack.md").write_text(text, encoding="utf-8")


def write_readme(export_dir: Path, count: int) -> None:
    readme = f"""# 印象笔记归档 · RTNF

> 导入时间：2026-05-23  
> 源目录：`{export_dir}`  
> 格式：印象笔记「多个 HTML」导出；**笔记正文未人工改写**（HTML→Markdown + 图片路径修正 + 库内链接映射）。

## 入口

- [[RTNF_MOC]] — 原索引页 + 分类目录
- [[../00_ResearchTrack]] — 项目运营 track（替代原分散索引的跟踪职能）

## 目录

| 路径 | 内容 |
|------|------|
| `notes/01_SMA/` | SMA 子线 |
| `notes/02_海马fMRI分析/` | ROI、全脑、结合分析 |
| `notes/03_行为与统计/` | SDS/SAS、ERQ 等 |
| `notes/04_实验与工作笔记/` | ResearchPlan、上机记录 |
| `notes/05_文献阅读/` | 待整理入 Zotero |
| `notes/06_方案与基建/` | OpenNFT、序列、设计 |
| `attachments/` | 各笔记 `*_files` 资源 |

共导入 **{count}** 篇笔记。
"""
    (ARCHIVE / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--export-dir", help="Path to RTNF HTML export folder")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    export_dir = find_export_dir(args.export_dir)
    print(f"Export: {export_dir}")

    html_map = build_html_map(export_dir)
    print(f"Notes to import: {len(html_map)}")

    html_to_wikilink = import_notes(export_dir, dry_run=args.dry_run)
    if args.dry_run:
        print("Dry run — no files written.")
        return

    write_moc(export_dir, html_to_wikilink)
    write_research_track()
    write_readme(export_dir, len(html_to_wikilink))
    fixed = fix_existing_image_links(NOTES)
    print(f"Done. Imported {len(html_to_wikilink)} notes -> {ARCHIVE}")
    if fixed:
        print(f"Fixed image paths (spaces) in {fixed} note(s).")


if __name__ == "__main__":
    main()
