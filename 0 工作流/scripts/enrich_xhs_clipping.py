#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪藏笔记 LLM 自动归类（默认 Gemini 多模态，适合小红书图文/视频转写）

配置: 复制 xhs-llm.example.json → xhs-llm.json
环境变量: GEMINI_API_KEY 或 GOOGLE_API_KEY 或 XHS_LLM_API_KEY
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("请先: pip install requests", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT = SCRIPT_DIR.parents[1]
CONFIG_FILE = SCRIPT_DIR / "xhs-llm.json"
GEMINI_API_ROOT = "https://generativelanguage.googleapis.com/v1beta"

SOCIAL_PROJECTS = [
    "[[00 工作系统3.0：海马+抑郁症+认知损伤的机制及诊疗]]",
    "[[临床医学知识库]]",
    "[[5 分支项目/5.1 眉彡/00_ResearchTrack]]",
    "7 可复用知识库",
    "[[日常随想]]",
]


def load_config() -> dict:
    cfg: dict = {}
    if CONFIG_FILE.is_file():
        cfg.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
    cfg.pop("_comment", None)
    cfg["api_key"] = (
        os.environ.get("GEMINI_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
        or os.environ.get("XHS_LLM_API_KEY")
        or cfg.get("api_key")
        or ""
    )
    cfg["provider"] = (cfg.get("provider") or "gemini").strip().lower()
    cfg["api_base"] = (os.environ.get("XHS_LLM_API_BASE") or cfg.get("api_base") or "").rstrip("/")
    cfg["model"] = os.environ.get("XHS_LLM_MODEL") or cfg.get("model") or "gemini-2.0-flash"
    cfg["vision_model"] = (cfg.get("vision_model") or cfg["model"]).strip()
    cfg["max_images"] = int(cfg.get("max_images") or 12)
    cfg["timeout_sec"] = int(cfg.get("timeout_sec") or 180)
    cfg["retries"] = int(cfg.get("retries") or 3)
    return cfg


def is_configured() -> bool:
    return bool(load_config().get("api_key"))


def split_note(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return "", text
    return parts[1].strip(), parts[2].lstrip("\n")


def parse_simple_yaml(fm: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in fm.splitlines():
        if ":" in line and not line.strip().startswith("-"):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def extract_section(body: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    return m.group(1).strip() if m else ""


def extract_wiki_images(body: str, vault: Path) -> list[Path]:
    out: list[Path] = []
    for m in re.finditer(r"!\[\[([^\]]+)\]\]", body):
        p = vault / m.group(1).strip()
        if p.is_file():
            out.append(p)
    return out


def read_transcript(body: str) -> str:
    m = re.search(
        r"<details>.*?<summary>.*?</summary>\s*(.*?)\s*</details>", body, re.S | re.I
    )
    return m.group(1).strip() if m else ""


def build_prompt(meta: dict[str, str], body: str, *, mode: str, with_images: bool) -> str:
    zhengwen = extract_section(body, "正文")
    transcript = read_transcript(body)
    lines = [
        f"标题: {meta.get('title', '')}",
        f"作者: {meta.get('author', '')}",
        f"模式: {mode}",
        f"配图数: {meta.get('image_count', '')}",
        f"有转写: {'是' if transcript else '否'}",
        "",
        "## 正文",
        zhengwen or "（无文字，信息可能在配图）",
    ]
    if transcript:
        lines += ["", "## 转写·原文（节选）", transcript[:12000]]
    if with_images:
        lines.append("\n请阅读所附配图，把图中书单、表格、步骤等写进要点。")
    lines += [
        "",
        "只输出 JSON，字段:",
        '{"ai_summary":"≤80字","tags":["≤3个"],"action":"read_later",',
        f'"projects":[],  // social 从 {SOCIAL_PROJECTS} 选0~2；radiology 含[[临床医学知识库]]',
        '"points":["图文6~8条或视频8~12条完整句"],"content_summary":"有转写则填否则""}',
        "禁止笼统话；图中可见的书名、年龄段、分级须写入要点。",
    ]
    return "\n".join(lines)


def image_inline_part(path: Path) -> dict:
    ext = path.suffix.lower()
    mime = {".png": "image/png", ".webp": "image/webp"}.get(ext, "image/jpeg")
    data = base64.standard_b64encode(path.read_bytes()).decode("ascii")
    return {"inline_data": {"mime_type": mime, "data": data}}


def image_data_url(path: Path) -> str:
    ext = path.suffix.lower()
    mime = {".png": "image/png", ".webp": "image/webp"}.get(ext, "image/jpeg")
    b64 = base64.standard_b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _request_with_retry(fn, cfg: dict):
    last: Exception | None = None
    for attempt in range(cfg["retries"]):
        try:
            return fn()
        except (requests.Timeout, requests.ConnectionError) as exc:
            last = exc
            if attempt + 1 < cfg["retries"]:
                time.sleep(2**attempt)
    raise RuntimeError(f"网络超时或无法连接（已重试 {cfg['retries']} 次）: {last}") from last


def chat_gemini_native(
    cfg: dict,
    *,
    system: str,
    user_text: str,
    image_paths: list[Path],
    model: str,
) -> str:
    parts: list[dict] = [{"text": user_text}]
    for p in image_paths[: cfg["max_images"]]:
        parts.append(image_inline_part(p))

    url = f"{GEMINI_API_ROOT}/models/{model}:generateContent"
    payload = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json",
        },
    }

    def do():
        r = requests.post(
            url,
            params={"key": cfg["api_key"]},
            json=payload,
            timeout=cfg["timeout_sec"],
        )
        if r.status_code >= 400:
            raise RuntimeError(f"Gemini API {r.status_code}: {r.text[:500]}")
        data = r.json()
        cands = data.get("candidates") or []
        if not cands:
            raise RuntimeError(f"Gemini 无返回: {json.dumps(data, ensure_ascii=False)[:500]}")
        out_parts = cands[0].get("content", {}).get("parts") or []
        texts = [p.get("text", "") for p in out_parts if p.get("text")]
        if not texts:
            raise RuntimeError("Gemini 返回空文本")
        return "".join(texts)

    return _request_with_retry(do, cfg)


def chat_openai_compat(
    cfg: dict,
    messages: list,
    model: str,
) -> str:
    base = cfg["api_base"] or f"{GEMINI_API_ROOT}/openai"

    def do():
        r = requests.post(
            f"{base}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {cfg['api_key']}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.3,
                "response_format": {"type": "json_object"},
            },
            timeout=cfg["timeout_sec"],
        )
        if r.status_code >= 400:
            raise RuntimeError(f"API {r.status_code}: {r.text[:500]}")
        return r.json()["choices"][0]["message"]["content"]

    return _request_with_retry(do, cfg)


def llm_complete(
    cfg: dict,
    *,
    system: str,
    user_text: str,
    image_paths: list[Path],
    model: str,
) -> str:
    provider = cfg["provider"]
    if provider in ("openai_compat", "openai", "deepseek"):
        if image_paths:
            content: list[dict] = [{"type": "text", "text": user_text}]
            for p in image_paths[: cfg["max_images"]]:
                content.append(
                    {"type": "image_url", "image_url": {"url": image_data_url(p)}}
                )
            user_msg = {"role": "user", "content": content}
        else:
            user_msg = {"role": "user", "content": user_text}
        return chat_openai_compat(
            cfg,
            [{"role": "system", "content": system}, user_msg],
            model,
        )
    return chat_gemini_native(
        cfg, system=system, user_text=user_text, image_paths=image_paths, model=model
    )


def parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```\w*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    return json.loads(text)


def rewrite_frontmatter(fm: str, result: dict, mode: str) -> str:
    tags = [str(t) for t in (result.get("tags") or [])[:3]]
    projects = [str(p) for p in (result.get("projects") or [])[:2]]
    if mode == "radiology" and "[[临床医学知识库]]" not in projects:
        projects = ["[[临床医学知识库]]"] + projects[:1]
    summary = str(result.get("ai_summary") or "").replace('"', "'")[:80]
    action = str(result.get("action") or "read_later")

    skip = {"tags", "project", "ai_summary", "status", "action"}
    lines: list[str] = []
    for line in fm.splitlines():
        key = line.split(":", 1)[0].strip() if ":" in line else ""
        if key in skip:
            continue
        lines.append(line)
    lines.append("status: classified")
    lines.append(f'ai_summary: "{summary}"')
    lines.append(f"action: {action}")
    if tags:
        lines.append("tags:")
        for t in tags:
            lines.append(f'  - "{t}"')
    else:
        lines.append("tags: []")
    if projects:
        lines.append("project:")
        for p in projects:
            lines.append(f'  - "{p}"')
    else:
        lines.append("project: []")
    return "\n".join(lines)


def apply_body(body: str, result: dict, has_transcript: bool) -> str:
    points = [str(p) for p in (result.get("points") or []) if str(p).strip()]
    pts = "\n".join(f"- {p}" for p in points)
    body = re.sub(
        r"^## 要点\s*\n.*?(?=^## |\Z)",
        f"## 要点\n\n{pts}\n\n",
        body,
        count=1,
        flags=re.M | re.S,
    )
    summary = (result.get("content_summary") or "").strip()
    if has_transcript and summary:
        if re.search(r"^## 内容纪要\s*$", body, re.M):
            body = re.sub(
                r"^## 内容纪要\s*\n.*?(?=^## |\Z)",
                f"## 内容纪要\n\n{summary}\n\n",
                body,
                count=1,
                flags=re.M | re.S,
            )
        else:
            idx = body.find("## 正文")
            block = f"## 内容纪要\n\n{summary}\n\n"
            body = body[:idx] + block + body[idx:] if idx >= 0 else block + body
    return body


def enrich_file(md_path: Path, *, vault: Path, mode: str = "social") -> None:
    cfg = load_config()
    if not cfg["api_key"]:
        raise RuntimeError("未配置 xhs-llm.json 或 GEMINI_API_KEY")

    text = md_path.read_text(encoding="utf-8")
    fm, body = split_note(text)
    meta = parse_simple_yaml(fm)
    points_sec = extract_section(body, "要点")
    if meta.get("status") == "classified" and "由 Cursor 填写" not in points_sec:
        return

    images = extract_wiki_images(body, vault)
    transcript = read_transcript(body)
    is_video = meta.get("note_type") == "video" or bool(transcript)

    # 图文/多图：走视觉；纯视频有转写：主要读转写文本
    use_images = bool(images) and not (is_video and transcript and len(images) <= 1)
    image_paths = images if use_images else []
    model = cfg["vision_model"] if image_paths else cfg["model"]

    prompt = build_prompt(meta, body, mode=mode, with_images=bool(image_paths))
    source = meta.get("source") or "xiaohongshu"
    system = (
        "你是 Obsidian 剪藏归类助手。根据剪藏笔记（含配图与转写）输出 JSON。"
        f"来源类型: {source}。要点用中文完整句，不编造正文中不存在的信息。"
    )

    raw = llm_complete(
        cfg,
        system=system,
        user_text=prompt,
        image_paths=image_paths,
        model=model,
    )
    result = parse_json(raw)
    fm_new = rewrite_frontmatter(fm, result, mode)
    body_new = apply_body(body, result, bool(transcript))
    md_path.write_text(f"---\n{fm_new}\n---\n{body_new}", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?")
    ap.add_argument("--vault", default=str(VAULT))
    ap.add_argument("--mode", choices=("social", "radiology"), default="social")
    ap.add_argument("--inbox", action="store_true")
    ap.add_argument("--force", action="store_true", help="已 classified 也重新生成")
    args = ap.parse_args()
    vault = Path(args.vault).resolve()

    if not is_configured():
        print("未配置 LLM，跳过", file=sys.stderr)
        return 2

    paths: list[Path] = []
    if args.inbox:
        inbox = vault / "Clippings" / "Xiaohongshu" / "_Inbox"
        paths = [
            p
            for p in sorted(inbox.glob("*.md"))
            if p.name.lower() != "readme.md"
        ]
    elif args.path:
        paths = [Path(args.path)]
        if not paths[0].is_absolute():
            paths[0] = (vault / paths[0]).resolve()
    else:
        ap.error("需要 path 或 --inbox")

    n = 0
    for p in paths:
        try:
            if args.force:
                text = p.read_text(encoding="utf-8")
                fm, body = split_note(text)
                fm = re.sub(r"status:\s*classified", "status: inbox", fm)
                p.write_text(f"---\n{fm}\n---\n{body}", encoding="utf-8")
            enrich_file(p, vault=vault, mode=args.mode)
            print(f"OK: {p}")
            n += 1
        except Exception as e:
            print(f"FAIL: {p}: {e}", file=sys.stderr)
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
