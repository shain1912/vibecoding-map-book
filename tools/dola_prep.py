#!/usr/bin/env python3
"""Dola 에 보낼 산문만 뽑고, 돌려받은 결과를 원고에 되꽂는다.

Dola 는 말투가 좋지만 구조와 리터럴을 망가뜨린다 (그림 참조 삭제, 예시 프롬프트
변조, 백틱 제거, 문장 통째 삭제). 그래서

  - 구조(헤딩·그림·코드펜스·표·팁 상자)는 아예 보내지 않는다.
  - 바뀌면 안 되는 조각(인라인 코드·큰따옴표 문구·각주)은 【1】 같은 토큰으로
    가려서 보내고, 돌아오면 표를 보고 원문으로 되돌린다.
  - 문단이 눈에 띄게 짧아지면 (기본 80% 미만) 그 문단은 원문을 유지한다.

    # 1) 보낼 산문 뽑기 (같은 폴더에 마스크표.json 이 함께 생긴다)
    py tools/dola_prep.py extract chapters/ch01.md --out 윤문비교/ch01/보낼산문.txt

    # 2) Dola 응답을 파일로 저장한 뒤 되꽂기
    py tools/dola_prep.py merge chapters/ch01.md 윤문비교/ch01/Dola_응답.txt --out 윤문비교/ch01/합친결과.md

    # 3) 내용이 바뀐 곳 찾기 (숫자·따옴표·인라인코드·각주)
    py tools/dola_prep.py check chapters/ch01.md 윤문비교/ch01/합친결과.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# 산문이 아닌 줄 — Dola 에 보내지 않는다
STRUCT = re.compile(
    r'^﻿?(\s*#{1,6}\s|\s*!\[|\s*///|\s*!!!|\s*```|\s*\||\s*>\s|\s*\[\^|\s*---\s*$|\s*[-*+]\s|\s*\d+\.\s)'
)

# 절대 바뀌면 안 되는 조각 — 보내기 전에 토큰으로 가린다
MASK_PATTERNS = [
    re.compile(r'\[\^\w+\]'),                 # 각주
    re.compile(r'`[^`\n]{1,120}`'),           # 인라인 코드
    re.compile(r'"[^"\n]{1,200}"'),           # 예시 프롬프트 등 큰따옴표
]
MASK_TOKEN = "【%d】"
MASK_FIND = re.compile(r'【\s*(\d+)\s*】')


def mask_para(text: str, table: dict, counter: list) -> str:
    """리터럴을 【n】 으로 바꾸고 table 에 원문을 적어 둔다."""
    def sub(m):
        counter[0] += 1
        table[str(counter[0])] = m.group(0)
        return MASK_TOKEN % counter[0]

    for rx in MASK_PATTERNS:
        text = rx.sub(sub, text)
    return text


def unmask(text: str, table: dict) -> str:
    """토큰 안에 토큰이 든 경우가 있어 더 안 바뀔 때까지 되돌린다."""
    def sub(m):
        return table.get(m.group(1), m.group(0))

    for _ in range(6):
        new = MASK_FIND.sub(sub, text)
        if new == text:
            break
        text = new
    return text


WORD = re.compile(r'[가-힣]{2,}|[A-Za-z][A-Za-z0-9_.]+|\d+')


def similar(a: str, b: str) -> float:
    """번호가 밀려 엉뚱한 문단이 들어온 것을 잡아내기 위한 낱말 겹침."""
    wa, wb = set(WORD.findall(a)), set(WORD.findall(b))
    if not wa:
        return 1.0
    return len(wa & wb) / len(wa)


def misaligned(i: int, new: str, lookup: dict, floor: float, span: int = 4) -> bool:
    """번호가 밀려 이웃 문단의 답이 들어왔는지 본다.

    Dola 는 낱말을 통째로 바꿔 쓰므로 겹침이 낮은 것만으로는 판단할 수 없다.
    제자리 문단보다 이웃 문단과 훨씬 더 닮았을 때만 밀린 것으로 본다.
    """
    here = similar(lookup[i], new)
    if here >= floor:
        return False
    for j in range(i - span, i + span + 1):
        if j == i or j not in lookup:
            continue
        if similar(lookup[j], new) >= here + 0.15:
            return True
    return False


def blocks(md: str) -> list[tuple[str, str]]:
    """('prose'|'struct', 텍스트) 순서대로. 코드펜스는 통째 struct."""
    out: list[tuple[str, str]] = []
    buf: list[str] = []
    kind = None
    in_code = False
    for ln in md.split("\n"):
        fence = ln.lstrip().startswith("```")
        if fence:
            in_code = not in_code
        this = "struct" if (in_code or fence or STRUCT.match(ln) or not ln.strip()) else "prose"
        if kind is None:
            kind = this
        if this != kind:
            out.append((kind, "\n".join(buf)))
            buf, kind = [], this
        buf.append(ln)
    if buf:
        out.append((kind, "\n".join(buf)))
    return out


def prose_items(md: str) -> list[tuple[int, str]]:
    """되꽂을 수 있게 번호를 붙인 산문 문단."""
    items: list[tuple[int, str]] = []
    n = 0
    for kind, txt in blocks(md):
        if kind != "prose":
            continue
        for para in [p.strip() for p in txt.split("\n") if p.strip()]:
            n += 1
            items.append((n, para))
    return items


HEADER_LINES = [
    "아래는 한국어 프로그래밍 교재의 본문 문단입니다. 말투를 자연스럽게 다듬어 주세요.",
    "",
    "규칙",
    "1. 번호를 그대로 유지하고, 문단 하나당 한 덩어리로 답해 주세요. 문단을 합치거나 나누지 마세요.",
    "2. 【1】 【2】 처럼 꺾쇠 안에 숫자가 든 표시는 건드리지 마세요. 숫자를 바꾸지도, 지우지도 말고",
    "   문장 안에서 원래 있던 자리에 그대로 두세요. 명령어와 예시 문구를 가려 둔 자리입니다.",
    "3. 숫자와 영문 용어는 그대로 두세요.",
    "4. 문장을 지우지 마세요. 문단의 정보량이 줄지 않게 해 주세요.",
    "5. 합니다체로 씁니다. 이모지는 넣지 마세요.",
    "6. 설명이나 요약은 붙이지 말고 번호와 다듬은 문단만 주세요.",
    "",
    "",
]


def cmd_extract(args) -> None:
    md = Path(args.src).read_text(encoding="utf-8")
    items = prose_items(md)

    table: dict[str, str] = {}
    counter = [0]
    masked = [(i, mask_para(p, table, counter)) for i, p in items]

    header = "\n".join(HEADER_LINES)
    body = "\n\n".join(f"[{i}] {p}" for i, p in masked)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(header + body, encoding="utf-8")

    mt = out.parent / "마스크표.json"
    mt.write_text(json.dumps(table, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"산문 문단 {len(items)}개 · {len(body):,}자 -> {args.out}")
    print(f"가린 리터럴 {len(table)}개 -> {mt}")


def parse_reply(text: str) -> dict[int, str]:
    """[n] 문단 형태를 파싱."""
    out: dict[int, str] = {}
    cur = None
    buf: list[str] = []
    for ln in text.split("\n"):
        m = re.match(r'^\s*\[(\d+)\]\s*(.*)$', ln)
        if m:
            if cur is not None:
                out[cur] = " ".join(x.strip() for x in buf if x.strip())
            cur = int(m.group(1))
            buf = [m.group(2)]
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        out[cur] = " ".join(x.strip() for x in buf if x.strip())
    return out


def cmd_merge(args) -> None:
    md = Path(args.src).read_text(encoding="utf-8")
    reply = parse_reply(Path(args.reply).read_text(encoding="utf-8"))
    items = prose_items(md)
    total = len(items)
    lookup = {i: p for i, p in items}

    mt_path = Path(args.mask) if args.mask else Path(args.reply).parent / "마스크표.json"
    table: dict[str, str] = {}
    if mt_path.exists():
        table = json.loads(mt_path.read_text(encoding="utf-8"))

    # 보낸 문단에 있던 토큰이 답에서 사라졌으면 그 문단은 원문을 쓴다.
    sent_path = Path(args.sent) if args.sent else Path(args.reply).parent / "보낼산문.txt"
    sent_tokens: dict[int, set] = {}
    if sent_path.exists():
        for i, p in parse_reply(sent_path.read_text(encoding="utf-8")).items():
            sent_tokens[i] = {m.group(1) for m in MASK_FIND.finditer(p)}

    shrunk: list[int] = []
    grown: list[int] = []
    unlike: list[int] = []
    leftover: list[int] = []
    dropped: list[int] = []
    broken: list[int] = []
    for i in list(reply):
        raw = reply[i]
        want = sent_tokens.get(i)
        if want and want - {m.group(1) for m in MASK_FIND.finditer(raw)}:
            dropped.append(i)
            reply[i] = lookup.get(i, raw)
            continue
        t = unmask(raw, table) if table else raw
        if MASK_FIND.search(t):
            leftover.append(i)
        orig = lookup.get(i, "")
        if orig and len(t) < len(orig) * args.min_ratio:
            shrunk.append(i)
            t = orig
        elif orig and len(t) > len(orig) * args.max_ratio:
            grown.append(i)
            t = orig
        elif orig and misaligned(i, t, lookup, args.min_sim):
            unlike.append(i)
            t = orig
        elif orig and t.count("`") != orig.count("`"):
            # 백틱 개수가 달라졌으면 인라인 코드 표시가 깨진 것이다
            broken.append(i)
            t = orig
        reply[i] = t

    missing = [i for i, _ in items if i not in reply or not reply[i].strip()]

    out_lines: list[str] = []
    n = 0
    for kind, txt in blocks(md):
        if kind != "prose":
            out_lines.append(txt)
            continue
        rebuilt: list[str] = []
        for line in txt.split("\n"):
            if not line.strip():
                rebuilt.append(line)
                continue
            n += 1
            rebuilt.append(reply.get(n) or lookup[n])   # 없으면 원문 유지
        out_lines.append("\n".join(rebuilt))

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n".join(out_lines), encoding="utf-8")

    print(f"되꽂기 완료 {total - len(missing)}/{total} 문단 -> {args.out}")
    if table:
        print(f"가려 둔 리터럴 {len(table)}개 복원")
    if missing:
        print(f"응답에 없어 원문을 유지한 문단: {missing}")
    if shrunk:
        print(f"분량이 {int(args.min_ratio * 100)}% 아래로 줄어 원문을 유지한 문단: {shrunk}")
    if grown:
        print(f"분량이 {int(args.max_ratio * 100)}% 넘게 늘어 원문을 유지한 문단 {len(grown)}개: {grown[:20]}")
    if unlike:
        print(f"내용이 딴판이라 원문을 유지한 문단 {len(unlike)}개: {unlike[:20]}")
    if dropped:
        print(f"토큰이 사라져 원문을 유지한 문단 {len(dropped)}개: {dropped[:20]}")
    if broken:
        print(f"백틱이 깨져 원문을 유지한 문단 {len(broken)}개: {broken[:20]}")
    if leftover:
        print(f"표에 없는 토큰이 남은 문단: {leftover}")


FACTS = [
    ("따옴표 문구", re.compile(r'"([^"\n]{2,80})"')),
    ("인라인 코드", re.compile(r'`([^`\n]{1,60})`')),
    ("숫자", re.compile(r'(?<![\w.])(\d[\d,.]*)(?![\w.])')),
    ("각주", re.compile(r'(\[\^\w+\])')),
]


def cmd_check(args) -> None:
    a = Path(args.src).read_text(encoding="utf-8")
    b = Path(args.new).read_text(encoding="utf-8")
    bad = 0
    for label, rx in FACTS:
        ca = Counter(m.group(1) for m in rx.finditer(a))
        cb = Counter(m.group(1) for m in rx.finditer(b))
        lost = [(x, ca[x] - cb.get(x, 0)) for x in ca if ca[x] > cb.get(x, 0)]
        new = [(x, cb[x] - ca.get(x, 0)) for x in cb if cb[x] > ca.get(x, 0)]
        if lost or new:
            bad += 1
            print(f"\n── {label}")
            for x, k in lost[:15]:
                print(f"  사라짐 x{k}: {x[:70]}")
            for x, k in new[:15]:
                print(f"  새로생김 x{k}: {x[:70]}")
    if not bad:
        print("내용 지표 이상 없음 (따옴표·인라인코드·숫자·각주 그대로)")
    sys.exit(1 if bad else 0)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract")
    e.add_argument("src")
    e.add_argument("--out", required=True)

    m = sub.add_parser("merge")
    m.add_argument("src")
    m.add_argument("reply")
    m.add_argument("--out", required=True)
    m.add_argument("--mask")
    m.add_argument("--sent")
    m.add_argument("--min-ratio", type=float, default=0.8)
    m.add_argument("--max-ratio", type=float, default=2.6)
    m.add_argument("--min-sim", type=float, default=0.35)

    c = sub.add_parser("check")
    c.add_argument("src")
    c.add_argument("new")

    args = ap.parse_args()
    {"extract": cmd_extract, "merge": cmd_merge, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    main()


