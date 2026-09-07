#!/usr/bin/env python3
"""윤문 전후 내용 보존 검사.

문체만 고쳤는지 확인한다. 코드·헤딩·그림·링크는 한 글자도 바뀌면 안 되고,
산문 분량이 크게 줄면 내용이 잘려 나간 것으로 본다.

usage: python tools/content_integrity.py <before.md> <after.md>
       python tools/content_integrity.py --git chapters/ch21.md   # HEAD와 비교
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

MAX_PROSE_SHRINK = 0.12   # 산문 12% 초과 감소면 실패


def parts(md: str) -> dict:
    code = re.findall(r"```.*?```", md, flags=re.S)
    heads = re.findall(r"^\s*#{1,6}\s.*$", md, flags=re.M)
    imgs = re.findall(r"!\[[^\]]*\]\(([^)]*)\)", md)
    links = re.findall(r"(?<!!)\[[^\]]*\]\(([^)]*)\)", md)
    caps = re.findall(r"^///\s*caption\s*\n(.+?)\n///", md, flags=re.M | re.S)
    inline = re.findall(r"`[^`\n]+`", md)
    prose = re.sub(r"```.*?```", " ", md, flags=re.S)
    prose = re.sub(r"^\s*#{1,6}\s.*$", " ", prose, flags=re.M)
    prose = re.sub(r"\s+", "", prose)
    return {"code": code, "heads": heads, "imgs": imgs, "links": links,
            "caps": caps, "inline": inline, "prose_len": len(prose)}


def check(before: str, after: str) -> tuple[bool, list[str]]:
    b, a = parts(before), parts(after)
    errs: list[str] = []

    if b["code"] != a["code"]:
        errs.append(f"코드 블록 변경됨 ({len(b['code'])} -> {len(a['code'])})")
    if b["heads"] != a["heads"]:
        errs.append(f"헤딩 변경됨 ({len(b['heads'])} -> {len(a['heads'])})")
    if b["imgs"] != a["imgs"]:
        errs.append(f"그림 참조 변경됨 ({len(b['imgs'])} -> {len(a['imgs'])})")
    if b["links"] != a["links"]:
        errs.append(f"링크 대상 변경됨 ({len(b['links'])} -> {len(a['links'])})")
    if len(b["caps"]) != len(a["caps"]):
        errs.append(f"그림 캡션 수 변경됨 ({len(b['caps'])} -> {len(a['caps'])})")

    # 인라인 코드(식별자)는 사라지면 안 된다
    lost = [x for x in set(b["inline"]) if x not in set(a["inline"])]
    if lost:
        errs.append(f"인라인 코드 사라짐 {len(lost)}개: {lost[:5]}")

    shrink = (b["prose_len"] - a["prose_len"]) / b["prose_len"] if b["prose_len"] else 0
    if shrink > MAX_PROSE_SHRINK:
        errs.append(f"산문 {shrink*100:.1f}% 감소 (허용 {MAX_PROSE_SHRINK*100:.0f}%) — 내용 잘림 의심")

    return (not errs), errs


def main() -> None:
    if sys.argv[1:2] == ["--git"]:
        files = sys.argv[2:]
        bad = 0
        for f in files:
            before = subprocess.run(["git", "show", f"HEAD:{f}"], capture_output=True, text=True,
                                    encoding="utf-8").stdout
            after = Path(f).read_text(encoding="utf-8")
            ok, errs = check(before, after)
            print(f"[{'OK ' if ok else 'BAD'}] {f}")
            for e in errs:
                print(f"        - {e}")
            bad += 0 if ok else 1
        sys.exit(1 if bad else 0)

    before = Path(sys.argv[1]).read_text(encoding="utf-8")
    after = Path(sys.argv[2]).read_text(encoding="utf-8")
    ok, errs = check(before, after)
    print("OK" if ok else "BAD")
    for e in errs:
        print(" -", e)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
