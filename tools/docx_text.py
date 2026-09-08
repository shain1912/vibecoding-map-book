#!/usr/bin/env python3
"""워드(.docx) 원고에서 본문을 뽑아 문체 메트릭에 넣을 수 있게 한다.

마크다운 원고가 아닌 책(예: 워드로 쓰는 원고)도 같은 기준으로 재려고 만들었다.
색(빨간 글씨)·강조·변경 추적이 있으면 함께 알려 준다.

    py tools/docx_text.py 원고.docx                    # 본문 추출 + 서식 요약
    py tools/docx_text.py 원고.docx --out ch1.md       # 파일로 저장
    py tools/docx_text.py 원고.docx --color C00000     # 특정 색 글자만 뽑기

추출한 뒤:
    py tools/style_metric.py ch1.md --show-hits 20
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _style_colors(z: zipfile.ZipFile) -> dict[str, str]:
    """문자 스타일 id -> 색. 색이 스타일로만 걸려 있는 문서가 흔하다."""
    try:
        xml = z.read("word/styles.xml").decode("utf-8")
    except KeyError:
        return {}
    out: dict[str, str] = {}
    for m in re.finditer(r'<w:style\b[^>]*w:styleId="([^"]+)"[^>]*>(.*?)</w:style>', xml, re.S):
        sid, body = m.group(1), m.group(2)
        c = re.search(r'<w:color w:val="([0-9A-Fa-f]{6})"', body)
        if c:
            out[sid] = c.group(1).upper()
    return out


def runs(z: zipfile.ZipFile):
    """(문단번호, 색, 굵게, 텍스트) 순서대로."""
    root = ET.fromstring(z.read("word/document.xml").decode("utf-8"))
    smap = _style_colors(z)
    for i, p in enumerate(root.iter(W + "p")):
        for r in p.iter(W + "r"):
            rpr = r.find(W + "rPr")
            color, bold = None, False
            if rpr is not None:
                c = rpr.find(W + "color")
                if c is not None:
                    color = (c.get(W + "val") or "").upper()
                rs = rpr.find(W + "rStyle")
                if color in (None, "", "AUTO") and rs is not None:
                    color = smap.get(rs.get(W + "val") or "")
                bold = rpr.find(W + "b") is not None
            txt = "".join(t.text or "" for t in r.iter(W + "t"))
            if txt:
                yield i, (color or "AUTO"), bold, txt


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--out", help="추출한 본문을 저장할 경로 (.md 권장)")
    ap.add_argument("--color", help="이 색 글자만 뽑는다 (예: C00000)")
    args = ap.parse_args()

    path = Path(args.docx)
    if not path.exists():
        sys.exit(f"파일이 없습니다: {path}")
    z = zipfile.ZipFile(path)

    paras: dict[int, list[str]] = {}
    picked: list[str] = []
    colors: Counter = Counter()
    bold_chars = 0
    total = 0
    for idx, color, bold, txt in runs(z):
        colors[color] += len(txt)
        total += len(txt)
        if bold:
            bold_chars += len(txt)
        paras.setdefault(idx, []).append(txt)
        if args.color and color.upper() == args.color.upper():
            picked.append(txt)

    body = "\n".join("".join(v).strip() for _, v in sorted(paras.items()) if "".join(v).strip())

    raw = z.read("word/document.xml").decode("utf-8")
    ins, dele = raw.count("<w:ins "), raw.count("<w:del ")

    print(f"문단 {len(paras)}개 · 글자 {total:,}자")
    print("색상별 글자수:", dict(colors.most_common(6)))
    print(f"굵게: {bold_chars:,}자 ({bold_chars/total*100:.1f}%)" if total else "굵게: 0")
    if ins or dele:
        print(f"변경 추적: 삽입 {ins} · 삭제 {dele}")
    if args.color:
        print(f"\n[{args.color}] 글자 {len(picked)}조각")
        for x in picked[:30]:
            print("  •", x.strip()[:120])

    if args.out:
        Path(args.out).write_text(body, encoding="utf-8")
        print(f"\n본문 저장: {args.out} ({len(body):,}자)")
        print(f"다음: py tools/style_metric.py {args.out} --show-hits 20")
    else:
        print("\n--- 본문 앞부분 ---")
        print(body[:600])


if __name__ == "__main__":
    main()
