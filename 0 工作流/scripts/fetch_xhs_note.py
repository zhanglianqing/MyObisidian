#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书单帖抓取 → Obsidian Markdown（无需 Claude Code）

思路同 https://github.com/chenxiachan/xhs-claude-skills ：
Chrome 登录态 cookies + HTTP 拉取页面 + 解析 window.__INITIAL_STATE__

用法:
  python fetch_xhs_note.py --url "https://www.xiaohongshu.com/explore/..."
  python fetch_xhs_note.py --url "..." --vault "E:/Obisidian/MyObisidian"

Cookie 文件（任选其一，优先级从高到低）:
  --cookies 指定路径
  %USERPROFILE%/cookies.json
  与本脚本同目录的 xhs-cookies.json
"""

from __future__ import annotations

import argparse
import json
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
OUT_SUBDIR = Path("Clippings/Xiaohongshu/_Inbox")
IMG_SUBDIR = Path("Clippings/Xiaohongshu/_assets")

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def _http_session() -> requests.Session:
    """直连小红书 CDN，不读 Windows 系统代理（Clash 等 127.0.0.1:8001 常致 HTTPS 握手失败）。"""
    s = requests.Session()
    s.trust_env = False
    return s


_HTTP = _http_session()


def find_cookie_file(explicit: str | None) -> Path | None:
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    candidates.append(Path.home() / "cookies.json")
    candidates.append(Path(__file__).parent / "xhs-cookies.json")
    for p in candidates:
        if p.is_file():
            return p
    return None


def load_cookie_header(path: Path) -> tuple[str, list[str]]:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise ValueError(f"Cookie 文件为空: {path}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw, []

    if isinstance(data, str):
        return data, []
    if isinstance(data, dict):
        if "cookie" in data:
            return str(data["cookie"]), []
        if "cookies" in data and isinstance(data["cookies"], str):
            return data["cookies"], []
    if isinstance(data, list):
        parts = []
        names = []
        for c in data:
            if isinstance(c, dict) and "name" in c and "value" in c:
                parts.append(f"{c['name']}={c['value']}")
                names.append(str(c["name"]))
        if parts:
            return "; ".join(parts), names
    raise ValueError(
        f"无法解析 Cookie 格式: {path}\n"
        "请使用 Chrome 控制台导出脚本生成 JSON 数组，或纯 cookie 字符串。"
    )


def warn_missing_session(names: list[str]) -> None:
    important = ["a1", "webId", "web_session"]
    missing = [n for n in important if n not in names]
    if missing:
        print(
            "警告: Cookie 可能不完整，缺少: " + ", ".join(missing),
            file=sys.stderr,
        )
        if "web_session" in missing:
            print(
                "  请在 Chrome：应用程序 → Cookie → xiaohongshu.com 中复制 web_session，\n"
                "  追加到 0 工作流/scripts/xhs-cookies.json（见 3.2 Workflow §一）",
                file=sys.stderr,
            )


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith("http"):
        url = "https://" + url
    return url


def extract_note_id(url: str) -> str | None:
    patterns = [
        r"xiaohongshu\.com/explore/([a-f0-9]+)",
        r"xiaohongshu\.com/discovery/item/([a-f0-9]+)",
        r"xhslink\.com/[a-zA-Z0-9/]+",  # 短链需跳转，此处仅占位
    ]
    for p in patterns[:2]:
        m = re.search(p, url, re.I)
        if m:
            return m.group(1)
    return None


def parse_initial_state(html: str) -> dict:
    patterns = [
        r"window\.__INITIAL_STATE__\s*=\s*(\{.+?\})\s*</script>",
        r"__INITIAL_STATE__\s*=\s*(\{.+?\})\s*</script>",
    ]
    raw = None
    for pat in patterns:
        m = re.search(pat, html, re.DOTALL)
        if m:
            raw = m.group(1)
            break
    if not raw:
        raise ValueError("页面中未找到 __INITIAL_STATE__（可能未登录、链接失效或需验证码）")

    raw = re.sub(r"\bundefined\b", "null", raw)
    # 部分版本含 JavaScript 表达式，尽力清理
    raw = re.sub(r":\s*!0\b", ": true", raw)
    raw = re.sub(r":\s*!1\b", ": false", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"__INITIAL_STATE__ JSON 解析失败: {e}") from e


def extract_video_url(video: dict | None) -> str | None:
    """从 note.video 解析可播放地址（h264/h265/av1 stream）。"""
    if not isinstance(video, dict):
        return None
    media = video.get("media")
    if isinstance(media, dict):
        stream = media.get("stream")
        if isinstance(stream, dict):
            for codec in ("h264", "h265", "hevc", "av1"):
                entries = stream.get(codec)
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    for key in ("masterUrl", "url"):
                        val = entry.get(key)
                        if isinstance(val, str) and val.startswith("http"):
                            return val
                    backup = entry.get("backupUrls")
                    if isinstance(backup, list) and backup:
                        u = backup[0]
                        if isinstance(u, str) and u.startswith("http"):
                            return u
    for key in ("url", "masterUrl", "videoUrl", "playUrl"):
        val = video.get(key)
        if isinstance(val, str) and val.startswith("http"):
            return val
    return None


def _note_has_video(note: dict) -> bool:
    if not isinstance(note, dict):
        return False
    if str(note.get("type") or "").lower() == "video":
        return True
    video = note.get("video")
    return bool(extract_video_url(video if isinstance(video, dict) else None))


def _note_has_body(note: dict) -> bool:
    if not isinstance(note, dict):
        return False
    if _note_has_video(note):
        return True
    title = (note.get("title") or "").strip()
    desc = (note.get("desc") or note.get("content") or "").strip()
    return len(desc) > 5 or len(title) > 2


def _note_is_candidate(note: dict) -> bool:
    if not isinstance(note, dict):
        return False
    if not _note_has_body(note):
        return False
    if "noteId" not in note and "type" not in note:
        return False
    return bool(note.get("user") or note.get("imageList") or _note_has_video(note))


def note_from_detail_map(state: dict, note_id: str | None) -> dict | None:
    """优先从 note.noteDetailMap 取帖（视频帖通常在此）。"""
    note_root = state.get("note")
    if not isinstance(note_root, dict):
        return None
    ndm = note_root.get("noteDetailMap")
    if not isinstance(ndm, dict):
        return None

    def unwrap(entry: dict) -> dict | None:
        n = entry.get("note") if isinstance(entry.get("note"), dict) else entry
        return n if isinstance(n, dict) and _note_has_body(n) else None

    if note_id and note_id in ndm and isinstance(ndm[note_id], dict):
        found = unwrap(ndm[note_id])
        if found:
            return found
    for key, entry in ndm.items():
        if not key or key == "null" or not isinstance(entry, dict):
            continue
        if note_id and str(key) != note_id:
            continue
        found = unwrap(entry)
        if found:
            return found
    return None


def find_note_in_state(state: dict, note_id: str | None) -> dict | None:
    """按 noteId 在整棵 state 树中查找；兼容 noteDetailMap 的 null 键。"""

    def walk(obj, depth=0):
        if depth > 18:
            return None
        if isinstance(obj, dict):
            oid = str(obj.get("noteId") or obj.get("id") or "")
            if note_id and oid == note_id and _note_is_candidate(obj):
                return obj
            if _note_is_candidate(obj):
                return obj
            if "noteDetailMap" in obj and isinstance(obj["noteDetailMap"], dict):
                ndm = obj["noteDetailMap"]
                if note_id and note_id in ndm:
                    wrap = ndm[note_id]
                    if isinstance(wrap, dict):
                        n = wrap.get("note") or wrap
                        if _note_is_candidate(n):
                            return n
                for v in ndm.values():
                    if isinstance(v, dict):
                        n = v.get("note") or v
                        if _note_is_candidate(n):
                            return n
            for v in obj.values():
                found = walk(v, depth + 1)
                if found:
                    return found
        elif isinstance(obj, list):
            for item in obj[:120]:
                found = walk(item, depth + 1)
                if found:
                    return found
        return None

    return walk(state)


def deep_find_note(state: dict, note_id: str | None = None):
    found = note_from_detail_map(state, note_id)
    if found:
        return found
    return find_note_in_state(state, note_id)


def _image_url_from_item(img: object) -> str | None:
    if isinstance(img, str) and img.startswith("http"):
        return img
    if not isinstance(img, dict):
        return None
    for key in (
        "urlDefault",
        "url",
        "urlPre",
        "originUrl",
        "picUrl",
        "infoList",
    ):
        val = img.get(key)
        if isinstance(val, str) and val.startswith("http"):
            return val
        if key == "infoList" and isinstance(val, list):
            for sub in val:
                u = _image_url_from_item(sub)
                if u:
                    return u
    return None


def extract_fields(note: dict) -> dict:
    user = note.get("user") or {}
    if not isinstance(user, dict):
        user = {}
    images: list[str] = []
    seen: set[str] = set()
    image_list = note.get("imageList") or note.get("images") or []
    if isinstance(image_list, list):
        for img in image_list:
            u = _image_url_from_item(img)
            if u and u not in seen:
                seen.add(u)
                images.append(u)

    video_obj = note.get("video") if isinstance(note.get("video"), dict) else {}
    video_url = extract_video_url(video_obj)
    note_type = (note.get("type") or "").strip()
    if not note_type and video_url:
        note_type = "video"

    return {
        "title": (note.get("title") or "").strip() or "小红书笔记",
        "desc": (note.get("desc") or note.get("content") or "").strip(),
        "author": (user.get("nickname") or user.get("name") or "").strip(),
        "note_id": note.get("noteId") or note.get("id") or "",
        "type": note_type,
        "images": images,
        "video_url": video_url or "",
    }


def resolve_note_url(url: str, cookie_header: str) -> str:
    """xhslink 短链 → 跟随跳转到 xiaohongshu.com 正文 URL。"""
    url = normalize_url(url)
    if "xhslink.com" not in url.lower():
        return url
    headers = {
        "User-Agent": UA,
        "Cookie": cookie_header,
        "Referer": "https://www.xiaohongshu.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    r = _HTTP.get(url, headers=headers, timeout=30, allow_redirects=True)
    r.raise_for_status()
    final = unquote(r.url)
    if "xiaohongshu.com" in final:
        return final
    raise ValueError(
        "短链未能打开笔记页。请在小红书 App 使用「分享→复制链接」（discovery/item 且含 xsec_token）。"
    )


def fetch_html(url: str, cookie_header: str) -> str:
    url = resolve_note_url(url, cookie_header)
    headers = {
        "User-Agent": UA,
        "Cookie": cookie_header,
        "Referer": "https://www.xiaohongshu.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    r = _HTTP.get(url, headers=headers, timeout=30, allow_redirects=True)
    r.raise_for_status()
    if len(r.text) < 500:
        raise ValueError("返回页面过短，可能被拦截")
    return r.text


def safe_filename(title: str, max_len: int = 70) -> str:
    t = re.sub(r'[\\/:*?"<>|]', "-", title).strip()
    return (t[:max_len] if t else "未命名") or "未命名"


def download_note_images(
    urls: list[str],
    vault: Path,
    note_id: str,
    cookie_header: str,
) -> list[str]:
    """下载配图到 vault，返回 Obsidian 相对路径列表（用于 ![[...]]）。"""
    if not urls:
        return []
    safe_id = re.sub(r"[^\w-]", "", note_id or "note")[:40] or "note"
    img_dir = vault / IMG_SUBDIR / safe_id
    img_dir.mkdir(parents=True, exist_ok=True)
    headers = {
        "User-Agent": UA,
        "Cookie": cookie_header,
        "Referer": "https://www.xiaohongshu.com/",
    }
    rel_paths: list[str] = []
    for i, url in enumerate(urls, 1):
        low = url.lower()
        if ".png" in low:
            ext = ".png"
        elif ".webp" in low:
            ext = ".webp"
        else:
            ext = ".jpg"
        dest = img_dir / f"{i:02d}{ext}"
        if not dest.is_file():
            r = _HTTP.get(url, headers=headers, timeout=90)
            r.raise_for_status()
            dest.write_bytes(r.content)
        rel_paths.append(dest.relative_to(vault).as_posix())
    return rel_paths


def format_image_embeds(paths: list[str]) -> str:
    if not paths:
        return ""
    lines = []
    for p in paths:
        if p.startswith("http"):
            lines.append(f"![]({p})")
        else:
            lines.append(f"![[{p}]]")
    if len(paths) > 1:
        header = f"## 配图（共 {len(paths)} 张）\n\n"
    else:
        header = "## 配图\n\n"
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
    video_policy: str = "transcript_only",
    transcript: str = "",
    transcript_status: str = "",
    local_video: str = "",
    default_projects: list[str] | None = None,
    local_images: list[str] | None = None,
) -> str:
    """
    video_policy:
      - transcript_only（默认）：笔记中不写 video_url / 播放器，仅 ## 转写
      - archive：影像学习类，保留 local_video（vault 内相对路径）
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    title = fields["title"]
    author = fields["author"]
    desc = fields["desc"]

    tags_yaml = "[]"
    note_type = fields.get("type") or ""
    embed_paths = local_images if local_images is not None else fields.get("images") or []
    img_lines = format_image_embeds(embed_paths)
    image_count = len(embed_paths)

    is_video = str(note_type).lower() == "video" or bool(fields.get("video_url"))
    summary_block = ""
    raw_block = ""
    if is_video:
        if transcript:
            summary_block = (
                "\n## 内容纪要\n\n"
                "（由 Cursor 根据「转写·原文」填写：去口语、分段、完整句；"
                "可用小标题；勿照抄 Whisper 口述稿。）\n"
            )
            raw_block = f"""
## 转写·原文

<details>
<summary>Whisper 口述稿（仅供参考，可折叠）</summary>

{transcript}

</details>
"""
        else:
            hint = transcript_status or (
                "（转写未完成。请安装 ffmpeg 与 faster-whisper，见 3.2 Workflow §二。）"
            )
            summary_block = f"\n## 内容纪要\n\n{hint}\n"

    archive_block = ""
    if video_policy == "archive" and local_video:
        archive_block = f"""
## 影像视频（本地存档）

![[{local_video}]]

"""

    policy_yaml = f'video_policy: "{video_policy}"\n'
    type_yaml = f'note_type: "{note_type}"\n' if note_type else ""
    image_count_yaml = (
        f"image_count: {image_count}\n" if image_count and not is_video else ""
    )
    local_yaml = ""
    if local_video:
        safe_lv = local_video.replace('"', "'")
        local_yaml = f'local_video: "{safe_lv}"\n'
    projects = default_projects or []
    project_yaml = _yaml_list("project", projects)

    body = f"""---
source: xiaohongshu
url: "{url}"
author: "{author}"
title: "{title.replace('"', "'")}"
{policy_yaml}{type_yaml}{image_count_yaml}{local_yaml}captured_at: {now}
status: inbox
tags: {tags_yaml}
{project_yaml}
ai_summary: ""
action: read_later
starred: true
fetcher: xhs-cookie-script
---

# {title}

> **@{author}** · [原文]({url})

## 要点

（由 Cursor 填写：视频 8～12 条；图文 6～8 条；有转写·原文则必填内容纪要。见 xhs-clipping.mdc）
{archive_block}{summary_block}{raw_block}
## 正文

{desc}

{img_lines}
"""
    filename = f"{date_prefix} {safe_filename(title)}.md"
    return filename, body


