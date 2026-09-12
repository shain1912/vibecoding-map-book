#!/usr/bin/env python3
"""지금 원고와 Dola 윤문본을 장별로 나란히 보여 주는 HTML 을 만든다.

    py tools/build_compare.py ch03 ch04 --out 윤문비교/원본_대_Dola.html
"""
from __future__ import annotations

import argparse
import difflib
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STRUCT = re.compile(r'^﻿?(\s*#{1,6}\s|\s*!\[|\s*///|\s*!!!|\s*```|\s*\||\s*>\s|\s*\[\^|\s*---\s*$|\s*[-*+]\s|\s*\d+\.\s)')


def mark(base: str, other: str) -> str:
    sm = difflib.SequenceMatcher(None, base, other, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        seg = html.escape(other[j1:j2])
        if tag == "equal":
            out.append(seg)
        elif seg:
            out.append(f"<mark>{seg}</mark>")
    return "".join(out)


CSS = """
:root{--bg:#faf9f7;--panel:#fff;--ink:#1f2225;--mut:#6c7076;--line:#e6e2db;
--base:#5b6470;--a:#9a4f2e;--hl:#ffe9a8;--shadow:0 1px 2px rgba(31,34,37,.05),0 6px 18px rgba(31,34,37,.06)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15181b;--panel:#1d2125;
--ink:#e9eae7;--mut:#9aa0a6;--line:#2c3238;--base:#93a0ae;--a:#e09a76;--hl:#5a4a1e;
--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 22px rgba(0,0,0,.35)}}
:root[data-theme="dark"]{--bg:#15181b;--panel:#1d2125;--ink:#e9eae7;--mut:#9aa0a6;--line:#2c3238;
--base:#93a0ae;--a:#e09a76;--hl:#5a4a1e;--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 22px rgba(0,0,0,.35)}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:'IBM Plex Sans KR',system-ui,sans-serif;line-height:1.75}
.wrap{max-width:1500px;margin:0 auto;padding:0 20px 80px}
header.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 92%,transparent);
backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.tin{max-width:1500px;margin:0 auto;padding:14px 20px;display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}
h1{font-family:'Gothic A1',sans-serif;font-weight:800;font-size:clamp(17px,2vw,22px);margin:0}
.sub{color:var(--mut);font-size:13px}
.legend{margin-left:auto;display:flex;gap:14px;font-size:12.5px;color:var(--mut);flex-wrap:wrap}
.legend .k0{color:var(--base)} .legend .k1{color:var(--a)}
h2.ch{font-family:'Gothic A1',sans-serif;font-size:17px;margin:34px 0 4px;padding-top:10px;border-top:2px solid var(--line)}
table{width:100%;border-collapse:collapse;margin-top:10px;table-layout:fixed}
th{position:sticky;top:56px;background:var(--bg);font-family:'Gothic A1',sans-serif;font-size:13.5px;
text-align:left;padding:9px 12px;border-bottom:2px solid var(--line);z-index:10}
th.c0,td.c0{color:var(--base)} th.c1,td.c1{color:var(--a)}
td{vertical-align:top;padding:13px 12px;border-bottom:1px solid var(--line);font-size:14.3px;
word-break:break-word;width:50%}
tr:hover td{background:color-mix(in srgb,var(--panel) 60%,transparent)}
mark{background:var(--hl);color:inherit;border-radius:3px;padding:0 1px}
.same td{opacity:.45}
.n{color:var(--mut);font-family:'IBM Plex Mono',monospace;font-size:11.5px;margin-right:6px}
footer{margin-top:36px;color:var(--mut);font-size:12.5px;line-height:1.8}
@media (max-width:900px){table,thead,tbody,tr,td,th{display:block;width:100%}
thead{display:none}td{width:100%;border:0;padding:8px 12px}
td::before{content:attr(data-l);display:block;font-family:'Gothic A1',sans-serif;font-size:11px;
color:var(--mut);margin-bottom:3px}
tr{display:block;border-bottom:1px solid var(--line);padding:8px 0}}
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapters", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--changed-only", action="store_true")
    args = ap.parse_args()

    parts = []
    total_changed = 0
    total_lines = 0
    for ch in args.chapters:
        src = ROOT / "chapters" / f"{ch}.md"
        new = ROOT / "윤문비교" / ch / "D_Dola_보정.md"
        if not new.exists():
            continue
        a = src.read_text(encoding="utf-8-sig").split("\n")
        b = new.read_text(encoding="utf-8-sig").split("\n")
        trs = []
        for i, (x, y) in enumerate(zip(a, b), 1):
            if not x.strip() or STRUCT.match(x):
                continue
            total_lines += 1
            same = x == y
            if same:
                if args.changed_only:
                    continue
            else:
                total_changed += 1
            cls = ' class="same"' if same else ""
            trs.append(
                f'<tr{cls}><td class="c0" data-l="지금 원고"><span class="n">{i}</span>{html.escape(x)}</td>'
                f'<td class="c1" data-l="Dola 윤문">{mark(x, y)}</td></tr>'
            )
        title = re.sub(r'^﻿?#\s*', '', a[0]).strip()
        parts.append(
            f'<h2 class="ch">{html.escape(ch)} · {html.escape(title)}</h2>'
            '<table><thead><tr><th class="c0">지금 원고</th><th class="c1">Dola 윤문</th></tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table>'
        )

    head = ("<title>원고 대 Dola 윤문</title>\n"
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
            'family=Gothic+A1:wght@500;700;800&family=IBM+Plex+Sans+KR:wght@400;500;600'
            '&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
            f"<style>{CSS}</style>\n")
    doc = (
        head +
        '<header class="top"><div class="tin">'
        '<h1>원고 대 Dola 윤문</h1>'
        f'<span class="sub">본문 {total_lines}줄 중 {total_changed}줄이 달라졌습니다</span>'
        '<div class="legend"><span class="k0"><b>왼쪽</b> 지금 원고</span>'
        '<span class="k1"><b>오른쪽</b> Dola가 다듬은 것</span>'
        '<span>노란 표시 = 달라진 글자</span></div></div></header>'
        '<div class="wrap">' + "".join(parts) +
        '<footer>왼쪽이 지금 책에 들어 있는 문장, 오른쪽이 Dola가 돌려준 문장입니다. '
        '헤딩·그림·코드·표는 애초에 보내지 않았으므로 여기 나오지 않습니다.<br>'
        '흐리게 보이는 줄은 Dola가 손대지 않은 줄입니다.</footer></div>'
    )
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(f"{args.out} 작성 · 본문 {total_lines}줄 · 달라진 줄 {total_changed}")


if __name__ == "__main__":
    main()
