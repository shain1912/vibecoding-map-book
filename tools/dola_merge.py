#!/usr/bin/env python3
"""prose/replies/chNN.txt 를 원고에 되꽂고 검사한다.

    py tools/dola_merge.py ch26 ch25
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(*args: str) -> str:
    p = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return ((p.stdout or "") + (p.stderr or "")).strip()


def one(ch: str) -> None:
    src = ROOT / "prose" / "replies" / f"{ch}.txt"
    dst = ROOT / "윤문비교" / ch / "Dola_응답.txt"
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    elif not dst.exists():
        print(f"{ch}: 응답 파일 없음 ({src})")
        return

    out = ROOT / "윤문비교" / ch / "D_Dola_보정.md"
    print(f"=== {ch}")
    print(run("tools/dola_prep.py", "merge", f"chapters/{ch}.md", str(dst), "--out", str(out)))
    print(run("tools/dola_prep.py", "check", f"chapters/{ch}.md", str(out)))
    print(run("tools/content_integrity.py", f"chapters/{ch}.md", str(out)))


if __name__ == "__main__":
    for ch in sys.argv[1:]:
        one(ch)
