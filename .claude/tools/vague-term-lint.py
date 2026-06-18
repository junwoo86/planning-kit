#!/usr/bin/env python3
# vague-term-lint — 고정 금지어(모호표현)의 *결정적* 탐지 (guideline §6/§14, blueprint §1.4).
# 이 파일이 금지어 목록의 **단일 출처**다 — completion-gate 가 여기서 import 한다(drift 방지).
#
# 결정적으로 잡는 것: 고정 목록의 측정불가 표현. 같은 줄에 재정의 마커(→측정:/[정의됨] 등)가 있으면 통과.
# 잡지 않는 것: 그 밖의 *의미적* 모호성 → LLM 보조 독립검토(§14). 도구는 값이 명확한 것만 판정한다.
#
# 사용:  sh .claude/hooks/launch.sh .claude/tools/vague-term-lint.py <파일 또는 디렉토리> [추가 경로 ...]
# 종료코드: 0 = 위반 없음, 1 = 위반, 2 = 인자 없음.

import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 고정 금지어(canonical). 측정불가·주관적 표현. 새 항목은 여기서만 추가한다.
VAGUE_TERMS = ["실시간", "100%", "빠르게", "빠른", "직관적", "쉽게", "간편",
               "유연", "원활", "매끄럽", "최적화", "강력", "최고", "사용자 친화", "효율적"]
# 확정 오탐(false positive) 예외 — 금지어를 부분문자열로 품지만 정당한 합성어/표현. 줄에서 먼저 마스킹한다.
# (한글은 교착어라 \b 경계가 부적합 → '유연근무'·'비실시간' 같은 합성어를 예외로 둔다. 새 오탐은 여기 추가.)
FALSE_POSITIVES = ["유연근무", "비실시간", "유연성"]
# 같은 줄에 있으면 '재정의됨'으로 보고 통과시키는 마커.
REDEFINE_MARKERS = ["측정:", "→측정", "[정의됨]", "[non-goal]", "[정의]"]
# 줄 자체를 건너뛰는 신호(설명·범례·주석).
SKIP_SIGNALS = ("금지어", "범례", "재정의", "모호표현")
# 영숫자(%포함) 금지어는 단어경계로 본다(한글은 예외 마스킹 후 부분일치).
_HAS_ASCII = re.compile(r"[A-Za-z0-9]")


def _term_hit(masked, term):
    """영숫자 토큰은 단어경계(앞뒤 비영숫자), 한글은 (예외 마스킹된) 부분일치."""
    if _HAS_ASCII.search(term):
        return re.search(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", masked) is not None
    return term in masked


def scan_vague(path):
    """단일 파일에서 (lineno, term, snippet) 위반 목록 반환. 없는 파일 → [].
    코드펜스(```/~~~) 블록과 FALSE_POSITIVES 예외는 제외하고, 한 줄의 *모든* 금지어를 보고한다."""
    hits = []
    if not os.path.isfile(path):
        return hits
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception:
        return hits
    in_fence = False
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = re.sub(r"<!--.*?-->", "", s).strip()   # 인라인 HTML 주석 제거(설명용 텍스트 오탐 방지)
        if not s or s.startswith("<!--") or s.startswith("-->"):
            continue
        if any(sig in s for sig in SKIP_SIGNALS):
            continue
        if any(mark in s for mark in REDEFINE_MARKERS):
            continue
        masked = s
        for exc in FALSE_POSITIVES:
            if exc in masked:
                masked = masked.replace(exc, " " * len(exc))
        for term in VAGUE_TERMS:   # break 제거 — 줄당 전건 보고
            if _term_hit(masked, term):
                hits.append((i, term, s[:80]))
    return hits


def _iter_targets(paths):
    for p in paths:
        if os.path.isdir(p):
            for name in sorted(os.listdir(p)):
                if name.endswith(".md"):
                    yield os.path.join(p, name)
        else:
            yield p


def main(argv):
    bad = [a for a in argv[1:] if a.startswith("--")]
    if bad:
        print(f"[vague-term-lint] 알 수 없는 옵션: {' '.join(bad)} (이 도구는 옵션 없음)", file=sys.stderr)
        return 2
    if len(argv) < 2:
        print("사용: sh .claude/hooks/launch.sh .claude/tools/vague-term-lint.py <파일|디렉토리> [...]", file=sys.stderr)
        return 2
    total = 0
    print("[vague-term-lint] 고정 금지어 검사")
    for path in _iter_targets(argv[1:]):
        hits = scan_vague(path)
        if hits:
            for ln, term, snip in hits:
                print(f"  ✗ {path}:{ln}  '{term}'  → {snip}")
            total += len(hits)
    if total:
        print(f"\n결과: FAIL — {total}건. 같은 줄에서 '→측정:' 또는 [정의됨]으로 SMART 재정의 필요.")
        return 1
    print("결과: PASS — 고정 금지어 미검출.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
