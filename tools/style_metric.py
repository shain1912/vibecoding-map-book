#!/usr/bin/env python3
"""점프투파이썬(JTP) 문체 근접도 메트릭.

교수 피드백에서 나온 두 가지 결함을 1급 지표로 삼는다.
  M1 예고성 메타 발화  "~을 보여드립니다 / 살펴봅니다 / 할 시간입니다"
  M2 중2병 재정의      "X는 Y이지 Z가 아닙니다" / "유효한 ~가 아닙니다"

기준선은 wikidocs 점프투파이썬 15개 절(산문 74,729자, 1,770문장)에서 실측했다.

탐지 패턴과 가중치는 tools/style_patterns.json 에 있다. 검수자가 놓친 표현을
발견하면 tools/add_pattern.py 로 그 파일에 추가하면 곧바로 이 메트릭에 반영된다.

usage:
    python tools/style_metric.py chapters/                # 종합
    python tools/style_metric.py chapters/ --per-file     # 파일별 순위
    python tools/style_metric.py chapters/ --gate         # 통과/실패 판정
    python tools/style_metric.py chapters/ch21.md --show-hits 20
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERN_FILE = ROOT / "tools" / "style_patterns.json"

_cfg = json.loads(PATTERN_FILE.read_text(encoding="utf-8"))
JTP = _cfg["baseline_jtp"]
AXES = _cfg["axes"]


def _compile(axis: dict) -> re.Pattern:
    """정규식 + 검수자가 넣은 문구(자동 이스케이프)를 하나로 합친다."""
    parts = list(axis.get("regex", []))
    parts += [re.escape(p) for p in axis.get("user_phrases", [])]
    if not parts:
        return re.compile(r"(?!x)x")  # 아무것도 매치하지 않음
    return re.compile("(" + "|".join(parts) + ")")


AXIS_RE = {k: _compile(v) for k, v in AXES.items()}

# 마크다운 전용 보조 지표
BOLD = re.compile(r"\*\*[^*\n]+\*\*")
EMDASH = re.compile(r"—")
DEGREE = re.compile(r"(아주|매우|정말|굉장히|무척|상당히|꽤|훨씬|완전히|절대적으로|압도적으로)")

MIN_CHARS = 3000  # 이보다 짧으면 비율 지표가 불안정하다

# 문장 길이는 두 코퍼스가 이미 비슷(41 vs 42)해서 느슨하게 본다
SENT_LEN_TOLERANCE = 8
SENT_LEN_WEIGHT = 8
BOLD_WEIGHT = 12
BOLD_SCALE = 4.0

GATE = {
    "score_min": 85.0,
    "bold_per1k_max": 1.5,   # JTP 실측 0.58의 약 2.5배까지 허용
    "sent_len_min": 33.0,    # 지나친 단문화 방지
    "sent_len_max": 50.0,
}


def strip_to_prose(md: str) -> str:
    """코드/표/그림/헤딩 등을 걷어내고 산문만 남긴다."""
    t = md.replace("\r", "")
    t = re.sub(r"```.*?```", " ", t, flags=re.S)              # 코드 펜스
    t = re.sub(r"`[^`\n]+`", "코드", t)                       # 인라인 코드 → 자리표시자
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)             # 주석
    t = re.sub(r"^\s*///.*$", " ", t, flags=re.M)             # caption 블록 마커
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)(\{[^}]*\})?", " ", t)   # 이미지
    t = re.sub(r"^\s*\|.*\|\s*$", " ", t, flags=re.M)         # 표
    t = re.sub(r"^\s*#{1,6}\s.*$", " ", t, flags=re.M)        # 헤딩
    t = re.sub(r"^\s*!!!.*$", " ", t, flags=re.M)             # admonition 헤더
    t = re.sub(r"^\s*[-*+]\s+", "", t, flags=re.M)            # 불릿 마커
    t = re.sub(r"^\s*>\s?", "", t, flags=re.M)                # 인용 마커
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)            # 링크 → 텍스트
    return t


def sentences(prose: str) -> list[str]:
    lines = [s.strip() for s in prose.split("\n")]
    lines = [s for s in lines if s and len(s) >= 15 and re.search(r"[.!?]$|다$|요$|자$|까$", s)]
    out: list[str] = []
    for ln in lines:
        for s in re.split(r"(?<=[.!?])\s+", ln):
            s = s.strip()
            if len(s) >= 8:
                out.append(s)
    return out


HEADING = re.compile(r"^\s*#{1,6}\s+(.*)$", re.M)


def heading_hits(md: str) -> list[tuple[str, str]]:
    """제목에 숨은 위반. strip_to_prose 가 헤딩을 지우므로 따로 검사한다."""
    out: list[tuple[str, str]] = []
    for h in HEADING.findall(md):
        for name, rx in AXIS_RE.items():
            m = rx.search(h)
            if m:
                out.append((name, h.strip()))
    return out


def analyse(md: str) -> dict:
    sents = sentences(strip_to_prose(md))
    prose = " ".join(sents)
    chars = len(prose)
    k = chars / 1000 if chars else 1

    lens = [len(s) for s in sents]
    mean = statistics.mean(lens) if lens else 0.0
    sd = statistics.pstdev(lens) if len(lens) > 1 else 0.0
    p90 = sorted(lens)[int(len(lens) * 0.9)] if lens else 0

    hits = {k2: [m.group(0) for m in rx.finditer(prose)] for k2, rx in AXIS_RE.items()}
    heads = heading_hits(md)
    out = {
        "prose_chars": chars,
        "sentences": len(sents),
        "sent_len_mean": round(mean, 1),
        "sent_len_sd": round(sd, 1),
        "sent_len_p90": p90,
        "bold_per1k": round(len(BOLD.findall(md)) / k, 2),
        "emdash_per1k": round(len(EMDASH.findall(md)) / k, 2),
        "degree_per1k": round(len(DEGREE.findall(prose)) / k, 2),
        "raw": {k2: len(v) for k2, v in hits.items()},
        "heading_violations": len(heads),
        "_hits": hits,
        "_heads": heads,
    }
    for name in AXES:
        out[f"{name}_per1k"] = round(len(hits[name]) / k, 2)
    return out


def score(a: dict) -> dict:
    """JTP 근접도 0~100. 가중치·목표치는 style_patterns.json 에서 온다."""
    pen: dict[str, float] = {}
    for name, ax in AXES.items():
        target = ax.get("target", 0.0)
        over = max(a[f"{name}_per1k"] - target, 0.0)
        pen[name] = min(over / ax["scale"], 1.0) * ax["weight"]

    pen["bold"] = min(max(a["bold_per1k"] - JTP["bold_per1k"], 0) / BOLD_SCALE, 1.0) * BOLD_WEIGHT
    gap = max(abs(a["sent_len_mean"] - JTP["sent_len_mean"]) - SENT_LEN_TOLERANCE, 0)
    pen["sent_len"] = min(gap / 20.0, 1.0) * SENT_LEN_WEIGHT

    total = 100 - sum(pen.values())
    out = {"score": round(max(total, 0), 1),
           "penalties": {k2: round(v, 1) for k2, v in pen.items()}}
    if a["prose_chars"] < MIN_CHARS:
        out["warning"] = f"산문 {a['prose_chars']}자 < {MIN_CHARS}자 — 비율 지표 불안정, 참고용"
    return out


def gate_check(a: dict, s: dict) -> tuple[bool, list[str]]:
    fails = []
    if s["score"] < GATE["score_min"]:
        fails.append(f"score {s['score']} < {GATE['score_min']}")
    for name, ax in AXES.items():
        v = a[f"{name}_per1k"]
        if v > ax["gate_max"]:
            fails.append(f"{ax['label']} {v} > {ax['gate_max']} ({a['raw'][name]}건)")
    if a.get("heading_violations"):
        fails.append(f"제목에 위반 {a['heading_violations']}건")
    if a["bold_per1k"] > GATE["bold_per1k_max"]:
        fails.append(f"볼드 {a['bold_per1k']} > {GATE['bold_per1k_max']}")
    if not (GATE["sent_len_min"] <= a["sent_len_mean"] <= GATE["sent_len_max"]):
        fails.append(f"문장길이 {a['sent_len_mean']} 가 "
                     f"[{GATE['sent_len_min']}, {GATE['sent_len_max']}] 밖")
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
            if not ok:
                bad += 1
            print(f"[{'PASS' if ok else 'FAIL'}] {f.name:<12} score={s['score']:>5}")
            for x in fails:
                print(f"         - {x}")
        print()
        print(f"{len(files) - bad}/{len(files)} 통과")
        sys.exit(1 if bad else 0)

    if args.per_file:
        rows = []
        for f in files:
            a = analyse(f.read_text(encoding="utf-8"))
            rows.append((f.name, score(a)["score"], a["meta_per1k"], a["pseudo_per1k"],
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
        a.pop("_hits"); a.pop("_heads")
        print(json.dumps({**a, **s}, ensure_ascii=False, indent=1))
        return

    print(f"파일 {len(files)}개 · 산문 {a['prose_chars']:,}자 · {a['sentences']:,}문장")
    print(f"\n{'지표':<22}{'우리 교재':>10}{'점프투파이썬':>14}")
    print("-" * 48)
    for name, ax in AXES.items():
        base = ax.get("target", 0.0)
        print(f"{ax['label']:<22}{a[f'{name}_per1k']:>10}{base:>14}")
    print(f"{'문장 길이 평균':<22}{a['sent_len_mean']:>10}{JTP['sent_len_mean']:>14}")
    print(f"{'볼드 (마크다운)':<22}{a['bold_per1k']:>10}{JTP['bold_per1k']:>14}")
    print(f"\nJTP 근접도 점수: {s['score']} / 100")
    print(f"감점: {s['penalties']}")
    if "warning" in s:
        print(f"주의: {s['warning']}")

    if args.show_hits:
        if a["_heads"]:
            print()
            print(f"[heading] 제목 위반 {len(a['_heads'])}건")
            for name, h in a["_heads"]:
                print(f"   [{AXES[name]['label']}] {h}")
        for name, ax in AXES.items():
            hh = a["_hits"][name]
            if hh:
                print(f"\n[{name}] {ax['label']} {len(hh)}건 (상위 {args.show_hits})")
                for h in hh[: args.show_hits]:
                    print("  ", h)


if __name__ == "__main__":
    main()
