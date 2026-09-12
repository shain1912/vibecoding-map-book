#!/usr/bin/env python3
"""문단 하나의 런(run) 서식을 들여다본다.

    py tools/docx_runs.py "최종교재/06장_Node.js_설치.docx" 3 25 31
"""
from __future__ import annotations

import sys

from docx import Document

d = Document(sys.argv[1])
for idx in [int(x) for x in sys.argv[2:]]:
    p = d.paragraphs[idx]
    print(f"── {idx} [{p.style.name}]")
    for j, r in enumerate(p.runs):
        f = r.font
        print(f"   {j}: name={f.name!r} size={f.size} bold={f.bold} italic={f.italic} "
              f"color={f.color.rgb if f.color and f.color.type else None} "
              f"style={r.style.name!r} :: {r.text[:60]!r}")
