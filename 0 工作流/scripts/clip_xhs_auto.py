#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书：粘贴 App「分享→复制链接」全文 → 抓取 → 视频转写 → 写入 Clippings

视频处理策略（--mode）:
  social（默认）  只保留转写文字，不在 vault 存 mp4 / 直链
  radiology       影像学习：mp4 存入 _assets + 转写

用法:
  python clip_xhs_auto.py "分享全文"
  python clip_xhs_auto.py "分享全文" --mode radiology
  python clip_xhs_auto.py "分享全文" --no-transcribe
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT = SCRIPT_DIR.parents[1]


def extract_url(text: str) -> str:
    text = text.strip()
    for pat in (
        r"https?://(?:www\.)?xiaohongshu\.com/[^\s\]\>\"']+",
        r"https?://(?:www\.)?xhslink\.com/[^\s\]\>\"']+",
    ):
        m = re.search(pat, text, re.I)
        if m:
            return m.group(0).rstrip(".,;)")
    raise ValueError(
        "未找到小红书链接。请用 App「分享→复制链接」，或含 xhslink.com / xiaohongshu.com 的分享全文。"
    )


def load_module(name: str, filename: str):
    path = SCRIPT_DIR / filename
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_fetch(
    url: str,
    vault: Path,
    *,
    mode: str = "social",
    transcribe: bool = True,
) -> Path:
    fetch = load_module("fetch_xhs_note", "fetch_xhs_note.py")
    cookie_path = fetch.find_cookie_file(None)
    if not cookie_path:
        raise RuntimeError(
            "未找到 Cookie 文件。见 0 工作流/workflows/3.2 Workflow §一、一次性配置"
        )

    cookie_header, cookie_names = fetch.load_cookie_header(cookie_path)
    fetch.warn_missing_session(cookie_names)
    html = fetch.fetch_html(url, cookie_header)
    state = fetch.parse_initial_state(html)
    note_id = fetch.extract_note_id(url)
    note = fetch.deep_find_note(state, note_id)
    if not note:
        raise RuntimeError(
            "抓取不到正文。请使用带 xsec_token 的完整分享链接，并检查 Cookie 是否过期。"
        )

    fields = fetch.extract_fields(note)
    video_policy = "archive" if mode == "radiology" else "transcript_only"
    transcript = ""
    transcript_status = ""
    local_video_rel = ""

    video_url = fields.get("video_url") or ""
    if video_url and transcribe:
        try:
            tx = load_module("transcribe_xhs_video", "transcribe_xhs_video.py")
            save_path = None
            if mode == "radiology":
                assets = vault / "Clippings" / "Xiaohongshu" / "_assets"
                assets.mkdir(parents=True, exist_ok=True)
                nid = (fields.get("note_id") or note_id or "video").strip()
                save_path = assets / f"{nid}.mp4"
            transcript = tx.process_video(
                video_url,
                cookie_header,
                save_path=save_path,
            )
            clean = load_module("transcript_cleanup", "transcript_cleanup.py")
            transcript = clean.cleanup_transcript(transcript)
            if save_path and save_path.is_file():
                local_video_rel = save_path.relative_to(vault).as_posix()
        except Exception as e:
            transcript_status = f"（转写失败: {e}）"

    default_projects = (
        ["[[临床医学知识库]]"] if mode == "radiology" else []
    )
    nid = (fields.get("note_id") or note_id or "note").strip()
    local_images: list[str] = []
    if fields.get("images") and not fields.get("video_url"):
        local_images = fetch.download_note_images(
            fields["images"], vault, nid, cookie_header
        )
    filename, md = fetch.build_markdown(
        url,
        fields,
        video_policy=video_policy,
        transcript=transcript,
        transcript_status=transcript_status,
        local_video=local_video_rel,
        default_projects=default_projects,
        local_images=local_images,
    )
    out_dir = vault / "Clippings" / "Xiaohongshu" / "_Inbox"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    if out_path.exists():
        out_path = out_dir / f"{out_path.stem}_{datetime.now().strftime('%H%M%S')}.md"
    out_path.write_text(md, encoding="utf-8")

    try:
        enrich = load_module("enrich_xhs_clipping", "enrich_xhs_clipping.py")
        if enrich.is_configured():
            enrich.enrich_file(out_path, vault=vault, mode=mode)
    except Exception as e:
        print(f"（LLM 归类跳过: {e}）", file=sys.stderr)

    return out_path


def main() -> int:
    _configure_stdio()
    parser = argparse.ArgumentParser(description="小红书剪藏抓取")
    parser.add_argument("text", nargs="?", default="", help="分享文案或 URL")
    parser.add_argument("--url", default="", help="直接指定 URL")
    parser.add_argument("--vault", default=str(VAULT))
    parser.add_argument(
        "--mode",
        choices=("social", "radiology"),
        default="social",
        help="social=仅转写；radiology=本地存 mp4+转写",
    )
    parser.add_argument(
        "--no-transcribe",
        action="store_true",
        help="跳过转写（仅元数据与正文标签）",
    )
    args = parser.parse_args()

    raw = args.url or args.text or ""
    if not raw.strip():
        raw = sys.stdin.read()
    if not raw.strip():
        print("请传入小红书分享链接或文案", file=sys.stderr)
        return 2

    try:
        url = extract_url(raw)
        vault = Path(args.vault).resolve()
        out_path = run_fetch(
            url,
            vault,
            mode=args.mode,
            transcribe=not args.no_transcribe,
        )
        result = {
            "url": url,
            "file": str(out_path),
            "mode": args.mode,
            "transcribed": not args.no_transcribe,
        }
        out = json.dumps(result, ensure_ascii=False)
        try:
            print(out)
        except UnicodeEncodeError:
            print(out.encode("utf-8", errors="replace").decode("utf-8"))
        return 0
    except Exception as e:
        print(f"失败: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
