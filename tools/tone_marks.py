#!/usr/bin/env python3
"""특정 표현이 원문과 도라 글에서 각각 몇 번 나오는지 센다."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tone_diff_study import pairs  # noqa: E402

MARKS = [
    ("겁니다", r"겁니다"),
    ("봅시다", r"봅시다"),
    ("보세요/하세요", r"(보|하|주)세요"),
    ("~것은 아닙니다", r"것(은|이)\s*아닙니다"),
    ("A가 아니라 B", r"가\s*아니라\s"),
    ("남습니다", r"남습니다"),
    ("느낌표", r"!"),
    ("물음표", r"\?"),
    ("드디어/마침내", r"(드디어|마침내)"),
    ("~게 됩니다", r"게\s*됩(니다|니까)"),
    ("~으로 보입니다", r"(으로|로)\s*보입니다"),
    ("눈으로/손으로", r"(눈으로|손으로)"),
    ("것입니다", r"것입니다"),
    ("바랍니다", r"바랍니다"),
    ("보겠습니다", r"보겠습니다"),
    ("해당", r"해당\s"),
    ("때문입니다", r"때문입니다"),
    ("반면", r"반면"),
    ("예를 들어", r"예를\s*들어"),
    ("사용/활용", r"(사용|활용)하"),
    ("쓰다(동사)", r"(쓰|씁|썼)"),
    ("여러분", r"여러분"),
    ("사용자", r"사용자"),
    ("따옴표 인용", r"[\"“”]"),
    ("물결 범위", r"\d+~\d+"),
]

ps = pairs()
A = "\n".join(a for a, _ in ps)
B = "\n".join(b for _, b in ps)
ka, kb = len(A) / 1000, len(B) / 1000
print(f"원문 {len(A):,}자 · 도라 {len(B):,}자\n")
print(f"{'표현':18s} {'원문':>7s} {'도라':>7s}   {'1천자당 변화':>12s}")
print("-" * 52)
for name, rx in MARKS:
    a = len(re.findall(rx, A))
    b = len(re.findall(rx, B))
    d = b / kb - a / ka
    print(f"{name:18s} {a:7d} {b:7d}   {d:+9.2f}")
