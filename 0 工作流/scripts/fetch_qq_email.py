#!/usr/bin/env python3
"""Fetch QQ mailbox via IMAP into vault _email_drop/. Credentials via env only."""
from __future__ import annotations

import argparse
import email
import imaplib
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from email.header import decode_header
from email.utils import parsedate_to_datetime
from pathlib import Path


QQ_IMAP_HOST = "imap.qq.com"
QQ_IMAP_PORT = 993
BJ = timezone(timedelta(hours=8))
ENV_FILE_NAME = ".qq_mail_imap.env"
IMPORTED_IDS_NAME = "_imported_message_ids.txt"


def load_credentials() -> tuple[str, str]:
    user = os.environ.get("QQ_MAIL_USER", "").strip()
    password = os.environ.get("QQ_MAIL_IMAP_PASSWORD", "").strip()
    if user and password:
        return user, password

    env_path = Path.home() / ENV_FILE_NAME
    if not env_path.is_file():
        return "", ""

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key == "QQ_MAIL_USER":
            user = val
        elif key == "QQ_MAIL_IMAP_PASSWORD":
            password = val
    return user.strip(), password.strip()


def decode_mime_header(value: str | None) -> str:
    if not value:
        return ""
    parts = []
    for frag, enc in decode_header(value):
        if isinstance(frag, bytes):
            parts.append(frag.decode(enc or "utf-8", errors="replace"))
        else:
            parts.append(str(frag))
    return "".join(parts).strip()


def sanitize_filename(text: str, max_len: int = 30) -> str:
    text = re.sub(r'[<>:"/\\|?*]', "", text)
    text = re.sub(r"\s+", "-", text.strip())
    if len(text) > max_len:
        text = text[:max_len]
    return text or "no-subject"


def find_vault_paths() -> tuple[Path, Path]:
    script_dir = Path(__file__).resolve().parent
    workflow_dir = script_dir.parent
    drop_dir = workflow_dir / "_email_drop"
    drop_dir.mkdir(parents=True, exist_ok=True)
    (drop_dir / "_done").mkdir(exist_ok=True)
    (drop_dir / "_failed").mkdir(exist_ok=True)
    return workflow_dir, drop_dir


def fallback_key_from_msg(msg: email.message.Message) -> str:
    from_addr = decode_mime_header(msg.get("From"))
    subject = decode_mime_header(msg.get("Subject"))
    date_hdr = msg.get("Date")
    date_ymd = ""
    if date_hdr:
        try:
            dt = parsedate_to_datetime(date_hdr)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=BJ)
            else:
                dt = dt.astimezone(BJ)
            date_ymd = dt.strftime("%Y-%m-%d")
        except (TypeError, ValueError):
            pass
    return f"fallback:{from_addr}|{subject}|{date_ymd}"


def normalize_message_id(msg: email.message.Message) -> str:
    mid = (msg.get("Message-ID") or "").strip()
    if mid:
        return mid
    return fallback_key_from_msg(msg)


def parse_message_id_from_drop(text: str) -> str | None:
    m = re.match(r"(?s)^---\s*\n(.*?)\n---", text)
    if not m:
        return None
    fm = m.group(1)
    hit = re.search(r"(?m)^message_id:\s*(.+)$", fm)
    if hit:
        return hit.group(1).strip().strip('"').strip("'")

    def field(name: str) -> str:
        h = re.search(rf"(?m)^{name}:\s*(.+)$", fm)
        return h.group(1).strip().strip('"').strip("'") if h else ""

    from_addr = field("from")
    subject = field("subject")
    received = field("received_at")
    date_ymd = received[:10] if received else ""
    if from_addr or subject:
        return f"fallback:{from_addr}|{subject}|{date_ymd}"
    return None


def load_imported_ids(drop_dir: Path) -> set[str]:
    ids: set[str] = set()
    manifest = drop_dir / IMPORTED_IDS_NAME
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                ids.add(line)

    for sub in ("", "_done", "_failed"):
        base = drop_dir / sub if sub else drop_dir
        if not base.is_dir():
            continue
        for path in base.glob("*.md"):
            if path.name in ("README.md",) or "template" in path.name.lower():
                continue
            try:
                mid = parse_message_id_from_drop(path.read_text(encoding="utf-8"))
            except OSError:
                continue
            if mid:
                ids.add(mid)
    return ids


def append_imported_id(drop_dir: Path, message_id: str) -> None:
    manifest = drop_dir / IMPORTED_IDS_NAME
    with manifest.open("a", encoding="utf-8") as f:
        f.write(message_id + "\n")


