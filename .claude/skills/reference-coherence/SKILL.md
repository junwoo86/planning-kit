---
name: reference-coherence
description: 전략기획 하네스의 참조 정합·교차 도메인 분석(S7). 도메인 PRD들을 성숙도 3그룹(확정/검토/컨셉)으로 분류해 목적별 경로로 두고, 참조 컨텍스트 맵을 가로질러 의존성·충돌·선제 완성 우선순위를 도출한다. 확정은 고정 제약으로, 열린(검토·컨셉) 도메인은 영향·의존성 판단 + 방향 수정 제안 대상으로 다룬다.
---

# reference-coherence — 참조 정합·교차 도메인 (S7)

방법론 SSoT = [guideline](../../../docs/planning-harness-guideline.md) §10. 템플릿 = [reference-context-map.md](../../templates/reference-context-map.md)·[cross-domain-analysis.md](../../templates/cross-domain-analysis.md). 절차만 실행한다.

## 산출물
- **입력**: 이 도메인 산출(`01`~`05`) + `docs/reference-context-map/`(finalized/open · `*.refs.md`). **하류 소비처**: S8 보고서 §5(교차 도메인 시사점)·선제 완성 우선순위.
- `06-cross-domain.md` — 이 도메인의 교차 시사점(헤더 `<!-- stage: S7 | status: done -->`).
- `docs/reference-context-map/{finalized|open}/<domain>.md` 추가/갱신 + 도메인 2개+면 `cross-domain-analysis.md` 재검토.

## 성숙도·역할·등재 (모델 SSoT = guideline §10)
모델 본문(역할·등재 경로·신선도)은 **guideline §10**을 따른다 — 여기 재서술하지 않는다. 운영 요점만:
- **확정 → `finalized/`(고정 제약)** · **검토·컨셉 → `open/`(참고 의견)**. 확정되면 open→finalized 이동.
- 등재 2경로: `source: 킷`(inputs/ 작업) vs `source: 참조`(사람 직접). **킷은 `source: 참조` 항목을 덮어쓰지 않는다.**
- **Notion 링크파일(`*.refs.md`)도 `source: 참조`의 한 표현형**(별도 경로 아님). finalized/·open/의 `<도메인>.refs.md`는 헤더 status로 분류하고 `notion-refs-lint`로 구조 점검. **finalized 링크 = 읽기전용**(fetch만, 수정·주석 금지) · open 링크 = 양방향 수정 제안 가능. 인증 세션에서만 fetch하고, 미인증·권한없음은 `[확인불가]`. 자식 페이지는 별도 page-id라 부모 등록만으론 못 막으니 **finalized 하위 트리 전체를 읽기전용으로** 다룬다(페이지 단위 한계).
- 통합 PRD(여러 도메인 섞임)는 도메인별로 쪼개 status 판정 — 모호하면 ASK.

## 절차
1. **등재·분류**: 대상 PRD(들)를 도메인으로 쪼개 status(확정/검토/컨셉)를 판정하고 위 경로에 요약 등재(템플릿 B 포맷).
2. **방어(정합성) — 비례 적용**: 고파급만 풀체크. 이 도메인이 다른 도메인 프로세스·데이터·정책을 악화시키는가.
3. **교차 도메인 분석(검토보고서)** → `cross-domain-analysis.md`: ① 의존성/영향도 매트릭스(확정 열은 제약 표시) ② 충돌 지점(확정 vs 열림이면 열린 쪽 조정) ③ **도메인별 방향 수정 제안**(열린 도메인만; 확정은 제외) ④ **선제 완성 우선순위**(어떤 *열린* 도메인을 먼저 확정하면 불확실성↓ — 피의존·leverage·비가역). ⑤ **확정 공유 수치(§2.5)**: 여러 도메인이 공유하는 확정 수치(총량·단가·에너지 등)는 공유수치표에 *단일 등재* — 도메인 산출물·핸드오프는 값을 복제하지 말고 "K#"로 인용(drift 방지).
4. **발산(거시 묘안)** — *상시 on, 라벨된 선택적 인사이트*(취사). scope 강박은 라벨로 방지.
5. **신뢰성 통제 + 구조 점검**: [출처·수집일·confidence] + 2+ 교차검증, 신선도 6개월. `python3 .claude/tools/ref-map-lint.py docs/reference-context-map`로 구조 검사.

## 산출 규약
- 참조 맵 항목 헤더에 `status: 확정|검토|컨셉` 필수(ref-map-lint가 검사).
- `_state.md`: S7 상태 갱신. 충돌·우선순위·status 변경은 결정 원장에. 적대적 독립검토가 필요하면 coherence-auditor 에이전트(**발동 트리거 = guideline §14 T5 단일정의** — T2면 veto 필수).
- **결정 변경 프로토콜**: 결정(D)을 번복·추가하면 같은 작업에서 그 D의 `_state` '반영지점' 전부 + 공유수치표(K#)를 동기화한다. 변경이력은 `(중간)`/`(최종)`으로 표기해 최종 상태를 명확히(stale·provenance 드리프트 방지).
