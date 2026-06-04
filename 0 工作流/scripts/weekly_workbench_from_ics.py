#!/usr/bin/env python3
"""Pull hospital shift ICS and print §一 rows for [[本周工作台]].

Usage:
  python weekly_workbench_from_ics.py --week 2026-05-18 --markdown

Markdown output columns (paste into §一):
  不可用时段 | 预计可用时段 | 带娃 / 火山
  (ICS 班表 → 不可用时段；会议/出行等固定占用需手填)
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
DATA_JSON = VAULT / ".obsidian/plugins/obsidian-full-calendar/data.json"
WEEKDAYS = "一二三四五六日"
KID_DEFAULT = "20–21 带读"
KID_NONE = "—"
DAY_PLAN_START = time(7, 0)
DAY_PLAN_END = time(23, 0)


@dataclass
class Slot:
    start: datetime
    end: datetime
    label: str
    event_start: date  # ICS 事件开始日，用于不可用时段列（不含昨日夜班延续）


def monday_of_week(d: date) -> date:
    return d - timedelta(days=d.weekday())


def load_url() -> str:
    text = DATA_JSON.read_text(encoding="utf-8")
    m = re.search(r'"url":\s*"([^"]+)"', text)
    if not m:
        raise SystemExit(f"No calendar URL in {DATA_JSON}")
    return m.group(1)


def parse_dt(raw: str) -> datetime:
    raw = raw.strip().replace("Z", "")
    if "T" in raw:
        return datetime.strptime(raw[:15], "%Y%m%dT%H%M%S")
    return datetime.strptime(raw[:8], "%Y%m%d")


def classify_slot(start: datetime, end: datetime, summary: str) -> str:
    if "补休" in summary:
        return "补休"
    if "MR13" in summary:
        return "7T"
    h = start.hour
    if "值班" in summary or h >= 22 or (h >= 18 and end.date() > start.date()):
        return "夜班"
    if h >= 18:
        return "晚班"
    if h >= 12 or "体检" in summary:
        return "下午班"
    if h >= 6:
        return "早班"
    return "晚班"


def fetch_events(ics: str) -> list[tuple[datetime, datetime, str]]:
    out: list[tuple[datetime, datetime, str]] = []
    for block in ics.split("BEGIN:VEVENT")[1:]:
        def field(name: str) -> str:
            m = re.search(rf"^{name}(?:;[^:]*)?:(.*)$", block, re.M)
            return m.group(1).strip() if m else ""

        summary = field("SUMMARY")
        if not summary:
            continue
        try:
            start = parse_dt(field("DTSTART"))
            end_raw = field("DTEND")
            end = parse_dt(end_raw) if end_raw else start + timedelta(hours=8)
        except ValueError:
            continue
        out.append((start, end, summary))
    return sorted(out)


def slots_for_week(week_of: date) -> dict[date, list[Slot]]:
    week_end = week_of + timedelta(days=7)
    req = urllib.request.Request(load_url(), headers={"User-Agent": "vault-shift-parser/1"})
    ics = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
    by_day: dict[date, list[Slot]] = {}

    for start, end, summary in fetch_events(ics):
        label = classify_slot(start, end, summary)
        event_start = start.date()
        last = end.date()
        cur = event_start
        while cur <= last:
            if week_of <= cur < week_end:
                plan_start = datetime.combine(cur, DAY_PLAN_START)
                plan_end = datetime.combine(cur, DAY_PLAN_END)
                seg_start = max(start, plan_start)
                seg_end = min(end, plan_end)
                if seg_end > seg_start:
                    by_day.setdefault(cur, []).append(
                        Slot(seg_start, seg_end, label, event_start)
                    )
            cur += timedelta(days=1)

    for day_slots in by_day.values():
        day_slots.sort(key=lambda s: s.start)
    return by_day


def simplify_day_labels(slots: list[Slot], on_day: date) -> str:
    """不可用时段列：只显示「事件从今日开始」的班，不含昨日夜班延续段。"""
    today_slots = [s for s in slots if s.event_start == on_day]
    if not today_slots:
        return "休" if not slots else "休"  # 仅有跨日延续段 → 表内仍标休
    seen: list[str] = []
    for s in today_slots:
        if s.label not in seen:
            seen.append(s.label)
    return " + ".join(seen)


def estimate_availability(slots: list[Slot]) -> str:
    """只写空档/可用时段；不可用时段列已体现 ICS 占用，不写「不可用」。"""
    if not slots:
        return "全天可规划（科研）"

    labels = [s.label for s in slots]
    if "补休" in labels:
        return "15:00–20:00 可轻量"

    work = [s for s in slots if s.label != "补休"]
    types = {s.label for s in work}

    if types == {"下午班"}:
        return "上午 + 晚上可规划（科研）"

    if types == {"夜班"}:
        return "白天 + 晚上可规划（科研）"

    if types == {"7T", "晚班"} or (types == {"晚班", "7T"}):
        return "09:00–17:00 7T 可科研"

    if types == {"7T"}:
        return "09:00–17:00 7T 可科研；早晚可规划（科研）"

    return _gaps_fallback(work)


def _gaps_fallback(work: list[Slot]) -> str:
    if not work:
        return "全天可规划（科研）"
    day = work[0].start.date()
    plan_start = datetime.combine(day, DAY_PLAN_START)
    plan_end = datetime.combine(day, DAY_PLAN_END)
    busy = sorted(work, key=lambda s: s.start)
    gaps: list[str] = []
    cursor = plan_start
    for b in busy:
        if b.start > cursor:
            gaps.append(_span_label(cursor, b.start))
        cursor = max(cursor, b.end)
    if cursor < plan_end:
        gaps.append(_span_label(cursor, plan_end))
    if not gaps:
        return "—"
    return "；".join(g + "可规划（科研）" for g in gaps)


def _span_label(start: datetime, end: datetime) -> str:
    h0, h1 = start.hour, end.hour
    if h1 <= 12:
        return "上午"
    if h0 >= 18:
        return "晚上"
    if h0 < 12 and h1 > 18:
        return "上午 + 晚上"
    return f"{start.strftime('%H:%M')}–{end.strftime('%H:%M')}"


def day_label(d: date) -> str:
    return f"周{WEEKDAYS[d.weekday()]} {d.strftime('%m-%d')}"


def kid_slot(slots: list[Slot]) -> str:
    """晚班与 20–21 冲突；夜班若 22:30 后上岗，20–21 仍可带读。"""
    for s in slots:
        if s.label == "晚班":
            return KID_NONE
    return KID_DEFAULT


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=str, help="周内任意一天，归到该周周一")
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()

    anchor = date.fromisoformat(args.week) if args.week else date.today()
    week_of = monday_of_week(anchor)
    by_day = slots_for_week(week_of)
    week_end = week_of + timedelta(days=7)
    rows: list[dict[str, str]] = []
    cur = week_of
    while cur < week_end:
        slots = by_day.get(cur, [])
        rows.append(
            {
                "day": day_label(cur),
                "shifts": simplify_day_labels(slots, cur),
                "available": estimate_availability(slots),
                "kid": kid_slot(slots),
            }
        )
        cur += timedelta(days=1)

    if args.markdown:
        print("# 粘贴列：不可用时段 | 预计可用时段 | 带娃 / 火山")
        for r in rows:
            print(
                f"| {r['day']} | {r['shifts']} | {r['available']} | {r['kid']} |  |"
            )
    else:
        print(json.dumps({"week_of": week_of.isoformat(), "rows": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
