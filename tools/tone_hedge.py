# -*- coding: utf-8 -*-
"""장의 산문 문단을 유보형 비중과 함께 보여 준다. 낮은 문단부터 고치면 된다."""
import re, sys
sys.path.insert(0, "tools")
import tone_scan as T

RAW = "--raw" in sys.argv


def sents(s):
    # --raw: 인라인 코드를 가리지 않는다. 그대로 복사해 apply_edits의 old로 쓸 수 있다.
    if not RAW:
        s = re.sub(r"\[\^\d+\]", "", T.INLINE.sub("X", s))
    return [x.strip() for x in re.split(r"(?<=[.?!])\s+", s) if len(x.strip()) > 4]

path = sys.argv[1]
only_flat = "--flat" in sys.argv
cand = "--cand" in sys.argv
rows = []
tot = hed = 0
for no, k, line in T.scan_file(path):
    if k not in T.SENT_SRC:
        continue
    S = sents(line)
    if not S:
        continue
    h = sum(1 for x in S if T.HEDGE.search(x.rstrip(".?! ")))
    tot += len(S); hed += h
    if len(S) >= 2:
        rows.append((h / len(S), h, len(S), no, line))
if cand:
    # 단정으로 끝나는 문장만 뽑는다. 「~수 있습니다」·「~것은 아닙니다」로 바꿀 후보다.
    FLAT = re.compile(r"(?<!수 있)(?<!수도 있)(합니다|됩니다|입니다|습니다)\.$")
    for no, k, line in T.scan_file(path):
        if k not in T.SENT_SRC:
            continue
        for x in sents(line):
            if FLAT.search(x) and not T.HEDGE.search(x.rstrip(".?! ")):
                print("%4d  %s" % (no, x))
    raise SystemExit

rows.sort()
for r, h, n, no, line in rows:
    if only_flat and h: continue
    print("%4d  유보 %d/%d" % (no, h, n))
    print("    " + line.strip()[:300])
    print()
print("이 장 전체: 문장 %d, 유보 %d (%.1f%%)  목표 20%%+" % (tot, hed, hed / max(tot,1) * 100))
