#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""교수님 원고 톤(tools/TONE_SPEC.md) 대비 위반을 찾고 정량 게이트를 판정한다.

    py tools/tone_scan.py                      # 전체 요약 + 게이트
    py tools/tone_scan.py chapters/ch01.md     # 한 파일 상세
    py tools/tone_scan.py --group em대시        # 그룹별 상세
"""
from __future__ import annotations

import argparse
import collections
import glob
import re
import statistics
import sys

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE = re.compile(r"``.+?``|`[^`]*`")


def kind(s: str) -> str:
    t = s.strip()
    if not t:
        return "빈줄"
    if t.startswith("#"):
        return "헤딩"
    if re.match(r"^\s*(!!!|\?\?\?)", s):
        return "상자제목"
    if t.startswith("![") or t.startswith("///") or t.startswith("그림 "):
        return "그림"
    if t.startswith("|"):
        return "표"
    if re.match(r"^\[\^", t):
        return "각주"
    if re.match(r"^-{3,}$", t):
        return "구분선"
    if t.startswith("> "):
        return "인용"
    if re.match(r"^\s*-\s+`", s):
        return "용어목록"
    if re.match(r"^\s*([-*]|\d+\.|[①②③④⑤⑥⑦⑧⑨]|Q\d)", t):
        return "불릿"
    if set(t) <= set("_ "):
        return "빈칸"
    return "산문"


PROSE_LIKE = {"산문", "불릿", "인용"}
BODY_ONLY = {"산문"}
STRICT_DASH = BODY_ONLY | {"불릿", "인용", "헤딩", "상자제목"}
SENT_SRC = {"산문", "불릿"}


def scan_file(path):
    rows, infence = [], False
    for i, line in enumerate(open(path, encoding="utf-8-sig"), 1):
        s = line.rstrip("\n")
        if FENCE.match(s):
            infence = not infence
            continue
        if infence:
            continue
        rows.append((i, kind(s), s))
    return rows


RULES = [
    ("em대시", r"—", STRICT_DASH),
    ("볼드", r"\*\*", BODY_ONLY | {"불릿", "인용"}),
    ("대구형 표어",
     r"[가-힣]{2,10}은 [^,.]{1,14}(가|이) [^,.]{0,10}(하고|이고), ?[가-힣]{2,10}은 [^,.]{1,14}(가|이) [^,.]{0,12}(합니다|입니다)"
     r"|[^.]{2,20}(한다|않는다), ?[^.]{2,20}(한다|않는다)\.", PROSE_LIKE),
    ("의문→판정",
     r"(의문이 들 수 있|생각할 수 있|물을 수 있|싶을 수 있)[^.]{0,40}\.\s*(필요합니다|있습니다|없습니다|아닙니다|안 됩니다|됩니다|그렇습니다|맞습니다)\."
     r"|까요\?\s*(안 됩니다|됩니다|아닙니다|맞습니다|그렇습니다|필요합니다|없습니다)\.", PROSE_LIKE),
    ("교훈 마무리",
     r"(습관|원칙|기본|자세|태도|이치|법)입니다\.\s*$|(모아 둡니다|들입니다)\.\s*$", PROSE_LIKE),
    ("명사형 종결",
     r"(?<![가-힣])(?:[가-힣A-Za-z0-9_.()`]+ )?(?:부분|자리|끝부분|한 곳|이름|순서|차례|목록|방식|상태|구조)\.\s*$",
     BODY_ONLY),
    ("문장형 괄호", r"\([^)]*(합니다|입니다|됩니다|하세요|하십|한다|됩니|니까요|때문입)[^)]*\)", PROSE_LIKE),
    ("긴 괄호", r"(?<!\])\([^)]{18,}\)", PROSE_LIKE),
    ("용어 정의 연속", r"^\*\*[^*]+\*\*\s*(은|는|이|가)\s", PROSE_LIKE),
    ("따옴표 명령문",
     r"[\"“][^\"”]{4,60}(하라|해라|하라는|말라|말라는|주세요|줘|해)[\"”]\s*(는|라는|이라는)?\s*(뜻|의미|말|소리)",
     PROSE_LIKE),
    ("개수 선언",
     r"(두|세|네|다섯|여섯|일곱|여덟) ?가지(만|를|가|는)?\s*(정리하면|이렇습니다|있습니다|말해|알려|짚|기억|나뉩니다|입니다|뿐)"
     r"|(두|세|네) ?(단계|박자|축|기둥|갈래)(로|가|는|입니다)"
     r"|(딱|정확히) (두|세|네|다섯) ?가지", PROSE_LIKE),
    ("첫째/둘째", r"(첫째|둘째|셋째|넷째)", PROSE_LIKE),
    ("즉/정리하면",
     r"(^|[\s(“\"])(즉(?![시각결])|다시 말해|말하자면|요약하면)|(^|[.!?]\s)정리하면", PROSE_LIKE),
    ("이것이/그것이", r"(?<![가-힣])(이것이|그것이|이게|그게)(\s|$)", PROSE_LIKE),
    ("비유",
     r"안전벨트|타임머신|리모컨|세이브 ?포인트|보스전|건축주|현장 감독|(?<![가-힣])도면|엔진입니다|열쇠|전기·수도|기반 설비|과외 선생님|"
     r"(?<!설치 )마법(?!사)|마술|주머니|서랍|창고|비서|집사|요리사|레시피|설계도|나침반|등대|망치[를이로]|톱니|뼈대|심장|혈관|"
     r"근육|지휘자|오케스트라|악보|배달부|우체부|우편함|택배|여권|신분증|명함|지문|보물|사진 한 장|계기판|운전대|벽돌|"
     r"비유하자면|비유하면|에 비유|비유합니다|마치 [^.]{0,30}처럼|같은 것입니다|셈입니다|셈이죠|셈이지요", PROSE_LIKE),
    ("구어체 훅",
     r"혹시 [^.?]{0,40}\?|(?<![임줄준])말입니다\.|있으신가요|아니신가요|거죠|것이죠|건데요|"
     r"니까요\.|(?<![달])답니다\.|군요\.|네요\.|[가-힣]죠[.?!]|[가-힣]죠$", PROSE_LIKE),
    ("과장·감탄",
     r"엄청나게|십중팔구|놀랍게도|드디어|훌륭한|훌륭합니다|축복|진리|기적|환상적|압도적|어마어마|굉장히|정말이지|무려|단연|"
     r"최고의|눈이 번쩍|짜릿|아주 좋습니다", PROSE_LIKE),
    ("독자 감정 대행",
     r"당황하지 마세요|걱정하지 마세요|걱정 마세요|기분이 좋|재미가 있|재미있습니다|설레|뿌듯|답답하겠|겁 없이|두렵지 않|"
     r"막막|근사하", PROSE_LIKE),
    ("예고 수사",
     r"다음 장 예고|차례입니다|시간입니다|여정|한 걸음 더|출발점입니다|첫걸음|관문|하이라이트|백미", PROSE_LIKE),
    ("장식 이모지", r"[\U0001F5E3\U0001F4A1⚠\U0001F50E\U0001F4CC\U0001F914✏✍\U0001F34E]", None),
]
COMPILED = [(g, re.compile(p, re.M), k) for g, p, k in RULES]

WHITELIST_LINES = ["카카오 지도 첫걸음", "바이브코딩 준비운동"]

GATES = {
    "em대시(산문)": ("== 0", 0),
    "볼드(산문)": ("== 0", 0),
    "문장형 괄호": ("== 0", 0),
    "긴 괄호(18자+)": ("<= 0.8", 0.8),
    "첫째/둘째": ("== 0", 0),
    "즉/정리하면": ("== 0", 0),
    "이것이/그것이": ("== 0", 0),
    "구어체 죠": ("== 0", 0),
    "유보형 종결%": (">= 20", 20),
    "입니다 종결 비중%": ("<= 13.3", 13.3),
    "60자 초과 문장 %": ("<= 8", 8),
    "문장 길이 평균": ("29~43", None),
}
REF = {"em대시(산문)": 0.0, "볼드(산문)": 0.0, "문장형 괄호": 0.0, "긴 괄호(18자+)": 0.0, "첫째/둘째": 0.0,
       "즉/정리하면": 0.0, "이것이/그것이": 0.0, "구어체 죠": 0.0, "유보형 종결%": 28.4, "입니다 종결 비중%": 10.81,
       "60자 초과 문장 %": 5.0, "문장 길이 평균": 37.0}


# 단정하지 않고 여지를 남기는 종결. 교수님 원고 실측 분포에 맞춘 목록이다.
#   ~수 있습니다/수도 12.8% · ~것은 아닙니다 5.7% · ~겠습니다 3.5% · ~ㄹ 겁니다 2.8%
#   ~수는 없습니다 1.4% · ~좋습니다 0.7% · ~겠지요 0.7%
# 「~면 됩니다」는 교수님 원고에 0회다. 세지 않는다.
HEDGE = re.compile(
    r"(것은 아닙니다|것만은 아닙니다|수는 없습니다|은 아닙니다|는 아닙니다|수도 있습니다|"
    r"수 있습니다|있을 겁니다|을 겁니다|ㄹ 겁니다|일 겁니다|텐데요|겠지요|겠습니다|을까요|모릅니다|"
    r"편입니다|쪽입니다|가깝습니다|듯합니다|같습니다|좋습니다|권합니다|낫습니다|어떨까요)$")

VERB_IMNIDA = re.compile(r"(?<![가-힣])(보|붙|쓰|쌓|섞)입니다\.$|움직입니다\.$")


def profile(rows):
    body = "\n".join(s for _, k, s in rows if k in PROSE_LIKE)
    strict = "\n".join(s for _, k, s in rows if k in BODY_ONLY)
    plain = re.sub(r"\[\^\d+\]", "", INLINE.sub("X", body))
    splain = INLINE.sub("X", strict)
    chars = max(len(re.sub(r"\s", "", plain)), 1)
    schars = max(len(re.sub(r"\s", "", splain)), 1)
    # 문장 지표는 저자가 쓴 산문·불릿만 센다. `> ` 인용은 AI에게 건네는 프롬프트 원문이라
    # 교수님 원고에 대응하는 글감이 없으므로 제외한다.
    sbody = "\n".join(s for _, k, s in rows if k in SENT_SRC)
    sbody = re.sub(r"\[\^\d+\]", "", INLINE.sub("X", sbody)).replace("\n", " ")
    sents = [x for x in re.split(r"(?<=[.?!])\s+", sbody) if len(x.strip()) > 4]
    lens = [len(re.sub(r"\s", "", x)) for x in sents] or [0]

    def p1k(pat):
        return len(re.findall(pat, plain)) / chars * 1000

    return {
        "chars": chars,
        "em대시(산문)": len(re.findall("—", splain)) / schars * 1000,
        "볼드(산문)": len(re.findall(r"\*\*", splain)) / schars * 1000,
        "문장형 괄호": len([m for m in re.findall(r"\(([^)]*)\)", plain)
                          if re.search(r"(합니다|입니다|됩니다|하세요|하십|니까요|때문입)", m)]) / chars * 1000,
        "긴 괄호(18자+)": len([m for m in re.findall(r"(?<!\])\(([^)]*)\)", plain)
                            if len(m) >= 18]) / chars * 1000,
        "첫째/둘째": p1k(r"(첫째|둘째|셋째|넷째)"),
        "즉/정리하면": p1k(r"(^|[\s(])(즉(?![시각결])|다시 말해|말하자면|요약하면)|(^|[.!?]\s)정리하면"),
        "이것이/그것이": p1k(r"(?<![가-힣])(이것이|그것이|이게|그게)"),
        "구어체 죠": p1k(r"[가-힣]죠[.?!]"),
        "유보형 종결%": len([x for x in sents if HEDGE.search(x.strip().rstrip(".?! "))])
                       / max(len(sents), 1) * 100,
        "입니다 종결 비중%": len([x for x in sents if x.strip().endswith("입니다.")
                                and not VERB_IMNIDA.search(x.strip())]) / max(len(sents), 1) * 100,
        "정보: 짧은 괄호": len([m for m in re.findall(r"\(([^)]*)\)", plain)
                            if len(m) < 9 and not re.search(r"(합니다|입니다|됩니다)", m)]) / chars * 1000,
        "정보: 습니다 종결": p1k(r"습니다[.]"),
        "60자 초과 문장 %": sum(1 for l in lens if l > 60) / len(lens) * 100,
        "문장 길이 평균": statistics.mean(lens),
    }


def gate_check(prof):
    fails = []
    for key, (desc, limit) in GATES.items():
        v = prof[key]
        if desc.startswith("=="):
            ok = v == 0
        elif desc.startswith("<="):
            ok = v <= limit
        elif desc.startswith(">="):
            ok = v >= limit
        elif desc == "7~14":
            ok = 7 <= v <= 14
        else:
            ok = 29 <= v <= 43
        if not ok:
            fails.append(key)
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--group")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    files = a.files or sorted(glob.glob("chapters/ch*.md"))
    hits, allrows = [], []
    per_file = collections.defaultdict(collections.Counter)

    for path in files:
        rows = scan_file(path)
        allrows += rows
        for ln, k, s in rows:
            if any(w in s for w in WHITELIST_LINES):
                continue
            probe = INLINE.sub(lambda m: " " * len(m.group(0)), s)
            for group, rx, kinds in COMPILED:
                if kinds is not None and k not in kinds:
                    continue
                for m in rx.finditer(probe):
                    hits.append((group, path, ln, m.group(0).strip()[:40], s.strip()))
                    per_file[path][group] += 1

    if a.group:
        n = 0
        for g, path, ln, txt, s in hits:
            if g == a.group:
                n += 1
                print(f"{path}:{ln}  [{txt}]\n    {s}\n")
        print(f"{a.group}: {n}건")
        return

    if not a.quiet:
        if len(files) == 1:
            for g, path, ln, txt, s in hits:
                print(f"{ln:5d}  [{g}] {txt}\n       {s}\n")
        else:
            print("=== 그룹별 총계 ===")
            for g, n in collections.Counter(h[0] for h in hits).most_common():
                print(f"{n:6d}  {g}")
            print("\n=== 파일별 ===")
            for path in sorted(per_file):
                print(f"{sum(per_file[path].values()):5d}  {path}   "
                      + " ".join(f"{g}:{n}" for g, n in per_file[path].most_common(5)))
        print(f"\n위반 총 {len(hits)}건")

    prof = profile(allrows)
    fails = gate_check(prof)
    print("\n=== 정량 프로파일 (1000자당) ===")
    print(f"{'지표':20s} {'우리':>8s} {'교수님':>8s} {'게이트':>8s}  판정")
    for key, (desc, _) in GATES.items():
        print(f"{key:20s} {prof[key]:8.2f} {REF[key]:8.2f} {desc:>8s}  "
              f"{'FAIL' if key in fails else 'ok'}")
    if fails:
        print(f"\n게이트 실패 {len(fails)}개: {', '.join(fails)}")
        sys.exit(1)
    print("\n게이트 전체 통과")


if __name__ == "__main__":
    main()
