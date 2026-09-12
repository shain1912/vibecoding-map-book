#!/usr/bin/env python3
"""03장 참고문헌 [19] 에 남아 있던 작업 메모를 지운다."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_polish import rewrite  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "최종교재" / "03장_개인정보_보호와_저작권_및_디지털_자료의_이용.docx"
NEW = "[19] 한국저작권위원회. AI 저작권 안내서 모음. 공식 자료."

d = Document(str(PATH))
done = 0
for p in d.paragraphs:
    if "기존 초안 인용 자료" in p.text:
        print(f"{p.text}\n  -> {NEW}")
        rewrite(p, NEW)
        done += 1
if done:
    bak = PATH.with_suffix(".docx.ref19bak")
    if not bak.exists():
        shutil.copy2(PATH, bak)
    d.save(str(PATH))
print(f"{done}곳")
