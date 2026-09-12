#!/usr/bin/env python3
"""윤문한 본문을 최종교재 docx 에 옮겨 넣는다.

최종교재의 장 번호는 리포 장 번호 + 4 다 (리포 ch00 = 최종 04장).
본문 문단만 갈아 끼우고 제목·소제목·그림·코드 블록은 건드리지 않는다.
문장 안의 장 번호와 그림 번호는 최종교재 번호로 바꾼다.

    py tools/apply_polish.py --ch 06 --dry
    py tools/apply_polish.py --ch 06
    py tools/apply_polish.py --all
"""
from __future__ import annotations

import argparse
import difflib
import re
import shutil
import sys
import unicodedata
from pathlib import Path

from docx import Document
from docx.shared import RGBColor

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dola_prep import prose_items  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "최종교재"
OFFSET = 4                      # 리포 ch00 -> 최종 04장

CODE_FONT = "Consolas"
CODE_SIZE = 107950              # 8.5pt (docx EMU)

SEG = re.compile(r"(`[^`\n]+`|\*\*[^*\n]+\*\*|\[\^\w+\])")
BULLET = re.compile(r"^\s*(?:[•▪·]|[-*+]\s|\d+[.)]\s)")


# '장'이 세는 단위로 쓰인 자리 (카드 두 장, 사진 세 장)
NOT_CHAPTER = re.compile(r"(카드|사진|종이|용지|스티커|이미지)\s*$")

KEYS = {
    "f5": "F5", "f12": "F12", "enter": "Enter", "esc": "Esc", "tab": "Tab",
    "ctrl": "Ctrl", "shift": "Shift", "alt": "Alt", "space": "Space",
}


def key_markup(t: str) -> str:
    """mkdocs 의 ++ctrl+shift+r++ 표기를 사람이 읽는 형태로 바꾼다."""
    def one(m):
        parts = [KEYS.get(x, x.upper()) for x in m.group(1).split("+") if x]
        return "+".join(parts)

    return re.sub(r"\+\+([A-Za-z0-9+]+)\+\+", one, t)


def renum(t: str) -> str:
    """문장 안의 장·그림 번호를 최종교재 번호로 올린다."""
    def fig(m):
        return f"그림 {int(m.group(1)) + OFFSET}.{m.group(2)}"

    def sec(m):
        return f"{int(m.group(1)) + OFFSET}.{m.group(2)}절"

    def rng(m):
        return f"{int(m.group(1)) + OFFSET}~{int(m.group(2)) + OFFSET}장"

    def chap(m):
        n = int(m.group(1))
        if NOT_CHAPTER.search(t[:m.start()]):
            return m.group(0)
        return f"{n + OFFSET}장" if 0 <= n <= 28 - OFFSET else m.group(0)

    t = key_markup(t)
    t = re.sub(r"그림\s*(\d{1,2})\.(\d{1,2})", fig, t)
    t = re.sub(r"(?<![\d.])(\d{1,2})\.(\d{1,2})절", sec, t)
    t = re.sub(r"(?<![\d.])(\d{1,2})\s*[~∼-]\s*(\d{1,2})장", rng, t)
    t = re.sub(r"(?<![\d.~-])(\d{1,2})장", chap, t)
    return t


DUAL_FIG = re.compile(r"그림\s*\d{1,2}\.\d{1,2}\s+(그림\s*\d{1,2}\.\d{1,2})")
DUAL_SEC = re.compile(r"(?<![\d.])\d{1,2}\.\d{1,2}\s+(\d{1,2}\.\d{1,2})(?![\d])")
DUAL_CH = re.compile(r"(?<![\d.])\d{1,2}장\s+(\d{1,2}장)")


def fix_numbers(t: str) -> str:
    """편집 중 남은 옛 번호를 지우거나, 아직 안 올린 번호를 올린다.

    옛 번호와 새 번호가 나란히 있으면 (예: '1장 5장') 뒤엣것만 남긴다.
    그런 흔적이 없으면 리포 번호로 보고 최종 번호로 올린다.
    """
    dual = False
    for rx in (DUAL_FIG, DUAL_SEC, DUAL_CH):
        t2 = rx.sub(lambda m: m.group(1), t)
        if t2 != t:
            dual = True
            t = t2
    return key_markup(t) if dual else renum(t)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", "", s)
    return re.sub(r"[·•\-–—~…\"'“”‘’()\[\]{}:;,.!?*`]", "", s)


def segments(md: str) -> list[tuple[str, str]]:
    """마크다운 한 문단을 (글자, 종류) 조각으로 나눈다."""
    out: list[tuple[str, str]] = []
    for part in SEG.split(md):
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            out.append((part[1:-1], "code"))
        elif part.startswith("**") and part.endswith("**"):
            out.append((part[2:-2], "bold"))
        elif part.startswith("[^") and part.endswith("]"):
            out.append((part[2:-1], "sup"))      # 각주 표시는 위첨자 숫자로
        else:
            out.append((part, "text"))
    return out


