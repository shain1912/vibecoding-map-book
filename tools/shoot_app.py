#!/usr/bin/env python3
"""지도 앱을 띄워 놓고 필요한 화면을 찍는다.

    py tools/shoot_app.py

18.1  필터 없이 모든 마커가 섞인 지도  (사이드바 접음)
18.4  카페 필터만 켠 지도             (사이드바 접음)
22.2  완성된 사이드바 장소 목록        (전체)
22.3  필터와 목록이 함께 걸러진 화면    (카페)
"""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "그림작업"
URL = "http://localhost:5173/"


def settle(page, ms=2500):
    page.wait_for_timeout(ms)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(viewport={"width": 1440, "height": 860},
                            device_scale_factor=2, locale="ko-KR")
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle")
        settle(page, 4000)

        # 사이드바를 접고 지도만 — 18.1
        page.evaluate("document.getElementById('sidebar').classList.add('collapsed'); document.getElementById('btn-expand').hidden=false")
        settle(page)
        page.screenshot(path=str(OUT / "shot_18_1.png"))

        # 카페 필터만 — 18.4 (접힌 상태에서 다시 펴서 누르고 접는다)
        page.evaluate("document.getElementById('sidebar').classList.remove('collapsed'); document.getElementById('btn-expand').hidden=true")
        settle(page, 1200)
        page.click('.filter-btn[data-category="cafe"]')
        settle(page, 1800)
        page.evaluate("document.getElementById('sidebar').classList.add('collapsed'); document.getElementById('btn-expand').hidden=false")
        settle(page)
        page.screenshot(path=str(OUT / "shot_18_4.png"))

        # 사이드바 목록 — 22.2 (전체)
        page.evaluate("document.getElementById('sidebar').classList.remove('collapsed'); document.getElementById('btn-expand').hidden=true")
        settle(page, 1200)
        page.click('.filter-btn[data-category="all"]')
        settle(page, 1800)
        page.screenshot(path=str(OUT / "shot_22_2.png"))

        # 필터와 목록이 함께 걸러진 화면 — 22.3
        page.click('.filter-btn[data-category="cafe"]')
        settle(page, 1800)
        page.screenshot(path=str(OUT / "shot_22_3.png"))

        b.close()
    for f in sorted(OUT.glob("shot_*.png")):
        print(f"{f.name} · {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
