#!/usr/bin/env python3
"""본문에 글자로 남은 각주 표기 [^1] 을 위첨자 숫자로 바꾼다.

    py tools/fix_footnote.py
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_polish import rewrite  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "최종교재"
MARK = re.compile(r"\[\^\w+\]")

n = 0
for path in sorted(FINAL.glob("*.docx")):
    d = Document(str(path))
    hit = 0
    for p in d.paragraphs:
        if MARK.search(p.text):
            rewrite(p, p.text)          # segments() 가 [^1] 을 위첨자로 처리한다
            hit += 1
    if hit:
        bak = path.with_suffix(".docx.fnbak")
        if not bak.exists():
            shutil.copy2(path, bak)
        d.save(str(path))
        print(f"{path.name}: {hit}곳")
        n += hit
print(f"합계 {n}곳")