def base_font(p):
    """코드가 아닌 첫 런의 서식을 기준으로 삼는다."""
    for r in p.runs:
        if r.font.name != CODE_FONT:
            f = r.font
            return {
                "name": f.name,
                "size": f.size,
                "bold": f.bold,
                "italic": f.italic,
                "color": f.color.rgb if (f.color and f.color.type is not None) else None,
            }
    return {"name": None, "size": None, "bold": None, "italic": None,
            "color": RGBColor(0, 0, 0)}


def rewrite(p, md: str) -> None:
    base = base_font(p)
    for r in list(p.runs):
        r._element.getparent().remove(r._element)
    for text, kind in segments(md):
        r = p.add_run(text)
        f = r.font
        f.name = CODE_FONT if kind == "code" else base["name"]
        f.size = CODE_SIZE if kind == "code" else base["size"]
        f.bold = True if kind == "bold" else base["bold"]
        f.italic = base["italic"]
        if kind == "sup":
            f.superscript = True
        if base["color"] is not None:
            f.color.rgb = base["color"]


def align(doc_texts: list[str], src_texts: list[str], floor: float = 0.42) -> dict[int, int]:
    """docx 문단 -> 리포 문단 짝짓기 (순서를 지키며)."""
    a = [norm(x) for x in doc_texts]
    b = [norm(x) for x in src_texts]
    m: dict[int, int] = {}
    used: set[int] = set()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                m[i1 + k] = j1 + k
                used.add(j1 + k)
            continue
        for i in range(i1, i2):
            best, bj = 0.0, None
            for j in range(j1, j2):
                if j in used:
                    continue
                r = difflib.SequenceMatcher(None, a[i], b[j], autojunk=False).ratio()
                if r > best:
                    best, bj = r, j
            if bj is not None and best >= floor:
                m[i] = bj
                used.add(bj)
    return m


def final_path(n: int) -> Path | None:
    for p in FINAL.glob(f"{n:02d}장_*.docx"):
        return p
    return None


def do_chapter(n: int, dry: bool, verbose: bool) -> None:
    ch = f"ch{n - OFFSET:02d}"
    src_md = ROOT / "윤문비교" / "원문" / f"{ch}.md"
    if not src_md.exists():
        src_md = ROOT / "chapters" / f"{ch}.md"
    new_md = ROOT / "윤문비교" / ch / "D_Dola_보정.md"
    docx_path = final_path(n)
    if not (src_md.exists() and new_md.exists() and docx_path):
        print(f"{n:02d}장 ({ch}): 자료가 부족해 건너뜁니다")
        return

    src_items = prose_items(src_md.read_text(encoding="utf-8"))
    new_items = prose_items(new_md.read_text(encoding="utf-8"))
    src_texts = [t for _, t in src_items]
    new_texts = [t for _, t in new_items]
    if len(src_texts) != len(new_texts):
        print(f"{n:02d}장 ({ch}): 문단 수가 다릅니다 {len(src_texts)} vs {len(new_texts)}")
        return

    d = Document(str(docx_path))
    cand = [(i, p) for i, p in enumerate(d.paragraphs)
            if p.style.name == "Normal" and p.text.strip()
            and not BULLET.match(p.text) and len(p.text.strip()) > 12]
    doc_texts = [p.text for _, p in cand]

    m = align(doc_texts, src_texts)
    changed = 0
    for di, si in sorted(m.items()):
        target = renum(new_texts[si])
        if target == doc_texts[di]:
            continue
        if verbose and changed < 3:
            print(f"  - 원본: {doc_texts[di][:70]}")
            print(f"    윤문: {target[:70]}")
        if not dry:
            rewrite(cand[di][1], target)
        changed += 1

    # 짝을 못 찾은 본문과 코드 블록에도 번호 체계를 맞춰 준다
    matched = {cand[i][0] for i in m}
    left = 0
    for i, p in enumerate(d.paragraphs):
        if i in matched or not p.text.strip():
            continue
        if p.style.name not in ("Normal", "Source Code"):
            continue
        fixed = fix_numbers(p.text)
        if fixed != p.text:
            if not dry:
                rewrite(p, fixed.replace("`", ""))
            left += 1

    print(f"{n:02d}장 ({ch}): 본문 {len(doc_texts)}개 중 {len(m)}개 짝지음 · {changed}개 교체"
          + (f" · 번호만 고친 줄 {left}개" if left else "")
          + (" [미리보기]" if dry else ""))

    if not dry and changed:
        bak = docx_path.with_suffix(".docx.bak")
        if not bak.exists():
            shutil.copy2(docx_path, bak)
        d.save(str(docx_path))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ch", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    ns = range(OFFSET, 30) if args.all else [args.ch]
    for n in ns:
        if n is None:
            ap.error("--ch 또는 --all 이 필요합니다")
        do_chapter(n, args.dry, args.verbose)


if __name__ == "__main__":
    main()
