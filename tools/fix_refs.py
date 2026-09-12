#!/usr/bin/env python3
"""검수에서 지적된 '내용이 틀린 곳'을 최종 구성(4부 29장)에 맞춰 고친다.

옛 원고는 5부 26장에 부록 A·B 가 있는 구성이었고, 최종교재는 00장 목차대로
1부 인공지능 윤리 시작하기(1~3장) / 2부 바이브코딩 준비하기(4~12장) /
3부 지도 웹 서비스 개발하기(13~27장) / 4부 지도 웹 서비스 배포하기(28~29장)
4부 29장이며 부록이 없다. 그래서 옛 구성을 설명하는 문장을 바로잡는다.

    py tools/fix_refs.py --dry
    py tools/fix_refs.py
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_polish import rewrite  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "최종교재"

P1 = ("제1부 「인공지능 윤리 시작하기」(1~3장)에서는 인공지능이 가져온 편익과 함께 "
      "생각해야 할 문제를 짚고, 국내외의 인공지능 윤리 동향과 법 제도를 살펴봅니다. "
      "이어서 개인정보 보호와 저작권, 디지털 자료를 쓸 때 지켜야 할 기준을 정리합니다. "
      "이 부에서 세운 기준은 뒤에서 지도 서비스를 만들 때 그대로 쓰입니다.")

P2 = ("제2부 「바이브코딩 준비하기」(4~12장)에서는 실습 환경을 준비합니다. "
      "이 책에서 무엇을 만드는지 확인하고 바이브코딩이 왜 지금 배우기 좋은 방식인지 알아본 뒤, "
      "저자가 실제로 쓰는 도구 — Node.js, Git, Claude Code, GitHub CLI, 여러 AI 도구를 함께 "
      "지휘하는 Orca — 를 차례로 설치합니다. 마지막으로 카카오 개발자 계정을 만들어 API 키를 "
      "받고 Vite로 프로젝트를 시작합니다. 설치 과정이 다소 지루하게 느껴질 수 있으나, "
      "여기서 준비한 도구는 마지막 장까지 계속 쓰게 되므로 꼼꼼히 준비하시기 바랍니다.")

P3 = ("제3부 「지도 웹 서비스 개발하기」(13~27장)는 이 책에서 가장 분량이 많은 부분입니다. "
      "브라우저에 첫 지도를 띄우고 지도를 다루는 법을 익힌 뒤, 마커를 찍고 장소 데이터 구조를 "
      "설계하며 말풍선을 답니다. 이어서 카테고리 필터와 키워드 검색, 클릭과 검색으로 장소를 "
      "추가하는 기능을 만들고, 브라우저에 데이터를 저장해 페이지를 다시 열어도 내용이 남게 합니다. "
      "저장한 장소를 사이드바 목록과 상세 패널에서 관리하고, 내 위치 표시와 링크 공유, 마커 "
      "클러스터러, 모바일 화면 대응까지 더합니다. 제3부를 마치면 그림 4.1과 같은 화면이 "
      "여러분의 브라우저에 나타나게 될 것입니다.")

P4 = ("제4부 「지도 웹 서비스 배포하기」(28~29장)에서는 완성한 애플리케이션을 GitHub에 "
      "올리고, GitHub Pages로 인터넷에 공개해 누구나 접속할 수 있는 주소를 얻는 과정을 "
      "설명합니다. 이 과정을 마치면 친구에게 링크를 보내 함께 지도를 확인해 볼 수 있을 것입니다.")

P5 = ("각 부의 끝에서는 그때까지 만든 것을 돌아보고, 다음 부에서 무엇을 더하는지 미리 짚습니다. "
      "순서대로 따라오시면 4부를 마쳤을 때 인터넷에 공개된 나만의 지도가 남습니다.")

P6 = ("실습에 쓴 요청문은 장마다 본문에 그대로 실어 두었습니다. "
      "\"지도가 회색으로 나와요\"처럼 자주 겪는 문제와 해결 방법도 해당 장 안에 함께 정리해 "
      "두었으니, 진행이 막히면 그 장의 문제 해결 부분을 먼저 보시기 바랍니다.")

FIXES: list[tuple[str, str, str]] = [
    # (파일 이름 일부, 찾을 문구, 바꿀 문단 전체)
    ("04장", "5부 26장으로 이어지는",
     "• 4부 29장으로 이어지는 책 전체의 여정을 한눈에 파악합니다"),
    ("04장", "4.4 책의 지도", "4.4 책의 지도: 4부로 떠나는 여정"),
    ("04장", "이 책은 전체 5부", "이 책은 전체 4부, 총 29개 장으로 구성되어 있습니다."),
    ("04장", "제1부 「바이브코딩 준비운동」", P1),
    ("04장", "제2부 「카카오 지도 첫걸음」", P2),
    ("04장", "제3부 「나만의 장소 지도 만들기」", P3),
    ("04장", "제4부 「한 단계 더」", P4),
    ("04장", "제5부 「세상에 공개하기」", P5),
    ("04장", "부록은 두 가지가 준비되어", P6),
    ("04장", "책은 5부 26장 구성입니다",
     "• 책은 4부 29장 구성입니다: 윤리 기준 세우기 → 도구 준비 → 지도 만들기 → 세상에 공개."),
    ("04장", "3부가 끝났을 때와 5부가 끝났을 때",
     "3. 3부가 끝났을 때와 4부가 끝났을 때, 내 앱은 각각 어떤 상태일까요? 한 문장씩 설명해 보세요."),
    ("05장", "이 책의 26개 장", None),          # 숫자만 바꾼다
    ("11장", "부록 B에 정리하여 두었습니다", None),
    ("28장", "이 책의 마지막인 5부에", None),
    ("28장", "5부에서는 이 앱을", None),
    ("29장", "부록 B의 문제 해결 표에도", None),
    ("29장", "30장에서는 스크린샷", None),
]

# 문단 전체를 새로 쓰지 않고 낱말만 바꾸는 것들
WORD_FIXES = [
    ("이 책의 26개 장", "이 책의 29개 장"),
    (" 보다 자세한 오류 해결 방법은 부록 B에 정리하여 두었습니다.", ""),
    ("보다 자세한 오류 해결 방법은 부록 B에 정리하여 두었습니다.", ""),
    ("이 책의 마지막인 5부에", "이 책의 마지막인 4부에"),
    ("5부에서는 이 앱을", "4부에서는 이 앱을"),
    (" 해당 증상과 대응 방법은 부록 B의 문제 해결 표에도 정리하여 두었습니다.", ""),
    ("해당 증상과 대응 방법은 부록 B의 문제 해결 표에도 정리하여 두었습니다.", ""),
]

# 29장 끝의 '다음 장 예고'는 더 이상 다음 장이 없다
LAST_NOTE = ("마치며 — 지도 앱이 드디어 인터넷에 살아 숨 쉬고 있습니다. "
             "이제 링크를 아는 사람은 누구나 여러분이 만든 지도를 열어 볼 수 있습니다. "
             "여기까지 오는 동안 도구를 갖추고, 기능을 하나씩 붙이고, 막힌 곳을 스스로 풀어 왔습니다. "
             "다음에 만들 것이 무엇이든 그 순서는 그대로 쓰입니다.")


def find(name: str) -> Path | None:
    for p in FINAL.glob(f"{name}*.docx"):
        return p
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    by_file: dict[str, list] = {}
    for f, needle, repl in FIXES:
        by_file.setdefault(f, []).append((needle, repl))

    for name, jobs in by_file.items():
        path = find(name)
        if not path:
            print(f"{name}: 파일 없음")
            continue
        d = Document(str(path))
        n = 0
        for p in d.paragraphs:
            t = p.text
            for needle, repl in jobs:
                if needle not in t:
                    continue
                if repl is not None:
                    new = repl
                elif "30장에서는 스크린샷" in t:
                    new = LAST_NOTE
                else:
                    new = t
                    for a, b in WORD_FIXES:
                        new = new.replace(a, b)
                    new = re.sub(r"\s{2,}", " ", new).strip()
                if new != t:
                    print(f"  [{name}] {t[:60]}")
                    print(f"      -> {new[:60]}")
                    if not args.dry:
                        rewrite(p, new)
                    n += 1
                break
        if n and not args.dry:
            bak = path.with_suffix(".docx.refbak")
            if not bak.exists():
                shutil.copy2(path, bak)
            d.save(str(path))
        print(f"{path.name}: {n}곳" + (" [미리보기]" if args.dry else ""))


if __name__ == "__main__":
    main()
