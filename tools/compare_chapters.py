#!/usr/bin/env python3
"""두 원고(최종교재 vs 윤문 원고)를 문단 단위로 정렬해 차이를 분류한다.

목적: 최종교재에 윤문본을 반영할 때 "교수님이 최종교재에만 넣은 내용"을
덮어쓰지 않도록, 무엇이 윤문 차이이고 무엇이 새 내용인지 가른다.

    py tools/compare_chapters.py 최종.txt 원고.txt
    py tools/compare_chapters.py 최종.txt 원고.txt --json out.json

분류
    same      글자까지 같다
    polished  같은 문단인데 표현만 다르다 (윤문)  → 원고 문장으로 교체 대상
    only_final  최종교재에만 있다                → 지키기 (교수님 내용일 수 있음)
    only_draft  원고에만 있다                    → 최종교재에 없는 것, 판단 필요
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import unicodedata
from pathlib import Path


def paras(text: str) -> list[str]:
    out = []
    for ln in text.split("\n"):
        s = ln.strip()
        if s:
            out.append(s)
    return out


def norm(s: str) -> str:
    """비교용 정규화 — 공백·문장부호·강조 제거."""
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\s​]+", "", s)
    s = re.sub(r"[·•\-–—~…\"'“”‘’()（）\[\]{}:;,.!?]", "", s)
    return s


def sim(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm(a), norm(b), autojunk=False).ratio()


def align(final: list[str], draft: list[str], thresh: float = 0.55) -> list[dict]:
    """정규화 텍스트로 1차 정렬한 뒤, 바뀐 구간만 유사도로 짝짓는다."""
    nf = [norm(x) for x in final]
    nd = [norm(x) for x in draft]
    rows: list[dict] = []
    sm = difflib.SequenceMatcher(None, nf, nd, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                rows.append({"kind": "same", "final": final[i1 + k], "draft": draft[j1 + k]})
            continue
        fs = list(range(i1, i2))
        ds = list(range(j1, j2))
        used_d: set[int] = set()
        for fi in fs:
            best, bj = 0.0, None
            for dj in ds:
                if dj in used_d:
                    continue
                r = sim(final[fi], draft[dj])
                if r > best:
                    best, bj = r, dj
            if bj is not None and best >= thresh:
                used_d.add(bj)
                rows.append({"kind": "polished", "sim": round(best, 3),
                             "final": final[fi], "draft": draft[bj]})
            else:
                # 짝이 없다 = 정말 새 내용일 수 있다. 최고 유사도를 같이 남긴다.
                rows.append({"kind": "only_final", "final": final[fi], "draft": "",
                             "best_sim": round(best, 3),
                             "verdict": "새 내용 의심" if best < 0.30 else "윤문으로 크게 바뀜"})
        for dj in ds:
            if dj not in used_d:
                rows.append({"kind": "only_draft", "final": "", "draft": draft[dj]})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("final")
    ap.add_argument("draft")
    ap.add_argument("--json")
    ap.add_argument("--show", type=int, default=6, help="분류별로 몇 개까지 보여줄지")
    ap.add_argument("--min-len", type=int, default=12, help="이보다 짧은 문단은 요약에서 제외")
    ap.add_argument("--thresh", type=float, default=0.55, help="같은 문단으로 볼 유사도 기준")
    ap.add_argument("--new-only", action="store_true", help="'새 내용 의심'만 출력")
    args = ap.parse_args()

    f = paras(Path(args.final).read_text(encoding="utf-8"))
    d = paras(Path(args.draft).read_text(encoding="utf-8"))
    rows = align(f, d, args.thresh)

    cnt: dict[str, int] = {}
    for r in rows:
        cnt[r["kind"]] = cnt.get(r["kind"], 0) + 1

    print(f"최종 {len(f)}문단 · 원고 {len(d)}문단")
    print("분류:", {k: cnt.get(k, 0) for k in ("same", "polished", "only_final", "only_draft")})

    if args.new_only:
        news = [r for r in rows if r["kind"] == "only_final"
                and r.get("verdict") == "새 내용 의심" and len(r["final"]) >= args.min_len]
        print()
        print(f"── 새 내용 의심 {len(news)}건")
        for r in news:
            print(f"  • [{r['best_sim']}] {r['final'][:160]}")
        return

    for kind, label in [("only_final", "최종교재에만 있음 (지켜야 할 수 있음)"),
                        ("only_draft", "원고에만 있음"),
                        ("polished", "윤문 차이 (교체 대상)")]:
        items = [r for r in rows if r["kind"] == kind
                 and len(r.get("final") or r.get("draft") or "") >= args.min_len]
        if not items:
            continue
        print(f"\n── {label} · {len(items)}건 (상위 {args.show})")
        for r in items[: args.show]:
            if kind == "polished":
                print(f"  [{r['sim']}]")
                print(f"    최종: {r['final'][:110]}")
                print(f"    원고: {r['draft'][:110]}")
            else:
                tag = f" [{r.get('verdict','')}·{r.get('best_sim','')}]" if kind == "only_final" else ""
                print(f"  •{tag} {(r['final'] or r['draft'])[:120]}")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"final_file": args.final, "draft_file": args.draft,
             "counts": cnt, "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n저장: {args.json}")


if __name__ == "__main__":
    main()
