#!/usr/bin/env python3
"""브라우저가 내려받은 Dola 응답을 받아 되꽂고 검사까지 한 번에 한다.

    py tools/dola_take.py ch00 ch01 ch02
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOWN = Path(os.environ["USERPROFILE"]) / "Downloads"


def run(*args: str) -> tuple[int, str]:
    p = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def take(ch: str) -> None:
    cands = sorted(DOWN.glob(f"dola_{ch}*.txt"), key=lambda p: p.stat().st_mtime)
    if not cands:
        print(f"{ch}: 내려받은 파일 없음")
        return
    src = cands[-1]
    dst = ROOT / "윤문비교" / ch / "Dola_응답.txt"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    for c in cands:
        c.unlink(missing_ok=True)

    out = ROOT / "윤문비교" / ch / "D_Dola_보정.md"
    rc1, o1 = run("tools/dola_prep.py", "merge", f"chapters/{ch}.md", str(dst), "--out", str(out))
    rc2, o2 = run("tools/dola_prep.py", "check", f"chapters/{ch}.md", str(out))
    rc3, o3 = run("tools/content_integrity.py", f"chapters/{ch}.md", str(out))
    print(f"=== {ch}")
    print(o1.strip())
    print(o2.strip())
    print(o3.strip())


if __name__ == "__main__":
    for ch in sys.argv[1:]:
        take(ch)
