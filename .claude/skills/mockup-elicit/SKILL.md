---
name: mockup-elicit
description: 전략기획 하네스의 목업 기반 UI/UX 도출 루프(S9, opt-in). PRD 마무리 시점 ASK G2에서 "Yes"일 때만 실행 — 자체 경량 HTML 목업을 생성(mockup-gen)해 전역 Playwright로 렌더·검증하고, 기획자 수정 프롬프트를 취합·충돌검사·정합성 재검 후 PRD(SSoT)에 반영한다. 기본 경로는 기획팀 Figma라 보통 호출되지 않는다.
---

# mockup-elicit — 목업 UI/UX 도출 루프 (S9) ★ · opt-in

방법론 SSoT = [guideline](../../../docs/planning-harness-guideline.md) §12. 도구 = [mockup-gen.py](../../tools/mockup-gen.py) + 전역 Playwright MCP(`mcp__playwright__*`).

## 활성화
- **ASK G2에서 "HTML 목업 진행 = Yes"일 때만.** 기본은 기획팀이 Figma로 와이어프레임 → 이 스킬 미호출.

## 산출물
- **입력**: `10-prd-handoff.md`(화면 상태 §4)·`04-workflow-edge.md`(화면 상태 목록) — ASK G2 "Yes"일 때만. **산출**: `docs/planning/<domain>/08-mockups/*.html`(자족적 단일 HTML). **하류 소비처**: prd-compose(SSoT 반영)·`09-readiness.md`.

## 루프 (guideline §12)
1. **목업 생성**: `sh .claude/hooks/launch.sh .claude/tools/mockup-gen.py docs/planning/<domain>/08-mockups/<screen>.html --title "..." --screens "..." [--design-system docs/design-system]`. *적정 충실도*로 — lo-fi 먼저(픽셀 bikeshedding 회피).
2. **렌더·검증**: 전역 Playwright MCP로 띄워 스크린샷·상호작용 확인. (복잡 상호작용은 Wizard-of-Oz로 흉내.)
3. **기획자 반응 수집**: 화면을 보고 "여길 이렇게" 수정 프롬프트를 받는다.
4. **취합 + 충돌 검사**: 프롬프트를 UI/UX 요구로 수집·중복제거하고 **프롬프트끼리 모순**("X 맨 위로" ↔ "X 제거")을 검사 → 충돌은 취합 전 ASK.
5. **정합성 재검**: 취합 변경(수정/추가/제거)을 §9 매트릭스 + 동결 문제집합 + 참조 맵에 다시 통과. 새 문제면 '변경 요청'.
6. **PRD 반영**: 통과한 변경을 **PRD(SSoT)에 반영**. 필요 시 목업 재생성.

## 리스크 규칙(반드시)
- **외형 ≠ 구현가능성**: 목업엔 "외형 전용·구현 검증 안 됨" 태그(mockup-gen이 배너 삽입). 암시 기능은 조용히 약속 말고 tech-planning 타당성으로 라우팅.
- **충실도 함정**: 목업은 *버릴 수 있는* 도출 도구. 최종 디자인 아님.
- **UI발 스코프 팽창**: 목업 보다 생긴 욕심도 문제집합·정합성 게이트 통과 필수.
- **PRD↔목업 drift**: **PRD가 SSoT**. 목업은 프로브 — 프롬프트가 PRD를 갱신한다.
- **루프 멈춤 기준(actionable-root)**: 목업 수정 **3라운드 초과면 ASK**(수렴 안 되는 신호 — 기획 의도/범위 재확인). 픽셀 bikeshedding으로 라운드 소모 금지.

## 산출 규약
- `_state.md`: S9 상태 갱신. 목업발 변경 결정은 결정 원장에. 통과 후 readiness(S10)·S12로.
