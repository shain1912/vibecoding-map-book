#!/usr/bin/env python3
"""윤문본에서 '바뀌면 안 되는 것'만 원문으로 되돌린다.

Dola 는 말투는 잘 다듬지만 큰따옴표 안의 예시 프롬프트·인라인 코드·숫자를
제멋대로 바꾼다. 문장은 Dola 것을 쓰되 이 조각만 원문으로 복원한다.

    py tools/restore_literals.py 원본.md 윤문본.md --out 결과.md
    py tools/restore_literals.py 원본.md 윤문본.md --out 결과.md --report
"""
from __future__ import annotations

import argparse
import difflib
import re
from pathlib import Path

QUOTE = re.compile(r'"([^"\n]{2,120})"')
CODE = re.compile(r'`([^`\n]{1,60})`')


def paras(t: str) -> list[str]:
    return [p for p in t.split("\n")]


def best_match(target: str, pool: list[str], used: set[int], floor: float = 0.45):
    best, bi = 0.0, None
    for i, c in enumerate(pool):
        if i in used:
            continue
        r = difflib.SequenceMatcher(None, target, c, autojunk=False).ratio()
        if r > best:
            best, bi = r, i
    return (bi, best) if bi is not None and best >= floor else (None, 0.0)


def restore_in_line(orig_line: str, new_line: str, log: list) -> str:
    """같은 줄로 짝지어진 원본/윤문본에서 리터럴을 복원."""
    out = new_line

    # 1) 큰따옴표 문구
    o_q = QUOTE.findall(orig_line)
    n_q = QUOTE.findall(out)
    if o_q and n_q:
        used: set[int] = set()
        for oq in o_q:
            if oq in n_q:                     # 이미 같으면 통과
                used.add(n_q.index(oq))
                continue
            bi, sc = best_match(oq, n_q, used)
            if bi is not None and n_q[bi] != oq:
                used.add(bi)
                out = out.replace(f'"{n_q[bi]}"', f'"{oq}"', 1)
                log.append(("따옴표", n_q[bi], oq, round(sc, 2)))

    # 2) 인라인 코드 — 사라진 것은 되살릴 위치를 알 수 없으니 보고만
    o_c = CODE.findall(orig_line)
    n_c = CODE.findall(out)
    for oc in o_c:
        if oc not in n_c:
            # 백틱 없이 맨몸으로 남아 있으면 백틱을 되씌운다
            bare = re.search(rf'(?<![`\w]){re.escape(oc)}(?![`\w])', out)
            if bare:
                out = out[:bare.start()] + f'`{oc}`' + out[bare.end():]
                log.append(("코드복원", oc, f'`{oc}`', 1.0))
            else:
                log.append(("코드유실", oc, "(못 찾음)", 0.0))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("orig")
    ap.add_argument("new")
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    o = paras(Path(args.orig).read_text(encoding="utf-8"))
    n = paras(Path(args.new).read_text(encoding="utf-8"))

    log: list = []
    if len(o) == len(n):
        merged = [restore_in_line(a, b, log) for a, b in zip(o, n)]
    else:
        # 줄 수가 다르면 유사도로 짝짓는다
        merged = []
        used: set[int] = set()
        for b in n:
            if not b.strip():
                merged.append(b); continue
            bi, _ = best_match(b, o, used)
            if bi is None:
                merged.append(b); continue
            used.add(bi)
            merged.append(restore_in_line(o[bi], b, log))

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(merged), encoding="utf-8")

    q = sum(1 for x in log if x[0] == "따옴표")
    c = sum(1 for x in log if x[0] == "코드복원")
    miss = [x for x in log if x[0] == "코드유실"]
    print(f"복원: 따옴표 문구 {q}개 · 인라인 코드 {c}개 -> {args.out}")
    if miss:
        print(f"되살리지 못한 코드 {len(miss)}개: {[m[1] for m in miss]}")
    if args.report and log:
        print("\n── 되돌린 내역")
        for kind, was, now, sc in log:
            if kind == "코드유실":
                continue
            print(f"  [{kind}] {was[:60]}")
            print(f"        -> {now[:60]}")


if __name__ == "__main__":
    main()
