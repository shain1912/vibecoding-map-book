#!/usr/bin/env python3
"""찾는 낱말이 든 문단의 전체 글을 보여 준다.

    py tools/show_para.py "최종교재/04장_이_책에서_만드는_것.docx" 부록 5부
"""
from __future__ import annotations

import sys

from docx import Document

d = Document(sys.argv[1])
words = sys.argv[2:]
for i, p in enumerate(d.paragraphs):
    t = p.text
    if any(w in t for w in words):
        print(f"── {i} [{p.style.name}] runs={len(p.runs)}")
        print(t)
        print()
