#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章抓取 → Obsidian Markdown

用法:
  python fetch_wechat_article.py --url "https://mp.weixin.qq.com/s/..."
  python fetch_wechat_article.py --url "..." --vault "E:/Obisidian/MyObisidian"

无需 Cookie（多数公开文章可直接访问）；若返回「环境异常」，请在微信内打开后复制全文入库。
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse

try:
    import requests
except ImportError:
    print("请先安装: pip install requests", file=sys.stderr)
    sys.exit(1)

DEFAULT_VAULT = Path(__file__).resolve().parents[2]
OUT_SUBDIR = Path("Clippings/WeChat/_Inbox")
IMG_SUBDIR = Path("Clippings/WeChat/_assets")

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

VERIFY_MARKERS = ("环境异常", "完成验证后即可继续访问", "secclient")


def _http_session() -> requests.Session:
    s = requests.Session()
    s.trust_env = False
    return s


_HTTP = _http_session()


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith("http"):
        url = "https://" + url.lstrip("/")
    return url.split("#")[0]


def extract_article_id(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    slug = path.rsplit("/", 1)[-1] if path else "article"
    slug = re.sub(r"[^\w-]", "", slug)[:48]
    return slug or "article"


def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://mp.weixin.qq.com/",
    }
    r = _HTTP.get(url, headers=headers, timeout=45, allow_redirects=True)
    r.raise_for_status()
    text = r.content.decode("utf-8", errors="replace")
    if any(m in text for m in VERIFY_MARKERS):
        raise RuntimeError(
            "微信返回验证页（环境异常）。请在微信内打开链接复制全文，或稍后重试。"
        )
    return text


def _decode_js_string(raw: str) -> str:
    """解码 var nickname = htmlDecode(\"...\") 等 JS 字符串。"""
    out = raw
    out = out.replace("\\x22", '"').replace("\\x27", "'")
    out = out.replace('\\"', '"').replace("\\'", "'")
    out = re.sub(r"\\x([0-9a-fA-F]{2})", lambda m: chr(int(m.group(1), 16)), out)
    return html.unescape(out)


def _extract_js_var(page: str, name: str) -> str:
    patterns = (
        rf"var {name}\s*=\s*htmlDecode\(\s*\"((?:\\.|[^\"])*)\"\s*\)",
        rf"var {name}\s*=\s*'((?:\\'|[^'])*)'\.html\(false\)",
        rf"var {name}\s*=\s*'((?:\\'|[^'])*)'",
        rf'var {name}\s*=\s*"((?:\\.|[^"])*)"',
    )
    for pat in patterns:
        m = re.search(pat, page)
        if m:
            return _decode_js_string(m.group(1)).strip()
    return ""


def _extract_create_time(page: str) -> str:
    m = re.search(r'var create_time\s*=\s*"(\d+)"\s*\*\s*1', page)
    if not m:
        m = re.search(r"var ct\s*=\s*'(\d+)'", page)
    if not m:
        return ""
    try:
        ts = int(m.group(1))
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except (ValueError, OSError):
        return ""


def extract_js_content(page: str) -> str:
    m = re.search(r'id="js_content"[^>]*>', page, re.I)
    if not m:
        return ""
    start = m.end()
    depth = 1
    i = start
    n = len(page)
    while i < n and depth > 0:
        open_m = re.search(r"<div[\s>]", page[i:], re.I)
        close_m = re.search(r"</div>", page[i:], re.I)
        if close_m is None:
            break
        if open_m and open_m.start() < close_m.start():
            depth += 1
            i += open_m.end()
        else:
            depth -= 1
            if depth == 0:
                return page[start : i + close_m.start()]
            i += close_m.end()
    return ""


def extract_image_urls(content_html: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for pat in (
        r'(?:data-src|src)\s*=\s*"(https?://mmbiz\.qpic\.cn/[^"]+)"',
        r"(?:data-src|src)\s*=\s*'(https?://mmbiz\.qpic\.cn/[^']+)'",
    ):
        for u in re.findall(pat, content_html, re.I):
            u = html.unescape(unquote(u)).strip()
            if u and u not in seen:
                seen.add(u)
                urls.append(u)
    return urls


def html_to_text(content_html: str) -> str:
    text = content_html
    text = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.I)
    text = re.sub(r"<img[\s\S]*?>", "\n", text, flags=re.I)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</(?:p|section|div|h[1-6]|li|tr)>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_article(page: str, url: str) -> dict:
    title = _extract_js_var(page, "msg_title")
    author = _extract_js_var(page, "nickname")
    if not author:
        m = re.search(r'id="js_name"[^>]*>([^<]+)<', page)
        if m:
            author = html.unescape(m.group(1)).strip()
    if not title:
        m = re.search(r'<h1[^>]*id="activity-name"[^>]*>([\s\S]*?)</h1>', page, re.I)
        if m:
            title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()

    content_html = extract_js_content(page)
    if not content_html:
        raise RuntimeError("未解析到正文（js_content）。链接可能失效或需在微信内打开。")

    publish_time = _extract_create_time(page)
    image_urls = extract_image_urls(content_html)
    body_text = html_to_text(content_html)

    return {
        "title": title or "未命名公众号文章",
        "author": author or "未知公众号",
        "content_html": content_html,
        "body_text": body_text,
        "publish_time": publish_time,
        "article_id": extract_article_id(url),
        "image_urls": image_urls,
    }


