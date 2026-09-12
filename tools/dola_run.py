#!/usr/bin/env python3
"""Dola 데스크톱(Cici)에 CDP 로 붙어 장별 윤문을 통째로 돌린다.

먼저 Cici 를 디버깅 포트와 함께 띄워 둔다.

    Stop-Process -Name Cici -Force
    Start-Process "C:\\Users\\seong\\AppData\\Local\\Cici\\Application\\Cici.exe" `
        -ArgumentList "--remote-debugging-port=9333"

그 다음:

    py tools/dola_run.py ch08 ch09 ch10 ...
    py tools/dola_run.py --rest          # 아직 안 된 장 전부

각 장마다 새 대화를 열고 prose/chNN.txt 를 첨부해 보낸 뒤, 답이 끝나면
prose/replies/chNN.txt 로 저장하고 이어서 되꽂기·검사까지 한다.
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROSE = ROOT / "prose"
REPLIES = PROSE / "replies"
CDP = "http://127.0.0.1:9333"

# 답이 끝났는지 보는 기준
IDLE_SECONDS = 8.0          # 글자 수가 이만큼 안 늘면 끝난 것으로 본다
MAX_WAIT = 420.0            # 한 장 최대 대기

EXTRACT = r"""
() => {
  const b = document.body.innerText;
  const idx = [...b.matchAll(/^\[1\]\s/gm)].map(m => m.index);
  if (!idx.length) return { max: 0, text: '' };
  let r = b.slice(idx[idx.length - 1]);
  for (const cut of ['\nMessage', '\n메시지 작성', '\nFast\n', '\n고속\n']) {
    const i = r.indexOf(cut);
    if (i > 0) r = r.slice(0, i);
  }
  r = r.trim();
  const nums = [...r.matchAll(/^\[(\d+)\]/gm)].map(x => +x[1]);
  return { max: nums.length ? Math.max(...nums) : 0, text: r, blocks: idx.length };
}
"""

NEW_CHAT = r"""
() => {
  const t = [...document.querySelectorAll('a,button,[role=button],div')]
    .filter(e => {
      const s = (e.innerText || '').trim();
      return s === 'New Chat' || s === '새 채팅';
    });
  if (!t.length) return false;
  t[0].click();
  return true;
}
"""

SEND = r"""
() => {
  const bs = [...document.querySelectorAll('button')].filter(b => {
    const r = b.getBoundingClientRect();
    return r.width >= 24 && r.width <= 52 && r.right > innerWidth * 0.6
           && r.bottom > innerHeight - 160;
  });
  if (!bs.length) return 'nobtn';
  if (bs.every(b => b.disabled)) return 'disabled';
  bs.forEach(b => b.click());
  return 'clicked';
}
"""


ATTACH_COUNT = r"""
() => {
  const t = document.body.innerText;
  const m = t.match(/and other (\d+) files/);
  if (m) return 1 + (+m[1]);
  return (t.match(/\b[\w-]+\.txt\b/g) || []).length;
}
"""


def expected_count(path: Path) -> int:
    txt = path.read_text(encoding="utf-8")
    nums = [int(m.group(1)) for m in re.finditer(r"^\[(\d+)\]", txt, re.M)]
    return max(nums) if nums else 0


def chat_page(browser):
    for ctx in browser.contexts:
        for pg in ctx.pages:
            if "dola-chat" in pg.url:
                return pg
    raise RuntimeError("Dola 채팅 화면을 찾지 못했습니다")


def run_one(pg, ch: str, retry: bool = False) -> bool:
    src = (PROSE / "retry" / f"{ch}.txt") if retry else (PROSE / f"{ch}.txt")
    if not src.exists():
        print(f"{ch}: 보낼 산문 없음")
        return False
    want = expected_count(src)

    # 화면을 새로 띄워야 앞 장의 첨부 파일이 남지 않는다
    pg.goto("chrome://dola-chat/chat")
    time.sleep(4.0)
    pg.evaluate(NEW_CHAT)
    time.sleep(2.5)

    inp = pg.locator("input[type=file]").first
    inp.set_input_files(str(src))
    time.sleep(3.0)

    n_att = pg.evaluate(ATTACH_COUNT)
    if n_att != 1:
        print(f"{ch}: 첨부가 {n_att}개라 건너뜁니다")
        return False

    for _ in range(10):
        state = pg.evaluate(SEND)
        if state == "clicked":
            break
        time.sleep(2.0)
    else:
        print(f"{ch}: 전송 버튼을 누르지 못했습니다")
        return False

    t0 = time.time()
    last_len, last_change = 0, time.time()
    while time.time() - t0 < MAX_WAIT:
        time.sleep(3.0)
        got = pg.evaluate(EXTRACT)
        n = len(got["text"])
        if n != last_len:
            last_len, last_change = n, time.time()
        done = got["max"] >= want and (time.time() - last_change) > IDLE_SECONDS
        if done:
            break
    else:
        print(f"{ch}: 시간 초과 (max={got['max']}/{want})")

    got = pg.evaluate(EXTRACT)
    if got["max"] < want:
        print(f"{ch}: 문단이 모자랍니다 {got['max']}/{want} — 그래도 저장합니다")
    REPLIES.mkdir(parents=True, exist_ok=True)
    if retry:
        # 같은 번호를 덮어쓰도록 기존 응답 뒤에 이어 붙인다
        base = ROOT / "윤문비교" / ch / "Dola_응답.txt"
        old = base.read_text(encoding="utf-8") if base.exists() else ""
        merged = old.rstrip() + "\n\n" + got["text"]
        (REPLIES / f"{ch}.txt").write_text(merged, encoding="utf-8")
    else:
        (REPLIES / f"{ch}.txt").write_text(got["text"], encoding="utf-8")
    print(f"{ch}: 받음 {len(got['text']):,}자 · 문단 {got['max']}/{want} "
          f"({int(time.time() - t0)}초)")
    return True


def merge(chs: list[str]) -> None:
    if not chs:
        return
    p = subprocess.run([sys.executable, "tools/dola_merge.py", *chs], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print((p.stdout or "") + (p.stderr or ""))


def main() -> None:
    args = sys.argv[1:]
    retry = "--retry" in args
    args = [a for a in args if a != "--retry"]
    if args == ["--rest"]:
        args = [f"ch{i:02d}" for i in range(29)
                if (PROSE / f"ch{i:02d}.txt").exists()
                and not (ROOT / "윤문비교" / f"ch{i:02d}" / "D_Dola_보정.md").exists()]
        print("남은 장:", " ".join(args))

    done: list[str] = []
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(CDP)
        pg = chat_page(b)
        for ch in args:
            try:
                if run_one(pg, ch, retry=retry):
                    done.append(ch)
                    merge([ch])
            except Exception as e:
                print(f"{ch}: 실패 — {e}")
    print("\n끝난 장:", " ".join(done) if done else "없음")


if __name__ == "__main__":
    main()
