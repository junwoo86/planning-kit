---
name: assumption-manage
description: 전략기획 하네스의 가정·가설 관리(S8). 기획이 깔고 있는 가정을 desirability·feasibility·viability × Known/Unknown × Important로 분류하고, Unknown+Important 가정을 '검증 필요 가정'으로 빼 위험한 것은 실험·조사로 검증한다. 가정한 채 큰 베팅하지 않게 막는다.
---

# assumption-manage — 가정·가설 관리 + 선례 보강 (S8)

방법론 SSoT = [guideline](../../../docs/planning-harness-guideline.md) §11. 절차만 실행한다.

## 산출물
- **입력**: 여기까지의 산출(`01`~`06`)이 깔고 있는 가정. **산출**: `07-assumptions.md`('검증 필요 가정' 섹션 필수 — 헤더 `<!-- stage: S8 | status: done -->`). **하류 소비처**: S8 보고서 §6·completion-gate cond8.

## 절차
1. **가정 매핑(Assumption Mapping)**: 기획이 깔고 있는 가정을 *desirability(원하나)·feasibility(되나)·viability(해야 하나)* × *Known/Unknown × Important*로 분류. **추출 멈춤 기준(actionable-root)**: 가정의 가정을 캐되 *통제 밖 도달 OR 반복 OR 해소 시 베팅이 안 흔들림* 닿으면 멈춘다.
2. **Unknown + Important 가정** → PRD/보고서의 **'검증 필요 가정' 섹션**으로 빼고, 위험한 것은 실험·조사로 검증(가정한 채 큰 베팅 금지). 각 가정에 *검증 방법* 명시.
3. **선례·경쟁 조사 연계**: S4 레퍼런스를 해법에 반영하되, 깊은 조사는 비-devkit `deep-research`(다출처·인용·사실/추정 분리)로 위임.
4. **종료 게이트 연동**: completion-gate cond8은 '검증 필요 가정' 섹션 존재를 구조적으로 확인한다. *누락 0*이 목표 — Unknown+Important인데 등재 안 된 가정이 없어야 한다.

## 산출 규약
- 각 가정: 분류(D/F/V·Known/Unknown·Important) · 검증 방법 · 확신도 태그. Unknown+Important는 [물어봄].
- `_state.md`: S8 상태 갱신. 미검증 큰 가정은 open-questions에도 연결. → S8 완료 = report-compose 트리거.
