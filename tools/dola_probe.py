#!/usr/bin/env python3
"""Dola 데스크톱(Cici) 채팅 화면 구조를 살핀다."""
from playwright.sync_api import sync_playwright

JS = r"""
() => {
  const eds = [...document.querySelectorAll('[contenteditable]')].map(e => ({
    tag: e.tagName, cls: String(e.className).slice(0, 50), len: e.textContent.length
  }));
  const files = [...document.querySelectorAll('input[type=file]')].map(e => e.accept.slice(0, 60));
  const btns = [...document.querySelectorAll('button')].map(e => {
    const r = e.getBoundingClientRect();
    return { t: (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 14),
             x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), d: e.disabled };
  }).filter(o => o.w > 0);
  return { url: location.href, eds, files, nbtn: btns.length,
           bottom: btns.filter(o => o.y > innerHeight - 160).slice(0, 12),
           text: document.body.innerText.slice(0, 300) };
}
"""

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9333")
    for ctx in b.contexts:
        for pg in ctx.pages:
            if "dola-chat" in pg.url:
                import json
                print(json.dumps(pg.evaluate(JS), ensure_ascii=False, indent=1))
