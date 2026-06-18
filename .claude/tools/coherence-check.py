#!/usr/bin/env python3
# coherence-check — 정합성 매트릭스(05-coherence-matrix.md)의 *결정적* 판정 (guideline §9 / blueprint §1.4)
#
# 판정하는 것(값/구조가 명확한 것만):
#   1. 매트릭스의 모든 악화(-) 칸이 완화책 id를 참조하는가  (맨 '-' = FAIL)
#   2. 참조된 id가 '악화(−) 원장'에 항목으로 존재하는가
#   3. 원장 항목의 구조화 필드(담당·구체행동·결정기록)가 채워졌고 플레이스홀더가 아닌가
#   4. status 어휘가 유효한가 (mitigated|blocking|rescoped)
# 판정하지 않는 것: 완화책의 *적절성*, 근본원인 해소 *여부* → 사람/독립검토(§14).
#
# 사용:  sh .claude/hooks/launch.sh .claude/tools/coherence-check.py <planning-dir>
# 종료코드: 0 = 통과, 1 = FAIL(미해결 악화/구조 결함), 3 = 입력 파일 없음.
#
# blocking 항목은 "기록은 됐으나 미해결"이다 → coherence-check은 통과시키되 결과에 표시한다.
# completion-gate가 종료(완성) 판정 시 blocking을 cond3 미충족으로 본다.

import os
import re
import sys

# Windows 콘솔(cp949 등)에서도 한글·기호를 깨지지 않게 출력
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

MATRIX_FILE = "05-coherence-matrix.md"
VALID_STATUS = {"mitigated", "blocking", "rescoped"}
REQUIRED_FIELDS = ("담당", "구체행동", "결정기록")
PLACEHOLDERS = {"", "-", "?", "tbd", "tba", "todo", "추후", "미정", "n/a", "na", "없음", "추후 결정", "추후결정"}

WORSEN_REF = re.compile(r"-\s*\[([^\]]+)\]")        # -[M1]
LEDGER_HEAD = re.compile(r"^###\s*\[([^\]]+)\]\s*$")  # ### [M1]
FIELD_LINE = re.compile(r"^-\s*([^:：]+)[:：]\s*(.*)$")  # - 담당: ...


def is_placeholder(value):
    raw = (value or "").strip()
    # 템플릿 스캐폴딩(<...>)은 미기입으로 본다
    if raw.startswith("<") and raw.endswith(">"):
        return True
    v = raw.lower()
    if v in PLACEHOLDERS:
        return True
    return v.startswith("추후") or v.startswith("tbd") or v.startswith("todo")


def split_sections(lines):
    """## 헤더 기준으로 섹션을 나눠 {제목: [라인...]} 반환 (제목은 '##' 제거·trim)."""
    sections, cur, buf = {}, None, []
    for ln in lines:
        m = re.match(r"^##\s+(.*?)\s*$", ln)
        if m:
            if cur is not None:
                sections[cur] = buf
            cur, buf = m.group(1), []
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        sections[cur] = buf
    return sections


def find_section(sections, *needles):
    for title, body in sections.items():
        low = title.lower()
        if all(n.lower() in low for n in needles):
            return body
    return None


def is_separator_row(cells):
    return all(set(c.strip()) <= set("-: ") and c.strip() for c in cells)


def parse_table(body):
    """| ... | 행들을 셀 리스트의 리스트로. 헤더/구분행 포함 그대로 반환."""
    rows = []
    for ln in body:
        s = ln.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            rows.append(cells)
    return rows


