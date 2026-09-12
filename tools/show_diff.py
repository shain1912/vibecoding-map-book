#!/usr/bin/env python3
"""원본과 윤문본을 줄 단위로 나란히 보여 준다. 필요하면 검색어로 걸러 본다.

    py tools/show_diff.py chapters/ch02.md 윤문비교/ch02/D_Dola_보정.md
    py tools/show_diff.py 원본.md 결과.md --grep 홀수
    py tools/show_diff.py 원본.md 결과.md --line 90
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("orig")
    ap.add_argument("new")
    ap.add_argument("--grep", help="이 낱말이 든 줄만")
    ap.add_argument("--line", type=int, help="이 줄 번호만")
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()

    a = Path(args.orig).read_text(encoding="utf-8-sig").split("\n")
    b = Path(args.new).read_text(encoding="utf-8-sig").split("\n")

    shown = 0
    for i, (x, y) in enumerate(zip(a, b), 1):
        if x == y:
            continue
        if args.line and i != args.line:
            continue
        if args.grep and args.grep not in x and args.grep not in y:
            continue
        print(f"── {i}")
        print(f"  원본: {x}")
        print(f"  결과: {y}")
        print()
        shown += 1
        if shown >= args.limit:
            print("… (더 있음)")
            break
    if len(a) != len(b):
        print(f"줄 수 다름: 원본 {len(a)} · 결과 {len(b)}")


if __name__ == "__main__":
    main()
