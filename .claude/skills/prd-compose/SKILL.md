---
name: prd-compose
description: 전략기획 하네스의 산출 단계(S11–S12). 동결 문제·성공기준·정합성 매트릭스를 이중 뷰 PRD로 합성한다 — 의사결정용 HTML(GO/조건부/NO-GO) + 개발 핸드오프용 md(devkit feature-spec 호환). 모든 줄 출처 태그. completion-gate 도구로 종료 8조건을 판정해 '완성/조건부'를 정한다. `/strategy-plan`의 마지막 단계.
---

# prd-compose — PRD 산출 + 무결성/종료 게이트 + 핸드오프 (S11–S12)

방법론 SSoT = [guideline](../../../docs/planning-harness-guideline.md) §14(PRD·게이트)·§15(핸드오프). 핸드오프 템플릿 = [.claude/templates/prd-handoff.md](../../templates/prd-handoff.md).
**독립검토 트리거 = §14 T5 단일정의**(T2=veto 필수·T1=권장·T0=불요): T2면 coherence-auditor veto 통과 후에만 '완성'. **NO-GO·1–10 루브릭·등급 변환식 = prd-handoff 템플릿 §"판정 루브릭·NO-GO"(T12)** 를 SSoT로.

## 산출물
- `10-prd.html` — 의사결정 뷰(HTML).
- `10-prd-handoff.md` — 개발 핸드오프 뷰(md, feature-spec 호환).
- `11-handoff.md` — feature-spec 매핑 + open-questions 이관.

## 절차
1. **이중 뷰 합성**(같은 SSoT, 두 표현) — §14:
   - **HTML(의사결정용)**: Executive Summary(**GO/조건부 GO/NO-GO**) 우선 → 문제 → 설계 결정(채택/기각) → Design Detail → 정합성 매트릭스/트레이드오프 시각화 → Risk → Next Step. devkit `decision-doc` 구조 참조. `docs/design-system/` 있으면 톤 참조, 없으면 중립.
     - **의사결정 신뢰성 스코어카드(Executive Summary 직하)**: 평가 항목(근본원인 정확도·근거 충분성·다각도 검토·정합성(악화 처리)·채택 실현가능성)별 점수 + **신뢰성 종합(상/중/하)** + **한계·주의 한 줄**(미검증 가정·blocking·열린 고위험Q). 종합 등급은 `completion-gate` 판정과 일관. 시각: 판정 신호등 · 정합성 +/0/− 색상 히트맵 · 상단 리스크 핀. 점수·코멘트는 정성 판단, 등급은 도구 보조(정직성 원칙).
   - **md(핸드오프용)**: 템플릿대로 fs 섹션 매핑(스코어카드도 md에 동반).
2. **출처·확신도 태그(모든 줄)** — §14: 출처 `[입력]/[AI보강]/[근본원인추론]/[현업검증]/[참조맵:as-of date]/[물어봄]` + 확신도 `[확실]/[추정]/[확인불가]`. 제로베이스일수록 추론 비중↑ → 태그 필수(silent-wrong 방지). 확신도는 스코어카드 '근거 충분성' 입력.
3. **무결성 게이트(셀프)** — technical-review 4축 셀프 체크: 빠진 정책·예외·전제 / 모호 요구(측정불가) / 문서 간 정합성 / 구현 리스크. 고위험(T2)이면 2차 모델·사람 **독립 검토** 추가(§14).
4. **종료(완료) 게이트 — 결정적 도구로 판정**(반드시 실행):
```
python3 .claude/tools/completion-gate.py docs/planning/<slug>
```
   - 8조건: 문제동결·성공기준 측정가능·미해결 악화 0·고위험 open-Q 0·readiness 통과·모호표현 0·미기록 결정 0·가정 누락 0.
   - **exit 0** = 8조건 PASS → '완성' 선언 가능. **exit 2** = 구조 통과·독립검토 대기 → **'조건부 GO'**. **exit 1** = FAIL → '미완', '조건부'로만 산출하고 무엇이 막혔는지 명시.
   - 도구가 출력하는 **신뢰성 종합 등급(상/중/하, 구조 기반)**을 스코어카드 '신뢰성 종합'에 그대로 반영한다(등급=도구, 점수·코멘트=사람/LLM).
   - 도구는 *값·구조*만 결정한다. 측정가능 *적절성*·가정 *누락* 같은 REVIEW 항목은 자동 통과 아님 → 독립검토로 종결(§14). **게이트가 조용한 통과를 막는 것이 정상이다.**
   - 비대화형(원샷)에서 미해결이 남으면 '완성' 금지 → '조건부'.
5. **S12 개발 핸드오프** — §15: PRD md 뷰를 devkit feature-spec 필드로 매핑(`11-handoff.md`). 빈틈은 추측 금지 → open-questions로 이관. devkit은 PRD 출처를 몰라도 된다(느슨 결합).

## 산출 규약
- `10-prd-handoff.md` 헤더 `<!-- stage: S11 | status: draft|done | updated: <date> -->`.
- `_state.md`: S11·S12 상태 갱신, 판정(GO/조건부/NO-GO)과 근거를 결정 원장에. 미해결은 open-questions에 남긴다.
