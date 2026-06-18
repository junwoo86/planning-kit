<!-- stage: S10 | status: <draft|done> | updated: <YYYY-MM-DD> -->
<!--
  09-readiness.md — S10 채택(adoptability) 선검증 템플릿.
  completion-gate: full 모드 cond5 = 'readiness: PASS' 문자열이 있어야 통과. report 모드에선 cond5 = N/A(Figma 이관).
  PASS는 *실측*(n≥5·30초·성공률≥80%) 합격 시에만. 목업 전이면 'readiness: 잠정'(PASS 금지).
-->

# 채택 준비도(readiness) — <SLUG>

## readiness 라벨
- **readiness: <PASS | FAIL | 잠정>**
  <!-- PASS = 절차1∧2∧3 모두 실측 충족 · 잠정 = 목업/Figma 전이라 실측 불가(PASS 아님) · FAIL = 하나라도 미달 -->

## 절차별 판정 (AND — 셋 다 충족해야 PASS)
| # | 항목 | 기준 | 결과 |
|---|---|---|---|
| 1 | 즉시 이해 | 첫 사용자 n≥5명, 도움 없이 핵심 과제 30초 내, 성공률 ≥80% | <PASS/FAIL/잠정> · n=<> 성공률=<%> 소요=<초> |
| 2 | 워크플로 적합 | 기존 as-is(S5)에 자연스럽게 끼움. **별도 행동 강요 = FAIL** | <PASS/FAIL> |
| 3 | 운영·교육·롤아웃 | 운영 주체·교육 주체·**단계적 롤아웃 계획 존재**(빅뱅 금지). 미정 = FAIL | <PASS/FAIL> |

## 미달 항목
- <미달 항목과 사유 — 채택 안 될 기획은 '미완'> [현업검증|물어봄]

## 충실도 주의
- 30초 이해 측정은 *실제 화면* 필요 → 목업/Figma 와이어프레임이 있어야 완전 검증. 그 전엔 **잠정** + "Figma 후 실측". [확인불가]
- 임계값(n·초·%)을 기본값에서 조정했으면 근거를 여기 기록. [AI보강]
