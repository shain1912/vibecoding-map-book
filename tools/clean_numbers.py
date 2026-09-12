#!/usr/bin/env python3
"""최종교재에 남아 있는 옛 번호를 지우고 새 번호만 검정으로 남긴다.

편집 과정에서 '2장 6장', '그림 2.1 그림 6.1'처럼 옛 번호(검정) 뒤에
새 번호(빨강)가 덧붙어 있다. 옛 번호를 지우고 새 번호를 본문 색으로 바꾼다.

    py tools/clean_numbers.py --all --dry
    py tools/clean_numbers.py --all
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

from docx import Document
from docx.shared import RGBColor

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "최종교재"
RED = "C00000"
BLACK = RGBColor(0, 0, 0)

NUMISH = re.compile(r"^(그림\s*)?\d{1,2}(\.\d{1,2})?(장|절)?$")


def is_num(t: str) -> bool:
    return bool(NUMISH.match(t.strip()))


def do_file(path: Path, dry: bool) -> int:
    d = Document(str(path))
    fixed = 0
    for p in d.paragraphs:
        runs = p.runs
        j = 0
        while j < len(runs):
            r = runs[j]
            c = r.font.color
            red = c is not None and c.type is not None and str(c.rgb) == RED
            if red and is_num(r.text) and j > 0 and is_num(runs[j - 1].text):
                old = runs[j - 1]
                old._element.getparent().remove(old._element)
                r.text = r.text.strip()
                r.font.color.rgb = BLACK
                fixed += 1
                runs = p.runs
                j = 0
                continue
            j += 1
    if fixed and not dry:
        bak = path.with_suffix(".docx.numbak")
        if not bak.exists():
            shutil.copy2(path, bak)
        d.save(str(path))
    print(f"{path.name}: 번호 {fixed}곳 정리" + (" [미리보기]" if dry else ""))
    return fixed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    files = sorted(FINAL.glob("*.docx")) if args.all else [Path(args.path)]
    total = sum(do_file(f, args.dry) for f in files)
    print(f"\n합계 {total}곳")


if __name__ == "__main__":
    main()
