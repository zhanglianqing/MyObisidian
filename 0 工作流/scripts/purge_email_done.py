#!/usr/bin/env python3
"""Delete old files under _email_drop/_done/ to avoid vault bloat."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

BJ = timezone(timedelta(hours=8))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=14, help="Delete if older than N days")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    done_dir = script_dir.parent / "_email_drop" / "_done"
    if not done_dir.is_dir():
        print("Purge-EmailDropDone: _done not found")
        return 0

    cutoff = datetime.now(BJ) - timedelta(days=args.days)
    removed = 0
    for path in done_dir.glob("*.md"):
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=BJ)
        if mtime >= cutoff:
            continue
        if args.dry_run:
            print(f"would delete: {path.name}")
        else:
            path.unlink()
        removed += 1

    verb = "would_remove" if args.dry_run else "removed"
    print(f"Purge-EmailDropDone: {verb}={removed} (older_than_days={args.days})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
