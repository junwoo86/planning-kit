# 동봉 예시 — quote-automation (완주 샘플)

킷이 **S0~S8 + 검토 보고서(G1=No)** 까지 끝까지 돈 모습의 *참고용 예시*입니다(가상 사례: B2B 견적 자동화).
실제 사용자 작업물이 아니라 **킷에 동봉된 레퍼런스**이므로 레포에 함께 추적됩니다(작업 디렉토리 `docs/planning/`과 분리).

## 구성
- `context.md` — 입력(원래 `inputs/quote-automation/`에 두는 S0 원본 맥락).
- `_state.md` — 재개 앵커(단계 상태·open-questions·결정 원장).
- `00-intake.md` … `07-assumptions.md` — 단계별 산출.
- `REPORT.md` — S8 검토 보고서(판정·신뢰성 스코어카드).

## 동작 확인 (온보딩 §동작확인과 동일)
```
sh .claude/hooks/launch.sh .claude/tools/completion-gate.py docs/examples/quote-automation --mode report
```
→ `판정: 보고서 생성 가능` + 종료코드 `2`(미해결 악화 0·고위험 open 0·모호표현 0, 측정가능성/가정은 독립검토 대기).
