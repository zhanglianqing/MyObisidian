#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从小红书视频直链提取语音并转写（临时下载，默认不保留 mp4）。

依赖（一次性）:
  pip install requests faster-whisper
  ffmpeg 在 PATH 中（Windows: winget install ffmpeg）

用法:
  python transcribe_xhs_video.py --url "https://sns-video-v3.xhscdn.com/..."
  python transcribe_xhs_video.py --url "..." --save "E:/vault/Clippings/Xiaohongshu/_assets/note.mp4"
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# 国内下载 Whisper 模型（可在系统环境变量中覆盖 HF_ENDPOINT）
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
# Anaconda + faster-whisper 常见 OpenMP 冲突
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

try:
    import requests
except ImportError:
    print("请先: pip install requests", file=sys.stderr)
    sys.exit(1)

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def _http_get(url: str, **kwargs):
    """直连 CDN，绕过 Windows 系统代理（见 fetch_xhs_note._http_session）。"""
    s = requests.Session()
    s.trust_env = False
    return s.get(url, **kwargs)


def _resolve_ffmpeg() -> str:
    """PATH 或 WinGet 便携目录（后台服务/计划任务常只有后者）。"""
    found = shutil.which("ffmpeg")
    if found:
        return found
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    winget_root = local / "Microsoft" / "WinGet" / "Packages"
    if winget_root.is_dir():
        for pkg in sorted(winget_root.glob("Gyan.FFmpeg_*")):
            for exe in pkg.rglob("ffmpeg.exe"):
                return str(exe)
    return ""


def download_video(url: str, dest: Path, cookie_header: str | None = None) -> None:
    headers = {
        "User-Agent": UA,
        "Referer": "https://www.xiaohongshu.com/",
    }
    if cookie_header:
        headers["Cookie"] = cookie_header
    with _http_get(url, headers=headers, stream=True, timeout=120) as r:
        r.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
    if dest.stat().st_size < 1024:
        raise ValueError("下载的视频文件过小，可能链接已失效")


def extract_audio_wav(video_path: Path, wav_path: Path) -> None:
    ffmpeg = _resolve_ffmpeg()
    if not ffmpeg:
        raise RuntimeError(
            "未找到 ffmpeg。请安装后加入 PATH，例如: winget install Gyan.FFmpeg；"
            "安装后请重启剪藏服务（计划任务 XhsClipService）。"
        )
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(wav_path),
    ]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        tail = (proc.stderr or "")[-500:]
        raise RuntimeError(f"ffmpeg 提取音频失败: {tail}")


def transcribe_wav(wav_path: Path, model_size: str = "small") -> str:
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise RuntimeError(
            "未安装 faster-whisper。请运行: pip install faster-whisper"
        ) from e

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(
        str(wav_path),
        language="zh",
        vad_filter=True,
    )
    lines = [seg.text.strip() for seg in segments if seg.text.strip()]
    text = "\n".join(lines).strip()
    if not text:
        raise ValueError("转写结果为空（可能为纯音乐/无声视频）")
    return text


def process_video(
    video_url: str,
    cookie_header: str | None = None,
    *,
    save_path: Path | None = None,
    model_size: str = "small",
) -> str:
    """
    下载 → 转写 → 可选保留 mp4 到 save_path。
    不保留时删除临时视频与音频。
    """
    with tempfile.TemporaryDirectory(prefix="xhs_vid_") as tmp:
        tmp_dir = Path(tmp)
        video_tmp = tmp_dir / "note.mp4"
        wav_path = tmp_dir / "audio.wav"

        download_video(video_url, video_tmp, cookie_header)

        if save_path:
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(video_tmp, save_path)

        extract_audio_wav(video_tmp, wav_path)
        return transcribe_wav(wav_path, model_size=model_size)


def main() -> int:
    parser = argparse.ArgumentParser(description="小红书视频 URL → 中文转写")
    parser.add_argument("--url", required=True)
    parser.add_argument("--save", default="", help="若指定则保留 mp4 到该路径")
    parser.add_argument("--model", default="small", help="faster-whisper 模型名")
    args = parser.parse_args()

    save = Path(args.save).expanduser() if args.save else None
    try:
        text = process_video(args.url, save_path=save, model_size=args.model)
        print(text)
        return 0
    except Exception as e:
        print(f"转写失败: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
