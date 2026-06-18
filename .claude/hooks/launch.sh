#!/usr/bin/env sh
# launch.sh — planning-kit OS중립 파이썬 런처 (T7 · Cycle 1b)
# 목적: 훅·결정적 도구를 python3/python/py 자동탐지로 실행해 Windows(Git Bash)·macOS·Linux에서 동일하게 동작.
#       Claude Code는 Windows에서 Git Bash, mac/linux에서 sh로 훅 명령을 실행하므로 이 POSIX 스크립트 하나로 충분하다.
# 사용:
#   가드 훅:  sh .claude/hooks/launch.sh --guard .claude/hooks/<guard>.py     # stdin=훅 JSON
#   도구:     sh .claude/hooks/launch.sh .claude/tools/<tool>.py [args...]
# 종료코드:
#   - 정상: 실행된 파이썬 스크립트의 종료코드를 그대로 전파(0/1/2/3 …).
#   - 파이썬 인터프리터 미발견(조용한 폴백 금지):
#       · --guard 모드  → exit 2  (가드 matcher는 쓰기성 도구 전부 → '보호 불가=쓰기 차단' fail-closed; T14·§11.1)
#       · 도구 모드     → exit 127 ('게이트 미실행=인프라 실패'; 완성 선언 차단은 오케스트레이터 §11.1 규칙)
set -u

GUARD=0
if [ "${1:-}" = "--guard" ]; then
  GUARD=1
  shift
fi

# 인터프리터 탐지 우선순위: python3 → python → py -3
PY=""
if command -v python3 >/dev/null 2>&1; then
  PY="python3"
elif command -v python >/dev/null 2>&1; then
  PY="python"
elif command -v py >/dev/null 2>&1; then
  PY="py -3"
fi

if [ -z "$PY" ]; then
  echo "[planning-kit launch] Python(python3/python/py)을 찾지 못했습니다 — 조용한 폴백 금지." >&2
  echo "  OS별 설치는 온보딩(docs/onboarding.html)을 따르세요." >&2
  if [ "$GUARD" = "1" ]; then
    exit 2     # 가드: 보호 불가 → 쓰기 차단(fail-closed)
  fi
  exit 127     # 도구: 게이트 미실행(인프라 실패)
fi

# 한글 stderr 인코딩 고정 — Windows 콘솔(cp949)에서 가드 차단 메시지 모지바케 + strict-cp949 fail-open 방지(T18 발견 B, 사람 승인 2026-06-18).
# 가드 2종(local-readonly-guard·notion-zone-guard)은 stderr를 reconfigure하지 않으므로 여기서 일괄 보장한다(도구는 자체 reconfigure, 무해 보강).
export PYTHONIOENCODING=utf-8

# PY가 "py -3"일 수 있어 의도적으로 비인용 확장. 인자는 인용 유지.
exec $PY "$@"
