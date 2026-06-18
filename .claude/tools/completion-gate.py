#!/usr/bin/env python3
# completion-gate — 종료(완성) 8조건의 *구조적* 판정 (guideline §14 / blueprint §1.4·6.3)
#
# 정직성 원칙(§14): 값·구조가 명확한 것만 결정적으로 PASS/FAIL 한다. 의미 판단(성공기준이 *진짜* 측정가능한가,
# 근본원인 *해소* 여부, 가정 *적절성*)은 자동 PASS 하지 않고 REVIEW-REQUIRED 로 독립검토(§14)에 넘긴다.
#
# 8조건: 1 문제동결 · 2 성공기준 측정가능 · 3 미해결 악화 0 · 4 고위험 open-Q 0 ·
#        5 readiness 통과 · 6 모호표현 0(고정 금지어) · 7 미기록 결정 0 · 8 Unknown+Important 가정 누락 0
#
# 사용:  sh .claude/hooks/launch.sh .claude/tools/completion-gate.py <planning-dir> [--mode report|full]
# 종료코드: 0 = '완성' 선언 가능 · 1 = FAIL 존재(미완) · 2 = 독립검토 대기(조건부) 또는 인자 없음 · 3 = _state.md(재개앵커) 없음.
#           (규약 SSoT: .claude/hooks/README.md)

import glob
import importlib.util
import os
import re
import sys

# Windows 콘솔(cp949 등)에서도 한글·기호를 깨지지 않게 출력
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))

# coherence-check.py(하이픈)를 importlib로 로드
_spec = importlib.util.spec_from_file_location("coherence_check", os.path.join(HERE, "coherence-check.py"))
coherence_check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(coherence_check)
split_sections = coherence_check.split_sections
parse_table = coherence_check.parse_table
is_separator_row = coherence_check.is_separator_row
is_placeholder = coherence_check.is_placeholder

# 고정 금지어(모호표현)는 vague-term-lint.py 가 단일 출처 — 여기서 import(drift 방지).
_vspec = importlib.util.spec_from_file_location("vague_term_lint", os.path.join(HERE, "vague-term-lint.py"))
vague_term_lint = importlib.util.module_from_spec(_vspec)
_vspec.loader.exec_module(vague_term_lint)
scan_vague = vague_term_lint.scan_vague

PASS, FAIL, REVIEW, NA = "PASS", "FAIL", "REVIEW", "N/A"


def header_status(path):
    """파일 첫 부분의 <!-- ... status: X ... --> 에서 status 추출."""
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        head = f.read(800)
    m = re.search(r"status\s*[:：]\s*([A-Za-z가-힣\-]+)", head)
    return m.group(1).strip().lower() if m else None


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_state_stage_status(state_lines):
    """단계 상태표에서 {S0: 'done', ...} 반환."""
    out = {}
    for cells in parse_table(state_lines):
        if is_separator_row(cells) or not cells:
            continue
        if re.match(r"^S\d+$", cells[0].strip()) and len(cells) >= 3:
            out[cells[0].strip()] = cells[2].strip().lower()
    return out


def subsection_table(section_body, sub_title_needle):
    """### <needle> 서브섹션 바로 아래의 표 행들을 반환."""
    rows, capturing = [], False
    for ln in section_body:
        s = ln.strip()
        hm = re.match(r"^###\s+(.*)$", s)
        if hm:
            capturing = sub_title_needle.lower() in hm.group(1).lower()
            continue
        if capturing and s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not is_separator_row(cells):
                rows.append(cells)
    return rows


