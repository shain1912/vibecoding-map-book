#!/usr/bin/env python3
"""제출 직전에 docx 를 훑어 남은 흔적을 찾는다.

    py tools/final_scan.py
"""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "출판사제출" / "본문"

CHECKS = [
    ("마스크 토큰", re.compile(r"【\s*\d+\s*】")),
    ("옛 번호 중복", re.compile(r"(?:^|\s)(\d{1,2})장\s+\d{1,2}장")),
    ("절 번호 중복", re.compile(r"(?:^|\s)(\d{1,2}\.\d{1,2})\s+\d{1,2}\.\d{1,2}(?:\s|$)")),
    ("그림 번호 중복", re.compile(r"그림\s*\d+\.\d+\s+그림\s*\d+\.\d+")),
    ("자리표시자", re.compile(r"0{5,}|TODO|TBD|XXX|\bLorem\b")),
    ("깨진 백틱", re.compile(r"`")),
    ("이모지", re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")),
]


def main() -> None:
    total = 0
    for docx in sorted(BOOK.glob("*.docx")):
        d = Document(str(docx))
        hits: dict[str, list[str]] = {}
        for i, p in enumerate(d.paragraphs):
            t = p.text
            if not t.strip():
                continue
            for name, rx in CHECKS:
                m = rx.search(t)
                if m:
                    hits.setdefault(name, []).append(f"{i}: {t[max(0, m.start() - 25):m.start() + 45]}")
        if hits:
            print(f"── {docx.name}")
            for name, lines in hits.items():
                print(f"   [{name}] {len(lines)}곳")
                for ln in lines[:3]:
                    print(f"      {ln}")
                total += len(lines)
    print(f"\n합계 {total}곳")


if __name__ == "__main__":
    main()
