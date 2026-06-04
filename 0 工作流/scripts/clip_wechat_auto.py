#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号：粘贴链接或分享文案 → 抓取 → 写入 Clippings/WeChat/_Inbox

用法:
  python clip_wechat_auto.py "https://mp.weixin.qq.com/s/..."
  python clip_wechat_auto.py "分享文案含链接"
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
        r"https?://mp\.weixin\.qq\.com/s[^\s\]\>\"']+",
        r"https?://mp\.weixin\.qq\.com/mp/appmsg[^\s\]\>\"']+",
    ):
        m = re.search(pat, text, re.I)
        if m:
            return m.group(0).rstrip(".,;)")
    raise ValueError(
        "未找到公众号链接。请粘贴 mp.weixin.qq.com/s/... 链接或含链接的分享文案。"
    )


def load_module(name: str, filename: str):
    path = SCRIPT_DIR / filename
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_fetch(url: str, vault: Path, *, download_imgs: bool = True) -> Path:
    fetch = load_module("fetch_wechat_article", "fetch_wechat_article.py")
    out_path, _fields = fetch.run_fetch(
        url,
        vault,
        download_imgs=download_imgs,
    )
    try:
        enrich = load_module("enrich_xhs_clipping", "enrich_xhs_clipping.py")
        if enrich.is_configured():
            enrich.enrich_file(out_path, vault=vault, mode="social")
    except Exception as e:
        print(f"（LLM 归类跳过: {e}）", file=sys.stderr)
    return out_path


def main() -> int:
    _configure_stdio()
    parser = argparse.ArgumentParser(description="微信公众号剪藏抓取")
    parser.add_argument("text", nargs="?", default="", help="分享文案或 URL")
    parser.add_argument("--url", default="", help="直接指定 URL")
    parser.add_argument("--vault", default=str(VAULT))
    parser.add_argument("--no-images", action="store_true", help="跳过配图下载")
    args = parser.parse_args()

    raw = args.url or args.text or ""
    if not raw.strip():
        raw = sys.stdin.read()
    if not raw.strip():
        print("请传入公众号链接或分享文案", file=sys.stderr)
        return 2

    try:
        url = extract_url(raw)
        vault = Path(args.vault).resolve()
        out_path = run_fetch(url, vault, download_imgs=not args.no_images)
        result = {
            "url": url,
            "file": str(out_path),
            "source": "wechat",
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
