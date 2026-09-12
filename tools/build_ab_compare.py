#!/usr/bin/env python3
"""원본 / A / B 세 벌을 문단 단위로 정렬해 한눈에 비교하는 HTML 을 만든다.

    py tools/build_ab_compare.py --out 윤문비교/ch01/한눈에비교.html
"""
from __future__ import annotations

import argparse
import difflib
import html
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def paras(text: str) -> list[str]:
    """문단 목록. 코드펜스는 통째로 한 덩어리로 둔다."""
    out, buf, in_code = [], [], False
    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            in_code = not in_code
            buf.append(ln)
            if not in_code:
                out.append("\n".join(buf)); buf = []
            continue
        if in_code:
            buf.append(ln); continue
        if not ln.strip():
            if buf:
                out.append("\n".join(buf)); buf = []
        else:
            buf.append(ln)
    if buf:
        out.append("\n".join(buf))
    return [p.strip() for p in out if p.strip()]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", "", s)
    return re.sub(r"[·•\-–—~…\"'“”‘’()\[\]{}:;,.!?*]", "", s)


def slice_range(ps: list[str], start_pat: str, end_pat: str | None) -> list[str]:
    s = next((i for i, p in enumerate(ps) if re.match(start_pat, p)), 0)
    e = len(ps)
    if end_pat:
        e = next((i for i, p in enumerate(ps) if i > s and re.match(end_pat, p)), len(ps))
    return ps[s:e]


