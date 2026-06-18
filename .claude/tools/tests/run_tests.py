#!/usr/bin/env python3
# run_tests.py — planning-kit 결정적 도구 9종 + 가드 2종 회귀 러너 (DoD §4.1·§2.5, G4·G2).
#   각 컴포넌트를 픽스처/JSON에 대해 서브프로세스로 돌려 종료코드 + 핵심 출력 토큰을 검증한다.
#   종료코드 규약(.claude/hooks/README.md): 0 통과·1 검증FAIL·2 인자오류/조건부/가드차단·3 리소스부재.
#   사용: python .claude/tools/tests/run_tests.py   (OS중립 — sys.executable)

import os
import sys
import subprocess
import tempfile
import shutil

FIX = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(FIX)
HOOKS = os.path.join(os.path.dirname(TOOLS), "hooks")
ROOT = os.path.dirname(os.path.dirname(TOOLS))
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")


def F(*p):
    return os.path.join(FIX, *p)


def run(script, args, stdin=None):
    cp = subprocess.run([sys.executable, script] + args, input=stdin,
                        capture_output=True, text=True, encoding="utf-8", errors="replace",
                        env=ENV, cwd=ROOT)
    return cp.returncode, (cp.stdout or "") + (cp.stderr or "")


def T(name):
    return os.path.join(TOOLS, name)


def H(name):
    return os.path.join(HOOKS, name)


# (라벨, 스크립트, 인자, stdin, 기대종료코드, 포함 토큰)
def tool_cases():
    return [
        ("vague-term-lint  · 위반 검출(FAIL)",   T("vague-term-lint.py"), [F("vague_fixture.md")], None, 1, "FAIL"),
        ("vague-term-lint  · clean(PASS)",        T("vague-term-lint.py"), [F("vague_clean.md")], None, 0, "PASS"),
        ("source-tag-lint  · 누락 검출(FAIL)",    T("source-tag-lint.py"), [F("srctag_fixture.md")], None, 1, "FAIL"),
        ("source-tag-lint  · clean(PASS)",        T("source-tag-lint.py"), [F("srctag_clean.md")], None, 0, "PASS"),
        ("coherence-check  · 빈매트릭스 경고+PASS", T("coherence-check.py"), [F("coh_empty")], None, 0, "경고"),
        ("coherence-check  · 미완화악화(FAIL)",   T("coherence-check.py"), [F("coh_fail")], None, 1, "FAIL"),
        ("coherence-check  · 매트릭스없음(exit3)", T("coherence-check.py"), [F("cg_fixture")], None, 3, "없음"),
        ("completion-gate  · cg_fixture(미완)",   T("completion-gate.py"), [F("cg_fixture")], None, 1, "미완"),
        ("completion-gate  · cg_pass(보고서가능)", T("completion-gate.py"), [F("cg_pass"), "--mode", "report"], None, 2, "보고서 생성 가능"),
        ("prd-handoff-map  · 완전(PASS)",         T("prd-handoff-map.py"), [F("prd_handoff_pass.md")], None, 0, "PASS"),
        ("prd-handoff-map  · 섹션누락(FAIL)",     T("prd-handoff-map.py"), [F("prd_handoff_missing_section.md")], None, 1, "누락"),
        ("prd-handoff-map  · 필드매핑누락(FAIL·4.6)", T("prd-handoff-map.py"), [F("prd_handoff_missing_field.md")], None, 1, "필드"),
        ("prd-handoff-map  · 파일없음(exit3)",    T("prd-handoff-map.py"), [F("__no_such_file__.md")], None, 3, "없음"),
        ("ref-map-lint     · 정합(PASS)",         T("ref-map-lint.py"), [F("refmap_pass")], None, 0, "PASS"),
        ("ref-map-lint     · 경로불일치(FAIL)",   T("ref-map-lint.py"), [F("refmap_fail")], None, 1, "불일치"),
        ("ref-map-lint     · 디렉토리없음(exit3)", T("ref-map-lint.py"), [F("__no_such_dir__")], None, 3, "없음"),
        ("notion-refs-lint · 정합(PASS)",         T("notion-refs-lint.py"), [F("notion_pass")], None, 0, "PASS"),
        ("notion-refs-lint · 존충돌(FAIL)",       T("notion-refs-lint.py"), [F("notion_conflict")], None, 1, "충돌"),
        ("inputs-extract   · csv 추출(PASS)",     T("inputs-extract.py"), [F("inputs_sample.csv")], None, 0, "김기획"),
        ("inputs-extract   · 미지원확장자(exit3)", T("inputs-extract.py"), [F("inputs_unsupported.xyz")], None, 3, "미지원"),
        ("inputs-extract   · 파일없음(exit3)",    T("inputs-extract.py"), [F("__no_such_file__.csv")], None, 3, "없음"),
        ("inputs-extract   · refs URL추출(PASS)", T("inputs-extract.py"), [F("inputs_sample.refs.md")], None, 0, "notion.so"),
        ("mockup-gen       · 인자없음(exit2)",    T("mockup-gen.py"), [], None, 2, "사용"),
        # 미지 옵션 거부(exit2) — 조용한 폴백 금지(§2.5)
        ("completion-gate  · 미지옵션(exit2)",    T("completion-gate.py"), [F("cg_pass"), "--bogus"], None, 2, "알 수 없는"),
        ("vague-term-lint  · 미지옵션(exit2)",    T("vague-term-lint.py"), [F("vague_clean.md"), "--bogus"], None, 2, "알 수 없는"),
        # 가드 2종(stdin JSON) — G2
        ("local-guard      · finalized Edit(차단2)", H("local-readonly-guard.py"), [],
         '{"tool_name":"Edit","tool_input":{"file_path":"docs/reference-context-map/finalized/README.md"}}', 2, "차단"),
        ("local-guard      · open Edit(통과0)",   H("local-readonly-guard.py"), [],
         '{"tool_name":"Edit","tool_input":{"file_path":"docs/reference-context-map/open/x.md"}}', 0, ""),
        ("local-guard      · 깨진JSON(fail-closed2)", H("local-readonly-guard.py"), [], "not json at all", 2, "파싱"),
    ]


def main():
    tmp = tempfile.mkdtemp(prefix="mockup_out_")
    cases = tool_cases()
    cases.append(("mockup-gen       · 생성(PASS)", T("mockup-gen.py"),
                  [os.path.join(tmp, "m.html"), "--title", "테스트 화면", "--screens", "목록,상세"], None, 0, "생성"))
    rows = []
    try:
        for label, script, args, stdin, exp, token in cases:
            code, out = run(script, args, stdin)
            ok = (code == exp) and (token in out)
            why = "" if ok else (f"exit={code}(기대{exp})" if code != exp else f"토큰 '{token}' 없음")
            rows.append((ok, label, code, why))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("== planning-kit 도구·가드 회귀 러너 ==")
    for ok, label, code, why in rows:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:<42} exit={code}  {why}")
    npass = sum(1 for r in rows if r[0])
    total = len(rows)
    comps = sorted({lbl.split('·')[0].strip() for _o, lbl, _c, _w in rows})
    print(f"\n컴포넌트 {len(comps)}종 · 케이스 {total}건 · 통과 {npass}/{total}")
    print("  전건 통과 ✅" if npass == total else "  불일치 있음 ❌ (위 FAIL 행 확인)")
    return 0 if npass == total else 1


if __name__ == "__main__":
    sys.exit(main())
