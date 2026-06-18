<!--
  planning-kit-blueprint.md — 전략기획 하네스를 "분리된 선택적 킷"으로 패키징하는 설계 청사진
  작성: 2026-06-16 · 출처: 대표 설계 인터뷰 8라운드.
  관계: planning-harness-guideline.md(방법론 SSoT)를 *어떻게 기계장치로 구성하는가*의 설계도.
  주의: 이 문서는 *설계도*다. 실제 스킬/훅/에이전트/도구 설치는 AI가 직접 하지 않는다 —
        제안 번들(creator/propose-harness-change) → 사람 승인·설치. (devkit 거버넌스 불변.)
-->

# planning-kit 설계 청사진 — devkit과 분리된 선택적 전략기획 킷

## 0. 설계 목표 (대표 결정 반영)

- **devkit에 강제로 엮지 않는다.** 평소 dev 작업(일반 기능·버그 등)엔 *오버헤드 0*. 안 부르면 작동하지 않는다.
- **유일한 접점 = 산출 PRD 아티팩트.** devkit `feature-planning`은 이 킷의 PRD를 *입력*으로 받기만 한다 —
  출처도, 존재도 몰라도 된다. 코드/게이트 결합 0(느슨 결합).
- **drift 방지.** devkit common 개념(ask-and-fallback·tier·출처태그·doc-quality)은 **복사하지 않고 참조/정렬**한다.
- **AI는 제안만.** 하네스 기계장치 설치·머지는 사람.

---

## 1. 컴포넌트 맵 (devkit outputs 분류 준수)

> 스킬=*절차*("실행한다") · 템플릿=*틀*("채운다") · 규칙=*기준*("지킨다/참조한다") · 도구=*결정적 판정*("돌린다").
> 스킬에 틀·규칙·결정적 로직을 박지 않고, 템플릿/규칙/도구를 *참조*만 한다.

### 1.1 규칙 (SSoT 기준)
> ⚠️ **현황 정정(2026-06-18, T9)**: 별도 `rules/` 디렉토리는 **아직 생성하지 않았다**(아래 standards 파일들 미존재). T9 결정 = 별도 standards 파일을 새로 만들지 않고, **guideline 해당 절을 잠정 SSoT로** 쓰고 **모호표현 금지어는 `vague-term-lint.py` 데이터를 단일 출처로** 둔다(본문은 링크만, 중복 0). `_devkit-alignment.md`는 devkit 비활성이라 **보류**(open-question).

| 규칙(잠정 SSoT 위치) | 역할 | 현 위치 |
|---|---|---|
| `planning-harness-guideline.md` | **마스터 SSoT**(방법론 본문) | ✅ 존재 |
| 정합성 기준(악화 처리·근본원인) | coherence-standards 대체 | guideline §9·§14 (잠정 SSoT) |
| 성공기준 기준(3층·사전약속 임계값) | success-criteria-standards 대체 | guideline §6·§14 (잠정 SSoT) |
| **모호표현 금지어 목록** | success-criteria의 금지어 | **`vague-term-lint.py` `VAGUE_TERMS`(단일 출처)** — 본문은 링크만 |
| 레퍼런스 기준(실사용·카고컬트) | reference-standards 대체 | guideline §7 (잠정 SSoT) |
| `_devkit-alignment.md` | devkit 참조 항목 명시 | **보류**(devkit 비활성 — open-question) |

