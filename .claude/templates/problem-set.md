<!-- stage: S2 | status: draft | updated: <YYYY-MM-DD> -->
<!--
  01-problem-set.md — S2 동결 문제집합 템플릿.
  completion-gate cond1: 이 파일 header status 가 'frozen' + _state 단계표 S2 상태가 'frozen' 이어야 통과.
  동결 전 = draft. 동결 시 위 status 를 frozen 으로 바꾸고 _state S2 도 frozen 으로.
-->

# 동결 문제집합 — <SLUG>

> 5whys로 근본원인까지 내려 **동결**. 동결 후 변경은 변경요청 프로토콜(guideline §5)로만.

## 5whys (요약)
1. <증상> → 왜? <…>
2. <…> → 왜? <…>
3. <…> → 왜? <…>
4. <…> → 왜? <…>
5. **근본원인**: <통제 밖 도달 OR 원인 반복 OR 해소 시 증상 재발 안 함 — 멈춤 휴리스틱(actionable-root)> [근본원인추론] [추정]

## frozen (동결 문제집합)
| id | 문제(근본원인 수준) | 증상 | 출처 | 확신도 |
|---|---|---|---|---|
| P1 | <근본원인 수준 문제> | <증상> | [입력] | [추정] |

## non-goal (이번 범위 밖)
- <이번에 풀지 않는 것 — 범위 부풀림 방지> [입력]

> 동결: <YYYY-MM-DD>. 변경 시 _state 변경이력 + 하류(S3·S5·S6·S7) stale 재실행.
