#!/usr/bin/env python3
"""ch00~ch28을 모아 book.md 한 파일로 합치는 스크립트.

mkdocs 웹북과는 별개인 '한 파일' 산출물(인쇄/PDF 검토용)입니다.
부 구성은 mkdocs.yml 의 nav 와 일치시켜 둡니다.

사용법:
    python3 build_book.py
    python3 build_book.py --src chapters --out book.md
"""
import argparse
import re
from pathlib import Path

BOOK_TITLE = "바이브코딩으로 만드는 나만의 지도 웹"
BOOK_SUBTITLE = "AI 에이전트와 페어 코딩으로 카카오지도 기반 맛집·여행·데이트 지도 웹앱을 만들어 배포하기"

PARTS = [
    ("1부 — 바이브코딩 준비운동", range(1, 7)),
    ("2부 — 카카오 지도 첫걸음", range(7, 11)),
    ("3부 — 나만의 장소 지도 만들기", range(11, 20)),
    ("4부 — 한 단계 더", range(20, 24)),
    ("5부 — 세상에 공개하기", range(24, 27)),
    ("부록", range(27, 29)),
]

PAGE_BREAK = "\n<!-- 페이지 나눔 -->\n\n"


def chapter_title(text: str) -> str:
    m = re.search(r"^# (\d+장 .+)$", text, re.MULTILINE)
    if m:
        return m.group(1)
    m = re.search(r"^# (부록 .+)$", text, re.MULTILINE)
    return m.group(1) if m else "(제목 없음)"


def build_toc(sources: dict[int, str]) -> str:
    lines = ["## 목차", ""]
    if 0 in sources:
        lines.append(f"**{chapter_title(sources[0])}**")
        lines.append("")
    for part_name, ch_range in PARTS:
        lines.append(f"**{part_name}**")
        for ch in ch_range:
            if ch in sources:
                lines.append(f"- {chapter_title(sources[ch])}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="챕터 마크다운을 한 책으로 합칩니다.")
    parser.add_argument("--src", default="chapters", help="챕터 .md가 들어 있는 폴더 (기본: chapters)")
    parser.add_argument("--out", default="book.md", help="출력 파일 경로 (기본: book.md)")
    args = parser.parse_args()

    src_dir = Path(args.src)
    out_path = Path(args.out)

    chapters = {}
    for fp in sorted(src_dir.glob("ch*.md")):
        m = re.match(r"ch(\d+)\.md", fp.name)
        if not m:
            continue
        chapters[int(m.group(1))] = fp.read_text(encoding="utf-8")

    if not chapters:
        raise SystemExit(f"챕터 파일이 {src_dir}에 없습니다.")

    parts = [
        f"# {BOOK_TITLE}",
        "",
        f"**{BOOK_SUBTITLE}**",
        "",
        build_toc(chapters),
    ]
    for ch in sorted(chapters):
        parts.append(PAGE_BREAK)
        parts.append(chapters[ch])

    out_path.write_text("\n".join(parts), encoding="utf-8")
    total_chars = sum(len(t) for t in chapters.values())
    print(f"[OK] {len(chapters)}개 챕터 -> {out_path} ({total_chars:,}자)")


if __name__ == "__main__":
    main()
