#!/usr/bin/env python3
"""Import selected Yinxiang/Evernote HTML notes into 1a-2a vault folder.

Workflow: 0 工作流/workflows/3.5 Workflow ：Legacy 前期项目入库.md (Step 6)
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup

try:
    import html2text
except ImportError:
    html2text = None  # type: ignore

VAULT = Path(__file__).resolve().parents[2]
PROJECT = VAULT / "1 主线项目/前期产出/1a-2a 海马宏观微观分割与抗抑郁疗效预测-梦月paper"
ARCHIVE = PROJECT / "印象笔记归档"
NOTES = ARCHIVE / "notes" / "00_核心"
ATTACHMENTS = ARCHIVE / "attachments"
VAULT_ATTACH_PREFIX = (
    "1 主线项目/前期产出/1a-2a 海马宏观微观分割与抗抑郁疗效预测-梦月paper/印象笔记归档/attachments"
)

WHITELIST_TITLE = re.compile(
    r"基于 TabPFN 的海马亚区疗效预测验证|"
    r"研究笔记：海马后部不对称性作为抗抑郁疗效预测的影像学标准|"
    r"Mengyue Paper 重修改重投|"
    r"2024年度 key points and review",
    re.I,
)


def safe_filename(stem: str, max_len: int = 120) -> str:
    stem = stem.strip().strip(".")
    stem = re.sub(r'[<>:"/\\|?*]', "-", stem)
    stem = re.sub(r"\s+", " ", stem)
    if len(stem) > max_len:
        stem = stem[:max_len].rstrip()
    return stem or "untitled"


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
    def repl(m: re.Match) -> str:
        src = _strip_path_wrapper(m.group(2))
        if src.startswith(("http://", "https://", "evernote://")):
            return m.group(0)
        fname = Path(src).name
        folder = f"{note_stem}_files"
        return to_vault_embed(f"{folder}/{fname}")

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, md)


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


def collect_whitelist(export_dir: Path) -> list[Path]:
    selected: list[Path] = []
    for html_path in sorted(export_dir.glob("*.html")):
        if "index" in html_path.name.lower():
            continue
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        title, _ = extract_note_body(soup)
        if WHITELIST_TITLE.search(title):
            selected.append(html_path)
    return selected


def import_notes(export_dir: Path, dry_run: bool = False) -> dict[str, str]:
    if html2text is None:
        raise SystemExit("pip install html2text beautifulsoup4 lxml")

    h2t = html2text.HTML2Text()
    h2t.body_width = 0
    h2t.ignore_links = False
    h2t.ignore_images = False
    h2t.unicode_snob = True

    selected = collect_whitelist(export_dir)
    if len(selected) != 4:
        titles = []
        for p in selected:
            soup = BeautifulSoup(p.read_text(encoding="utf-8", errors="replace"), "html.parser")
            t, _ = extract_note_body(soup)
            titles.append(t)
        raise SystemExit(f"Expected 4 whitelist notes, found {len(selected)}: {titles}")

    html_to_wikilink: dict[str, str] = {}
    for html_path in selected:
        md_stem = safe_filename(html_path.stem)
        html_to_wikilink[html_path.name] = f"印象笔记归档/notes/00_核心/{md_stem}"

    if not dry_run:
        NOTES.mkdir(parents=True, exist_ok=True)
        ATTACHMENTS.mkdir(parents=True, exist_ok=True)

    for html_path in selected:
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        title, fragment = extract_note_body(soup)
        md_stem = safe_filename(html_path.stem)
        md_body = html_to_markdown(fragment, h2t)
        md_body = rewrite_asset_paths(md_body, html_path.stem)
        md_body = rewrite_internal_links(md_body, html_to_wikilink)
        fm = (
            "---\n"
            f'title: "{title.replace(chr(34), chr(39))}"\n'
            "source: evernote_html\n"
            f'source_html: "{html_path.name}"\n'
            'category: "00_核心"\n'
            "imported: 2026-05-23\n"
            "---\n\n"
        )
        out_path = NOTES / f"{md_stem}.md"
        if not dry_run:
            out_path.write_text(fm + f"# {title}\n\n{md_body}\n", encoding="utf-8")
            copy_assets(export_dir, html_path.stem)
        print(f"{'[dry-run] ' if dry_run else ''}import: {title}")

    return html_to_wikilink


def write_moc(html_to_wikilink: dict[str, str]) -> None:
    lines = [
        "---",
        "title: 1a-2a 印象笔记核心笔记",
        "type: moc",
        "imported: 2026-05-23",
        "---",
        "",
        "# 1a-2a 印象笔记核心笔记",
        "",
        "> 2026-05-23 自「控制台」导出包**白名单**迁入（TabPFN / 梦月稿 / Eur Radiol key points）。",
        "> 总控：[[1a-2a 海马宏观微观分割与抗抑郁疗效预测]]",
        "",
        "## 核心笔记",
        "",
    ]
    for wlink in sorted(html_to_wikilink.values(), key=lambda x: x.split("/")[-1]):
        name = wlink.split("/")[-1]
        lines.append(f"- [[{wlink}|{name}]]")
    lines.append("")
    (ARCHIVE / "1a2a_MOC.md").write_text("\n".join(lines), encoding="utf-8")


def write_readme(export_dir: Path, count: int) -> None:
    readme = f"""# 印象笔记归档 · 1a-2a

> 导入时间：2026-05-23（白名单 4 篇）  
> 源目录：`{export_dir}`  
> 流程：[[0 工作流/workflows/3.5 Workflow ：Legacy 前期项目入库]] Step 6

## 入口

- [[1a2a_MOC]] — 核心笔记目录
- [[../1a-2a 海马宏观微观分割与抗抑郁疗效预测]] — 项目总控

| 路径 | 内容 |
|------|------|
| `notes/00_核心/` | TabPFN 验证、后部不对称性研究笔记、梦月稿改投、Eur Radiol key points |
| `attachments/` | 各笔记 `*_files` 资源 |

共导入 **{count}** 篇笔记。
"""
    (ARCHIVE / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--export-dir", default=r"F:\SYSTEM\DESKTOP\印象笔记导出")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    export_dir = Path(args.export_dir)
    if not export_dir.is_dir():
        raise SystemExit(f"Export dir not found: {export_dir}")

    html_to_wikilink = import_notes(export_dir, dry_run=args.dry_run)
    if args.dry_run:
        print("Dry run — no files written.")
        return

    write_moc(html_to_wikilink)
    write_readme(export_dir, len(html_to_wikilink))
    print(f"Done -> {ARCHIVE}")


if __name__ == "__main__":
    main()
