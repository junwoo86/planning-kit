---
name: report-compose
description: 전략기획 하네스의 S8 검토 보고서 산출 — S0~S8 진행분을 통합한 1차 의사결정 보고서를 만들고, 참조 컨텍스트 맵을 갱신하며, 보고서 게이트로 신뢰성 등급을 판정한다. 그다음 ASK G1("PRD 보완 진행?")으로 연장 여부를 묻는다. 목업(S9)은 포함하지 않는다(기획팀 Figma 별도).
---

# report-compose — S8 검토 보고서 + 참조 맵 갱신 (종결 체크포인트)

방법론 SSoT = [guideline](../../../docs/planning-harness-guideline.md) §2(ASK-게이트 플로우)·§14(스코어카드). 템플릿 = [report.md](../../templates/report.md).

## 산출물
- `docs/planning/<domain>/REPORT.md` (헤더 `<!-- stage: S8-report | status: draft|done -->`).
- `docs/reference-context-map/<domain>.md` 추가/갱신.

## 절차
1. **통합 합성**: S0~S8 산출(`00`~`07`)을 보고서로 통합 — 요약·판정·동결 문제·성공기준·정합성 결론·교차 도메인 시사점·검증 필요 가정·열린 이슈. 목업(S9)은 *제외*.
   - **참조 맵 반영**: `reference-context-map/finalized/`(확정)는 **반드시 맞춰야 할 제약**으로, `open/`(검토·컨셉)은 **참고 가능한 의견**으로 §6에 끌어온다(open은 구속력 없이 참고 반영).
2. **의사결정 신뢰성 스코어카드**(요약 직하): 항목별 1–10 점수 + 신뢰성 종합(상/중/하) + 한계·주의 한 줄. **루브릭·등급 변환식·NO-GO 조건은 prd-handoff 템플릿 §"판정 루브릭·NO-GO"(T12)를 SSoT로 따른다**(평균 상≥8/중5–7.9/하<5, 한 항목 ≤3이면 '하' 강등). 종합 등급은 보고서 게이트 출력과 교차확인(불일치 시 보수적). **보고서 단계엔 '채택 실현가능성' 항목을 가중 0.5 + (잠정)** 으로 — 목업/Figma 전이라 실측 불가(readiness 잠정과 일관).
3. **출처·확신도 태그(모든 줄)**: 출처 + [확실]/[추정]/[확인불가].
4. **보고서 게이트(결정적, 반드시 실행)**:
```
sh .claude/hooks/launch.sh .claude/tools/completion-gate.py docs/planning/<domain> --mode report
sh .claude/hooks/launch.sh .claude/tools/source-tag-lint.py docs/planning/<domain>/REPORT.md
sh .claude/hooks/launch.sh .claude/tools/vague-term-lint.py docs/planning/<domain>/REPORT.md
```
   exit 0/2 = 보고서 생성 가능(2=조건부), exit 1 = 미흡(결함 명시 후 보강). cond5(readiness)는 N/A(Figma 이관).
5. **참조 맵 갱신**: 이 도메인 요약을 `reference-context-map/<domain>.md`에 등재. 도메인 2개+면 `cross-domain-analysis.md` 재검토(reference-coherence).
6. **ASK G1**: 사용자에게 **"PRD 보완작업을 진행할까요?"** → *No* = 보고서로 종료(참조 맵 확장 모드) / *Yes* = prd-compose(S10·S11)로 진행.

## 산출 규약
- `_state.md`: S8 보고서 행 갱신, 판정(보고서/조건부)과 신뢰성 등급을 결정 원장에. 다음 ASK를 현재 포인터에 명시.
