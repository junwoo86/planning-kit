#!/usr/bin/env python3
# prd-handoff-map — PRD 핸드오프 뷰(md)가 devkit feature-spec 매핑을 *실질적으로* 갖는지 결정적 검사 (guideline §15).
# 빈틈은 추측으로 메우지 않고 open-questions로 넘기는지의 구조 점검 — 매핑 완전성만 본다(내용 적절성은 사람).
#   (4.6 강화) 형식(소스 섹션 헤딩 존재)만이 아니라, 각 섹션 헤딩이 대응 feature-spec 필드(→ fs§N / open-questions)를
#   실제로 가리키는지(매핑 주석 존재)를 확인하고, 누락된 *필드*를 이름으로 보고한다.
#
# 사용:  sh .claude/hooks/launch.sh .claude/tools/prd-handoff-map.py <10-prd-handoff.md>
# 종료코드: 0 = 모든 섹션·필드 매핑 존재, 1 = 누락(섹션 or 필드), 2 = 인자 없음, 3 = 파일 없음. (규약: .claude/hooks/README.md)

import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# (라벨, [헤딩에서 찾을 소스 키워드 후보], fs 필드 토큰(헤딩에 있어야 매핑됨), fs 필드 설명)
REQUIRED = [
    ("문제집합·목적",   ["문제집합", "목적"],            "fs§3",          "기능 목적·non-goal"),
    ("성공기준",        ["성공기준"],                    "fs§10",         "완료 기준"),
    ("워크플로(to-be)", ["워크플로"],                    "fs§4",          "유저 플로우"),
    ("화면 상태",       ["화면 상태", "화면상태"],        "fs§5",          "화면 상태"),
    ("정책·규칙",       ["정책"],                        "fs§6",          "정책·규칙"),
    ("엣지·예외",       ["엣지", "예외"],                "fs§8",          "예외 케이스"),
    ("검증 필요 가정",  ["검증 필요", "검증필요", "가정"], "open-questions", "검증 필요 가정"),
    ("미해결·악화",     ["미해결", "악화"],              "open-questions", "미해결·악화"),
]


def headings(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            s = ln.strip()
            if s.startswith("#"):
                out.append(s.lstrip("#").strip())
    return out


def main(argv):
    bad = [a for a in argv[1:] if a.startswith("--")]
    if bad:
        print(f"[prd-handoff-map] 알 수 없는 옵션: {' '.join(bad)} (이 도구는 옵션 없음)", file=sys.stderr)
        return 2
    if len(argv) < 2:
        print("사용: sh .claude/hooks/launch.sh .claude/tools/prd-handoff-map.py <10-prd-handoff.md>", file=sys.stderr)
        return 2
    path = argv[1]
    if not os.path.isfile(path):
        print(f"[prd-handoff-map] 파일 없음: {path}", file=sys.stderr)
        return 3
    heads = headings(path)
    print(f"[prd-handoff-map] {path}")
    missing_section, missing_field = [], []
    for label, kws, fs_token, fs_desc in REQUIRED:
        matching = [h for h in heads if any(kw in h for kw in kws)]
        section_ok = bool(matching)
        # 매핑 완전성: 소스 섹션 헤딩이 대응 fs 필드 토큰(→ fs§N / open-questions)을 실제로 가리켜야 한다.
        mapping_ok = any(fs_token in h for h in matching)
        if not section_ok:
            mark, note = "✗", "섹션 없음"
            missing_section.append(label)
        elif not mapping_ok:
            mark, note = "✗", f"섹션은 있으나 → {fs_token} 매핑 주석 누락"
            missing_field.append((label, fs_token, fs_desc))
        else:
            mark, note = "✓", "OK"
        print(f"  {mark} {label}  → {fs_token} {fs_desc}  [{note}]")

    if missing_section or missing_field:
        if missing_section:
            print(f"\n  · 섹션 누락 {len(missing_section)}개: {', '.join(missing_section)}")
        if missing_field:
            fields = ", ".join(f"{lbl}→{tok}" for lbl, tok, _ in missing_field)
            print(f"  · 필드 매핑 누락 {len(missing_field)}개: {fields}")
        print("\n결과: FAIL — 매핑 완전성 미달. 빈틈은 추측 말고 open-questions로 이관(누락 섹션·필드를 채우거나 명시).")
        return 1
    print("\n결과: PASS — 8개 소스 섹션 + feature-spec 필드 매핑 완전.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
