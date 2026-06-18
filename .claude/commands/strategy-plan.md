---
description: 전략기획 하네스 시작/재개 — 가변 입력을 적응형 인터뷰로 받아 S8 검토 보고서를 내고(opt-in으로 PRD까지) 흔들리지 않는 기획을 만든다(devkit과 분리·선택적).
argument-hint: [기획 주제 또는 slug] (생략 가능 — 진행 중인 작업이 있으면 재개)
---

# /strategy-plan — 상류 전략기획 하네스 오케스트레이터

당신은 지금 **전략기획 하네스**(devkit과 분리된 상류 킷)를 구동한다. 목표는 "빨리"가 아니라 **"조용히 틀린 기획 없이"** — 착수 후 정책이 비어 방향을 잃거나, 두 문제를 풀며 한 문제를 몰래 악화시키는 일이 **0**이 되는 PRD를 만든다. *틀린 채 통과하는 것이 불완전한 것보다 나쁘다.*

방법론 SSoT = [docs/planning-harness-guideline.md](../../docs/planning-harness-guideline.md). 거버넌스 = 루트 `CLAUDE.md`. 아래는 *오케스트레이션*만 한다 — 각 단계의 방법론은 SSoT를, 절차는 스킬을 따른다.

## 0. 재개 우선 (resume-first)
1. `docs/planning/` 아래 진행 중 작업이 있는지 본다. 인자로 slug가 오면 그 폴더, 아니면 가장 최근 `_state.md`.
2. **있으면**: `docs/planning/<slug>/_state.md`를 *먼저* 읽고 → "현재 포인터 → 다음 액션"부터 이어간다. 이미 완료된 단계를 다시 묻지 않는다.
3. **없으면**: 새 기획. 사용자에게 주제를 확인하고 slug를 정한다. **S0 원본 맥락은 `inputs/<slug>/`에서 읽는다**(있으면 전부 읽고, 없으면 사용자에게 맥락을 묻는다). 그 뒤 `docs/planning/<slug>/`와 `_state.md`(템플릿 [.claude/templates/_state.md](../templates/_state.md))를 만든다.

## 1. 파이프라인 — S8 보고서 체크포인트 + ASK 게이트(opt-in 연속)
순서가 기본이되, 각 단계가 끝나면 `_state.md`를 갱신하고 *약속된 파일*에 산출을 남긴다(중단해도 산출물만 보고 이어가게).
**S12까지 직진하지 않는다 — S8에서 보고서를 내고, 연장은 사용자에게 묻는다.**

| 단계 | 스킬(배선) | 산출 | 성숙도 |
|---|---|---|---|
| S0–S1 | **strategy-intake** | `00-intake.md` | ✅ MVP 실증 |
| S2–S3 | **problem-freeze** | `01-problem-set.md`(frozen)·`02-success.md` | ✅ MVP 실증 |
| S4 / S5 | **reference-scout** / **workflow-edge-map** | `03-references.md`·`04-workflow-edge.md` | 초안(배선됨) |
| S6 | **coherence-matrix** | `05-coherence-matrix.md` | ✅ MVP 실증 |
| S7 / S8 | **reference-coherence** / **assumption-manage** | `06-cross-domain.md`·`07-assumptions.md` + 참조맵 | 초안(배선됨) |
| **S8 완료 → 보고서** | **report-compose** (+ 템플릿 `report.md`) | **`REPORT.md`** | ✅ MVP 실증 |
| **ASK G1** "PRD 보완 진행?" | — | No→종료 / Yes↓ | — |
| S10 / S11 | **adoptability-check** / **prd-compose** | `09-readiness.md`·`10-prd.html`·`10-prd-handoff.md` | ✅ MVP 실증 |
| **ASK G2** "HTML 목업(S9) 진행?" | — | No→'조건부' 종료(Figma 이관) / Yes↓ | — |
| S9 → S12 | **mockup-elicit** → prd-compose | `08-mockups/`·`11-handoff.md` | 초안(배선됨) |

> **종결 모델(guideline §2)**: S8 보고서가 1차 산출물. **ASK G1**(보고서 시점)에서 PRD 진행을 묻고, *Yes*면 PRD 작성 →
> **ASK G2**(PRD 마무리)에서 HTML 목업을 묻는다. 기본은 *목업 No = 기획팀이 Figma로 별도 와이어프레임* → PRD '조건부' 종료.
> *Yes*면 S9 목업 루프로 PRD 보강·readiness 검증 후 S12까지 풀 진행.
> **초안(배선됨)** 단계는 파이프라인에 *호출 경로가 있고 절차 골격이 있으나* MVP 실사용 검증 전이라 첫 실사용에서 고도화한다(거짓 '작동' 주장 금지). 산출이 비거나 얕으면 게이트(`--mode report`)가 N/A/REVIEW로 잡아 '조건부'로 정직하게 표시한다.

## 2. 인터뷰 원칙 (전 단계 공통)
- **추천 우선**: 질문만 던지지 말고 가진 맥락으로 합리적 방안 1~3개를 *장점·단점·리스크 + 추천*과 함께 제시.
- **의존성 순차**: 한 답이 다음 선택지를 바꾸면 배치를 쪼갠다. 독립 질문은 묶고, 여러 ASK는 모아 한 번에.
- **ASK 바닥(불변)**: 비가역·경계(인증·결제·PII)·토대(문제정의·성공기준·기획 의도 범위)는 tier·확신 무관 무조건 멈추고 묻는다.
- **비대화형(원샷)**: 막지 말고 진행하되 미해결을 `[물어봄]`으로 남기고 PRD는 '완성' 아닌 '조건부'.

## 3. 결정적 게이트 (스킬이 호출, 여기서 보장)
- 정합성: `sh .claude/hooks/launch.sh .claude/tools/coherence-check.py docs/planning/<slug>` — 미해결 악화 0 확인.
- **S8 보고서 게이트**: `sh .claude/hooks/launch.sh .claude/tools/completion-gate.py docs/planning/<slug> --mode report` — 목업/readiness 조건 N/A. 보고서 생성 가능 여부 + 신뢰성 종합 등급.
- **종료(완성) 게이트**: `sh .claude/hooks/launch.sh .claude/tools/completion-gate.py docs/planning/<slug> --mode full` — 8조건. exit 0=완성·2=조건부·1=미완. **0 전엔 '완성'을 선언하지 않는다.** (ASK G2에서 목업 Yes → 풀 진행한 경우에만 완성 가능.)

## 4. 참조 컨텍스트 맵 갱신 (S8 보고서 직후 · reference-coherence 위임)
- 도메인 요약을 성숙도별로 `docs/reference-context-map/{finalized|open}/`에 등재한다. **모델·역할·등재규칙 = guideline §10**(단일 컨트롤), 절차 = `reference-coherence` 스킬.
- 도메인 2개+면 `cross-domain-analysis.md` 재검토. 구조 점검 = `sh .claude/hooks/launch.sh .claude/tools/ref-map-lint.py docs/reference-context-map`. 폴더는 `ensure-refmap` 훅이 자동 보장.

## 5. 마무리
- 산출 요약은 과정을 못 본 독자 기준 완전한 문장으로: 판정(보고서/조건부/완성)·신뢰성 종합 등급·근거·남은 open-questions·다음 ASK.
- 하네스 자체(스킬/도구/규칙)를 임의 수정하지 않는다 — 변경은 제안+사람 승인(거버넌스).

$ARGUMENTS
