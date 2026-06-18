#!/usr/bin/env python3
# suggest-activation (DRAFT 훅) — UserPromptSubmit 용. 강한 전략·전사·혁신·도메인충돌 신호를 감지하면
# planning-kit 사용을 *조용히 제안*만 한다(강제 X, 거부 가능). blueprint §1.6 활성화 훅.
#
# ⚠️ 초안이며 settings.json에 *미연결*이다. 활성화는 .claude/hooks/README.md 참고.
# 입력: stdin JSON({"prompt": "..."} 형태 가정). 출력: 감지 시 additionalContext로 가벼운 제안.

import json
import sys

SIGNALS = ["전사", "IPO", "상장", "프로세스 파괴", "다팀", "여러 팀", "전략 방향",
           "혁신", "도메인 충돌", "의존성", "큰 베팅", "신사업", "비전"]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = (data.get("prompt") or data.get("user_prompt") or "")
    hits = [s for s in SIGNALS if s in prompt]
    if len(hits) >= 2:  # 약한 신호 1개로는 제안하지 않음(노이즈 방지)
        msg = ("[planning-kit 제안] 강한 전략/전사 신호 감지(" + ", ".join(hits[:3]) +
               "). 흔들리지 않는 기획이 필요하면 `/strategy-plan`을 고려하세요. (제안일 뿐 — 무시해도 됩니다.)")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                 "additionalContext": msg}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
