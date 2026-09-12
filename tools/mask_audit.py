#!/usr/bin/env python3
"""Dola 응답에서 빠진 마스크 토큰을 찾는다.

    py tools/mask_audit.py ch13
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIND = re.compile(r"【\s*(\d+)\s*】")


def main() -> None:
    for ch in sys.argv[1:]:
        base = ROOT / "윤문비교" / ch
        table = json.loads((base / "마스크표.json").read_text(encoding="utf-8"))
        reply = (base / "Dola_응답.txt").read_text(encoding="utf-8")
        sent = (base / "보낼산문.txt").read_text(encoding="utf-8")
        in_sent = {m.group(1) for m in FIND.finditer(sent)}
        in_reply = {m.group(1) for m in FIND.finditer(reply)}
        lost = sorted(in_sent - in_reply, key=int)
        print(f"=== {ch}: 표 {len(table)}개 · 보낸 토큰 {len(in_sent)} · "
              f"돌아온 토큰 {len(in_reply)} · 빠짐 {len(lost)}")
        for k in lost[:20]:
            print(f"   {k}: {table.get(k, '?')[:60]}")


if __name__ == "__main__":
    main()
