#!/usr/bin/env python3
"""검수에서 나온 '뜻이 바뀐 두 문단'을 바로잡는다."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_polish import rewrite  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "최종교재"

JOBS = [
    ("29장", "위치 정보는 각 사용자의 브라우저에 저장되기",
     "이 주소를 다른 사람에게 전달하여도 문제없이 접속할 수 있습니다. 다만 한 가지 "
     "알아두어야 할 점이 있습니다. 다른 사람이 접속하여 보는 지도는 사용자가 저장한 내용이 "
     "아닌 빈 지도라는 점입니다. localStorage는 각자의 브라우저에 저장되므로, 여러분이 "
     "저장한 장소 데이터는 여러분의 브라우저에만 남습니다. 다른 사람은 각자의 데이터를 "
     "입력하여 자기 지도를 만들게 됩니다. 애플리케이션 자체는 동일하지만 저장되는 데이터는 "
     "사용자별로 분리되는 것입니다. 이것이 현재 구조의 특징이자 제한 사항입니다. 모든 "
     "사용자가 동일한 데이터를 확인할 수 있도록 하려면 별도의 서버와 데이터베이스가 "
     "필요합니다. 이 책에서는 거기까지 다루지 않지만, 지금 만든 구조 위에 서버를 얹는 것이 "
     "다음 단계입니다."),
    ("21장", "진짜로 지웠다가 백업으로 살려 내는\"를 통하여",
     "23장에서 장소 삭제 기능이 추가되면, 그때 실제로 삭제한 뒤 백업 파일로 되살리는 과정을 "
     "한 번 더 실습해 보시기 바랍니다. 이번 장에서 구현한 내보내기와 가져오기 기능이 그때의 "
     "데이터 손실 사고로부터 여러분의 데이터를 지켜 주는 안전망이 됩니다."),
]

for name, needle, new in JOBS:
    path = next(FINAL.glob(f"{name}*.docx"), None)
    if not path:
        print(f"{name}: 파일 없음")
        continue
    d = Document(str(path))
    done = 0
    for p in d.paragraphs:
        if needle in p.text:
            rewrite(p, new)
            done += 1
    if done:
        bak = path.with_suffix(".docx.twobak")
        if not bak.exists():
            shutil.copy2(path, bak)
        d.save(str(path))
    print(f"{path.name}: {done}곳")
