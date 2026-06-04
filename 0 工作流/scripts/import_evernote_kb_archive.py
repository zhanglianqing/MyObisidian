#!/usr/bin/env python3
"""Import remaining Evernote HTML export into 7 可复用知识库/印象笔记存档."""

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

VAULT = Path(__file__).resolve().parents[2]
ARCHIVE = VAULT / "7 可复用知识库/印象笔记存档"
NOTES = ARCHIVE / "notes"
ATTACHMENTS = ARCHIVE / "attachments"
VAULT_ATTACH_PREFIX = "7 可复用知识库/印象笔记存档/attachments"


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
        return to_vault_embed(f"{note_stem}_files/{fname}")

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


def parse_index(export_dir: Path) -> list[tuple[str, str]]:
    for p in export_dir.glob("*index*.html"):
        soup = BeautifulSoup(p.read_text(encoding="utf-8", errors="replace"), "html.parser")
        items: list[tuple[str, str]] = []
        for a in soup.select("ul li a[href]"):
            href = unquote(a["href"].split("#")[0])
            if href.endswith(".html"):
                items.append((a.get_text(strip=True) or href, href))
        return items
    return []


def remove_orphan_asset_dirs(export_dir: Path) -> list[str]:
    html_stems = {p.stem for p in export_dir.glob("*.html")}
    removed: list[str] = []
    for d in export_dir.iterdir():
        if not d.is_dir():
            continue
        name = d.name
        if name.endswith("_files"):
            stem = name[:-6]
            if stem not in html_stems:
                shutil.rmtree(d)
                removed.append(name)
    return removed


def import_notes(
    export_dir: Path, dry_run: bool = False, append: bool = False
) -> dict[str, str]:
    if html2text is None:
        raise SystemExit("pip install html2text beautifulsoup4 lxml")

    h2t = html2text.HTML2Text()
    h2t.body_width = 0
    h2t.ignore_links = False
    h2t.ignore_images = False
    h2t.unicode_snob = True

    html_paths = [
        p
        for p in sorted(export_dir.glob("*.html"))
        if "index" not in p.name.lower()
    ]
    html_to_wikilink: dict[str, str] = {}
    for html_path in html_paths:
        md_stem = safe_filename(html_path.stem)
        html_to_wikilink[html_path.name] = f"印象笔记存档/notes/{md_stem}"

    if not dry_run:
        if append:
            NOTES.mkdir(parents=True, exist_ok=True)
            ATTACHMENTS.mkdir(parents=True, exist_ok=True)
            for md_path in NOTES.glob("*.md"):
                html_to_wikilink.setdefault(
                    f"{md_path.stem}.html",
                    f"印象笔记存档/notes/{md_path.stem}",
                )
        else:
            if ARCHIVE.exists():
                shutil.rmtree(ARCHIVE)
            NOTES.mkdir(parents=True, exist_ok=True)
            ATTACHMENTS.mkdir(parents=True, exist_ok=True)

    for html_path in html_paths:
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        title, fragment = extract_note_body(soup)
        if not title:
            title = html_lib.unescape(html_path.stem)
        md_stem = safe_filename(html_path.stem)
        md_body = html_to_markdown(fragment, h2t)
        md_body = rewrite_asset_paths(md_body, html_path.stem)
        md_body = rewrite_internal_links(md_body, html_to_wikilink)
        fm = (
            "---\n"
            f'title: "{title.replace(chr(34), chr(39))}"\n'
            "source: evernote_html\n"
            f'source_html: "{html_path.name}"\n'
            "imported: 2026-05-23\n"
            "---\n\n"
        )
        if not dry_run:
            (NOTES / f"{md_stem}.md").write_text(fm + f"# {title}\n\n{md_body}\n", encoding="utf-8")
            copy_assets(export_dir, html_path.stem)

    return html_to_wikilink


