#!/usr/bin/env python3
# ref-map-lint — 참조 컨텍스트 맵의 성숙도/경로 구조를 *결정적* 검증 (guideline §10, 3그룹 모델).
# 검사: 각 도메인 항목 헤더에 status(확정|검토|컨셉)가 있고, 경로(finalized/ vs open/)와 일치하는가.
#   - finalized/<d>.md  → status 반드시 '확정'
#   - open/<d>.md       → status 반드시 '검토' 또는 '컨셉'
# 판정하지 않는 것: status *분류 자체의 타당성*(그 PRD가 정말 확정인가) → 사람 판단.
#
# 사용:  sh .claude/hooks/launch.sh .claude/tools/ref-map-lint.py docs/reference-context-map
# 종료코드: 0 = 구조 정합, 1 = 불일치, 2 = 인자 없음, 3 = 디렉토리 없음. (규약: .claude/hooks/README.md)

import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

STATUS_RE = re.compile(r"status\s*[:：]\s*(확정|검토|컨셉)")
OPEN_OK = {"검토", "컨셉"}


def header_status(path):
    with open(path, encoding="utf-8") as f:
        head = f.read(600)
    m = STATUS_RE.search(head)
    return m.group(1) if m else None


def scan(folder):
    out = []
    if not os.path.isdir(folder):
        return out
    for name in sorted(os.listdir(folder)):
        # 폴더 안내 README·언더스코어/점 시작 파일은 도메인 항목이 아니므로 제외
        if name.endswith(".md") and name.lower() != "readme.md" and not name.startswith(("_", ".")):
            out.append(os.path.join(folder, name))
    return out


def main(argv):
    bad = [a for a in argv[1:] if a.startswith("--")]
    if bad:
        print(f"[ref-map-lint] 알 수 없는 옵션: {' '.join(bad)} (이 도구는 옵션 없음)", file=sys.stderr)
        return 2
    if len(argv) < 2:
        print("사용: sh .claude/hooks/launch.sh .claude/tools/ref-map-lint.py docs/reference-context-map", file=sys.stderr)
        return 2
    root = argv[1]
    if not os.path.isdir(root):
        print(f"[ref-map-lint] 디렉토리 없음: {root}  (첫 도메인 기획 때 생성)", file=sys.stderr)
        return 3

    fails, count = [], 0
    print(f"[ref-map-lint] {root}")
    for kind, folder, allowed in (("finalized", os.path.join(root, "finalized"), {"확정"}),
                                  ("open", os.path.join(root, "open"), OPEN_OK)):
        for path in scan(folder):
            count += 1
            st = header_status(path)
            if st is None:
                fails.append(f"{path}: 헤더에 status(확정|검토|컨셉) 없음")
            elif st not in allowed:
                fails.append(f"{path}: status='{st}' 인데 {kind}/ 폴더 → 경로 불일치 "
                             f"({'open/으로 이동' if st in OPEN_OK else 'finalized/으로 이동'})")
            else:
                print(f"  ✓ {os.path.relpath(path, root)}  (status: {st})")

    idx = os.path.join(root, "index.md")
    if not os.path.isfile(idx):
        fails.append("index.md 없음 (전체 도메인 인덱스 필요)")

    if fails:
        print()
        for f in fails:
            print(f"  ✗ {f}")
        print(f"\n결과: FAIL — {len(fails)}건. (확정=finalized/, 검토·컨셉=open/)")
        return 1
    print(f"\n결과: PASS — 도메인 {count}개 status/경로 정합.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