### 1.2 스킬 (`skills/` — 파이프라인 단계별 절차)
| 스킬 | 단계 | 산출 |
|---|---|---|
| `strategy-intake` | S0–S1 | 입력유형 분류·tier 보정·적응형 진입 |
| `problem-freeze` | S2 | 5whys 근본원인 → 동결 문제집합 |
| `success-criteria` | S3 | 계층형 3층 + 측정가능 지표 |
| `reference-scout` | S4 | 실사용 레퍼런스·unknown-unknowns(카고컬트 게이트) |
| `workflow-edge-map` | S5 | as-is/to-be + 엣지 강제질문 |
| `coherence-matrix` | S6 | 문제↔요소 매트릭스·대안→게이트·RICE/ICE |
| `reference-coherence` | S7 | 방어(비례)+발산(선택적 인사이트) |
| `assumption-manage` | S8 | 검증 필요 가정 + 선례 보강(→ devkit research/deep-research) |
| `mockup-elicit` | S9 | mock HTML 생성·프롬프트 취합·정합성 재검·PRD 반영 |
| `adoptability-check` | S10 | 현업 준비도(readiness) |
| `prd-compose` | S11 | 이중 뷰 PRD·출처태그·무결성/종료 게이트 |
| `handoff-to-dev` | S12 | feature-spec 매핑·open-questions 이관 |

> **양방향 다리(원칙 §1.4)는 별도 스킬이 아니라 *교차 관심사*다**: 전략 승격 = `problem-freeze`(S2)에 주입,
> 현업 검증 = `workflow-edge-map`(S5)·`adoptability-check`(S10)에 주입. 두 방향이 누락되지 않게 각 스킬 체크리스트에 명시한다.

### 1.3 템플릿 (`templates/` — 채울 틀)
`problem-set`(동결 원장) · `success-criteria` · `coherence-matrix` · `reference-context-map`(포맷·신선도 규칙) ·
`assumptions` · `readiness` · `prd`(이중 뷰: HTML decision-doc + md handoff) · `reference-teardown`.

### 1.4 도구 (`tools/` — 결정적 판정, LLM 아님)
| 도구 | 판정 |
|---|---|
| `coherence-check` | *완화책 없는 악화(−) 칸* 존재 → fail. 완화책 칸은 *구조화 필드(담당·구체 행동·결정기록 링크)* 필수 — 플레이스홀더("추후")는 fail (doc-quality 패턴) |
| `vague-term-lint` | **고정 금지어 목록**("실시간·100%·빠르게·직관적"…) 탐지 → 재정의 요구 (결정적). 그 밖의 *의미적* 모호성은 LLM 보조 검토(비결정적 → 독립검토) |
| `completion-gate` | 종료 **8조건**(동결·성공기준·악화0·고위험Q0·**readiness 통과**·모호0·미기록0·**가정누락0**) 판정 |
| `source-tag-lint` | 모든 줄 출처 태그 존재 검사 |
| `prd-handoff-map` | PRD 섹션 → feature-spec 필드 매핑 완전성 검사 |

> 정직성 원칙: 도구는 *값·구조가 명확한* 것만 결정적으로 판정한다(금지어 목록·악화 칸 구조·매핑 완전성·태그 존재).
> 완화책 *적절성*·열린 *의미적 모호성*·근본원인 *해소 여부* 같은 판단은 LLM 보조이며, 자동 게이트가 아니라 §14 독립 검토로 간다.

### 1.5 에이전트 (`agents/`)
| 에이전트 | 역할 | 비고 |
|---|---|---|
| `strategy-planner` | 인터뷰 오케스트레이터(상류 PM) | product-planner의 *상류* 짝 |
| `reference-scout` | 독립 레퍼런스 탐색 | 카고컬트 게이트 적용 |
| `coherence-auditor` | 매트릭스·PRD 적대적 독립검토 | spec-reviewer 패턴(veto) |
| `mockup-elicitor` | mock 화면 생성·프롬프트 취합 | 외형 전용 태그 강제 |

### 1.6 훅 (`hooks/`)
- **활성화 훅(opt-in + 감지 제안)**: 명시 호출(슬래시) 기본. *강한 전략·전사·혁신 신호* 감지 시 "이 킷 쓸까요?"
  **제안만**(거부 가능). 절대 자동 강제 안 함.
- **종료 게이트 훅(T2)**: `completion-gate` 통과 전 "완성" 선언 차단(devkit Stop 게이트 패턴 *참조*).

