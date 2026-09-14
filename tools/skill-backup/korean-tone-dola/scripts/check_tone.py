#!/usr/bin/env python3
"""저자가 물린 표현이 남아 있는지 훑는다.

    py check_tone.py 원고.md
    py check_tone.py "chapters/*.md" --quiet
    py check_tone.py 원고.docx --all      # 주의 항목까지

기준은 Dola로 윤문한 교재 29장을 전수 비교해 뽑았다. 자세한 수치는
references/evidence.md 에 있다.

  금지  Dola 가 사실상 쓰지 않는 표현. 0건이 목표다.
  주의  Dola 도 가끔 쓰지만 원문보다 확실히 줄인 표현. --all 로 본다.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BAN = [
    ("구어 축약", r"[가-힣]\s*겁니다", "~것입니다"),
    ("청유형", r"[가-힣]\s*봅시다", "~해 보겠습니다"),
    ("명령형", r"[가-힣](보|하|주|해)세요", "~시기 바랍니다 / ~하십시오"),
    ("남습니다체", r"남습니다", "유지됩니다 / 그대로입니다"),
    ("몸으로 비유", r"(눈으로|손으로|몸으로)\s", "'확인', '직접' 으로"),
    ("예고성 메타", r"(보여\s*드립니다|구경하는\s*시간|먼저\s*보여\s*드|하는\s*시간입니다)",
     "예고하지 말고 바로 본론"),
    ("감탄", r"(드디어|마침내|놀랍게도)", "빼기"),
    ("독자 넘겨짚기", r"(궁금하시|느끼실|아시겠지만|하실\s*겁니다|하셨을\s*겁니다)",
     "빼거나 사실만 쓴다"),
    ("부정대조", r"[가-힣]가\s*아니(라|고)\s", "B입니다 로 바로 쓴다"),
]

WARN = [
    ("부정대조(약)", r"것(은|이)\s*아닙니다", "긍정문으로 바로 쓸 수 있는지 본다"),
    ("억지 유보", r"(으로|로)\s*보입니다", "단정하거나 근거를 댄다"),
    ("이중 명사화", r"[가-힣]{2,}화의\s*[가-힣]{2,}화", "동사로 푼다"),
    ("~게 되는지", r"게\s*되(는지|는가)", "~하는지"),
    ("쓰다 동사", r"(을|를)\s*(쓰면|씁니다|쓰는|썼습니다)", "사용합니다 / 활용합니다"),
    ("느낌표", r"[가-힣]\s*!", "마침표"),
]

# 구조 줄은 말투 대상이 아니다
SKIP = re.compile(r"^\s*(```|!{3}|\||!\[|/{3}|#|\[\^|[-*+]\s|\d+[.)]\s|>\s)")


def lines_of(path: Path) -> list[str]:
    if path.suffix.lower() == ".docx":
        from docx import Document
        return [p.text for p in Document(str(path)).paragraphs]
    return path.read_text(encoding="utf-8-sig").split("\n")


def scan(path: Path, quiet: bool, show_warn: bool) -> tuple[int, int]:
    ban = warn = 0
    in_code = False
    rules = BAN + (WARN if show_warn else [])
    for n, line in enumerate(lines_of(path), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line.strip() or SKIP.match(line):
            continue
        # 큰따옴표 안은 예시 프롬프트라 건드리지 않는다
        bare = re.sub(r'"[^"\n]*"', "", line)
        for name, rx, how in rules:
            for m in re.finditer(rx, bare):
                hard = (name, rx, how) in BAN
                if hard:
                    ban += 1
                else:
                    warn += 1
                if not quiet:
                    s = max(0, m.start() - 22)
                    mark = "금지" if hard else "주의"
                    print(f"  {n:5d} [{mark} {name}] …{bare[s:m.end() + 26].strip()}…")
                    print(f"           -> {how}")
    tail = f" · 주의 {warn}곳" if show_warn else ""
    print(f"{path.name}: 금지 {ban}곳{tail}")
    return ban, warn


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--all", action="store_true", help="주의 항목까지 본다")
    args = ap.parse_args()

    tb = tw = 0
    for pat in args.paths:
        found = sorted(Path().glob(pat)) if any(c in pat for c in "*?") else [Path(pat)]
        for p in found:
            if p.exists():
                b, w = scan(p, args.quiet, args.all)
                tb += b
                tw += w
    print(f"\n합계 금지 {tb}곳" + (f" · 주의 {tw}곳" if args.all else ""))
    sys.exit(1 if tb else 0)


if __name__ == "__main__":
    main()
