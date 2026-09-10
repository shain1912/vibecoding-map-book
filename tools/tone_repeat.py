# -*- coding: utf-8 -*-
"""같은 종결어미가 연달아 반복되는 곳을 찾는다. 유보형을 억지로 넣으면 생기는 문제다."""
import re, sys, glob, os
sys.path.insert(0, "tools")
import tone_scan as T

END = re.compile(r"([가-힣]{2,7})[.?!]$")
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 3
total = 0
for path in sorted(glob.glob("chapters/ch*.md")):
    for no, k, line in T.scan_file(path):
        if k != "산문":
            continue
        s = re.sub(r"\[\^\d+\]", "", T.INLINE.sub("X", line))
        S = [x.strip() for x in re.split(r"(?<=[.?!])\s+", s) if len(x.strip()) > 4]
        run, prev = 1, None
        for i, x in enumerate(S):
            m = END.search(x)
            e = m.group(1) if m else None
            if e and e == prev:
                run += 1
            else:
                run = 1
            if run >= LIMIT:
                total += 1
                print("%s:%d  '%s' %d연속" % (os.path.basename(path), no, e, run))
                for y in S[max(0, i - run + 1):i + 1]:
                    print("     " + y[:76])
                print()
                run = 1
            prev = e
print("합계 %d곳 (연속 %d개 이상)" % (total, LIMIT))