def main() -> int:
    parser = argparse.ArgumentParser(description="抓取小红书笔记到 Obsidian Clippings")
    parser.add_argument("--url", required=True, help="小红书帖子链接")
    parser.add_argument("--vault", default=str(DEFAULT_VAULT), help="Obsidian vault 根目录")
    parser.add_argument("--cookies", default=None, help="cookies.json 路径")
    parser.add_argument("--stdout", action="store_true", help="只打印 Markdown 不写文件")
    args = parser.parse_args()

    url = normalize_url(args.url)
    if "xiaohongshu" not in url and "xhslink" not in url:
        print("错误: 不是小红书链接", file=sys.stderr)
        return 2

    cookie_path = find_cookie_file(args.cookies)
    if not cookie_path:
        print(
            "错误: 未找到 Cookie 文件。\n"
            "请按 0 工作流/workflows/3.2 Workflow §2.6 导出 cookies 到:\n"
            f"  {Path.home() / 'cookies.json'}\n"
            f"  或 {Path(__file__).parent / 'xhs-cookies.json'}",
            file=sys.stderr,
        )
        return 3

    try:
        cookie_header, cookie_names = load_cookie_header(cookie_path)
        warn_missing_session(cookie_names)
        html = fetch_html(url, cookie_header)
        state = parse_initial_state(html)
        note_id = extract_note_id(url)
        note = deep_find_note(state, note_id)
        if not note:
            hint = ""
            if "xsec_token" not in url:
                hint = " 请改用 App「分享→复制链接」得到的**完整 URL**（通常含 xsec_token=）。"
            raise ValueError(
                "页面里没有笔记正文（SSR 为空或链接不完整）。" + hint
            )
        fields = extract_fields(note)
        vault_path = Path(args.vault).expanduser()
        nid = fields.get("note_id") or note_id or "note"
        local_images = download_note_images(
            fields["images"], vault_path, nid, cookie_header
        )
        filename, md = build_markdown(url, fields, local_images=local_images)
    except Exception as e:
        print(f"抓取失败: {e}", file=sys.stderr)
        return 1

    if args.stdout:
        print(md)
        return 0

    out_dir = Path(args.vault).expanduser() / OUT_SUBDIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    if out_path.exists():
        stem = out_path.stem + f"_{datetime.now().strftime('%H%M%S')}"
        out_path = out_dir / f"{stem}.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"OK: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
