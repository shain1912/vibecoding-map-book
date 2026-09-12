#!/usr/bin/env python3
"""최종교재 캡션과 그림 폴더를 맞춰 보고, 출판사에 낼 그림 목록을 만든다.

    py tools/check_figures.py
    py tools/check_figures.py --list 최종교재/그림목록.csv
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "최종교재"
FIGDIR = FINAL / "그림"

CAP = re.compile(r"^\s*그림\s*([\d.]+[\d])\s*[—\-–:]?\s*(.*)$")


def fig_files() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for p in FIGDIR.iterdir():
        if not p.is_file():
            continue
        m = re.match(r"^그림\s*([\d.\-]+)", p.stem)
        if m:
            out[m.group(1).replace("-", ".")] = p
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list")
    args = ap.parse_args()

    have = fig_files()
    rows: list[tuple[str, str, str, str]] = []
    missing: list[tuple[str, str]] = []

    for docx in sorted(FINAL.glob("*.docx")):
        d = Document(str(docx))
        for p in d.paragraphs:
            if p.style.name != "Caption":
                continue
            m = CAP.match(p.text)
            if not m:
                continue
            num, cap = m.group(1), m.group(2).strip()
            f = have.get(num)
            rows.append((num, f.name if f else "(없음)", cap, docx.name))
            if not f:
                missing.append((num, docx.name))

    used = {r[0] for r in rows}
    unused = sorted(set(have) - used, key=lambda s: [int(x) for x in s.split(".")])

    print(f"캡션 {len(rows)}개 · 그림 파일 {len(have)}개")
    if missing:
        print(f"\n파일이 없는 그림 {len(missing)}개")
        for num, doc in missing[:30]:
            print(f"  그림 {num}  ({doc})")
    else:
        print("모든 캡션에 해당하는 그림 파일이 있습니다")
    if unused:
        print(f"\n본문에서 안 쓰이는 그림 파일 {len(unused)}개: "
              + ", ".join(unused[:20]))

    if args.list:
        out = ROOT / args.list
        with out.open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["그림 번호", "파일명", "캡션", "수록 장"])
            for r in rows:
                w.writerow(["그림 " + r[0], r[1], r[2], r[3]])
        print(f"\n그림 목록 -> {out}")


if __name__ == "__main__":
    main()