def write_moc(
    export_dir: Path,
    html_to_wikilink: dict[str, str],
    append: bool = False,
    new_count: int = 0,
) -> None:
    index_items = parse_index(export_dir)
    lines = [
        "---",
        "title: 印象笔记存档目录",
        "type: moc",
        "imported: 2026-05-23",
        "---",
        "",
        "# 印象笔记存档",
        "",
        "> 控制台笔记本组剩余笔记；正文未改写。Cursor 默认不索引（见 vault `.cursorignore`），需要时在 Obsidian 内搜 topic。",
        "",
    ]
    if append and new_count:
        lines.append(
            f"> 追加导入 {new_count} 篇（保留既有笔记；部分已迁出至各项目 `印象笔记归档/`）。"
        )
        lines.append("")
    if index_items:
        lines.extend(["## 原笔记本顺序", ""])
        for title, href in index_items:
            key = Path(href).name
            if key in html_to_wikilink:
                lines.append(f"- [[{html_to_wikilink[key]}|{title}]]")
            else:
                lines.append(f"- {title} *(未迁入: {href})*")
        lines.append("")

    seen: set[str] = set()
    wlinks: list[str] = []
    for wlink in html_to_wikilink.values():
        if wlink not in seen and (NOTES / f"{wlink.split('/')[-1]}.md").exists():
            seen.add(wlink)
            wlinks.append(wlink)
    lines.extend(["## 按标题（A–Z）", ""])
    for wlink in sorted(wlinks, key=lambda w: w.split("/")[-1].lower()):
        name = wlink.split("/")[-1]
        lines.append(f"- [[{wlink}|{name}]]")
    lines.append("")
    (ARCHIVE / "MOC.md").write_text("\n".join(lines), encoding="utf-8")


def write_readme(export_dir: Path, count: int, append: bool = False) -> None:
    total = len(list(NOTES.glob("*.md"))) if NOTES.is_dir() else count
    mode = "追加" if append else "全量"
    text = f"""# 印象笔记存档

> {mode}导入：2026-05-23 · 源：`{export_dir}`  
> 库内 **{total}** 篇 · 扁平 `notes/` · 附件在 `attachments/`  
> Cursor 索引：已 `.cursorignore`（按需 Obsidian 搜索或手动 `@` 单篇）

## 入口

- [[MOC]] — 全量目录

## 说明

- 从桌面「印象笔记导出」迁入；不含已入 1a-2a 核心的 4 篇。
- 后续按 topic 整理时，可从此目录子集迁出到具体项目或 Zotero（见 `extract_kb_to_ppc.py`）。
"""
    (ARCHIVE / "README.md").write_text(text, encoding="utf-8")


def clear_export(export_dir: Path) -> int:
    n = 0
    for p in list(export_dir.iterdir()):
        if p.name.startswith("."):
            continue
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--export-dir", default=r"F:\SYSTEM\DESKTOP\印象笔记导出")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--keep-export", action="store_true", help="Do not empty desktop export after import")
    ap.add_argument(
        "--append",
        action="store_true",
        help="Merge into existing archive (do not wipe 印象笔记存档/)",
    )
    args = ap.parse_args()

    export_dir = Path(args.export_dir)
    if not export_dir.is_dir():
        raise SystemExit(f"Export dir not found: {export_dir}")

    orphans = remove_orphan_asset_dirs(export_dir)
    if orphans:
        print(f"Removed {len(orphans)} orphan *_files folders")
    else:
        print("No orphan *_files folders")

    before = len(list(NOTES.glob("*.md"))) if args.append and NOTES.is_dir() else 0
    html_to_wikilink = import_notes(export_dir, dry_run=args.dry_run, append=args.append)
    new_count = len(
        [p for p in export_dir.glob("*.html") if "index" not in p.name.lower()]
    )
    print(f"Notes in batch: {new_count}")

    if args.dry_run:
        print("Dry run — no vault or export changes.")
        return

    write_moc(export_dir, html_to_wikilink, append=args.append, new_count=new_count)
    write_readme(export_dir, new_count, append=args.append)
    after = len(list(NOTES.glob("*.md")))
    print(f"Done -> {ARCHIVE} ({before} + {after - before} = {after} notes)")

    if not args.keep_export:
        removed = clear_export(export_dir)
        print(f"Cleared export dir ({removed} items)")


if __name__ == "__main__":
    main()
