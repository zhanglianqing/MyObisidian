#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为已入库但转写失败的视频笔记补转写（原地更新 md）。"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT = SCRIPT_DIR.parents[1]
FAIL_MARK = "转写失败"


def _safe_print(msg: str, *, err: bool = False) -> None:
    stream = sys.stderr if err else sys.stdout
    try:
        print(msg, file=stream, flush=True)
    except UnicodeEncodeError:
        print(msg.encode("utf-8", errors="replace").decode("utf-8"), file=stream, flush=True)


def load_module(name: str, filename: str):
    path = SCRIPT_DIR / filename
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_url(text: str) -> str:
    clip = load_module("clip_xhs_auto", "clip_xhs_auto.py")
    return clip.extract_url(text)


def parse_frontmatter_url(md: str) -> str:
    m = re.search(r'^url:\s*["\']?([^"\'\n]+)', md, re.M)
    return m.group(1).strip() if m else ""


def needs_retranscribe(text: str) -> bool:
    if FAIL_MARK in text:
        return True
    if 'note_type: "video"' in text or "note_type: video" in text:
        return "## 转写·原文" not in text and "转写未完成" in text
    return False


def patch_video_sections(md: str, transcript: str) -> str:
    summary = (
        "\n## 内容纪要\n\n"
        "（由 Cursor 根据「转写·原文」填写：去口语、分段、完整句；"
        "可用小标题；勿照抄 Whisper 口述稿。）\n"
    )
    raw = f"""
## 转写·原文

<details>
<summary>Whisper 口述稿（仅供参考，可折叠）</summary>

{transcript}

</details>
"""
    if "## 内容纪要" in md:
        md = re.sub(
            r"\n## 内容纪要\n.*?(?=\n## )",
            summary.rstrip() + "\n",
            md,
            count=1,
            flags=re.S,
        )
    else:
        md = md.replace("## 要点\n", f"## 要点\n{summary}", 1)
    if "## 转写·原文" not in md:
        md = re.sub(r"(\n## 正文\n)", raw + r"\1", md, count=1)
    else:
        md = re.sub(
            r"\n## 转写·原文\n.*?</details>\n",
            raw,
            md,
            count=1,
            flags=re.S,
        )
    return md


def retranscribe_file(md_path: Path, vault: Path) -> bool:
    text = md_path.read_text(encoding="utf-8")
    if not needs_retranscribe(text):
        return False

    url = parse_frontmatter_url(text)
    if not url:
        _safe_print(f"跳过（无 url）: {md_path.name}", err=True)
        return False

    fetch = load_module("fetch_xhs_note", "fetch_xhs_note.py")
    tx = load_module("transcribe_xhs_video", "transcribe_xhs_video.py")
    clean = load_module("transcript_cleanup", "transcript_cleanup.py")

    cookie_path = fetch.find_cookie_file(None)
    if not cookie_path:
        raise RuntimeError("未找到 xhs-cookies.json")
    cookie_header, names = fetch.load_cookie_header(cookie_path)
    fetch.warn_missing_session(names)

    html = fetch.fetch_html(url, cookie_header)
    state = fetch.parse_initial_state(html)
    note_id = fetch.extract_note_id(url)
    note = fetch.deep_find_note(state, note_id)
    if not note:
        raise RuntimeError(f"抓取不到笔记: {md_path.name}")

    fields = fetch.extract_fields(note)
    video_url = fields.get("video_url") or ""
    if not video_url:
        _safe_print(f"跳过（非视频）: {md_path.name}", err=True)
        return False

    _safe_print(f"转写: {md_path.name} …")
    transcript = tx.process_video(video_url, cookie_header)
    transcript = clean.cleanup_transcript(transcript)
    md_path.write_text(patch_video_sections(text, transcript), encoding="utf-8")
    _safe_print(f"OK: {md_path}")
    return True


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="补转写失败的 XHS 视频笔记")
    parser.add_argument(
        "paths",
        nargs="*",
        help="md 文件或目录，默认 Clippings/Xiaohongshu",
    )
    parser.add_argument("--vault", default=str(VAULT))
    args = parser.parse_args()

    vault = Path(args.vault).resolve()
    targets: list[Path] = []
    if args.paths:
        for p in args.paths:
            path = Path(p).expanduser()
            if path.is_dir():
                targets.extend(path.rglob("*.md"))
            elif path.is_file():
                targets.append(path)
    else:
        root = vault / "Clippings" / "Xiaohongshu"
        targets = list(root.rglob("*.md"))

    ok = 0
    for md in sorted(set(targets)):
        if md.name.startswith("00") or "list.md" in md.name.lower():
            continue
        try:
            if retranscribe_file(md, vault):
                ok += 1
        except Exception as e:
            _safe_print(f"失败 {md.name}: {e}", err=True)
    _safe_print(f"完成，成功补转写 {ok} 篇")
    return 0 if ok or not targets else 1


if __name__ == "__main__":
    sys.exit(main())