def safe_filename(title: str, max_len: int = 70) -> str:
    t = re.sub(r'[\\/:*?"<>|]', "-", title).strip()
    return (t[:max_len] if t else "未命名") or "未命名"


def download_images(urls: list[str], vault: Path, article_id: str) -> list[str]:
    if not urls:
        return []
    safe_id = re.sub(r"[^\w-]", "", article_id or "article")[:48] or "article"
    img_dir = vault / IMG_SUBDIR / safe_id
    img_dir.mkdir(parents=True, exist_ok=True)
    headers = {
        "User-Agent": UA,
        "Referer": "https://mp.weixin.qq.com/",
    }
    rel_paths: list[str] = []
    for i, img_url in enumerate(urls, 1):
        low = img_url.lower()
        if ".png" in low:
            ext = ".png"
        elif ".gif" in low:
            ext = ".gif"
        elif ".webp" in low:
            ext = ".webp"
        else:
            ext = ".jpg"
        dest = img_dir / f"{i:02d}{ext}"
        if not dest.is_file():
            r = _HTTP.get(img_url, headers=headers, timeout=90)
            r.raise_for_status()
            dest.write_bytes(r.content)
        rel_paths.append(dest.relative_to(vault).as_posix())
    return rel_paths


def format_image_embeds(paths: list[str]) -> str:
    if not paths:
        return ""
    header = f"## 配图（共 {len(paths)} 张）\n\n" if len(paths) > 1 else "## 配图\n\n"
    lines = [f"![[{p}]]" for p in paths]
    return header + "\n\n".join(lines) + "\n"


def _yaml_list(key: str, items: list[str]) -> str:
    if not items:
        return f"{key}: []"
    lines = [key + ":"]
    for item in items:
        safe = item.replace('"', "'")
        lines.append(f'  - "{safe}"')
    return "\n".join(lines)


def build_markdown(
    url: str,
    fields: dict,
    *,
    local_images: list[str] | None = None,
    default_projects: list[str] | None = None,
) -> tuple[str, str]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    title = fields["title"]
    author = fields["author"]
    body_text = fields["body_text"]
    publish_time = fields.get("publish_time") or ""
    embed_paths = local_images if local_images is not None else []
    image_count = len(embed_paths)
    img_lines = format_image_embeds(embed_paths)
    projects = default_projects or []
    project_yaml = _yaml_list("project", projects)

    pub_line = f" · 发布 {publish_time}" if publish_time else ""
    image_count_yaml = f"image_count: {image_count}\n" if image_count else ""
    safe_title = title.replace('"', "'")
    safe_author = author.replace('"', "'")

    body = f"""---
source: wechat
url: "{url}"
author: "{safe_author}"
title: "{safe_title}"
{image_count_yaml}captured_at: {now}
published_at: "{publish_time}"
status: inbox
tags: []
{project_yaml}
ai_summary: ""
action: read_later
starred: true
fetcher: wechat-script
---

# {title}

> **{author}**{pub_line} · [原文]({url})

## 要点

（由 Cursor 填写：6～8 条完整句，保留方法、数据、结论与专有名词。见 wechat-clipping.mdc）

## 正文

{body_text}

{img_lines}"""
    filename = f"{date_prefix} {safe_filename(title)}.md"
    return filename, body


def run_fetch(
    url: str,
    vault: Path,
    *,
    download_imgs: bool = True,
    default_projects: list[str] | None = None,
) -> tuple[Path, dict]:
    url = normalize_url(url)
    page = fetch_html(url)
    fields = parse_article(page, url)
    local_images: list[str] = []
    if download_imgs and fields.get("image_urls"):
        local_images = download_images(fields["image_urls"], vault, fields["article_id"])
    filename, md = build_markdown(
        url,
        fields,
        local_images=local_images,
        default_projects=default_projects,
    )
    out_dir = vault / OUT_SUBDIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    if out_path.exists():
        out_path = out_dir / f"{out_path.stem}_{datetime.now().strftime('%H%M%S')}.md"
    out_path.write_text(md, encoding="utf-8")
    return out_path, fields


def main() -> int:
    parser = argparse.ArgumentParser(description="抓取微信公众号文章到 Obsidian Clippings")
    parser.add_argument("--url", required=True, help="公众号文章链接 mp.weixin.qq.com/s/...")
    parser.add_argument("--vault", default=str(DEFAULT_VAULT), help="Obsidian vault 根目录")
    parser.add_argument("--no-images", action="store_true", help="跳过配图下载")
    parser.add_argument("--stdout", action="store_true", help="只打印 Markdown 不写文件")
    args = parser.parse_args()

    url = normalize_url(args.url)
    if "mp.weixin.qq.com" not in url:
        print("错误: 不是微信公众号链接", file=sys.stderr)
        return 2

    vault = Path(args.vault).resolve()
    page = fetch_html(url)
    fields = parse_article(page, url)
    local_images: list[str] = []
    if not args.no_images and fields.get("image_urls"):
        local_images = download_images(fields["image_urls"], vault, fields["article_id"])
    filename, md = build_markdown(url, fields, local_images=local_images)

    if args.stdout:
        print(md)
        return 0

    out_dir = vault / OUT_SUBDIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    if out_path.exists():
        out_path = out_dir / f"{out_path.stem}_{datetime.now().strftime('%H%M%S')}.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"已写入: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
