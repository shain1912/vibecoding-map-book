#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""장별 게이트 통과 현황을 한 표로 보여 준다.

    py tools/tone_status.py
"""
import glob
import re
import subprocess
import sys

rows = []
for p in sorted(glob.glob("chapters/ch*.md")):
    out = subprocess.run([sys.executable, "tools/tone_lines.py", p],
                         capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stdout
    prof = {}
    for m in re.finditer(r"^  (\S[^ ]*(?: \S+)*?)\s{2,}([\d.]+) \(교수님 [\d.]+, [^)]+\)\s+(ok|FAIL)",
                         out, re.M):
        prof[m.group(1)] = (float(m.group(2)), m.group(3))
    fails = [k for k, (v, s) in prof.items() if s == "FAIL"]
    n = re.search(r"고칠 줄 (\d+)개", out)
    rows.append((p[9:13], int(n.group(1)) if n else 0, fails))

print(f"{'장':5s} {'고칠줄':>6s} {'실패':>4s}  실패 항목")
for c, n, fails in rows:
    mark = "  " if not fails else "!!"
    print(f"{mark}{c:4s} {n:6d} {len(fails):4d}  {','.join(fails)}")
ok = sum(1 for r in rows if not r[2])
print(f"\n게이트 전부 통과: {ok}/{len(rows)}장 · 남은 고칠 줄 {sum(r[1] for r in rows)}개")
