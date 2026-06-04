#!/usr/bin/env python3
"""Register existing drop files into _imported_message_ids.txt (one-time / after bulk import)."""
from __future__ import annotations

import re
from pathlib import Path

# Reuse keys from fetch_qq_email
import fetch_qq_email as fe


def fallback_from_drop(text: str) -> str | None:
    m = re.match(r"(?s)^---\s*\n(.*?)\n---", text)
    if not m:
        return None
    fm = m.group(1)

    def field(name: str) -> str:
        hit = re.search(rf"(?m)^{name}:\s*(.+)$", fm)
        if not hit:
            return ""
        return hit.group(1).strip().strip('"').strip("'")

    from_addr = field("from")
    subject = field("subject")
    received = field("received_at")
    date_ymd = received[:10] if received else ""
    if not from_addr and not subject:
        return None
    return f"fallback:{from_addr}|{subject}|{date_ymd}"


def main() -> int:
    _, drop_dir = fe.find_vault_paths()
    ids = fe.load_imported_ids(drop_dir)
    added = 0
    for sub in ("", "_done", "_failed"):
        base = drop_dir / sub if sub else drop_dir
        if not base.is_dir():
            continue
        for path in base.glob("*.md"):
            if "template" in path.name.lower():
                continue
            text = path.read_text(encoding="utf-8")
            mid = fe.parse_message_id_from_drop(text)
            key = mid or fallback_from_drop(text)
            if not key or key in ids:
                continue
            fe.append_imported_id(drop_dir, key)
            ids.add(key)
            added += 1
    print(f"Register-EmailDrops: added={added} total={len(ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
