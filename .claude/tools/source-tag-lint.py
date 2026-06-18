#!/usr/bin/env python3
# source-tag-lint — 산출물(PRD/보고서)의 실질 내용 줄에 *출처 태그*가 달렸는지 결정적 검사 (guideline §14).
# AI 추측을 항상 가시화하는 규율을 기계적으로 보장한다(silent-wrong 방지).
#
# 검사 대상 줄: 본문의 '- ' 불릿(실질 진술). 헤딩·표·코드·주석·범례 섹션·짧은 토막은 제외(오탐 억제).
# 통과 조건: 줄에 허용 출처 태그 [입력]/[AI보강]/[근본원인추론]/[현업검증]/[참조맵...]/[물어봄] 중 1개 이상.
#           (확신도 [확실]/[추정]/[확인불가]는 보조라 필수 아님.) `<!-- no-tag -->`로 줄 면제 가능.
#
# 사용:  sh .claude/hooks/launch.sh .claude/tools/source-tag-lint.py <md 파일> [...]
# 종료코드: 0 = 모든 내용 줄 태그 있음, 1 = 누락, 2 = 인자 없음.

import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SOURCE_TAGS = ["입력", "AI보강", "근본원인추론", "현업검증", "참조맵", "물어봄"]
TAG_RE = re.compile(r"\[(입력|AI보강|근본원인추론|현업검증|참조맵[^\]]*|물어봄)\]")
BULLET_RE = re.compile(r"^[-*]\s+\S")
# 태그 면제 섹션(헤딩에 이 단어가 들어가면 그 섹션은 검사 제외).
SKIP_SECTION = ("범례", "태그", "스코어카드")
MIN_STATEMENT_LEN = 12   # 이보다 짧은 토막은 실질 진술로 보지 않음(매직넘버 → 명명 상수)


def lint(path):
    """반환: (missing 줄 목록, 검사한 줄 수)."""
    missing, checked = [], 0
    if not os.path.isfile(path):
        return [("(파일 없음)", 0)], 0
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    in_comment = False
    in_fence = False
    skip_section = False
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if "<!--" in s and "-->" not in s:
            in_comment = True
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if s.startswith("```") or s.startswith("~~~"):   # 코드펜스 토글 — 내부 줄은 검사 제외
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if s.startswith("#"):
            skip_section = any(w in s for w in SKIP_SECTION)
            continue
        if skip_section or not BULLET_RE.match(s):
            continue
        if "<!-- no-tag -->" in ln or "[정의됨]" in s:
            continue
        if len(s) < MIN_STATEMENT_LEN:  # 너무 짧은 토막은 진술로 보지 않음
            continue
        checked += 1
        if not TAG_RE.search(s):
            missing.append((i, s[:80]))
    return missing, checked


def main(argv):
    bad = [a for a in argv[1:] if a.startswith("--")]
    if bad:
        print(f"[source-tag-lint] 알 수 없는 옵션: {' '.join(bad)} (이 도구는 옵션 없음)", file=sys.stderr)
        return 2
    if len(argv) < 2:
        print("사용: sh .claude/hooks/launch.sh .claude/tools/source-tag-lint.py <md 파일> [...]", file=sys.stderr)
        return 2
    total_missing = 0
    print("[source-tag-lint] 출처 태그 누락 검사")
    for path in argv[1:]:
        missing, checked = lint(path)
        print(f"  {path} — 검사 {checked}줄")
        for ln, snip in missing:
            print(f"    ✗ L{ln}: 출처 태그 없음 → {snip}")
        total_missing += len([m for m in missing if isinstance(m[0], int)])
    if total_missing:
        print(f"\n결과: FAIL — {total_missing}줄 출처 태그 누락. (면제: 줄 끝 '<!-- no-tag -->')")
        return 1
    print("\n결과: PASS — 모든 내용 줄에 출처 태그 존재.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
