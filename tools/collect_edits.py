#!/usr/bin/env python3
"""윤문 전후 '바뀐 문장'만 뽑아 검수용 데이터로 만든다.

git 리비전 두 개를 비교해, 문단 단위로 달라진 곳을 찾고
문장 단위로 짝지어 before/after 를 낸다.

usage:
  python tools/collect_edits.py --base <rev> --out edits.json
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
from pathlib import Path


def git_show(rev: str, path: str) -> str:
    r = subprocess.run(["git", "show", f"{rev}:{path}"],
                       capture_output=True, text=True, encoding="utf-8")
    return r.stdout


def blocks(md: str) -> list[str]:
    """코드 블록을 통째로 보존하며 문단으로 나눈다."""
    parts, buf, in_code = [], [], False
    for ln in md.split("\n"):
        if ln.lstrip().startswith("```"):
            in_code = not in_code
        if not in_code and not ln.strip():
            if buf:
                parts.append("\n".join(buf))
                buf = []
        else:
            buf.append(ln)
    if buf:
        parts.append("\n".join(buf))
    return parts


def split_sents(p: str) -> list[str]:
    p = re.sub(r"\s+", " ", p).strip()
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", p) if s.strip()]


def classify(b: str, a: str) -> str:
    """볼드만 뗀 것인지, 실제로 문장을 고쳐 쓴 것인지 구분한다."""
    nb = b.replace("**", "")
    na = a.replace("**", "")
    if nb == na:
        return "bold_only"
    # 공백까지 무시했을 때 같으면 서식 정리로 본다
    if re.sub(r"\s+", "", nb) == re.sub(r"\s+", "", na):
        return "bold_only"
    return "rewrite"


def pair_changes(before: str, after: str) -> list[dict]:
    """문단 매칭 → 문장 매칭 순으로 좁혀 실제 바뀐 문장만 남긴다."""
    b_blocks, a_blocks = blocks(before), blocks(after)
    out: list[dict] = []
    sm = difflib.SequenceMatcher(None, b_blocks, a_blocks, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        bs = [s for blk in b_blocks[i1:i2] if not blk.lstrip().startswith("```")
              for s in split_sents(blk)]
        as_ = [s for blk in a_blocks[j1:j2] if not blk.lstrip().startswith("```")
               for s in split_sents(blk)]
        sm2 = difflib.SequenceMatcher(None, bs, as_, autojunk=False)
        for t2, x1, x2, y1, y2 in sm2.get_opcodes():
            if t2 == "equal":
                continue
            b_txt = " ".join(bs[x1:x2]).strip()
            a_txt = " ".join(as_[y1:y2]).strip()
            if not b_txt and not a_txt:
                continue
            if b_txt == a_txt:
                continue
            out.append({"before": b_txt, "after": a_txt, "kind": classify(b_txt, a_txt)})
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="윤문 이전 리비전")
    ap.add_argument("--out", default="edits.json")
    ap.add_argument("--dir", default="chapters")
    args = ap.parse_args()

    files = sorted(Path(args.dir).glob("*.md"))
    doc: dict = {"base": args.base, "files": []}
    total = 0
    for f in files:
        rel = f.as_posix()
        before = git_show(args.base, rel)
        if not before:
            continue
        after = f.read_text(encoding="utf-8")
        if before == after:
            continue
        changes = pair_changes(before, after)
        if not changes:
            continue
        total += len(changes)
        doc["files"].append({
            "file": f.name,
            "n_rewrite": sum(1 for c in changes if c["kind"] == "rewrite"),
            "n_bold": sum(1 for c in changes if c["kind"] == "bold_only"),
            "changes": changes,
        })

    doc["total_changes"] = total
    doc["total_rewrite"] = sum(f["n_rewrite"] for f in doc["files"])
    doc["total_bold"] = sum(f["n_bold"] for f in doc["files"])
    Path(args.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(doc['files'])}개 파일 · 문장 재작성 {doc['total_rewrite']}곳 · "
          f"볼드 정리 {doc['total_bold']}곳 -> {args.out}")


if __name__ == "__main__":
    main()
