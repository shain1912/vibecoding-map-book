#!/usr/bin/env python3
"""점프투파이썬(JTP) 문체 근접도 메트릭.

교수 피드백에서 나온 두 가지 결함을 1급 지표로 삼는다.
  M1 예고성 메타 발화  "~을 보여드립니다 / 살펴봅니다 / 할 시간입니다"
  M2 중2병 재정의      "X는 Y이지 Z가 아닙니다" / "유효한 ~가 아닙니다"

기준선은 wikidocs 점프투파이썬 15개 절(산문 74,729자, 1,770문장)에서 실측했다.
JS(브라우저)와 파이썬 양쪽에서 같은 정규식·같은 문장 추출 규칙을 쓴다.

usage:
    python tools/style_metric.py chapters/*.md
    python tools/style_metric.py --json chapters/ch00.md
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

# ── 실측 기준선 (점프투파이썬) ──────────────────────────────────
JTP = {
    "sent_len_mean": 41.2,
    "sent_len_sd": 18.4,
    "sent_len_p90": 67,
    "meta_per1k": 0.00,
    "pseudo_per1k": 0.00,
    "drama_per1k": 0.01,
    "degree_per1k": 0.48,
}

# ── 패턴 (JS 구현과 1:1로 일치시킬 것) ─────────────────────────
META = re.compile(
    r"(보여\s?드립니다|보여\s?줍니다|살펴봅니다|살펴보겠습니다|알아봅니다|알아보겠습니다"
    r"|해\s?보겠습니다|돌아보겠습니다|구경하는"
    # '이제 ~할 시간/차례/순서입니다' 형태만 (명사 '순서입니다' 단독은 정상 문장)
    r"|(?:할|볼|풀|짤|쓸|만들|배울|익힐|나눌|고칠|옮길|넘길|맞출|채울|풀어낼"
    r"|정리할|확인할|시작할|마무리할|자랑할|조립할|회수할|돌아볼|살펴볼|알아볼)"
    r"\s*(?:시간|차례|순서)입니다)"
)
PSEUDO = re.compile(
    r"((이지|가 아니라|이 아니라)[^.!?]{0,30}(가|이) 아닙니다"
    r"|(진짜|유효한|온전한|제대로 된|참된)[^.!?]{0,20}(가|이) 아닙니다"
    r"|(이지|지),?\s*[^.!?]{0,20}(가|이) 아닙니다)"
)
DRAMA = re.compile(r"(바로 그|다름 아닌|그것이 바로|여기서 진짜|비밀은|정체는|핵심은|셈입니다|셈이죠)")
DEGREE = re.compile(r"(아주|매우|정말|굉장히|무척|상당히|꽤|훨씬|완전히|절대적으로|압도적으로)")

# M3 독자 반응 대행 · 예고 후 본론 — codex/grok 블라인드 심사 공통 지적
MINDREAD = re.compile(
    r"(궁금해집니다|궁금해질|궁금하실|궁금할 겁니다|의문이 듭니다|질문이 생깁니다"
    r"|주의할 점이|짚고 넘어가|생각이 들 겁니다|느끼실 겁니다|느낌이 들|당황할 수도"
    r"|이런 생각이 들|하고 싶어질|들지도 모릅니다)"
)
# M4 대립·등치 수사 — "A는 B이지 C가 아니다" 약형, "A가 곧 B" 재정의
CONTRAST = re.compile(
    r"((?:이|가) 곧 [^.!?]{2,25}입니다|(?:은|는) 곧 [^.!?]{2,25}입니다"
    r"|[^.!?]{2,25}지만 [^.!?]{2,25}(?:못합니다|못 합니다|않습니다)"
    r"|[^.!?]{2,20}이지 [^.!?]{2,20}(?:가|이) 아)"
)

# 마크다운 전용 보조 지표
BOLD = re.compile(r"\*\*[^*\n]+\*\*")
EMDASH = re.compile(r"—")


def strip_to_prose(md: str) -> str:
    """코드/표/그림/헤딩 등을 걷어내고 산문만 남긴다 (브라우저 쪽 innerText 추출과 동등)."""
    t = md.replace("\r", "")
    t = re.sub(r"```.*?```", " ", t, flags=re.S)          # 코드 펜스
    t = re.sub(r"`[^`\n]+`", " ", t)                      # 인라인 코드
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)         # 주석
    t = re.sub(r"^\s*///.*$", " ", t, flags=re.M)         # caption 블록 마커
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)(\{[^}]*\})?", " ", t)  # 이미지
    t = re.sub(r"^\s*\|.*\|\s*$", " ", t, flags=re.M)     # 표
    t = re.sub(r"^\s*#{1,6}\s.*$", " ", t, flags=re.M)    # 헤딩
    t = re.sub(r"^\s*!!!.*$", " ", t, flags=re.M)         # admonition 헤더
    t = re.sub(r"^\s*[-*+]\s+", "", t, flags=re.M)        # 불릿 마커
    t = re.sub(r"^\s*>\s?", "", t, flags=re.M)            # 인용 마커
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)        # 링크 → 텍스트
    return t


def sentences(prose: str) -> list[str]:
    """브라우저 쪽 sentences()와 같은 규칙."""
    lines = [s.strip() for s in prose.split("\n")]
    lines = [s for s in lines if s and len(s) >= 15 and re.search(r"[.!?]$|다$|요$|자$|까$", s)]
    out: list[str] = []
    for ln in lines:
        for s in re.split(r"(?<=[.!?])\s+", ln):
            s = s.strip()
            if len(s) >= 8:
                out.append(s)
    return out


def analyse(md: str) -> dict:
    prose_raw = strip_to_prose(md)
    sents = sentences(prose_raw)
    prose = " ".join(sents)
    chars = len(prose)
    k = chars / 1000 if chars else 1

    lens = [len(s) for s in sents]
    mean = statistics.mean(lens) if lens else 0.0
    sd = statistics.pstdev(lens) if len(lens) > 1 else 0.0
    p90 = sorted(lens)[int(len(lens) * 0.9)] if lens else 0

    hits = {
        "meta": [m.group(0) for m in META.finditer(prose)],
        "pseudo": [m.group(0) for m in PSEUDO.finditer(prose)],
        "drama": [m.group(0) for m in DRAMA.finditer(prose)],
        "degree": [m.group(0) for m in DEGREE.finditer(prose)],
        "mindread": [m.group(0) for m in MINDREAD.finditer(prose)],
        "contrast": [m.group(0) for m in CONTRAST.finditer(prose)],
    }
    return {
        "prose_chars": chars,
        "sentences": len(sents),
        "sent_len_mean": round(mean, 1),
        "sent_len_sd": round(sd, 1),
        "sent_len_p90": p90,
        "meta_per1k": round(len(hits["meta"]) / k, 2),
        "pseudo_per1k": round(len(hits["pseudo"]) / k, 2),
        "drama_per1k": round(len(hits["drama"]) / k, 2),
        "degree_per1k": round(len(hits["degree"]) / k, 2),
        "mindread_per1k": round(len(hits["mindread"]) / k, 2),
        "contrast_per1k": round(len(hits["contrast"]) / k, 2),
        "bold_per1k": round(len(BOLD.findall(md)) / k, 2),
        "emdash_per1k": round(len(EMDASH.findall(md)) / k, 2),
        "raw": {key: len(v) for key, v in hits.items()},
        "_hits": hits,
    }


MIN_CHARS = 3000  # 이보다 짧으면 비율 지표가 불안정하다


def score(a: dict) -> dict:
    """JTP 근접도 0~100.

    가중치는 '무엇이 실제로 두 코퍼스를 가르는가'로 정했다.
      meta / pseudo  교수 피드백의 1·2순위이자 JTP 실측 0건 → 최대 가중
      drama          JTP 0.01 vs 우리 0.21 → 변별력 있음
      bold           JTP 산문에 거의 없음 · taxonomy J-1 과도한 볼드
      sent_len       두 코퍼스가 이미 비슷(41 vs 42) → 느슨한 허용치
      degree         우리가 JTP보다 오히려 적음(0.28 vs 0.48) → 점수에서 제외
    """
    pen_meta = min(a["meta_per1k"] / 0.20, 1.0) * 35
    pen_pseudo = min(a["pseudo_per1k"] / 0.20, 1.0) * 30
    pen_drama = min(max(a["drama_per1k"] - JTP["drama_per1k"], 0) / 0.40, 1.0) * 10
    pen_mind = min(a["mindread_per1k"] / 0.30, 1.0) * 8
    pen_contrast = min(a["contrast_per1k"] / 0.30, 1.0) * 7
    pen_bold = min(max(a["bold_per1k"] - 1.0, 0) / 5.0, 1.0) * 12
    len_gap = max(abs(a["sent_len_mean"] - JTP["sent_len_mean"]) - 8, 0)
    pen_len = min(len_gap / 20.0, 1.0) * 8
    total = 100 - (pen_meta + pen_pseudo + pen_drama + pen_mind + pen_contrast + pen_bold + pen_len)
    out = {
        "score": round(max(total, 0), 1),
        "penalties": {
            "meta": round(pen_meta, 1),
            "pseudo": round(pen_pseudo, 1),
            "drama": round(pen_drama, 1),
            "mindread": round(pen_mind, 1),
            "contrast": round(pen_contrast, 1),
            "bold": round(pen_bold, 1),
            "sent_len": round(pen_len, 1),
        },
    }
    if a["prose_chars"] < MIN_CHARS:
        out["warning"] = f"산문 {a['prose_chars']}자 < {MIN_CHARS}자 — 비율 지표 불안정, 참고용"
    return out


# ── 롤아웃 게이트 ────────────────────────────────────────────
GATE = {
    "score_min": 85.0,
    "meta_per1k_max": 0.0,     # 교수 지적 1순위 — 무관용
    "pseudo_per1k_max": 0.0,   # 교수 지적 2순위 — 무관용
    "drama_per1k_max": 0.05,
    "mindread_per1k_max": 0.10,
    "contrast_per1k_max": 0.10,
    "bold_per1k_max": 2.0,
    "sent_len_min": 33.0,      # 지나친 단문화 방지 (JTP 41.2, 현 교재 42.3)
    "sent_len_max": 50.0,
}


def gate_check(a: dict, s: dict) -> tuple[bool, list[str]]:
    fails = []
    if s["score"] < GATE["score_min"]:
        fails.append(f"score {s['score']} < {GATE['score_min']}")
    if a["meta_per1k"] > GATE["meta_per1k_max"]:
        fails.append(f"예고성 메타 {a['meta_per1k']} > {GATE['meta_per1k_max']} ({a['raw']['meta']}건)")
    if a["pseudo_per1k"] > GATE["pseudo_per1k_max"]:
        fails.append(f"중2병 재정의 {a['pseudo_per1k']} > {GATE['pseudo_per1k_max']} ({a['raw']['pseudo']}건)")
    if a["drama_per1k"] > GATE["drama_per1k_max"]:
        fails.append(f"극적 지시 {a['drama_per1k']} > {GATE['drama_per1k_max']} ({a['raw']['drama']}건)")
    if a["mindread_per1k"] > GATE["mindread_per1k_max"]:
        fails.append(f"독자반응 대행 {a['mindread_per1k']} > {GATE['mindread_per1k_max']} ({a['raw']['mindread']}건)")
    if a["contrast_per1k"] > GATE["contrast_per1k_max"]:
        fails.append(f"대립 수사 {a['contrast_per1k']} > {GATE['contrast_per1k_max']} ({a['raw']['contrast']}건)")
    if a["bold_per1k"] > GATE["bold_per1k_max"]:
        fails.append(f"볼드 {a['bold_per1k']} > {GATE['bold_per1k_max']}")
    if not (GATE["sent_len_min"] <= a["sent_len_mean"] <= GATE["sent_len_max"]):
        fails.append(f"문장길이 {a['sent_len_mean']} 가 [{GATE['sent_len_min']}, {GATE['sent_len_max']}] 밖")
    return (not fails), fails


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--show-hits", type=int, default=0, help="상위 N개 위반 문구 출력")
    ap.add_argument("--per-file", action="store_true")
    ap.add_argument("--gate", action="store_true", help="파일별 통과/실패 판정")
    args = ap.parse_args()

    files: list[Path] = []
    for p in args.paths:
        pp = Path(p)
        files.extend(sorted(pp.glob("*.md")) if pp.is_dir() else [pp])

    if args.gate:
        bad = 0
        for f in files:
            a = analyse(f.read_text(encoding="utf-8"))
            s = score(a)
            ok, fails = gate_check(a, s)
            mark = "PASS" if ok else "FAIL"
            if not ok:
                bad += 1
            print(f"[{mark}] {f.name:<12} score={s['score']:>5}")
            for x in fails:
                print(f"         - {x}")
        print()
        print(f"{len(files) - bad}/{len(files)} 통과")
        sys.exit(1 if bad else 0)

    if args.per_file:
        rows = []
        for f in files:
            a = analyse(f.read_text(encoding="utf-8"))
            s = score(a)
            rows.append((f.name, s["score"], a["meta_per1k"], a["pseudo_per1k"],
                         a["drama_per1k"], a["sent_len_mean"], a["prose_chars"]))
        rows.sort(key=lambda r: r[1])
        print(f"{'file':<12}{'score':>7}{'meta':>7}{'pseudo':>8}{'drama':>7}{'len':>7}{'chars':>8}")
        for r in rows:
            print(f"{r[0]:<12}{r[1]:>7}{r[2]:>7}{r[3]:>8}{r[4]:>7}{r[5]:>7}{r[6]:>8}")
        return

    merged = "\n\n".join(f.read_text(encoding="utf-8") for f in files)
    a = analyse(merged)
    s = score(a)
    if args.json:
        a.pop("_hits")
        print(json.dumps({**a, **s}, ensure_ascii=False, indent=1))
        return

    print(f"파일 {len(files)}개 · 산문 {a['prose_chars']:,}자 · {a['sentences']:,}문장")
    print(f"\n{'지표':<22}{'우리 교재':>10}{'점프투파이썬':>14}")
    print("-" * 48)
    for key, label in [("meta_per1k", "예고성 메타 발화"), ("pseudo_per1k", "중2병 재정의"),
                       ("drama_per1k", "극적 지시"), ("mindread_per1k", "독자반응 대행"),
                       ("contrast_per1k", "대립 수사"), ("degree_per1k", "정도부사"),
                       ("sent_len_mean", "문장 길이 평균"), ("sent_len_sd", "문장 길이 편차")]:
        base = JTP.get(key, "-")
        print(f"{label:<22}{a[key]:>10}{base:>14}")
    print(f"{'볼드 (마크다운)':<22}{a['bold_per1k']:>10}{'-':>14}")
    print(f"\nJTP 근접도 점수: {s['score']} / 100")
    print(f"감점: {s['penalties']}")

    if args.show_hits:
        for key in ("meta", "pseudo", "drama", "mindread", "contrast"):
            hits = a["_hits"][key]
            if hits:
                print(f"\n[{key}] {len(hits)}건 (상위 {args.show_hits})")
                for h in hits[: args.show_hits]:
                    print("  ", h)


if __name__ == "__main__":
    main()