def main(argv):
    bad = [a for a in argv[1:] if a.startswith("--") and a.split("=", 1)[0] not in {"--mode", "--report"}]
    if bad:
        print(f"[completion-gate] 알 수 없는 옵션: {' '.join(bad)} (지원: --mode report|full)", file=sys.stderr)
        return 2
    args = [a for a in argv[1:] if not a.startswith("--")]
    # 모드: full(기본, S0~S12 종료 8조건) | report(S8 보고서 게이트 — 목업/readiness 의존 조건 제외)
    mode = "full"
    if "--mode" in argv:
        i = argv.index("--mode")
        if i + 1 < len(argv):
            mode = argv[i + 1]
    elif "--report" in argv:
        mode = "report"
    if not args:
        print("사용: sh .claude/hooks/launch.sh .claude/tools/completion-gate.py <planning-dir> [--mode report|full]", file=sys.stderr)
        return 2
    d = args[0]
    results = []  # (n, name, verdict, detail)

    def add(n, name, verdict, detail):
        results.append((n, name, verdict, detail))

    state_path = os.path.join(d, "_state.md")
    if not os.path.isfile(state_path):
        print(f"[completion-gate] _state.md 없음 ({state_path}) — 재개 앵커가 있어야 판정 가능.", file=sys.stderr)
        return 3   # 리소스 부재(규약: 입력 파일/디렉토리 없음 = 3). 비-0이라 §11.1 '완성 차단'은 동일.
    state_sections = split_sections(read(state_path).splitlines())
    stage_status = parse_state_stage_status(read(state_path).splitlines())

    # 1. 문제집합 동결
    ps = os.path.join(d, "01-problem-set.md")
    if not os.path.isfile(ps):
        add(1, "문제집합 동결", FAIL, "01-problem-set.md 없음")
    elif header_status(ps) != "frozen" or stage_status.get("S2") != "frozen":
        add(1, "문제집합 동결", FAIL,
            f"frozen 아님 (파일 status={header_status(ps)}, _state S2={stage_status.get('S2')})")
    else:
        add(1, "문제집합 동결", PASS, "01-problem-set.md frozen")

    # 2. 성공기준 측정가능(구조: 3층 존재 + 모호표현 0은 cond6에서)
    sc = os.path.join(d, "02-success.md")
    if not os.path.isfile(sc):
        add(2, "성공기준 측정가능", FAIL, "02-success.md 없음")
    else:
        body = read(sc)
        layers = sum(k in body for k in ("①", "②", "③"))
        if layers < 3:
            add(2, "성공기준 측정가능", FAIL, f"계층형 3층 마커(①②③) 중 {layers}개만 존재")
        else:
            add(2, "성공기준 측정가능", REVIEW, "3층 구조 존재 — 측정가능성 *적절성*은 독립검토(§14)")

    # 3. 미해결 악화 0 (coherence-check + blocking 없음)
    cc = coherence_check.run(d)
    if cc.get("missing"):
        add(3, "미해결 악화 0", FAIL, "05-coherence-matrix.md 없음")
    elif not cc["ok"]:
        add(3, "미해결 악화 0", FAIL, "; ".join(cc["failures"][:3]) + (" …" if len(cc["failures"]) > 3 else ""))
    elif cc["blocking_ids"]:
        add(3, "미해결 악화 0", FAIL, f"blocking(미해결) 항목: {', '.join(cc['blocking_ids'])}")
    else:
        add(3, "미해결 악화 0", PASS, "모든 악화 칸 구조화 완화책으로 해소")

    # 4. 고위험 open-question 0
    oq_section = None
    for title, b in state_sections.items():
        if "open-question" in title.lower() or "결정 원장" in title:
            oq_section = b
            break
    HIGH_RISK = {"high", "높음", "상", "critical", "치명", "크리티컬"}
    OPEN_STAT = {"open", "열림", "미해결", "미결"}
    high_open = []
    if oq_section is not None:
        rows = subsection_table(oq_section, "미해결")
        hdr = None
        risk_idx = stat_idx = None
        for cells in rows:
            if hdr is None:
                hdr = [c.lower() for c in cells]
                risk_idx = next((i for i, h in enumerate(hdr)
                                 if any(k in h for k in ("위험", "리스크", "risk", "심각", "impact"))), None)
                stat_idx = next((i for i, h in enumerate(hdr)
                                 if any(k in h for k in ("상태", "status", "state"))), None)
                continue

            def _toks(idx):  # 셀을 토큰 집합으로(부분문자열 'high-level'·'highlight' 오탐 방지)
                if idx is None or idx >= len(cells):
                    return set()
                return set(re.split(r"[\s/,·|()]+", cells[idx].lower().strip()))
            if risk_idx is not None and stat_idx is not None:
                risk_high = bool(_toks(risk_idx) & HIGH_RISK)
                still_open = bool(_toks(stat_idx) & OPEN_STAT)
            else:  # 컬럼 식별 실패 → 보수적: 행 전체를 토큰 단위로(여전히 substring 아님)
                rowtoks = set(re.split(r"[\s/,·|()]+", " ".join(cells).lower()))
                risk_high = bool(rowtoks & HIGH_RISK)
                still_open = bool(rowtoks & OPEN_STAT)
            if risk_high and still_open:
                high_open.append(cells[1] if len(cells) > 1 else cells[0])
    if high_open:
        add(4, "고위험 open-Q 0", FAIL, f"열린 고위험 항목: {'; '.join(high_open)}")
    else:
        add(4, "고위험 open-Q 0", PASS, "열린 고위험 open-question 없음")

    # 5. readiness 통과 — 목업 의존. report 모드(Figma 이관)에선 N/A.
    rd = os.path.join(d, "09-readiness.md")
    if mode == "report":
        add(5, "readiness 통과", NA, "보고서 게이트 — 목업/현업검증은 Figma 이관(S9 제외)")
    elif not os.path.isfile(rd):
        add(5, "readiness 통과", FAIL, "09-readiness.md 없음 (S10 미수행)")
    elif "readiness: pass" not in read(rd).lower():
        add(5, "readiness 통과", FAIL, "09-readiness.md 에 'readiness: PASS' 표식 없음")
    else:
        add(5, "readiness 통과", PASS, "readiness: PASS")

    # 6. 모호표현 0 (고정 금지어) — planning-dir 전체 *.md 스캔(3파일 한정 → 전체로 확대)
    vague = []
    for f in sorted(glob.glob(os.path.join(d, "*.md"))):
        for ln, term, _ in scan_vague(f):
            vague.append((os.path.basename(f), ln, term))
    if vague:
        sample = "; ".join(f"{term}@{fn}:L{ln}" for fn, ln, term in vague[:4])
        add(6, "모호표현 0", FAIL, f"{len(vague)}건 (재정의 필요): {sample}")
    else:
        add(6, "모호표현 0", PASS, "고정 금지어 미검출")

    # 7. 미기록 결정 0
    bad_dec = []
    if oq_section is not None:
        rows = subsection_table(oq_section, "결정")
        hdr = None
        for cells in rows:
            if hdr is None:
                hdr = cells
                continue
            # 컬럼: id | 결정 | 결정자 | 날짜 | 근거 | 반영지점
            need = cells[2:6] if len(cells) >= 6 else cells[1:]
            if any(is_placeholder(c) for c in need):
                bad_dec.append(cells[0] if cells else "?")
    if bad_dec:
        add(7, "미기록 결정 0", FAIL, f"결정자/날짜/근거/반영지점 누락: {', '.join(bad_dec)}")
    else:
        add(7, "미기록 결정 0", PASS, "모든 결정 종결 필드 기록됨")

    # 8. Unknown+Important 가정 누락 0
    asm = os.path.join(d, "07-assumptions.md")
    if not os.path.isfile(asm):
        add(8, "가정 누락 0", FAIL, "07-assumptions.md 없음 (S8 미수행)")
    else:
        body = read(asm)
        if "검증 필요" not in body and "검증필요" not in body:
            add(8, "가정 누락 0", FAIL, "'검증 필요 가정' 섹션 없음")
        else:
            add(8, "가정 누락 0", REVIEW, "구조 존재 — Unknown+Important 누락 여부는 독립검토(§14)")

    # 보조 정책 게이트(T3·T4): 잠정 동결([현업검증=확인불가]) → full '완성' 차단 · 토대 [확인불가]/med open 누적 → 신뢰성 '하' 강등.
    prov_unverified = foundation_unverified = False
    med_open = 0
    for f in glob.glob(os.path.join(d, "*.md")):
        t = read(f)
        if "[현업검증=확인불가]" in t:
            prov_unverified = True
        if os.path.basename(f) in ("01-problem-set.md", "02-success.md") and "[확인불가]" in t:
            foundation_unverified = True
    if oq_section is not None:
        hdr = None
        for cells in subsection_table(oq_section, "미해결"):
            if hdr is None:
                hdr = 1
                continue
            toks = set(re.split(r"[\s/,·|()]+", " ".join(cells).lower()))
            if ({"med", "중", "medium"} & toks) and ({"open", "열림", "미해결", "미결"} & toks):
                med_open += 1
    if mode != "report" and prov_unverified:
        add(9, "현업검증 잠정(보조)", REVIEW, "[현업검증=확인불가](잠정 동결) 존재 → '완성' 불가·'조건부' 강제(T3)")

    # --- 리포트 ---
    label = "S8 보고서 게이트" if mode == "report" else "종료 게이트(8조건)"
    print(f"[completion-gate · {label}] {d}")
    fails = [r for r in results if r[2] == FAIL]
    reviews = [r for r in results if r[2] == REVIEW]
    for n, name, verdict, detail in sorted(results):
        mark = {"PASS": "✓", "FAIL": "✗", "REVIEW": "?", "N/A": "·"}[verdict]
        print(f"  {mark} 조건{n} {name}: {verdict} — {detail}")

    # 독립검토 완료 표식(T5, guideline §14) → REVIEW를 PASS로 승격(표식 없으면 유지).
    if "[독립검토=완료]" in read(state_path) and reviews:
        print(f"  · 독립검토 완료 표식 감지([독립검토=완료]) → REVIEW {len(reviews)}건 승격(§14·T5)")
        reviews = []

    # 신뢰성 종합 등급(구조 기반) — 스코어카드 '신뢰성 종합'에 반영. 점수·코멘트는 사람/LLM(도구는 등급만).
    grade = "하" if fails else ("중" if reviews else "상")
    demote = (["토대 [확인불가]"] if foundation_unverified else []) + ([f"med open {med_open}건"] if med_open >= 5 else [])
    if demote:
        grade = "하"
        print(f"  · 신뢰성 강등(T4 보조): {' · '.join(demote)} → '하'")
    print(f"\n신뢰성 종합(구조 기반): {grade}  — 스코어카드 '신뢰성 종합'에 반영. 점수·코멘트는 사람/LLM 판단.")

    if mode == "report":
        if fails:
            print(f"판정: 보고서 미흡 — FAIL {len(fails)}건. 보고서를 내되 결함을 명시하고 보강.")
            return 1
        print(f"판정: 보고서 생성 가능 — S0~S8 구조 충족"
              + (f"(독립검토 대기 {len(reviews)}건은 보고서 '주의'로 명시)." if reviews else ".")
              + " PRD 진행 여부는 ASK 게이트로.")
        return 2 if reviews else 0

    if fails:
        print(f"판정: 미완(NOT COMPLETE) — FAIL {len(fails)}건. '완성' 선언 불가, '조건부'로만 산출.")
        return 1
    if reviews:
        print(f"판정: 조건부 — 구조 8조건 통과, 독립검토 대기 {len(reviews)}건(§14). 검토 후 '완성'.")
        return 2
    print("판정: 완성 가능(COMPLETE) — 8조건 모두 PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