def message_to_drop(
    uid: bytes,
    raw: bytes,
    drop_dir: Path,
    imported_ids: set[str],
) -> tuple[Path | None, str | None]:
    msg = email.message_from_bytes(raw)
    message_id = normalize_message_id(msg)
    fallback = fallback_key_from_msg(msg)
    if message_id in imported_ids or fallback in imported_ids:
        return None, message_id

    subject = decode_mime_header(msg.get("Subject"))
    from_addr = decode_mime_header(msg.get("From"))
    date_hdr = msg.get("Date")
    try:
        dt = parsedate_to_datetime(date_hdr) if date_hdr else datetime.now(BJ)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=BJ)
        else:
            dt = dt.astimezone(BJ)
    except (TypeError, ValueError):
        dt = datetime.now(BJ)
    received_at = dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")

    body_parts: list[str] = []
    attachments: list[str] = []
    if msg.is_multipart():
        for part in msg.walk():
            cd = str(part.get("Content-Disposition") or "")
            if "attachment" in cd.lower():
                fn = part.get_filename()
                if fn:
                    attachments.append(decode_mime_header(fn))
                continue
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    body_parts.append(payload.decode(charset, errors="replace"))
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            body_parts.append(payload.decode(charset, errors="replace"))

    body = "\n".join(body_parts).strip()
    if not body:
        body = "(empty body)"

    stamp = dt.strftime("%Y%m%d-%H%M%S")
    slug = sanitize_filename(subject)
    out_name = f"{stamp}-{slug}.md"
    out_path = drop_dir / out_name
    if out_path.exists():
        out_name = f"{stamp}-{slug}-{uid.decode(errors='ignore')[:6]}.md"
        out_path = drop_dir / out_name

    uid_str = uid.decode(errors="ignore")
    mid_esc = message_id.replace('"', "'")
    att_line = "; ".join(attachments) if attachments else ""
    fm = (
        "---\n"
        f'from: "{from_addr.replace(chr(34), chr(39))}"\n'
        f'subject: "{subject.replace(chr(34), chr(39))}"\n'
        f"received_at: {received_at}\n"
        "source: qq-imap\n"
        f'message_id: "{mid_esc}"\n'
        f"imap_uid: {uid_str}\n"
    )
    if att_line:
        fm += f'attachments: "{att_line.replace(chr(34), chr(39))}"\n'
    fm += "---\n\n"
    out_path.write_text(fm + body, encoding="utf-8")
    imported_ids.add(message_id)
    append_imported_id(drop_dir, message_id)
    if fallback != message_id:
        imported_ids.add(fallback)
        append_imported_id(drop_dir, fallback)
    return out_path, message_id


def mark_uid_seen(mail: imaplib.IMAP4_SSL, uid: bytes) -> None:
    try:
        mail.uid("STORE", uid, "+FLAGS", "(\\Seen)")
    except imaplib.IMAP4.error:
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch QQ mail into _email_drop")
    parser.add_argument("--max-count", type=int, default=20, dest="max_count")
    parser.add_argument("--since-days", type=int, default=7, dest="since_days")
    parser.add_argument("--unread-only", action="store_true", default=True)
    parser.add_argument("--all", action="store_true", help="Include read mail")
    parser.add_argument(
        "--mark-seen",
        action="store_true",
        default=True,
        help="Mark imported messages as Seen on server (default: on)",
    )
    parser.add_argument(
        "--no-mark-seen",
        action="store_true",
        help="Do not mark as read on QQ after import",
    )
    args = parser.parse_args()
    unread_only = args.unread_only and not args.all
    mark_seen = args.mark_seen and not args.no_mark_seen

    user, password = load_credentials()
    if not user or not password:
        env_path = Path.home() / ENV_FILE_NAME
        print(
            "Fetch-QQEmail: set QQ_MAIL_USER and QQ_MAIL_IMAP_PASSWORD, or create",
            env_path,
            file=sys.stderr,
        )
        return 2

    _, drop_dir = find_vault_paths()
    imported_ids = load_imported_ids(drop_dir)
    since = datetime.now(BJ) - timedelta(days=args.since_days)
    since_str = since.strftime("%d-%b-%Y")

    written = 0
    skipped = 0
    marked = 0
    try:
        mail = imaplib.IMAP4_SSL(QQ_IMAP_HOST, QQ_IMAP_PORT)
        mail.login(user, password)
        mail.select("INBOX")

        criteria = f'(SINCE "{since_str}")'
        if unread_only:
            criteria = f'(UNSEEN SINCE "{since_str}")'

        typ, data = mail.uid("search", None, criteria)
        if typ != "OK":
            print("Fetch-QQEmail: search failed", file=sys.stderr)
            return 1

        uids = data[0].split()
        if not uids:
            print("Fetch-QQEmail: fetched=0 skipped=0 marked=0")
            return 0

        uids = uids[-args.max_count :]
        for uid in reversed(uids):
            typ, msg_data = mail.uid("fetch", uid, "(RFC822)")
            if typ != "OK" or not msg_data or not msg_data[0]:
                continue
            raw = msg_data[0][1]
            out_path, mid = message_to_drop(uid, raw, drop_dir, imported_ids)
            if out_path is None:
                skipped += 1
                if mark_seen and mid:
                    mark_uid_seen(mail, uid)
                    marked += 1
                continue
            written += 1
            if mark_seen:
                mark_uid_seen(mail, uid)
                marked += 1

        mail.logout()
    except imaplib.IMAP4.error as e:
        print(f"Fetch-QQEmail: IMAP error: {e}", file=sys.stderr)
        return 1

    print(f"Fetch-QQEmail: fetched={written} skipped={skipped} marked={marked}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
