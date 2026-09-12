#!/usr/bin/env python3
"""00장 작가 소개에서 자리표시자로 남아 있던 조성호 항목을 채운다."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_polish import rewrite  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "최종교재" / "00장_표지_작가소개_작가의말_도입글_목차.docx"

NEW = {
    16: "코드코리아 대표",
    17: "부산대학교 AI융합교육원 강사",
    18: "웹 서비스 개발과 AI를 활용한 소프트웨어 교육 분야에서 활동하고 있습니다.",
    20: "『바이브코딩으로 배우는 인공지능 윤리』 공저",
}

d = Document(str(PATH))
for i, text in NEW.items():
    p = d.paragraphs[i]
    print(f"{i}: {p.text}  ->  {text}")
    rewrite(p, text)

bak = PATH.with_suffix(".docx.biobak")
if not bak.exists():
    shutil.copy2(PATH, bak)
d.save(str(PATH))
print("저장했습니다")
