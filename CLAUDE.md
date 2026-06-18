# Planning — 전략기획 프로젝트 (planning-kit)

이 프로젝트는 **devkit과 분리된, 선택적으로 호출하는 상류(上流) 전략기획 하네스 "planning-kit"** 자체를 구축·운용하는 곳이다.
devkit 플러그인은 비활성(`.claude/settings.json`의 `enabledPlugins:false`)이며, 거버넌스는 아래 *기획자 전용* 지침을 따른다.

## 거버넌스 (행동 규칙)
@CLAUDE.planning-lite.md

> 위 import = 기획팀 공통 행동 거버넌스(출처 가시화·정책 완전성·정합성 검증·ASK 바닥·단일 원장). **방법론**(어떻게 PRD를 만드는가)은 별도 SSoT다 — 아래 작업 지도 참조.

## 작업 지도

### 핵심 문서 (SSoT)
- 방법론 SSoT = [docs/planning-harness-guideline.md](docs/planning-harness-guideline.md) — 성공 방정식 4원칙 · 파이프라인 S0~S12 · 워크드 예시.
- 킷 설계도 = [docs/planning-kit-blueprint.md](docs/planning-kit-blueprint.md) — 컴포넌트 맵 · §6 확정 결정 · 단계적 구축(P0~P3).
- 참조 컨텍스트 맵 = `docs/reference-context-map/`(세션 시작 시 `ensure-refmap` 훅이 폴더 자동 보장) — `finalized/`(확정=고정 제약)·`open/`(검토·컨셉=참고 의견)·`cross-domain-analysis.md`. Notion 링크는 `<도메인>.refs.md`로 둘 수 있다(finalized=읽기전용 · open=조정 가능; 검증 `notion-refs-lint`).

### planning-kit (`.claude/`)
- **시작/재개** = `/strategy-plan` (별칭: "전략기획 시작"·"기획 하네스"). 진행 중 작업이 있으면 `_state.md`부터 재개.
- 스킬(11종) = [.claude/skills/](.claude/skills/): **코어** `strategy-intake`(S0–S1)·`problem-freeze`(S2–S3)·`coherence-matrix`(S6)·`prd-compose`(S11–S12) · **P2 초안** `reference-scout`(S4)·`workflow-edge-map`(S5)·`reference-coherence`(S7)·`assumption-manage`(S8)·`report-compose`(S8보고서)·`mockup-elicit`(S9)·`adoptability-check`(S10).
- 에이전트(4종) = [.claude/agents/](.claude/agents/): `strategy-planner`·`reference-scout`·`coherence-auditor`·`mockup-elicitor`.
- 결정적 도구(9종) = [.claude/tools/](.claude/tools/): `coherence-check`·`completion-gate`(report/full) · `vague-term-lint`·`source-tag-lint`·`prd-handoff-map`·`mockup-gen`·`ref-map-lint` · `inputs-extract`(원본→텍스트, `*.refs.` URL 추출) · `notion-refs-lint`(`.refs.md` 헤더↔존 정합·존충돌·finalized 매니페스트).
- 템플릿(6종) = [.claude/templates/](.claude/templates/): `_state`·`coherence-matrix`·`prd-handoff`·`report`·`reference-context-map`·`cross-domain-analysis`.
- 훅 = [.claude/hooks/](.claude/hooks/): **연결됨(settings.json PreToolUse, exit 2)** `local-readonly-guard`·`notion-zone-guard`(finalized 읽기전용 강제 — 기존 내용 수정·finalized Notion 쓰기 차단). DRAFT·미연결 — `ensure-refmap`(스캐폴드, 1회 실행됨)·`suggest-activation`·`completion-gate-reminder`.

### 입력·산출물 위치 (섞지 않는다)
- **입력(사람이 넣음)** = `inputs/<slug>/` — S0 원본 맥락(녹취·문제+방향·제로베이스·기존 문서). 단일 파일이면 `inputs/<slug>/context.md`. Notion 링크는 `*.refs.md`(파일명에 `.refs.`)로 둘 수 있다(URL 한 줄씩).
- **산출(하네스가 만듦)** = `docs/planning/<slug>/` — 재개 앵커 `_state.md` + 단계별 산출(`00-intake.md` … `11-handoff.md`). slug는 입력과 동일.
  - **파일번호↔단계 매핑**: 파일번호 = 산출 슬롯 순번(0부터) → 대체로 **파일번호 = 단계번호 − 1**(`00`=S1 … `07`=S8 … `11`=S12). 헷갈리는 지점 = **`03`=S4·`06`=S7·`07`=S8**, 목업 `08-mockups/`(S9)는 번호상 PRD(`10`)보다 앞이나 *실행*은 ASK G2 후. 동일 표·전체 = [`_state` 템플릿](.claude/templates/_state.md)·[README §4](README.md). 파일명은 도구가 하드코딩 참조 → 변경 금지.
- `./docs/` = 산출물(한 주제 한 문서, 복사 말고 링크). 의사결정(PRD)은 HTML, 방법론·명세는 md.
- 기획팀 사용 매뉴얼 = 루트 [README.md](README.md)(사람용). 이 CLAUDE.md는 *AI 거버넌스+지도*.

## 구축 현황
- P0·P1 완료 · **P2 초안 배선 완료** — 11스킬 전부 작성·orchestrator 파이프라인 **배선됨**. 코어(intake·problem-freeze·coherence-matrix·report-compose·adoptability·prd-compose)는 MVP 실증, P2 5종(reference-scout·workflow-edge-map·reference-coherence·assumption-manage·mockup-elicit)은 **초안(배선) — 첫 실사용에서 고도화**(거짓 '작동' 주장 금지). 상세 = [blueprint §5](docs/planning-kit-blueprint.md)(구축 현황 SSoT).

> 하네스 컴포넌트(스킬·도구·규칙)는 AI가 임의 수정하지 않는다 — 변경은 diff+이유 제안으로, 적용은 사람 승인.