def run(planning_dir):
    """반환: dict(ok, failures, warnings, blocking_ids, report)."""
    res = {"ok": True, "failures": [], "warnings": [], "blocking_ids": [], "report": []}
    path = os.path.join(planning_dir, MATRIX_FILE)
    if not os.path.isfile(path):
        res["ok"] = False
        res["missing"] = True
        res["failures"].append(f"{MATRIX_FILE} 없음 ({path})")
        res["report"].append(f"[coherence-check] {MATRIX_FILE} 없음 ({path}) — 매트릭스 파일이 있어야 판정 가능.")
        return res

    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    sections = split_sections(lines)

    # --- 매트릭스 표에서 악화 칸 수집 ---
    matrix = find_section(sections, "매트릭스")
    referenced = []   # (problem, element, id)
    bare_worsen = []  # (problem, element)
    headers = None
    if matrix is None:
        res["ok"] = False
        res["failures"].append("'## 매트릭스' 섹션을 찾지 못함")
    else:
        rows = parse_table(matrix)
        data_rows = []
        for cells in rows:
            if is_separator_row(cells):
                continue
            if headers is None:
                headers = cells
                continue
            data_rows.append(cells)
        if not data_rows:
            res["warnings"].append(
                "매트릭스에 데이터 행이 없음 — 검증할 문제×요소 칸이 비어 있음"
                "(빈 매트릭스인지 확인; '악화 0'을 검증된 결과로 보지 말 것).")
        for cells in data_rows:
            problem = cells[0] if cells else "?"
            for ci in range(1, len(cells)):
                cell = cells[ci]
                col = headers[ci] if headers and ci < len(headers) else f"열{ci}"
                if cell in ("+", "0", ""):
                    continue
                if cell.lstrip().startswith("-") or cell.lstrip().startswith("−"):
                    m = WORSEN_REF.search(cell.replace("−", "-"))
                    if m:
                        referenced.append((problem, col, m.group(1).strip()))
                    else:
                        bare_worsen.append((problem, col))
                else:
                    res["warnings"].append(f"알 수 없는 셀 표기 '{cell}' ({problem} × {col})")

    for problem, col in bare_worsen:
        res["ok"] = False
        res["failures"].append(f"악화 칸에 완화책 id 없음: {problem} × {col}  (→ '-[id]' 표기 필요)")

    # --- 악화(−) 원장 파싱 ---
    ledger_body = find_section(sections, "악화")
    entries = {}  # id -> {field: value}
    if ledger_body is not None:
        cur_id, cur = None, {}
        for ln in ledger_body:
            hm = LEDGER_HEAD.match(ln.strip())
            if hm:
                if cur_id is not None:
                    entries[cur_id] = cur
                cur_id, cur = hm.group(1).strip(), {}
                continue
            if cur_id is not None:
                fm = FIELD_LINE.match(ln.strip())
                if fm:
                    cur[fm.group(1).strip()] = fm.group(2).strip()
        if cur_id is not None:
            entries[cur_id] = cur

    ref_ids = {rid for _, _, rid in referenced}

    # 참조됐으나 원장에 없는 id
    for problem, col, rid in referenced:
        if rid not in entries:
            res["ok"] = False
            res["failures"].append(f"악화 칸 {problem} × {col} 의 완화책 [{rid}] 원장 항목 없음")

    # 원장 항목 구조 검사
    for rid, fields in entries.items():
        status = (fields.get("status") or "").strip().lower()
        if status not in VALID_STATUS:
            res["ok"] = False
            res["failures"].append(f"[{rid}] status 무효: '{status}' (mitigated|blocking|rescoped)")
        if status == "blocking":
            res["blocking_ids"].append(rid)
        for fld in REQUIRED_FIELDS:
            if is_placeholder(fields.get(fld)):
                res["ok"] = False
                res["failures"].append(f"[{rid}] 필드 '{fld}' 비어있거나 플레이스홀더: '{fields.get(fld, '')}'")
        if rid not in ref_ids:
            res["warnings"].append(f"원장 [{rid}] 항목이 매트릭스 어느 악화 칸에서도 참조되지 않음(고아)")

    # --- 리포트 구성 ---
    r = res["report"]
    r.append(f"[coherence-check] {path}")
    r.append(f"  악화(-) 칸: {len(referenced) + len(bare_worsen)}개  /  원장 항목: {len(entries)}개")
    if res["blocking_ids"]:
        r.append(f"  ⚠ blocking(미해결, 사람 결정 대기): {', '.join(res['blocking_ids'])}")
    for w in res["warnings"]:
        r.append(f"  · 경고: {w}")
    if res["failures"]:
        for fmsg in res["failures"]:
            r.append(f"  ✗ {fmsg}")
        r.append("  결과: FAIL — 미해결 악화/구조 결함을 해소해야 한다.")
    else:
        r.append("  결과: PASS — 모든 악화 칸이 구조화된 완화책으로 처리됨"
                 + ("(단, blocking 항목은 종료 게이트에서 미해결로 본다)." if res["blocking_ids"] else "."))
    return res


def main(argv):
    bad = [a for a in argv[1:] if a.startswith("--")]
    if bad:
        print(f"[coherence-check] 알 수 없는 옵션: {' '.join(bad)} (이 도구는 옵션 없음)", file=sys.stderr)
        return 2
    if len(argv) < 2:
        print("사용: sh .claude/hooks/launch.sh .claude/tools/coherence-check.py <planning-dir>", file=sys.stderr)
        return 2
    res = run(argv[1])
    print("\n".join(res["report"]))
    if res.get("missing"):
        return 3
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