---

## 2. 활성화 모델 (둘 다)

1. **명시 호출(기본)** — `/strategy-plan` (별칭: "전략기획 시작"·"기획 하네스") 또는 스킬 트리거로 시작. 평소엔 침묵.
2. **맥락 감지 제안** — IPO·전사·"기존 프로세스 파괴"·다팀 영향 등 강한 신호 감지 시 *조용한 제안*.
   감지는 *제안*까지만, 실행은 사용자 승인.

---

## 3. 아티팩트 핸드오프 (devkit 연결의 전부)

```
[planning-kit]  적응형 인터뷰 → PRD(이중 뷰)
                                  │  (md 뷰 = feature-spec 호환)
                                  ▼
[devkit]        feature-planning → tech-planning → 구현 → 검증
```

- PRD의 **md 핸드오프 뷰**가 devkit feature-spec 필드로 매핑(`prd-handoff-map` 도구로 완전성 검사).
- 빈틈 → open-questions로 이관(추측 금지). devkit은 PRD 출처를 몰라도 된다.

---

## 4. drift 방지 (분리의 대가 관리)

- 별도 킷이 devkit 개념을 *복사*하면 두 곳이 어긋난다(SSoT 위반). → `_devkit-alignment.md`에
  *참조하는 항목*(ask-and-fallback·tier·출처태그·doc-quality 철학)과 *버전*을 명시하고, 복사본을 두지 않는다.
- devkit이 바뀌면 정렬 문서만 갱신(단일 지점).

---

## 5. 단계적 구축 순서 (제안 번들로)

> 전부를 한 번에 만들지 않는다. 검증하며 키운다.

| 단계 | 범위 | 상태(as-of) |
|---|---|---|
| **P0** | 방법론 지침 SSoT + 이 청사진 | ✅ 완료 |
| **P1 (MVP)** | 코어 4 스킬(`strategy-intake`·`problem-freeze`·`coherence-matrix`·`prd-compose`) + `coherence-check`·`completion-gate` + 핵심 템플릿 + `/strategy-plan` + 거버넌스 | ✅ 완료 |
| **P2** | 차별 기둥 — 7 스킬(`reference-scout`·`workflow-edge-map`·`reference-coherence`·`assumption-manage`·`report-compose`·`mockup-elicit`·`adoptability-check`) + 4 에이전트 + 5 도구(linter류) + 3 훅(드래프트) + 참조맵 모델 | 🟡 **초안 배선 완료** — orchestrator 파이프라인 **배선됨**(미구축 토큰 0). 절차 골격이라 첫 실사용에서 고도화(거짓 '작동' 주장 금지) |
| **(킷 구축 DoD)** | 종료 8게이트 갭축소 — [planning-kit-dod.md](planning-kit-dod.md) | 🟢 진행 — G2·G4·G5·G6·G7 충족, G1·G3·G8 작업 중 |
| **P3** | 운영 — 참조맵 콘텐츠 축적 + 훅 정식 연결 + tier 자동화 | ⏳ 예정 |

> 이 표가 **구축 현황의 SSoT**다(per-session `CLAUDE.md`엔 기록을 두지 않고 여기로 링크). 스킬은 절차 골격이라 첫 실사용에서 빠진 질문·엣지가 드러나고, 그게 다음 고도화 입력이 된다. 미완 단계 산출이 없으면 게이트가 '조건부'로 정직하게 표시(설계대로).

각 단계는 **creator/propose-harness-change 제안 번들**(why + diff + 근거) → **사람 승인·설치**.
안전·거버넌스 코어는 제안 대상도 아니다(사람이 repo에서 직접).

---

## 6. 후속 결정 — 확정 (2026-06-16)

