---
name: strategy-intake
description: 전략기획 하네스의 진입 단계(S0–S1). 기획을 *시작*할 때 — 녹취/관찰·문제+방향·제로베이스·기존문서 등 가변 입력을 받아 입력유형·tier·참조맵 상태를 확정하고, 적응형 인테이크로 공통 산출(동결 후보 문제·맥락)에 수렴시킨다. `/strategy-plan`이 첫 단계로 호출. "전략기획 시작"·"기획 하네스"에도 반응.
---

# strategy-intake — 세션 시작 + 적응형 인테이크 (S0–S1)

방법론 SSoT = [docs/planning-harness-guideline.md](../../../docs/planning-harness-guideline.md) §3·§4·§16. 이 스킬은 그 절차를 *실행*만 한다(방법론 본문을 여기 복붙하지 않는다 — drift 방지).

## 입력 소스 (S0 맥락)
- 사용자가 제공한 *원본* 맥락은 **`inputs/<slug>/`** 에 있다(녹취·문제+방향 메모·제로베이스 목표·기존 문서). 단일 파일이면 보통 `inputs/<slug>/context.md`.
- 시작 시 `inputs/<slug>/`의 파일을 *전부* 읽어 입력유형을 판별한다. 비어있으면 사용자에게 맥락을 묻거나(대화형) `[물어봄]`으로 남긴다(원샷).
- **원본 추출 호출(inputs-extract)**: `inputs/<slug>/`에 텍스트가 아닌 원본(`.xlsx`·`.html`·`.csv`·`.tsv`)이 있으면 **strategy-intake(이 단계)가** `sh .claude/hooks/launch.sh .claude/tools/inputs-extract.py <파일>`로 텍스트를 뽑아 맥락에 병합한다(`.md`/`.txt`는 직접 읽음, `.pdf`는 Read 도구 `pages`). 미지원·실패는 `[확인불가]`로(조용한 폴백 금지).
- `inputs/`는 *원본*(사람이 넣음), `docs/planning/`은 *산출*(하네스가 만듦) — 섞지 않는다.
- **Notion 링크파일(`*.refs.md`)**: `inputs/<slug>/`에 파일명에 `.refs.`가 든 파일(줄바꿈으로 Notion URL 구분)이 있으면 `inputs-extract`가 URL 목록을 뽑는다(헤더 선택). **인증 확인 후** `mcp__claude_ai_Notion__fetch`로 각 URL을 fetch해 `[입력-Notion(as-of=last_edited_time)]` 태그로 맥락에 병합한다. 미인증·권한없음·404는 fetch하지 말고 open-questions에 `[확인불가]`로 남긴다(**조용한 폴백 금지**). 참조맵 링크(finalized/·open/)는 reference-coherence가 처리.

## 산출물
- 작업 폴더 `docs/planning/<slug>/` 생성(slug = 기획 주제, kebab-case — `inputs/<slug>/`와 동일 slug).
- `_state.md` — 템플릿 [.claude/templates/_state.md](../../templates/_state.md) 복사 후 채움(재개 앵커).
- `00-intake.md` — 입력유형·tier·참조맵 상태 + 적응형 인테이크 결과.

## 절차
0. **이해 요지 선(先)컨펌.** `inputs/<slug>/`와 사용자 입력을 읽고 *이해한 요지를 1~3줄로 먼저 요약 → 컨펌*받는다. 어긋나면 S0 전에 바로잡는다(토대 오해 조기 차단). 모호·정보 부족이면 판별 질문부터.
1. **S0 — 세 가지 확정(추측 금지, 묻는다)** — guideline §3:
   1. **입력유형 분류**: (a)녹취/관찰 (b)문제+방향 (c)제로베이스 (d)기존문서. 섞이면 해당 진입을 *모두 돌려 병합*, 불분명하면 *판별 질문* 먼저.
   2. **참조 컨텍스트 맵 상태**: `docs/reference-context-map/` 존재·신선도 확인 → 최신/낡음/비어있음. 비었거나 낡으면 §10 단언 금지, "맵 미보유" 플래그.
   3. **tier 판별(3문)** — guideline §16: ①비가역·경계(인증·결제·PII)? ②2개+팀 영향? ③큰 베팅? 하나라도 예 → **T2**. 셋 다 아니고 국소 → **T0**. 사이 → **T1**.
2. **S1 — 적응형 인테이크** — guideline §4. 유형별로 다르게 시작하되 같은 산출로 수렴:
   - (a)녹취=테마 클러스터링으로 문제·워크플로 귀납 / (b)방향=전제·범위 검증 후 확장 / (c)제로베이스=목표서 역산(Working Backwards) 발산 / (d)기존문서=빈칸 플래그.
   - **추천 우선**: 질문만 던지지 말고 가진 맥락으로 합리적 방안 1~3개를 *장점·단점·리스크 + 추천*과 함께 제시(§4).
   - **의존성 기반 순차**: 한 답이 다음 선택지를 바꾸면 배치를 쪼개 답을 받아 재구성. 독립 질문은 묶는다.
3. **ASK 바닥(불변)** — 비가역·경계·토대(핵심 문제정의·성공기준·기획 의도 범위)는 tier·확신 무관 **무조건 ASK**(CLAUDE 거버넌스).
4. **비대화형(원샷)이면** 막지 말고 진행하되 미해결을 `_state.md` open-questions에 `[물어봄]`으로 남기고, 최종 PRD는 '완성'이 아닌 '조건부'로 간다(§4).

## 산출 파일 규약
- `00-intake.md` 헤더: `<!-- stage: S1 | status: done | updated: <YYYY-MM-DD> -->`. 모든 줄 출처 태그(입력/AI보강/물어봄…).
- `_state.md`: S0·S1 행을 done으로, 현재 포인터=S2, tier·입력유형·참조맵 상태를 채운다.
- 끝나면 사용자에게 "다음: problem-freeze(S2 문제 동결)로 진행" 안내.
