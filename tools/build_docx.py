#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""교재 전체를 출판사 전달용 .docx 한 편으로 묶는다.

    py tools/build_docx.py                 # 원고_전체.docx
    py tools/build_docx.py --out 파일.docx

mkdocs-material 전용 문법을 Word가 이해할 수 있는 형태로 바꾼 뒤 pandoc에 넘긴다.

  !!! tip "제목" + 4칸 들여쓴 본문   ->  인용 블록(> **제목** / > 본문)
  /// caption ... ///               ->  기울임 캡션 문단
  ++ctrl+shift+r++                  ->  `Ctrl+Shift+R`
  ____ (빈칸 줄)                    ->  \\_ 이스케이프(수평선으로 바뀌는 것 방지)
  장 제목 #                         ->  ## (부 제목이 #을 차지한다)

코드 블록 안은 한 글자도 건드리지 않는다.
"""
from __future__ import annotations

import argparse
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# (부 제목, [(장 제목, 파일)]) — mkdocs.yml nav과 같은 순서
NAV = [
    (None, [("시작", "index.md"), ("0장 이 책에서 만드는 것", "ch00.md")]),
    ("1부 바이브코딩 준비운동", [
        ("1장 왜 바이브코딩인가", "ch01.md"),
        ("2장 Node.js 설치", "ch02.md"),
        ("3장 Git for Windows 설치", "ch03.md"),
        ("4장 Claude Code 설치와 첫 사용", "ch04.md"),
        ("5장 GitHub CLI로 깃허브 연결", "ch05.md"),
        ("6장 Orca로 여러 에이전트 다루기", "ch06.md"),
    ]),
    ("2부 카카오 지도 첫걸음", [
        ("7장 카카오 개발자 계정과 앱 만들기", "ch07.md"),
        ("8장 Vite로 프로젝트 시작", "ch08.md"),
        ("9장 첫 지도 띄우기", "ch09.md"),
        ("10장 지도 다루기", "ch10.md"),
    ]),
    ("3부 나만의 장소 지도 만들기", [
        ("11장 마커 찍기", "ch11.md"),
        ("12장 장소 데이터 설계", "ch12.md"),
        ("13장 커스텀 오버레이 말풍선", "ch13.md"),
        ("14장 카테고리 필터", "ch14.md"),
        ("15장 키워드 장소 검색", "ch15.md"),
        ("16장 클릭·검색으로 장소 추가", "ch16.md"),
        ("17장 localStorage 저장", "ch17.md"),
        ("18장 사이드바 장소 목록", "ch18.md"),
        ("19장 상세 패널", "ch19.md"),
    ]),
    ("4부 한 단계 더", [
        ("20장 내 위치 표시", "ch20.md"),
        ("21장 URL로 지도 공유", "ch21.md"),
        ("22장 마커 클러스터러", "ch22.md"),
        ("23장 모바일 대응", "ch23.md"),
    ]),
    ("5부 세상에 공개하기", [
        ("24장 GitHub에 올리기", "ch24.md"),
        ("25장 GitHub Pages 배포", "ch25.md"),
        ("26장 README 작성과 공개", "ch26.md"),
    ]),
    ("부록", [
        ("부록 A 프롬프트 템플릿 모음", "ch27.md"),
        ("부록 B 트러블슈팅 & 치트시트", "ch28.md"),
    ]),
]

PAGEBREAK = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'

FENCE = re.compile(r"^\s*(```|~~~)")
ADMON = re.compile(r'^(!!!|\?\?\?)\+?\s+(\w+)(?:\s+"(.*)")?\s*$')
KEYS = re.compile(r"\+\+([a-z0-9+⌘⌘]+)\+\+")
BLANKLINE = re.compile(r"^(\s*)(_{3,})\s*$")

KEYNAME = {
    "ctrl": "Ctrl", "shift": "Shift", "alt": "Alt", "win": "Win",
    "cmd": "Cmd", "tab": "Tab", "esc": "Esc", "enter": "Enter",
    "space": "Space", "backspace": "Backspace", "del": "Del",
    "⌘": "⌘",
}


def keyname(part: str) -> str:
    if part in KEYNAME:
        return KEYNAME[part]
    if re.fullmatch(r"f\d{1,2}", part):
        return part.upper()
    return part.upper() if len(part) == 1 else part.capitalize()


def fix_keys(s: str) -> str:
    return KEYS.sub(lambda m: "`" + "+".join(keyname(p) for p in m.group(1).split("+")) + "`", s)


FOOTREF = re.compile(r"\[\^(\d+)\]")


def convert(md: str, tag: str = "") -> str:
    """한 장의 mkdocs 마크다운을 pandoc이 읽을 마크다운으로 바꾼다."""
    if tag:
        # 각주 번호는 장마다 1부터 시작한다. 한 파일로 합치면 겹치므로 장 이름을 붙인다.
        md = FOOTREF.sub(lambda m: "[^%s-%s]" % (tag, m.group(1)), md)
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i, infence = 0, False

    while i < len(lines):
        line = lines[i]

        if FENCE.match(line):
            infence = not infence
            out.append(line)
            i += 1
            continue
        if infence:
            out.append(line)
            i += 1
            continue

        # /// caption ... ///  ->  기울임 캡션
        if line.strip() == "/// caption":
            j = i + 1
            cap: list[str] = []
            while j < len(lines) and lines[j].strip() != "///":
                cap.append(lines[j].strip())
                j += 1
            text = " ".join(x for x in cap if x)
            if text:
                out.append("*" + fix_keys(text) + "*")
            i = j + 1
            continue

        # !!! type "제목"  ->  인용 블록
        m = ADMON.match(line.strip())
        if m and line[:1] in ("!", "?"):
            title = (m.group(3) or m.group(2)).strip()
            body: list[str] = []
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if nxt.strip() == "":
                    body.append("")
                    j += 1
                    continue
                if nxt.startswith("    "):
                    body.append(nxt[4:])
                    j += 1
                    continue
                break
            while body and body[-1] == "":
                body.pop()
            out.append("> **" + fix_keys(title) + "**")
            out.append(">")
            bfence = False
            for b in body:
                if FENCE.match(b):
                    bfence = not bfence
                    out.append("> " + b)
                    continue
                if bfence:
                    out.append("> " + b)
                    continue
                bl = BLANKLINE.match(b)
                if bl:
                    out.append("> " + bl.group(1) + "\\_" * len(bl.group(2)))
                    continue
                out.append(("> " + fix_keys(b)).rstrip())
            out.append("")
            i = j
            continue

        # 헤딩 한 단계 내리기 (부 제목이 #을 쓴다)
        if re.match(r"^#{1,5} ", line):
            line = "#" + line

        bl = BLANKLINE.match(line)
        if bl:
            out.append(bl.group(1) + "\\_" * len(bl.group(2)))
            i += 1
            continue

        out.append(fix_keys(line))
        i += 1

    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="원고_전체.docx")
    ap.add_argument("--keep-md", action="store_true", help="중간 마크다운을 남긴다")
    a = ap.parse_args()

    parts: list[str] = ["% 바이브코딩으로 만드는 나만의 지도 웹", "%", "%", ""]
    first = True
    for part_title, chapters in NAV:
        if part_title:
            if not first:
                parts.append(PAGEBREAK)
            parts.append("# " + part_title + "\n")
        for _, fname in chapters:
            if not first:
                parts.append(PAGEBREAK)
            src = (DOCS / fname).read_text(encoding="utf-8-sig")
            parts.append(convert(src, Path(fname).stem).strip() + "\n")
            first = False

    merged = "\n".join(parts)
    tmp = ROOT / "_docx_input.md"
    tmp.write_text(merged, encoding="utf-8", newline="\n")

    cmd = [
        "pandoc", str(tmp),
        "-f", "markdown+footnotes+link_attributes+pipe_tables+raw_attribute",
        "-t", "docx",
        "-o", str(ROOT / a.out),
        "--resource-path", str(DOCS),
        "--toc", "--toc-depth=3",
        "--highlight-style", "tango",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.stdout:
        print(r.stdout.strip())
    if r.stderr:
        print(r.stderr.strip(), file=sys.stderr)
    if not a.keep_md:
        tmp.unlink()
    if r.returncode:
        sys.exit(r.returncode)
    size = (ROOT / a.out).stat().st_size
    print(f"만들었습니다: {a.out} ({size/1024/1024:.1f} MB)")


main()
