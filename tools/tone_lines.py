#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""한 장의 고칠 줄을 위반 태그와 함께 한 번씩만 출력한다 (장별 윤문 작업용).

    py tools/tone_lines.py chapters/ch00.md
    py tools/tone_lines.py chapters/ch00.md --paren   # 긴 괄호도 함께
"""
import sys, re, collections
sys.path.insert(0, "tools")
from tone_scan import scan_file, COMPILED, PROSE_LIKE, INLINE, WHITELIST_LINES, profile, GATES, REF, gate_check

path = sys.argv[1]
rows = scan_file(path)
tags = collections.defaultdict(set)
text = {}
for ln, k, s in rows:
    if any(w in s for w in WHITELIST_LINES):
        continue
    probe = INLINE.sub(lambda m: " " * len(m.group(0)), s)
    for group, rx, kinds in COMPILED:
        if kinds is not None and k not in kinds:
            continue
        if rx.search(probe):
            tags[ln].add(group)
            text[ln] = s.strip()

for ln in sorted(tags):
    print(f"{ln:5d} [{' '.join(sorted(tags[ln]))}]")
    print(f"      {text[ln]}\n")

print(f"고칠 줄 {len(tags)}개")

# 정의문(~입니다.) 종결 문장 목록 — 서술문으로 바꿀 후보
body = "\n".join(s for _, k, s in rows if k in PROSE_LIKE)
plain = INLINE.sub("X", body)
defs = [x.strip() for x in re.split(r"(?<=[.?!])\s+", plain.replace("\n", " "))
        if x.strip().endswith("입니다.")]
print(f"\n--- '~입니다.'로 끝나는 문장 {len(defs)}개 (일부를 서술문으로) ---")
for d in defs[:40]:
    print("  ", d[:110])

prof = profile(rows)
fails = gate_check(prof)
print(f"\n--- 이 장 프로파일 ---")
for key, (desc, _) in GATES.items():
    print(f"  {key:20s} {prof[key]:8.2f} (교수님 {REF[key]:.2f}, {desc})  {'FAIL' if key in fails else 'ok'}")
