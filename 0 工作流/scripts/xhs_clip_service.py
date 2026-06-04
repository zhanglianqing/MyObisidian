#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iPhone 快捷指令 -> 队列 -> clip_xhs_auto

入队方式（二选一）：
  1. 坚果云：快捷指令把分享全文存为 Clippings/_Inbox/_xhs_queue/*.txt（推荐，免 Tailscale）
  2. 局域网 POST：http://<IP>:8765/clip（旧路径，可选）

  python xhs_clip_service.py              # HTTP + 队列轮询
  python xhs_clip_service.py --queue-only # 仅轮询队列（坚果云主路径）

首次运行生成 xhs-clip-token.txt（仅 HTTP 模式需要，勿提交 Git）。
"""

from __future__ import annotations

import argparse
import cgi
import json
import os
import shutil
import subprocess
import sys
import threading
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
from urllib.parse import parse_qs, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT = SCRIPT_DIR.parents[1]
TOKEN_FILE = SCRIPT_DIR / "xhs-clip-token.txt"
QUEUE_DIR = VAULT / "Clippings" / "_Inbox" / "_xhs_queue"
DONE_DIR = QUEUE_DIR / "_done"
FAILED_DIR = QUEUE_DIR / "_failed"
CLIP_PS1 = SCRIPT_DIR / "Clip-Xhs-Auto.ps1"
WECHAT_CLIP_PS1 = SCRIPT_DIR / "Clip-WeChat-Auto.ps1"
LOG_FILE = SCRIPT_DIR / "xhs-clip-receiver.log"

DEFAULT_PORT = 8765
POLL_SEC = 15
XHS_MARKERS = ("xiaohongshu.com", "xhslink.com")
WECHAT_MARKERS = ("mp.weixin.qq.com",)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_or_create_token() -> str:
    if TOKEN_FILE.is_file():
        return TOKEN_FILE.read_text(encoding="utf-8").strip()
    token = uuid.uuid4().hex
    TOKEN_FILE.write_text(token + "\n", encoding="utf-8")
    print(f"已生成令牌: {TOKEN_FILE}", flush=True)
    return token


def ensure_dirs() -> None:
    for d in (QUEUE_DIR, DONE_DIR, FAILED_DIR):
        d.mkdir(parents=True, exist_ok=True)


def append_log(line: str) -> None:
    try:
        with LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(f"[{utc_now()}] {line}\n")
    except OSError:
        pass


def _field_value(item: cgi.FieldStorage) -> str:
    val = item.value
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")
    return str(val or "")


def parse_post_body(content_type: str, raw: bytes) -> str:
    if not raw:
        return ""
    ctype = (content_type or "").split(";")[0].strip().lower()
    if ctype == "application/json":
        try:
            obj = json.loads(raw.decode("utf-8"))
            if isinstance(obj, str):
                return obj.strip()
            if isinstance(obj, dict):
                for key in ("text", "url", "content", "body", "input"):
                    val = obj.get(key)
                    if val:
                        return str(val).strip()
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    if ctype == "multipart/form-data":
        environ = {
            "REQUEST_METHOD": "POST",
            "CONTENT_TYPE": content_type,
            "CONTENT_LENGTH": str(len(raw)),
        }
        fs = cgi.FieldStorage(
            fp=BytesIO(raw), environ=environ, keep_blank_values=True
        )
        parts: list[str] = []
        for key in fs.keys():
            item = fs[key]
            if isinstance(item, list):
                for sub in item:
                    parts.append(_field_value(sub))
            else:
                parts.append(_field_value(item))
        return "\n".join(p for p in parts if p).strip()
    if ctype == "application/x-www-form-urlencoded":
        form = parse_qs(raw.decode("utf-8", errors="replace"), keep_blank_values=True)
        for key in ("text", "url", "content", "body"):
            if key in form and form[key]:
                return form[key][0].strip()
    return raw.decode("utf-8", errors="replace").strip()


def contains_xhs(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in XHS_MARKERS)


def contains_wechat(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in WECHAT_MARKERS)


def detect_clip_source(text: str) -> str:
    low = text.lower()
    if any(m in low for m in WECHAT_MARKERS):
        return "wechat"
    if any(m in low for m in XHS_MARKERS):
        return "xhs"
    return "xhs"


def list_pending_jobs() -> list[Path]:
    ensure_dirs()
    jobs = list(QUEUE_DIR.glob("*.json")) + list(QUEUE_DIR.glob("*.txt"))
    return sorted(jobs, key=lambda p: p.name)


def load_job(job_path: Path) -> dict:
    if job_path.suffix.lower() == ".json":
        job = json.loads(job_path.read_text(encoding="utf-8"))
        if not isinstance(job, dict):
            raise ValueError("job json must be an object")
        return job

    if job_path.suffix.lower() != ".txt":
        raise ValueError(f"unsupported queue file: {job_path.name}")

    raw = job_path.read_text(encoding="utf-8").strip()
    if not raw:
        raise ValueError("empty txt job")

    mode = "social"
    text = raw
    lines = raw.splitlines()
    if lines and lines[0].strip().lower().startswith("mode:"):
        mode = lines[0].split(":", 1)[1].strip().lower() or "social"
        text = "\n".join(lines[1:]).strip()
        if not text:
            raise ValueError("txt job has mode line but no share text")

    if mode not in ("social", "radiology"):
        mode = "social"

    return {
        "id": job_path.stem,
        "created": utc_now(),
        "mode": mode,
        "text": text,
        "source": "nutstore_txt",
    }


def enqueue(text: str, mode: str) -> Path:
    ensure_dirs()
    job_id = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}_{uuid.uuid4().hex[:8]}"
    job_path = QUEUE_DIR / f"{job_id}.json"
    payload = {
        "id": job_id,
        "created": utc_now(),
        "mode": mode,
        "text": text.strip(),
    }
    job_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return job_path


def run_clip(job: dict) -> tuple[int, str]:
    source = job.get("source") or detect_clip_source(job.get("text") or "")
    if source == "wechat":
        clip_ps1 = WECHAT_CLIP_PS1
        if not clip_ps1.is_file():
            return 1, f"未找到 {clip_ps1}"
        cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(clip_ps1),
            job["text"],
            "-VaultRoot",
            str(VAULT),
        ]
    else:
        clip_ps1 = CLIP_PS1
        if not clip_ps1.is_file():
            return 1, f"未找到 {clip_ps1}"
        cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(clip_ps1),
            job["text"],
            "-VaultRoot",
            str(VAULT),
            "-Mode",
            job.get("mode") or "social",
        ]
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        cmd,
        cwd=str(SCRIPT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def parse_clip_md_path(log: str) -> Path | None:
    for line in log.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
            fp = data.get("file")
            if fp:
                p = Path(fp)
                if p.is_file():
                    return p
        except json.JSONDecodeError:
            continue
    return None


def run_enrich(md_path: Path, mode: str) -> tuple[int, str]:
    enrich_py = SCRIPT_DIR / "enrich_xhs_clipping.py"
    if not enrich_py.is_file():
        return 0, "enrich script missing"
    proc = subprocess.run(
        [
            sys.executable,
            str(enrich_py),
            str(md_path),
            "--vault",
            str(VAULT),
            "--mode",
            mode,
        ],
        cwd=str(SCRIPT_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 2:
        return 0, "LLM not configured, skip enrich"
    if proc.returncode != 0:
        return 1, out.strip() or "enrich failed"
    return 0, out.strip() or f"enriched: {md_path.name}"


def process_one_job(job_path: Path) -> None:
    try:
        job = load_job(job_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        shutil.move(str(job_path), str(FAILED_DIR / job_path.name))
        (FAILED_DIR / f"{job_path.stem}.log").write_text(str(exc), encoding="utf-8")
        return

    code, log = run_clip(job)
    stamp = utc_now().replace(":", "-")
    if code == 0:
        dest = DONE_DIR / job_path.name
        shutil.move(str(job_path), str(dest))
        log_lines = [log] if log else []
        md_path = parse_clip_md_path(log or "")
        if md_path:
            ec, em = run_enrich(md_path, job.get("mode") or "social")
            log_lines.append(em)
            if ec != 0:
                append_log(f"enrich {job['id']} fail: {em}")
        if log_lines:
            (DONE_DIR / f"{job['id']}_{stamp}.log").write_text(
                "\n".join(log_lines), encoding="utf-8"
            )
    else:
        dest = FAILED_DIR / job_path.name
        shutil.move(str(job_path), str(dest))
        (FAILED_DIR / f"{job['id']}_{stamp}.log").write_text(
            f"exit={code}\n{log}", encoding="utf-8"
        )


def worker_loop(stop: threading.Event) -> None:
    while not stop.is_set():
        jobs = list_pending_jobs()
        for job_path in jobs:
            if stop.is_set():
                break
            process_one_job(job_path)
        stop.wait(POLL_SEC)


class ClipHandler(BaseHTTPRequestHandler):
    server_version = "XhsClipService/1.0"
    token: str = ""

    def parse_request(self) -> bool:
        if not super().parse_request():
            return False
        append_log(
            f"REQ {self.client_address[0]} {self.command} {self.path}"
        )
        return True

    def log_message(self, fmt: str, *args) -> None:
        print(f"[{utc_now()}] {self.address_string()} {fmt % args}", flush=True)

    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _unauthorized(self) -> None:
        self._json(401, {"ok": False, "error": "invalid token"})

    def _check_token(self) -> bool:
        got = self.headers.get("X-Clip-Token", "").strip()
        if not got:
            auth = self.headers.get("Authorization", "")
            if auth.lower().startswith("bearer "):
                got = auth[7:].strip()
        return got == self.token

    def do_GET(self) -> None:
        path = urlparse(self.path).path.rstrip("/") or "/"
        if path in ("/health", "/"):
            pending = len(list_pending_jobs()) if QUEUE_DIR.is_dir() else 0
            self._json(200, {"ok": True, "queue": pending, "service": "xhs_clip"})
            return
        if path == "/clip":
            self._json(
                200,
                {
                    "ok": True,
                    "hint": "Safari 仅用于测试请打开 /health；剪藏请用快捷指令 POST 本路径",
                    "post": "Header X-Clip-Token + form field text=分享全文",
                },
            )
            return
        self._json(404, {"ok": False, "error": "not found", "try": "/health"})

    def do_POST(self) -> None:
        client = self.client_address[0]
        ctype = self.headers.get("Content-Type", "")

        if not self._check_token():
            append_log(f"POST {client} 401 invalid token")
            self._unauthorized()
            return

        path = urlparse(self.path).path.rstrip("/") or "/"
        if path not in ("/clip", "/"):
            append_log(f"POST {client} 404 path={path!r}")
            self._json(
                404,
                {
                    "ok": False,
                    "error": "not found",
                    "path": path,
                    "use": "POST http://<ip>:8765/clip (no trailing slash)",
                },
            )
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length > 0 else b""
        text = parse_post_body(ctype, raw)
        if not text:
            append_log(
                f"POST {client} 400 empty body ctype={ctype!r} bytes={len(raw)}"
            )
            self._json(
                400,
                {
                    "ok": False,
                    "error": "empty body; use request body Text=Clipboard, not File",
                },
            )
            return

        qs = parse_qs(urlparse(self.path).query)
        mode = (qs.get("mode") or ["social"])[0].strip().lower()
        if mode not in ("social", "radiology"):
            mode = "social"

        if not contains_xhs(text):
            preview = text[:120].replace("\n", " ")
            append_log(
                f"POST {client} 400 no xhs marker ctype={ctype!r} preview={preview!r}"
            )
            self._json(
                400,
                {
                    "ok": False,
                    "error": "body must contain xiaohongshu.com or xhslink.com",
                    "preview": preview,
                },
            )
            return

        job_path = enqueue(text, mode)
        append_log(f"POST {client} 202 queued={job_path.name} mode={mode}")
        self._json(
            202,
            {
                "ok": True,
                "queued": job_path.name,
                "mode": mode,
                "message": "已入队，后台将自动抓取",
            },
        )


def local_ipv4_hint() -> str:
    try:
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


def process_queue_once() -> int:
    for job_path in list_pending_jobs():
        process_one_job(job_path)
    return 0


def main() -> int:
    global POLL_SEC

    parser = argparse.ArgumentParser(description="小红书剪藏：iPhone -> 局域网接收")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--poll", type=int, default=POLL_SEC, help="队列轮询秒数")
    parser.add_argument(
        "--process-once",
        action="store_true",
        help="处理队列中待办后退出（不启动 HTTP）",
    )
    parser.add_argument(
        "--queue-only",
        action="store_true",
        help="仅轮询坚果云/队列文件（不启动 HTTP，无需 token）",
    )
    args = parser.parse_args()

    if args.process_once:
        return process_queue_once()

    POLL_SEC = max(5, args.poll)
    ensure_dirs()

    if args.queue_only:
        print("=" * 60, flush=True)
        print(f"Vault: {VAULT}", flush=True)
        print(f"队列:  {QUEUE_DIR}", flush=True)
        print(f"模式:  仅轮询（坚果云 .txt / .json），每 {POLL_SEC}s", flush=True)
        print(f"日志:  {LOG_FILE}", flush=True)
        print("=" * 60, flush=True)
        stop = threading.Event()
        try:
            while not stop.is_set():
                jobs = list_pending_jobs()
                for job_path in jobs:
                    if stop.is_set():
                        break
                    process_one_job(job_path)
                    append_log(f"queue {job_path.name} processed")
                stop.wait(POLL_SEC)
        except KeyboardInterrupt:
            print("\n正在停止…", flush=True)
        return 0

    token = load_or_create_token()

    stop = threading.Event()
    worker = threading.Thread(target=worker_loop, args=(stop,), daemon=True)
    worker.start()

    ClipHandler.token = token
    httpd = ThreadingHTTPServer((args.host, args.port), ClipHandler)

    ip = local_ipv4_hint()
    print("=" * 60, flush=True)
    print(f"Vault: {VAULT}", flush=True)
    print(f"队列:  {QUEUE_DIR}", flush=True)
    print(f"监听:  http://{ip}:{args.port}/clip", flush=True)
    print(f"健康:  http://{ip}:{args.port}/health", flush=True)
    print(f"令牌:  {TOKEN_FILE.name}（Header: X-Clip-Token）", flush=True)
    print(f"日志:  {LOG_FILE}", flush=True)
    print("=" * 60, flush=True)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n正在停止…", flush=True)
        stop.set()
        httpd.shutdown()
        worker.join(timeout=3)
    return 0


if __name__ == "__main__":
    sys.exit(main())