def align3(base: list[str], a: list[str], b: list[str]) -> list[tuple[str, str, str]]:
    """원본을 기준으로 A·B 를 각각 붙인다."""
    def pair(src: list[str], dst: list[str]) -> dict[int, str]:
        m: dict[int, str] = {}
        used: set[int] = set()
        sm = difflib.SequenceMatcher(None, [norm(x) for x in src], [norm(x) for x in dst],
                                     autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                for k in range(i2 - i1):
                    m[i1 + k] = dst[j1 + k]; used.add(j1 + k)
                continue
            for i in range(i1, i2):
                best, bj = 0.0, None
                for j in range(j1, j2):
                    if j in used:
                        continue
                    r = difflib.SequenceMatcher(None, norm(src[i]), norm(dst[j])).ratio()
                    if r > best:
                        best, bj = r, j
                if bj is not None and best >= 0.35:
                    m[i] = dst[bj]; used.add(bj)
                else:
                    m[i] = ""
        return m

    ma, mb = pair(base, a), pair(base, b)
    return [(base[i], ma.get(i, ""), mb.get(i, "")) for i in range(len(base))]


def mark(base: str, other: str) -> str:
    """base 대비 other 에서 바뀐 글자를 표시한다."""
    if not other:
        return '<span class="gone">— 없음 —</span>'
    sm = difflib.SequenceMatcher(None, base, other, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        seg = html.escape(other[j1:j2])
        if tag == "equal":
            out.append(seg)
        elif seg:
            out.append(f'<mark>{seg}</mark>')
    return "".join(out)


CSS = """
:root{--bg:#faf9f7;--panel:#fff;--ink:#1f2225;--mut:#6c7076;--line:#e6e2db;
--base:#5b6470;--a:#9a4f2e;--b:#2f6b52;--hl:#ffe9a8;--shadow:0 1px 2px rgba(31,34,37,.05),0 6px 18px rgba(31,34,37,.06)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15181b;--panel:#1d2125;
--ink:#e9eae7;--mut:#9aa0a6;--line:#2c3238;--base:#93a0ae;--a:#e09a76;--b:#7fc9a6;--hl:#5a4a1e;
--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 22px rgba(0,0,0,.35)}}
:root[data-theme="dark"]{--bg:#15181b;--panel:#1d2125;--ink:#e9eae7;--mut:#9aa0a6;--line:#2c3238;
--base:#93a0ae;--a:#e09a76;--b:#7fc9a6;--hl:#5a4a1e;--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 22px rgba(0,0,0,.35)}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:'IBM Plex Sans KR',system-ui,sans-serif;line-height:1.7}
.wrap{max-width:1500px;margin:0 auto;padding:0 20px 80px}
header.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 92%,transparent);
backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.tin{max-width:1500px;margin:0 auto;padding:16px 20px;display:flex;gap:18px;align-items:baseline;flex-wrap:wrap}
h1{font-family:'Gothic A1',sans-serif;font-weight:800;font-size:clamp(18px,2.2vw,23px);margin:0}
.sub{color:var(--mut);font-size:13px}
.legend{margin-left:auto;display:flex;gap:14px;font-size:12.5px;color:var(--mut);flex-wrap:wrap}
.legend b{font-weight:600}
.legend .k0{color:var(--base)} .legend .k1{color:var(--a)} .legend .k2{color:var(--b)}
table{width:100%;border-collapse:collapse;margin-top:18px;table-layout:fixed}
th{position:sticky;top:62px;background:var(--bg);font-family:'Gothic A1',sans-serif;font-size:13.5px;
text-align:left;padding:10px 12px;border-bottom:2px solid var(--line);z-index:10}
th.c0{color:var(--base)} th.c1{color:var(--a)} th.c2{color:var(--b)}
td{vertical-align:top;padding:14px 12px;border-bottom:1px solid var(--line);font-size:14.3px;
word-break:break-word;width:33.33%}
tr:hover td{background:color-mix(in srgb,var(--panel) 60%,transparent)}
td.c0{color:var(--base)} td.c1{color:var(--a)} td.c2{color:var(--b)}
mark{background:var(--hl);color:inherit;border-radius:3px;padding:0 1px}
.gone{color:var(--mut);font-style:italic;opacity:.7}
code,.mono{font-family:'IBM Plex Mono',monospace;font-size:12.6px;background:color-mix(in srgb,var(--line) 45%,transparent);
padding:1px 5px;border-radius:4px;display:inline-block;word-break:break-all}
.struct td{font-size:12.6px}
.n{color:var(--mut);font-family:'IBM Plex Mono',monospace;font-size:11.5px}
.stats{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap}
.pill{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:6px 14px;
font-size:12.5px;box-shadow:var(--shadow)}
footer{margin-top:30px;color:var(--mut);font-size:12.5px;line-height:1.8}
@media (max-width:900px){table,thead,tbody,tr,td,th{display:block;width:100%}
th{position:static;border:0;padding-bottom:2px}thead{display:none}
td{width:100%;border:0;padding:8px 12px}
td::before{content:attr(data-l);display:block;font-family:'Gothic A1',sans-serif;font-size:11px;
color:var(--mut);margin-bottom:3px}
tr{display:block;border-bottom:1px solid var(--line);padding:8px 0}}
"""


def is_struct(p: str) -> bool:
    return bool(re.match(r'^(#{1,6}\s|!\[|///|!!!|```|\||\s*[-*]\s)', p))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="윤문비교/ch01/원본.md")
    ap.add_argument("--a", default="윤문비교/ch01/A_Dola.md")
    ap.add_argument("--b", default="윤문비교/ch01/B_노하우.md")
    ap.add_argument("--start", default=r"^##\s*1\.1")
    ap.add_argument("--end", default=r"^##\s*1\.3")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    base = slice_range(paras((ROOT/args.base).read_text(encoding="utf-8")), args.start, args.end)
    a = paras((ROOT/args.a).read_text(encoding="utf-8"))
    b = slice_range(paras((ROOT/args.b).read_text(encoding="utf-8")), args.start, args.end)
    rows = align3(base, a, b)

    trs = []
    for i, (o, x, y) in enumerate(rows, 1):
        cls = ' class="struct"' if is_struct(o) else ""
        fmt = (lambda s: f'<span class="mono">{html.escape(s)}</span>') if is_struct(o) else None
        c0 = fmt(o) if fmt else html.escape(o)
        c1 = (fmt(x) if (fmt and x) else mark(o, x))
        c2 = (fmt(y) if (fmt and y) else mark(o, y))
        if fmt and not x:
            c1 = '<span class="gone">— 없음 —</span>'
        if fmt and not y:
            c2 = '<span class="gone">— 없음 —</span>'
        trs.append(f'<tr{cls}><td class="c0" data-l="원본"><span class="n">{i}</span> {c0}</td>'
                   f'<td class="c1" data-l="A · Dola">{c1}</td>'
                   f'<td class="c2" data-l="B · 노하우">{c2}</td></tr>')

    head = ("<title>윤문 A/B 한눈에 비교</title>\n"
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
            'family=Gothic+A1:wght@500;700;800&family=IBM+Plex+Sans+KR:wght@400;500;600'
            '&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
            f"<style>{CSS}</style>\n")
    html_doc = (
        head +
        '<header class="top"><div class="tin">'
        '<h1>윤문 A/B 한눈에 비교</h1>'
        '<span class="sub">1장 1.1~1.2절 · 문단 단위 정렬</span>'
        '<div class="legend"><span class="k0"><b>원본</b> 지금 원고</span>'
        '<span class="k1"><b>A</b> Dola에 통째로 맡김</span>'
        '<span class="k2"><b>B</b> 분석해서 얻은 노하우로 직접</span>'
        '<span>노란 표시 = 원본과 달라진 글자</span></div>'
        '</div></header>'
        '<div class="wrap">'
        '<table><thead><tr><th class="c0">원본</th><th class="c1">A · Dola</th>'
        '<th class="c2">B · 노하우</th></tr></thead><tbody>'
        + "".join(trs) +
        '</tbody></table>'
        '<footer>노란 표시는 원본 대비 바뀐 글자입니다. 회색 기울임 “— 없음 —”은 그 문단이 통째로 사라졌다는 뜻입니다.<br>'
        '고정폭으로 표시된 줄은 헤딩·그림·캡션·팁 상자처럼 본문이 아닌 구조입니다.</footer>'
        '</div>'
    )
    out = ROOT/args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")
    print(f"{args.out} 작성 · 문단 {len(rows)}개")


if __name__ == "__main__":
    main()
