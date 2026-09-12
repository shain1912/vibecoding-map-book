#!/usr/bin/env python3
"""캡션 글을 바꾼다. 번호는 그대로 두고 설명만 손댄다.

    py tools/fix_caption.py "최종교재/04장_....docx" 4.7 "이 책의 로드맵: 4부 29장의 흐름"
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_polish import rewrite  # noqa: E402

path = Path(sys.argv[1])
num, text = sys.argv[2], sys.argv[3]

d = Document(str(path))
done = 0
for p in d.paragraphs:
    if re.match(rf"^\s*그림\s*{re.escape(num)}\b", p.text):
        rewrite(p, f"그림 {num} — {text}")
        done += 1
        break
if done:
    bak = path.with_suffix(".docx.capbak")
    if not bak.exists():
        shutil.copy2(path, bak)
    d.save(str(path))
print(f"캡션 {num}: {done}곳 수정")
