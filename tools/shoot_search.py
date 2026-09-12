#!/usr/bin/env python3
"""19장 검색 결과 화면을 찍는다 ('성수동 카페' 검색 결과 목록)."""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "그림작업"

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 860},
                        device_scale_factor=2, locale="ko-KR")
    page = ctx.new_page()
    page.goto("http://localhost:5173/", wait_until="networkidle")
    page.wait_for_timeout(4000)
    page.fill("#search-input", "성수동 카페")
    page.click("#btn-search")
    page.wait_for_timeout(3500)
    page.screenshot(path=str(OUT / "shot_19_4.png"))
    b.close()
print("shot_19_4.png 찍음")
