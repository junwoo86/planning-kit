#!/usr/bin/env python3
# completion-gate-reminder (DRAFT 훅) — Stop 용. 진행 중 기획이 종료 게이트를 통과하지 않았는데
# 멈추려 하면 *비차단 리마인더*를 띄운다("완성"을 섣불리 선언하지 않게). blueprint §1.6 종료 게이트 훅.
#
# ⚠️ 초안이며 settings.json에 *미연결*이다. 또 *비차단*(exit 0)으로 시작한다 — 하드 차단은 검증 후.
# 진행 중 도메인 = docs/planning/<d>/_state.md 가 있고 REPORT.md/PRD 가 아직 게이트 미통과인 것.

import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "..", "tools", "completion-gate.py")


def main():
    pending = []
    for state in glob.glob("docs/planning/*/_state.md"):
        d = os.path.dirname(state)
        try:
            r = subprocess.run([sys.executable, GATE, d, "--mode", "report"],
                               capture_output=True, text=True, timeout=30)
            if r.returncode == 1:  # 보고서 게이트조차 미흡
                pending.append(os.path.basename(d))
        except Exception:
            continue
    if pending:
        print(f"[planning-kit 리마인더] 다음 도메인이 보고서 게이트 미통과 상태입니다: {', '.join(pending)}. "
              f"'완성/확정'을 선언하기 전에 `completion-gate`로 확인하세요. (비차단 안내)")
    return 0  # 비차단


if __name__ == "__main__":
    sys.exit(main())
