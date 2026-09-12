#!/usr/bin/env python3
"""Dola 가 토큰을 지워 원문으로 되돌린 문단만 다시 보낼 파일을 만든다.

    py tools/dola_retry.py ch11 ch12 ch13
    py tools/dola_retry.py --all

같은 번호를 그대로 쓰므로, 돌아온 답을 윤문비교/chNN/Dola_응답.txt 뒤에
이어 붙인 뒤 다시 되꽂으면 그 문단만 새 것으로 바뀐다.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dola_prep import HEADER_LINES, parse_reply, prose_items  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "prose" / "retry"


def one(ch: str) -> int:
    orig_p = ROOT / "chapters" / f"{ch}.md"
    cur_p = ROOT / "윤문비교" / ch / "D_Dola_보정.md"
    sent_p = ROOT / "윤문비교" / ch / "보낼산문.txt"
    if not (orig_p.exists() and cur_p.exists() and sent_p.exists()):
        print(f"{ch}: 자료 부족")
        return 0

    orig = dict(prose_items(orig_p.read_text(encoding="utf-8")))
    cur = dict(prose_items(cur_p.read_text(encoding="utf-8")))
    sent = parse_reply(sent_p.read_text(encoding="utf-8"))

    todo = [i for i in orig if cur.get(i) == orig[i] and i in sent]
    if not todo:
        print(f"{ch}: 다시 보낼 문단 없음")
        return 0

    body = "\n\n".join(f"[{i}] {sent[i]}" for i in todo)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{ch}.txt").write_text("\n".join(HEADER_LINES) + body, encoding="utf-8")
    print(f"{ch}: 다시 보낼 문단 {len(todo)}개 · {len(body):,}자")
    return len(todo)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--all"]:
        args = sorted(p.name for p in (ROOT / "윤문비교").iterdir()
                      if p.is_dir() and p.name.startswith("ch")
                      and (p / "D_Dola_보정.md").exists())
    for ch in args:
        one(ch)
