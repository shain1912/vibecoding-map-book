#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""문체 치환을 chapters/ 와 docs/ 에 동시에 적용한다.

치환 목록은 JSON 파일로 준다.

    [
      {"file": "chapters/ch01.md", "old": "...", "new": "..."},
      ...
    ]

각 old 는 파일 안에서 정확히 한 번 나와야 한다. 아니면 아무것도 쓰지 않고 실패한다.
코드 블록 안의 문자열과 겹치면 거부한다(코드는 손대지 않는다).

앞선 기계 패스(볼드 제거, 라벨 대시->콜론)로 old 가 어긋난 경우에는 자동으로 보정해 본다.

    py tools/apply_edits.py edits.json
    py tools/apply_edits.py edits.json --dry
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import defaultdict

FENCE = re.compile(r"^\s*(```|~~~)")
DASH = "—"
LABEL_DASH = re.compile(r"^(\s*(?:[-*]|\d+\.)\s+[^" + DASH + r"]{2,45}?) " + DASH + " ")
HEAD_DASH = re.compile(r"^(#{1,6} [^" + DASH + r"]+?)\s*" + DASH + r"\s*")


def _label_to_colon(s):
    return LABEL_DASH.sub(lambda m: m.group(1) + ": ", s)


def _head_to_colon(s):
    return HEAD_DASH.sub(lambda m: m.group(1) + ": ", s)


def variants(old):
    """기계 패스로 달라졌을 수 있는 형태들."""
    nb = old.replace("**", "")
    seen, out = {old}, []
    for c in (nb, _label_to_colon(old), _label_to_colon(nb),
              _head_to_colon(old), _head_to_colon(nb)):
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def code_spans(text):
    """코드 펜스 구간의 (시작, 끝) 오프셋 목록."""
    spans, pos, infence, start = [], 0, False, 0
    for line in text.splitlines(keepends=True):
        if FENCE.match(line):
            if not infence:
                infence, start = True, pos
            else:
                infence = False
                spans.append((start, pos + len(line)))
        pos += len(line)
    if infence:
        spans.append((start, pos))
    return spans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edits")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    edits = json.loads(pathlib.Path(a.edits).read_text(encoding="utf-8"))
    by_file = defaultdict(list)
    for e in edits:
        by_file[e["file"]].append(e)

    errors, applied, fixed = [], 0, 0
    staged = {}

    for fname, items in by_file.items():
        path = pathlib.Path(fname)
        if not path.exists():
            errors.append(f"{fname}: 파일 없음")
            continue
        text = path.read_text(encoding="utf-8")
        for e in items:
            old, new = e["old"], e["new"]
            if text.count(old) != 1:
                for c in variants(old):
                    if text.count(c) == 1:
                        old = c
                        fixed += 1
                        break
            n = text.count(old)
            if n != 1:
                errors.append(f"{fname}: {n}회 일치 (1회여야 함) :: {old[:70]!r}")
                continue
            idx = text.index(old)
            if any(s <= idx < t for s, t in code_spans(text)):
                errors.append(f"{fname}: 코드 블록 안 :: {old[:70]!r}")
                continue
            text = text[:idx] + new + text[idx + len(old):]
            applied += 1
        staged[fname] = text

    if errors:
        print("실패 — 아무것도 쓰지 않았습니다.")
        for e in errors:
            print("  " + e)
        sys.exit(1)

    note = f" (자동 보정 {fixed}건)" if fixed else ""
    if a.dry:
        print(f"검증 통과: {applied}건{note} (쓰지 않음)")
        return

    for fname, text in staged.items():
        p = pathlib.Path(fname)
        p.write_text(text, encoding="utf-8")
        mirror = pathlib.Path("docs") / p.name
        if mirror.exists():
            mirror.write_text(text, encoding="utf-8")
    print(f"적용 {applied}건{note} · 파일 {len(staged)}개 (docs 동기화 완료)")


if __name__ == "__main__":
    main()
