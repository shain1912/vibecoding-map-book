#!/usr/bin/env python3
"""빨간 글씨(편집자가 넣은 새 번호)가 어디에 있는지 모아 본다.

    py tools/red_runs.py "최종교재/06장_Node.js_설치.docx"
    py tools/red_runs.py --all
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parent.parent
RED = "C00000"


def one(path: Path) -> None:
    d = Document(str(path))
    hits = []
    for i, p in enumerate(d.paragraphs):
        for j, r in enumerate(p.runs):
            c = r.font.color
            if c and c.type is not None and str(c.rgb) == RED:
                prev = p.runs[j - 1].text if j else ""
                hits.append((i, p.style.name, repr(prev[-14:]), repr(r.text)))
    print(f"── {path.name}: 빨간 런 {len(hits)}개")
    for h in hits[:14]:
        print(f"   {h[0]:4d} [{h[1][:10]:10s}] 앞={h[2]:18s} 빨강={h[3]}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--all"]:
        for p in sorted((ROOT / "최종교재").glob("*.docx")):
            one(p)
    else:
        one(Path(sys.argv[1]))
