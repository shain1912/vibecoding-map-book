#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""문단 안에서 '연결 없는 단문'이 몇 개나 연달아 오는지 잰다.

    py tools/tone_flow.py                    # 29장 요약 + 심한 문단 목록
    py tools/tone_flow.py chapters/ch00.md   # 한 장만
    py tools/tone_flow.py --min 5            # 연속 5개 이상만

tone_scan.py의 게이트는 전부 '장 단위 평균'이다. 평균이 맞아도 문단 안에서
짧은 종결 문장이 줄줄이 이어지면 낭독체로 읽힌다. 독자는 평균이 아니라
문단을 읽으므로 이 지표를 따로 잰다.

교수님 원고 실측: 최대 연속 4개, 5개 이상인 문단 0%.
"""
from __future__ import annotations

import argparse
import glob
import re
import sys

sys.path.insert(0, "tools")
import tone_scan as T

# 문장을 다음 문장과 엮는 연결어미. 이게 없으면 문장이 홀로 끝난다.
CONN = re.compile(
    r"(는데|은데|지만|면서|으면|하면|어서|아서|해서|니까|므로|으며|하며|이며|거나|려면|"
    r"도록|더라도|아도|어도|해도|기에|느라|자마자|이고|하고|든지|커녕|뿐만)"
)
SHORT = 42  # 이 길이 이하를 '단문'으로 본다


def sentences(par: str) -> list[str]:
    par = re.sub(r"\[\^\d+\]", "", T.INLINE.sub("X", par))
    return [x.strip() for x in re.split(r"(?<=[.?!])\s+", par) if len(x.strip()) > 4]


def longest_run(sents: list[str]) -> int:
    best = cur = 0
    for x in sents:
        if len(re.sub(r"\s", "", x)) <= SHORT and not CONN.search(x):
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def scan(path: str):
    for no, kind, line in T.scan_file(path):
        if kind != "산문":
            continue
        s = sentences(line)
        if len(s) < 3:
            continue
        yield no, longest_run(s), s


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--min", type=int, default=5, help="이 값 이상 연속이면 출력")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    files = a.files or sorted(glob.glob("chapters/ch*.md"))
    hits, total = [], 0
    for f in files:
        for no, run, s in scan(f):
            total += 1
            if run >= a.min:
                hits.append((run, f, no, s))

    hits.sort(key=lambda x: (-x[0], x[1], x[2]))
    if not a.quiet:
        for run, f, no, s in hits:
            print("%s:%d  연속 단문 %d개" % (f, no, run))
            for x in s:
                mark = "  " if (len(re.sub(r"\s", "", x)) > SHORT or CONN.search(x)) else "* "
                print("   %s%s" % (mark, x[:76]))
            print()

    over = len(hits)
    print("문단 %d개 중 연속 %d개 이상 %d개 (%.1f%%)  · 교수님 원고 기준: 최대 4개, 5개 이상 0%%"
          % (total, a.min, over, over / max(total, 1) * 100))


main()
