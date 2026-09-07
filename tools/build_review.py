#!/usr/bin/env python3
"""윤문 검수 페이지를 만든다 (Artifact 로 발행).

collect_edits.py 가 뽑은 변경 목록 + 파일별 점수를 받아
"바뀐 문장만" 훑어볼 수 있는 HTML 을 만든다.
검수자가 'AI 티 남음' 을 누르면 db 에 쌓이고, 그걸 읽어 탐지 범위를 넓힌다.

usage: python tools/build_review.py --edits edits.json --scores scores.json --out review.html
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

STYLE = """
:root{--bg:#faf9f7;--panel:#fff;--ink:#1f2225;--mut:#6c7076;--line:#e6e2db;
--accent:#0d9488;--accent-soft:#0d94881a;--del:#b4413c;--del-bg:#b4413c0f;
--add:#2f7a5e;--add-bg:#2f7a5e0f;--shadow:0 1px 2px rgba(31,34,37,.05),0 6px 20px rgba(31,34,37,.06)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15181b;--panel:#1d2125;
--ink:#e9eae7;--mut:#9aa0a6;--line:#2c3238;--accent:#2dd4bf;--accent-soft:#2dd4bf1f;
--del:#e88a85;--del-bg:#e88a8514;--add:#6ec9a4;--add-bg:#6ec9a414;
--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35)}}
:root[data-theme="dark"]{--bg:#15181b;--panel:#1d2125;--ink:#e9eae7;--mut:#9aa0a6;--line:#2c3238;
--accent:#2dd4bf;--accent-soft:#2dd4bf1f;--del:#e88a85;--del-bg:#e88a8514;--add:#6ec9a4;
--add-bg:#6ec9a414;--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35)}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:'IBM Plex Sans KR',system-ui,sans-serif;line-height:1.65}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px 90px}
header.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 90%,transparent);
backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.tin{max-width:1000px;margin:0 auto;padding:16px 20px;display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center}
h1{font-family:'Gothic A1',sans-serif;font-weight:800;font-size:clamp(18px,2.4vw,24px);margin:0;letter-spacing:-.01em}
.big{margin-left:auto;display:flex;align-items:center;gap:10px;font-family:'IBM Plex Mono',monospace;font-size:13px;flex-wrap:wrap}
.pill{border:1px solid var(--line);background:var(--panel);border-radius:999px;padding:5px 12px;white-space:nowrap}
.pill.up{border-color:var(--accent);color:var(--accent)}
.filters{display:flex;gap:8px;flex-wrap:wrap;padding:12px 0 0}
.filters button{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--panel);
color:var(--ink);border-radius:999px;padding:6px 14px;cursor:pointer}
.filters button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
.addbox{margin:18px 0 6px;background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:14px 16px;box-shadow:var(--shadow)}
.addbox h3{font-family:'Gothic A1',sans-serif;font-size:14px;margin:0 0 4px}
.addbox p{margin:0 0 10px;color:var(--mut);font-size:13px}
.addrow{display:flex;gap:8px;flex-wrap:wrap}
.addrow input{flex:1 1 260px;font:inherit;font-size:14px;padding:9px 12px;border:1px solid var(--line);
border-radius:9px;background:var(--bg);color:var(--ink)}
.addrow button{font:inherit;font-size:14px;font-weight:600;border:0;background:var(--accent);color:#fff;
border-radius:9px;padding:9px 18px;cursor:pointer}
.file{margin-top:30px}
.file h2{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-family:'Gothic A1',sans-serif;
font-size:16px;margin:0 0 10px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.fn{font-family:'IBM Plex Mono',monospace;color:var(--accent);background:var(--accent-soft);
padding:2px 8px;border-radius:6px;font-size:13px}
.sc{font-family:'IBM Plex Mono',monospace;font-size:13px}
.sc .lo{color:var(--del)} .sc .hi{color:var(--add)} .sc .ar{color:var(--mut);margin:0 5px}
.cnt{margin-left:auto;color:var(--mut);font-size:12.5px;font-weight:400}
.chg{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:11px;
padding:12px 14px 34px;margin-bottom:10px;box-shadow:var(--shadow)}
.side{display:flex;gap:10px;align-items:flex-start}
.side+.side{margin-top:8px;padding-top:8px;border-top:1px dashed var(--line)}
.side p{margin:0;font-size:14.5px;word-break:break-word}
.side.b p{color:var(--del)} .side.a p{color:var(--add)}
.tag{flex:0 0 auto;font-family:'Gothic A1',sans-serif;font-size:11px;font-weight:700;padding:1px 7px;
border-radius:5px;margin-top:3px}
.side.b .tag{color:var(--del);background:var(--del-bg)}
.side.a .tag{color:var(--add);background:var(--add-bg)}
.flag{position:absolute;right:10px;bottom:9px;font:inherit;font-size:12px;border:1px solid var(--line);
background:var(--bg);color:var(--mut);border-radius:7px;padding:4px 10px;cursor:pointer;opacity:.8}
.chg:hover .flag{opacity:1}
.flag[aria-pressed="true"]{background:var(--del);border-color:var(--del);color:#fff;opacity:1}
.chg[data-kind="bold_only"]{display:none}
body.showbold .chg[data-kind="bold_only"]{display:block}
.chg[data-kind="bold_only"] .side p{font-size:13.5px}
#flagged{margin-top:26px;background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:14px 16px;box-shadow:var(--shadow)}
#flagged h3{font-family:'Gothic A1',sans-serif;font-size:14px;margin:0 0 8px}
#flagged ul{margin:0;padding-left:18px;font-size:13.5px}
#flagged li{margin-bottom:5px}
.note{color:var(--mut);font-size:12.5px;margin-top:6px;min-height:1em}
footer{margin-top:40px;padding-top:18px;border-top:1px solid var(--line);color:var(--mut);font-size:12.5px;line-height:1.75}
@media (max-width:560px){.big{margin-left:0;width:100%}}
"""

SCRIPT = """
(function(){
  var body=document.body, rw=document.getElementById('f-rw'), all=document.getElementById('f-all');
  function mode(showBold){ body.classList.toggle('showbold', showBold);
    rw.setAttribute('aria-pressed', String(!showBold)); all.setAttribute('aria-pressed', String(showBold)); }
  rw.onclick=function(){mode(false);}; all.onclick=function(){mode(true);};

  function escape(s){ return String(s||'').replace(/[<>&]/g,function(c){
    return c==='<'?'&lt;':c==='>'?'&gt;':'&amp;'; }); }

  var listEl=document.getElementById('flaglist'), box=document.getElementById('flagged');
  function render(items){
    if(!items.length){ box.hidden=true; return; }
    box.hidden=false;
    listEl.innerHTML = items.map(function(x){
      var head = x.kind==='phrase' ? '<b>문구</b> ' : '<b>'+escape(x.file)+'</b> ';
      return '<li>'+head+escape(x.text)+'</li>';
    }).join('');
  }

  var msg=document.getElementById('phmsg');
  var dbp = (window.claude && window.claude.use) ? window.claude.use('db') : Promise.resolve(null);
  dbp.then(function(db){
    if(!db){ msg.textContent='(이 화면에서는 저장 기능을 쓸 수 없습니다. 문구를 채팅으로 알려 주세요.)'; return; }

    db.collection('flags').onSnapshot(function(snap){
      var items = snap.docs.map(function(d){ return d.data(); });
      render(items);
      var seen={}; items.forEach(function(x){ if(x.cid) seen[x.cid]=1; });
      document.querySelectorAll('.flag').forEach(function(b){
        if(seen[b.dataset.id]) b.setAttribute('aria-pressed','true');
      });
    }, function(){});

    document.querySelectorAll('.flag').forEach(function(b){
      b.onclick=function(){
        if(b.getAttribute('aria-pressed')==='true') return;
        b.setAttribute('aria-pressed','true');
        db.collection('flags').add({kind:'sentence', cid:b.dataset.id, file:b.dataset.file,
                                    text:b.dataset.txt, at:Date.now()}).catch(function(){
          b.setAttribute('aria-pressed','false');
        });
      };
    });

    var inp=document.getElementById('ph');
    function addPhrase(){
      var v=(inp.value||'').trim(); if(!v) return;
      db.collection('flags').add({kind:'phrase', text:v, at:Date.now()}).then(function(){
        inp.value=''; msg.textContent='저장했습니다.';
      }).catch(function(){ msg.textContent='저장하지 못했습니다.'; });
    }
    document.getElementById('add').onclick=addPhrase;
    inp.addEventListener('keydown',function(e){ if(e.key==='Enter') addPhrase(); });
  });
})();
"""


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def build(edits: dict, scores: dict) -> str:
    files = edits["files"]
    ov = scores.get("overall", {})
    per = scores.get("files", {})

    sections = []
    for f in files:
        name = f["file"]
        sc = per.get(name, {})
        b, a = sc.get("before"), sc.get("after")
        badge = ""
        if b is not None:
            badge = (f'<span class="sc"><b class="lo">{b}</b>'
                     f'<span class="ar">&rarr;</span><b class="hi">{a}</b></span>')
        rows = []
        for i, c in enumerate(f["changes"]):
            cid = f"{name}:{i}"
            bt = esc(c["before"]) or "<i>(없음)</i>"
            at = esc(c["after"]) or "<i>(삭제됨)</i>"
            rows.append(
                f'<div class="chg" data-kind="{c["kind"]}">'
                f'<div class="side b"><span class="tag">전</span><p>{bt}</p></div>'
                f'<div class="side a"><span class="tag">후</span><p>{at}</p></div>'
                f'<button class="flag" data-id="{esc(cid)}" data-file="{esc(name)}" '
                f'data-txt="{esc(c["after"][:400])}">AI 티 남음</button></div>'
            )
        sections.append(
            f'<section class="file"><h2><span class="fn">{esc(name)}</span>{badge}'
            f'<span class="cnt">재작성 {f["n_rewrite"]} · 볼드 {f["n_bold"]}</span></h2>'
            f'<div class="rows">{"".join(rows)}</div></section>'
        )

    head = (
        "<title>윤문 검수 — 나만의 지도</title>\n"
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        "family=Gothic+A1:wght@500;700;800&family=IBM+Plex+Sans+KR:wght@400;500;600"
        '&family=IBM+Plex+Mono:wght@500&display=swap">\n'
        f"<style>{STYLE}</style>\n"
    )
    header = (
        '<header class="top"><div class="tin">'
        "<h1>윤문 검수 — 바뀐 문장만</h1>"
        f'<div class="big"><span class="pill">파일 {len(files)}</span>'
        f'<span class="pill">재작성 {edits.get("total_rewrite", 0)}</span>'
        f'<span class="pill">볼드 {edits.get("total_bold", 0)}</span>'
        f'<span class="pill up">{ov.get("before", "-")} &rarr; {ov.get("after", "-")}</span>'
        "</div></div></header>"
    )
    controls = (
        '<div class="filters">'
        '<button id="f-rw" aria-pressed="true">문장 재작성만</button>'
        '<button id="f-all" aria-pressed="false">볼드 정리도 보기</button></div>'
        '<div class="addbox"><h3>메트릭이 놓친 표현 알려주기</h3>'
        "<p>읽다가 “이것도 AI 티인데” 싶은 문구를 그대로 적어 주세요. "
        "탐지 범위에 넣어 교재 전체를 다시 훑겠습니다.</p>"
        '<div class="addrow"><input id="ph" autocomplete="off" '
        'placeholder="예: 결과물을 먼저 구경하는 시간입니다">'
        '<button id="add">추가</button></div>'
        '<p class="note" id="phmsg"></p></div>'
        '<div id="flagged" hidden><h3>지금까지 표시한 것</h3><ul id="flaglist"></ul></div>'
    )
    footer = (
        "<footer>전 = 윤문 전, 후 = 윤문 후. 코드·헤딩·그림·캡션은 건드리지 않았습니다.<br>"
        "표시하신 문구는 저장되어, 다음 작업 때 탐지 규칙(<code>tools/style_patterns.json</code>)에 "
        "추가됩니다.</footer>"
    )
    return (head + header + '<div class="wrap">' + controls + "".join(sections)
            + footer + "</div>\n<script>" + SCRIPT + "</script>\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edits", required=True)
    ap.add_argument("--scores", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    edits = json.loads(Path(args.edits).read_text(encoding="utf-8"))
    scores = json.loads(Path(args.scores).read_text(encoding="utf-8"))
    Path(args.out).write_text(build(edits, scores), encoding="utf-8")
    print(f"{args.out} 작성 ({len(edits['files'])}개 파일)")


if __name__ == "__main__":
    main()
