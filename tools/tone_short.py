# -*- coding: utf-8 -*-
"""장 안의 짧은 산문 문장을 줄 번호와 함께 보여 준다(문장 길이 평균 올릴 때 씀)."""
import re
import sys

sys.path.insert(0, "tools")
import tone_scan as T


def main():
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    for no, k, line in T.scan_file(path):
        if k not in T.PROSE_LIKE:
            continue
        plain = re.sub(r"\[\^\d+\]", "", T.INLINE.sub("X", line))
        sents = [x for x in re.split(r"(?<=[.?!])\s+", plain) if len(x.strip()) > 4]
        for s in sents:
            n = len(re.sub(r"\s", "", s))
            if n <= limit:
                print("%5d %3d  %s" % (no, n, s.strip()))


main()
