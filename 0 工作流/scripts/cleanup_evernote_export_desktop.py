#!/usr/bin/env python3
"""Remove imported / rejected HTML from Evernote desktop export folder."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from bs4 import BeautifulSoup

EXPORT = Path(r"F:\SYSTEM\DESKTOP\印象笔记导出")

WHITELIST_IMPORTED = re.compile(
    r"基于 TabPFN 的海马亚区疗效预测验证|"
    r"研究笔记：海马后部不对称性作为抗抑郁疗效预测的影像学标准|"
    r"Mengyue Paper 重修改重投|"
    r"2024年度 key points and review",
    re.I,
)

EXCLUDE_TITLE = re.compile(
    r"周记|weekly|tracking system|monthly summary|daily\s*log|priority this week|"
    r"账单|发票|报销|模板|^0\s*initiate|控制台|"
    r"工作系统[：:]\s*1\.0|工作系统2\.[01]|工作系统：海马\+精神疾病|"
    r"健身|每日生活|印象笔记使用技巧|做个鹅|20小时学习|阅读的4个层次|"
    r"轻躁狂发作\s*诊断|话术参考|三阶段筛选法",
    re.I,
)

PERIOD_LOG = re.compile(
    r"^\d{4}\s*[一二三四]季度|"
    r"^\d{4}\s*[一二三四五六七八九十]+月|"
    r"^\d{4}/\d{2}|^\d{4}二季度每日生活|"
    r"dailylog|daily log|"
    r"^2022\s*一季度|^2023\s*[一二三四]季度|"
    r"^2022/07|^2022/09|^2022/10",
    re.I,
)

EXPLICIT_REJECT = re.compile(r"^实验设计$|需要文献update的事情", re.I)


def note_title(html_path: Path) -> str:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "html.parser")
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else html_path.stem


def should_delete(title: str) -> bool:
    if WHITELIST_IMPORTED.search(title):
        return True
    if EXPLICIT_REJECT.search(title):
        return True
    if EXCLUDE_TITLE.search(title):
        return True
    if PERIOD_LOG.search(title):
        return True
    return False


def remove_note(html_path: Path) -> None:
    stem = html_path.stem
    files_dir = EXPORT / f"{stem}_files"
    html_path.unlink(missing_ok=True)
    if files_dir.is_dir():
        shutil.rmtree(files_dir)


def main() -> None:
    deleted: list[str] = []
    kept = 0
    for html_path in sorted(EXPORT.glob("*.html")):
        if "index" in html_path.name.lower():
            continue
        title = note_title(html_path)
        if should_delete(title):
            remove_note(html_path)
            deleted.append(title)
        else:
            kept += 1
    print(f"Deleted {len(deleted)} notes (+ attachments)")
    print(f"Remaining (non-index) HTML: {kept}")
    for t in deleted[:5]:
        print(f"  - {t}")
    if len(deleted) > 5:
        print(f"  ... +{len(deleted) - 5} more")


if __name__ == "__main__":
    main()
