#!/usr/bin/env python3
"""백틱 개수가 달라진 문단을 찾는다.

    py tools/tick_check.py ch11
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dola_prep import prose_items  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TICK = chr(96)

for ch in sys.argv[1:]:
    o = dict(prose_items((ROOT / "chapters" / f"{ch}.md").read_text(encoding="utf-8")))
    n = dict(prose_items((ROOT / "윤문비교" / ch / "D_Dola_보정.md").read_text(encoding="utf-8")))
    for i in o:
        a, b = o[i].count(TICK), n.get(i, "").count(TICK)
        if a != b:
            print(f"=== {ch} 문단 {i}: 백틱 {a} -> {b}")
            print(f"  원: {o[i][:260]}")
            print(f"  새: {n.get(i, '')[:260]}")
            print()