### 6.1 킷 배포 = 프로젝트 로컬 `.claude/` (MVP)
이 프로젝트(`c:\WORKPLACE\Planning`)의 `.claude/`에 둔다. 구조:
```
.claude/
├── settings.json              # devkit 격리 + 권한 (6.2)
├── skills/<name>/SKILL.md      # planning-kit 스킬 (§1.2)
├── agents/<name>/agent.md      # 에이전트 (§1.5)
├── commands/strategy-plan.md   # 슬래시 명령 (6.2)
└── hooks/hooks.json            # 활성화/종료 게이트 훅 (§1.6)
```
프로젝트 루트 `CLAUDE.md` = **`CLAUDE.planning-lite.md`(기획자 전용 거버넌스)**. devkit common core + **planning-team 규칙**의
*기획 버전* 압축 — 개발 전용 `CLAUDE.fable5-lite.md`가 **아니다**(그건 dev-team용: TDD·code-style·코드 검증 4축).
devkit 주입 없이 *기획* 거버넌스(출처 태그·정책 완전성·기획 의도 보존·단일 원장·정합성 검증)를 가져온다.
방법론은 별도 SSoT(`docs/planning-harness-guideline.md`), 이 파일은 *행동 거버넌스*.

### 6.2 슬래시 명령 = `/strategy-plan` + devkit 도구 격리 (Claude Code 공식 문서 검증 완료)
- **슬래시 명령**: `/strategy-plan` (별칭 트리거: "전략기획 시작"·"기획 하네스"). 파일 `.claude/commands/strategy-plan.md`.
- **devkit 격리** — planning-kit은 devkit *플러그인* 도구가 불필요(코어 WebSearch/WebFetch + 비-devkit `deep-research` 스킬 +
  자체 HTML 생성으로 충분). 따라서 **완전 비활성**이 가장 깨끗(노이즈 0, SessionStart 주입까지 정지):
```json
{
  "enabledPlugins": { "devkit@allosta-internal": false },
  "permissions": { "deny": ["mcp__plugin_devkit_*"] }
}
```
  `enabledPlugins:false` → devkit의 MCP·스킬·에이전트·**SessionStart 주입 전부 정지**. deny는 안전망.
- **취사선택이 꼭 필요할 때만**(권장 아님): 플러그인을 *켜둔 채* `permissions.deny`로 *원치 않는* 서버만 차단(figma·playwright)
  + `skillOverrides`로 불필요 스킬 `off`. **유지할 도구는 deny하지 않는다** — ⚠️ deny가 allow를 이기므로(precedence)
  "전체 deny 후 일부 allow"는 불가. 단, 이 경로는 devkit SessionStart 주입이 남는 트레이드오프.
  (출처: code.claude.com/docs — permissions(deny>ask>allow)·settings(enabledPlugins·skillOverrides)·plugins.)

### 6.3 재개(resume) 장치 — 산출물만 보고 이어가기
S0~S12는 순차 진행하며 **각 단계가 약속된 경로의 약속된 파일에 상태를 명시**한다. 중단 후 돌아와도 산출물만으로 이어간다.
- 작업 폴더: **`docs/planning/<slug>/`** (slug = 기획 주제).
- **`_state.md` = 재개 앵커(필수)**: 단계 상태표(S0~S12 = done/in-progress/pending) · *현재 포인터* · *다음 액션* · 최종수정.
- 단계별 산출(약속된 이름): `00-intake.md` · `01-problem-set.md` · `02-success.md` · `03-references.md` · `04-workflow-edge.md` ·
  `05-coherence-matrix.md` · `06-cross-domain.md` · `07-assumptions.md` · `08-mockups/`(HTML) · `09-readiness.md` ·
  `10-prd.html` + `10-prd-handoff.md` · `11-handoff.md`.
- 각 파일 헤더 = 단계 · 상태(draft/frozen/done) · 최종수정 · 출처태그. frozen은 *변경 요청 프로토콜*로만 바뀐다.
- **재개 규약**: 세션 시작 시 `_state.md`를 먼저 읽고 *현재 포인터의 다음 액션*부터 재개. (devkit `state.md` 패턴 차용.)
- `completion-gate`는 `_state.md` + 산출 파일을 읽어 종료 8조건 판정.

