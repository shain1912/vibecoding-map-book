#!/usr/bin/env python3
"""검수자가 잡아낸 문구를 탐지 범위에 추가한다.

메트릭이 놓친 표현을 발견하면 그 문구를 그대로 넣으면 된다.
정규식을 몰라도 되게 문자열은 자동으로 이스케이프한다.

    # 어떤 축이 있는지 보기
    py tools/add_pattern.py --list

    # 추가하기 전에 이 문구가 교재 어디에 있는지 먼저 확인
    py tools/add_pattern.py --scan "구경하는 시간입니다"

    # 탐지 범위에 추가 (여러 개 한 번에)
    py tools/add_pattern.py --axis meta "보여 드리겠습니다" "소개해 드립니다"

    # 새 축을 만들어 추가
    py tools/add_pattern.py --new-axis cliche --label "상투어" --weight 8 "말 그대로"

추가한 뒤에는 자동으로 교재 전체를 다시 훑어 새로 걸린 곳을 보여 준다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERNS = ROOT / "tools" / "style_patterns.json"
CHAPTERS = ROOT / "chapters"


def load() -> dict:
    return json.loads(PATTERNS.read_text(encoding="utf-8"))


def save(d: dict) -> None:
    PATTERNS.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def scan(phrases: list[str]) -> dict[str, list[tuple[str, str]]]:
    """교재에서 그 문구가 들어간 문장을 찾는다."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("sm", ROOT / "tools" / "style_metric.py")
    sm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sm)

    found: dict[str, list[tuple[str, str]]] = {p: [] for p in phrases}
    for f in sorted(CHAPTERS.glob("*.md")):
        prose = sm.strip_to_prose(f.read_text(encoding="utf-8"))
        for s in sm.sentences(prose):
            for p in phrases:
                if p in s:
                    found[p].append((f.name, s))
    return found


def main() -> None:
    ap = argparse.ArgumentParser(description="탐지 문구 추가")
    ap.add_argument("phrases", nargs="*", help="추가할 문구 (그대로 적으면 됨)")
    ap.add_argument("--axis", help="기존 축 이름 (meta/pseudo/drama/mindread/contrast)")
    ap.add_argument("--new-axis", help="새 축 이름")
    ap.add_argument("--label", help="새 축의 한글 이름")
    ap.add_argument("--why", default="검수자 지적", help="새 축을 만든 이유")
    ap.add_argument("--weight", type=float, default=8.0, help="새 축 가중치")
    ap.add_argument("--gate-max", type=float, default=0.0, help="새 축 게이트 상한")
    ap.add_argument("--list", action="store_true", help="축 목록 보기")
    ap.add_argument("--scan", action="store_true", help="추가하지 않고 어디 있는지만 확인")
    args = ap.parse_args()

    d = load()

    if args.list:
        print(f"{'축':<12}{'이름':<18}{'가중치':>6}{'게이트':>8}{'정규식':>7}{'추가문구':>9}")
        print("-" * 62)
        for k, ax in d["axes"].items():
            print(f"{k:<12}{ax['label']:<18}{ax['weight']:>6}{ax['gate_max']:>8}"
                  f"{len(ax['regex']):>7}{len(ax['user_phrases']):>9}")
        return

    if not args.phrases:
        ap.error("추가할 문구를 적어 주세요 (--list 로 축 목록 확인)")

    if args.scan:
        for p, hits in scan(args.phrases).items():
            print(f"\n[{p}] {len(hits)}곳")
            for fn, s in hits[:10]:
                print(f"  {fn}: {s[:100]}")
        return

    if args.new_axis:
        key = args.new_axis
        if key in d["axes"]:
            sys.exit(f"'{key}' 축이 이미 있습니다. --axis {key} 로 추가하세요.")
        d["axes"][key] = {
            "label": args.label or key,
            "why": args.why,
            "weight": args.weight,
            "scale": 0.20,
            "gate_max": args.gate_max,
            "regex": [],
            "user_phrases": [],
        }
        target = key
    elif args.axis:
        if args.axis not in d["axes"]:
            sys.exit(f"'{args.axis}' 축이 없습니다. --list 로 확인하세요.")
        target = args.axis
    else:
        ap.error("--axis 또는 --new-axis 를 지정하세요")

    added = []
    for p in args.phrases:
        if p in d["axes"][target]["user_phrases"]:
            print(f"이미 있음: {p}")
            continue
        d["axes"][target]["user_phrases"].append(p)
        added.append(p)

    if added:
        save(d)
        print(f"[{d['axes'][target]['label']}] 축에 {len(added)}개 추가\n")

    print("=== 교재에서 새로 걸리는 곳 ===")
    for p, hits in scan(added or args.phrases).items():
        print(f"\n[{p}] {len(hits)}곳")
        for fn, s in hits[:8]:
            print(f"  {fn}: {s[:100]}")
    print("\n다시 채점하려면: py tools/style_metric.py chapters/ --gate")


if __name__ == "__main__":
    main()
