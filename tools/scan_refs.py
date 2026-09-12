#!/usr/bin/env python3
"""검수에서 지적된 흔적이 남아 있는지 다시 훑는다.

    py tools/scan_refs.py
"""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "최종교재"

CHECKS = [
    ("각주 표기", re.compile(r"\[\^\w+\]")),
    ("키 표기", re.compile(r"\+\+[A-Za-z0-9+]+\+\+")),
    ("없는 장", re.compile(r"(?<![\d.])(3[0-9])장")),
    ("옛 부 번호", re.compile(r"제?5부")),
    ("옛 구성 설명", re.compile(r"5부\s*2?6?개?\s*장|26개\s*장|전체\s*5부")),
    ("부록 언급", re.compile(r"부록\s*[AB]")),
    ("마스크 토큰", re.compile(r"【\s*\d+\s*】")),
    ("옛 번호 중복", re.compile(r"(?<![\d.])\d{1,2}장\s+\d{1,2}장")),
]


def main() -> None:
    total = 0
    for docx in sorted(BOOK.glob("*.docx")):
        d = Document(str(docx))
        for i, p in enumerate(d.paragraphs):
            t = p.text
            if not t.strip():
                continue
            for name, rx in CHECKS:
                m = rx.search(t)
                if m:
                    total += 1
                    print(f"[{name}] {docx.name} 문단{i}: "
                          f"{t[max(0, m.start() - 30):m.start() + 50]}")
    print(f"\n합계 {total}곳")


if __name__ == "__main__":
    main()
