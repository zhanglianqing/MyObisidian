#!/usr/bin/env python3
"""Refresh 邮件待整理队列.md index from _email_drop pending files."""
from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


def parse_frontmatter_field(text: str, field: str) -> str | None:
    m = re.match(r"(?s)^---\s*\n(.*?)\n---", text)
    if not m:
        return None
    fm = m.group(1)
    pat = re.compile(rf"^{re.escape(field)}:\s*(.+)$", re.MULTILINE)
    hit = pat.search(fm)
    if not hit:
        return None
    val = hit.group(1).strip().strip('"').strip("'")
    return val


def row_from_file(path: Path, rel_prefix: str, pilot: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    received = parse_frontmatter_field(text, "received_at") or "-"
    from_addr = parse_frontmatter_field(text, "from") or "-"
    subject = parse_frontmatter_field(text, "subject") or path.stem
    subject = re.sub(r"\s+", " ", subject.replace("|", "/"))
    if len(subject) > 60:
        subject = subject[:57] + "..."
    if pilot:
        subject += " (pilot)"
    rel = f"{rel_prefix}/{path.name}".replace("\\", "/")
    return f"| {received} | {from_addr} | {subject} | [[0 工作流/{rel}]] |"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-pilot", action="store_true")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    workflow_dir = script_dir.parent
    drop_dir = workflow_dir / "_email_drop"
    queue_path = workflow_dir / "邮件待整理队列.md"

    rows: list[str] = []
    for f in sorted(drop_dir.glob("*.md")):
        if f.name in ("README.md",) or "template" in f.name.lower():
            continue
        rows.append(row_from_file(f, "_email_drop"))

    if args.include_pilot:
        pilot_dir = drop_dir / "_pilot"
        if pilot_dir.is_dir():
            for f in sorted(pilot_dir.glob("*.md")):
                rows.append(row_from_file(f, "_email_drop/_pilot", pilot=True))

    table_body = "\n".join(rows) if rows else "| - | - | (no pending drop) | - |"
    today = date.today().isoformat()

    content = f"""---
type: email-queue
updated: {today}
---

# 邮件待整理队列

> 由 `Merge-EmailDrop.ps1` / `merge_email_drop.py` 从 [[0 工作流/_email_drop/README]] 刷新。整理用 Cursor：`邮件整理`。  
> 主文档：[[0 工作流/workflows/3.7 Workflow ：QQ 邮件筛选入库#定稿摘要（调用入口）]]

## 待处理

| 收到时间 | 发件人 | 主题 | drop 文件 |
|----------|--------|------|-----------|
{table_body}

## 说明

- 本页**仅索引**，正文在 `_email_drop/` 各 `.md` 中（勿在文件树逐封浏览）。
- **整理确认后：直接删除**对应 drop（不必移 `_done/`）。
- Phase 2：`Fetch-QQEmail.ps1` 拉取的新邮件也会出现在上表。
"""
    queue_path.write_text(content, encoding="utf-8")
    pilot_n = sum(1 for r in rows if "(pilot)" in r)
    print(f"Merge-EmailDrop: indexed={len(rows)} (pilot={pilot_n})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
