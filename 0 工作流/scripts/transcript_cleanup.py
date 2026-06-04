#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Whisper 口述稿轻度整理（去语气词、合并过短行）。精修由 Cursor 写入「内容纪要」。"""

from __future__ import annotations

import re

# 句首/独立语气词（保留专业内容）
_FILLER_PREFIX = re.compile(
    r"^(嗯+|啊+|呃+|那个|就是|其实|然后|所以说|对吧|好吗|好吧|所以呢|怎么说呢|"
    r"那么|然后呢|所以说呢|我跟你说|大家知道|好吧)\s*[,，、]?\s*"
)
_STANDALONE_FILLER = re.compile(
    r"^(嗯+|啊+|呃+|那个|就是|对吧|好吗|好吧|然后呢|所以说呢)$"
)


def cleanup_transcript(text: str) -> str:
    lines_out: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if lines_out and lines_out[-1] != "":
                lines_out.append("")
            continue
        if _STANDALONE_FILLER.match(line):
            continue
        prev = line
        for _ in range(4):
            line = _FILLER_PREFIX.sub("", line)
            if line == prev:
                break
            prev = line
        line = re.sub(r"[，,]{2,}", "，", line).strip("，, ")
        if len(line) < 2:
            continue
        lines_out.append(line)
    # 去掉尾部空行
    while lines_out and lines_out[-1] == "":
        lines_out.pop()
    return "\n".join(lines_out)
