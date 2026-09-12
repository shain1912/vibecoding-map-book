#!/usr/bin/env python3
"""03장 그림 3.4·3.5 캡션에 링크 글자가 앞에 남은 것을 정리한다."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_polish import rewrite  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "최종교재" / "03장_개인정보_보호와_저작권_및_디지털_자료의_이용.docx"

NEW = {
    118: "그림 3.4 — 한국저작권위원회의 AI·저작권 안내서 제공 페이지",
    120: "그림 3.5 — 미국 저작권청의 AI·저작권 자료 제공 페이지",
}

d = Document(str(PATH))
for i, text in NEW.items():
    p = d.paragraphs[i]
    for h in p._p.findall(qn("w:hyperlink")):
        p._p.remove(h)
    rewrite(p, text)
    print(f"{i}: {text}")

bak = PATH.with_suffix(".docx.capfix")
if not bak.exists():
    shutil.copy2(PATH, bak)
d.save(str(PATH))
print("저장")