### 6.4 목업(S9) = opt-in. 기본 = Figma 와이어프레임(기획팀 별도), 선택 시 자체 경량 HTML
- **활성화 모델(2026-06-16 확정)**: S9 목업은 *제거가 아니라 ASK 게이트(opt-in)*다. 기본 경로 = 기획팀이 **Figma**로 와이어프레임을
  별도 진행(킷은 안 함). PRD 마무리 시점 **ASK G2**에서 "HTML 목업을 진행할까요?"에 *Yes*일 때만 아래 자체 HTML 루프를 돈다.
- 자체 경량 HTML 생성기(`mockup-gen` 도구)를 둔다. 산출 = 자족적 단일 HTML → `docs/planning/<slug>/08-mockups/`.
- **디자인시스템 경로 = `docs/design-system/`**. 여기에 디자인시스템 문서(`docs/design-system/index.html` 또는 토큰 파일)가
  *있으면* 그 톤앤매너(색·타이포·간격·컴포넌트)를 참조해 생성, *없으면* 중립 lo-fi(흑백·플레이스홀더).
- **렌더·스크린샷·상호작용 검증 = 전역 Playwright MCP(`mcp__playwright__*`)**. 이건 `~/.claude.json` 전역 설정이라
  **devkit과 무관하게 모든 킷에서 사용 가능**(devkit 비활성과 무관). devkit 번들 `mcp__plugin_devkit_playwright__*`는 꺼져도
  전역 것이 남는다(둘 다 `@playwright/mcp`, 기능 동일). 목업 HTML을 실제로 띄워 보고 캡처·검증하는 데 쓴다.

### 6.5 참조 컨텍스트 맵 — 설계 결정(모델 본문은 guideline §10이 SSoT)
> ⚠️ 이 절은 *결정 기록*이다. 모델의 작동(역할·등재 경로·신선도 규칙) 본문은 **guideline §10**에만 둔다(단일 컨트롤). 바뀌면 §10만 고친다.
- **리프레임 결정(2026-06-16)**: "전사 컨텍스트 맵" → 목적을 단정하지 않는 **참조 컨텍스트 맵**(도메인 산출물의 점진 확장 모음집)으로 일반화.
- **실무 반영(2026-06-16)**: 성숙도 3그룹(확정/검토/컨셉) + 역할(확정=고정 제약 · 검토·컨셉=참고 의견) + 등재 2경로(킷 via `inputs/` · 사람 직접 참조). → 상세 = guideline §10.
- **위치**: `docs/reference-context-map/`(`index.md`·`finalized/`·`open/`·`cross-domain-analysis.md`). 템플릿 = `.claude/templates/reference-context-map.md`·`cross-domain-analysis.md` · 구조 점검 = `ref-map-lint` · 폴더 자동 보장 = `ensure-refmap` 훅.

### 6.6 산출 종결 모델 — S8 보고서 체크포인트 + ASK 게이트 (2026-06-16 확정)
- 파이프라인은 S12까지 직진하지 않고 *선택적으로 연장*한다(어떤 단계도 제거하지 않음).
- **S8 완료 → `docs/planning/<domain>/REPORT.md` 생성**(템플릿 `report.md`) + 참조 맵 갱신. `completion-gate --mode report`로 보고서 게이트.
- **ASK G1**("PRD 보완 진행?") No→보고서 종료 / Yes→S10·S11. **ASK G2**(PRD 마무리, "HTML 목업 진행?") No→'조건부' 종료(Figma 이관) /
  Yes→S9 목업 루프+readiness+**S12 풀 진행**(`--mode full`).
- 착수 게이트: 6.1~6.4 적용 + planning-kit `.claude/` 세팅 완료 후. (참조 맵은 첫 도메인 기획부터 채워진다.)
