#!/usr/bin/env python3
"""내가 쓴 원문과 Dola 가 다듬은 글을 통째로 견줘 규칙을 뽑는다.

    py tools/tone_diff_study.py            # 요약
    py tools/tone_diff_study.py --pairs 40 # 바뀐 문장 짝 보기
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dola_prep import prose_items  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / "윤문비교" / "원문"

SENT = re.compile(r"[^.!?]*[.!?]")
TAIL = re.compile(r"([가-힣]{1,6})[.!?]\s*$")


def sentences(t: str) -> list[str]:
    return [s.strip() for s in SENT.findall(t) if len(s.strip()) > 6]


def pairs() -> list[tuple[str, str]]:
    out = []
    for i in range(29):
        ch = f"ch{i:02d}"
        a = ORIG / f"{ch}.md"
        b = ROOT / "윤문비교" / ch / "D_Dola_보정.md"
        if not (a.exists() and b.exists()):
            continue
        oa = dict(prose_items(a.read_text(encoding="utf-8")))
        ob = dict(prose_items(b.read_text(encoding="utf-8")))
        for k in oa:
            if k in ob and oa[k] != ob[k]:
                out.append((oa[k], ob[k]))
    return out


def tails(texts: list[str]) -> Counter:
    c = Counter()
    for t in texts:
        for s in sentences(t):
            m = TAIL.search(s)
            if m:
                c[m.group(1)] += 1
    return c


def words(texts: list[str], n: int = 2) -> Counter:
    c = Counter()
    for t in texts:
        toks = re.findall(r"[가-힣]{2,}", t)
        for i in range(len(toks) - n + 1):
            c[" ".join(toks[i:i + n])] += 1
    return c


def side_by_side(c_a: Counter, c_b: Counter, label: str, top: int = 22) -> None:
    ta, tb = sum(c_a.values()), sum(c_b.values())
    rows = []
    for k in set(c_a) | set(c_b):
        pa = c_a.get(k, 0) / max(ta, 1) * 1000
        pb = c_b.get(k, 0) / max(tb, 1) * 1000
        if c_a.get(k, 0) + c_b.get(k, 0) < 25:
            continue
        rows.append((pb - pa, k, c_a.get(k, 0), c_b.get(k, 0)))
    rows.sort()
    print(f"\n## {label} — Dola 가 줄인 것")
    for d, k, a, b in rows[:top]:
        print(f"  {k:22s} 원문 {a:5d} -> 도라 {b:5d}  ({d:+.1f}/1k)")
    print(f"\n## {label} — Dola 가 늘린 것")
    for d, k, a, b in rows[-top:][::-1]:
        print(f"  {k:22s} 원문 {a:5d} -> 도라 {b:5d}  ({d:+.1f}/1k)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, default=0)
    args = ap.parse_args()

    ps = pairs()
    A = [a for a, _ in ps]
    B = [b for _, b in ps]
    sa = [s for t in A for s in sentences(t)]
    sb = [s for t in B for s in sentences(t)]
    print(f"짝 지은 문단 {len(ps):,}개 · 원문 {len(sa):,}문장 / 도라 {len(sb):,}문장")
    print(f"문단 평균 길이 원문 {sum(map(len, A)) / len(A):.0f}자 "
          f"-> 도라 {sum(map(len, B)) / len(B):.0f}자")
    print(f"문장 평균 길이 원문 {sum(map(len, sa)) / len(sa):.0f}자 "
          f"-> 도라 {sum(map(len, sb)) / len(sb):.0f}자")
    print(f"문단당 문장 수 원문 {len(sa) / len(A):.1f} -> 도라 {len(sb) / len(B):.1f}")

    side_by_side(tails(A), tails(B), "문장 끝맺음", 18)
    side_by_side(words(A), words(B), "두 낱말 묶음", 20)

    if args.pairs:
        print("\n## 바뀐 문단 보기")
        for a, b in ps[:args.pairs]:
            print(f"\n원문: {a[:200]}")
            print(f"도라: {b[:200]}")


if __name__ == "__main__":
    main()
