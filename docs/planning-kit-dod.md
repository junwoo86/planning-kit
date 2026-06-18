<!--
  planning-kit-dod.md - 킷 구축 완성 정답지(Definition of Done)
  작성: 2026-06-18 · 출처: 전수 정책공백 스윕(9-에이전트 워크플로 run wf_9c37d54d-fd4, 후보 183건) + 선행 감사 6대 문제.
  위상: 킷 *구축*의 수용기준 SSoT. 방법론 SSoT(planning-harness-guideline.md)·설계 SSoT(planning-kit-blueprint.md)와 별개로
        "킷이 언제 완성인가"를 측정가능하게 못박고 갭축소 사이클의 기준선이 된다. dogfooding: 킷의 completion-gate를 킷 자신에게.
  거버넌스: 정책 결정(§9 T1~T14)은 사람 인터뷰로 종결. 하네스 본체 수정은 diff+이유 제안 -> 사람 승인. 이 문서는 새 산출물이라 생성 허용.
  상태: 정책 14개 확정(2026-06-18, 전 항목 추천안)·인터뷰 종결. **§10 게이트 G1~G8 8/8 충족(2026-06-18) → DoD 기준 '킷 구축 완성' 조건 충족**(정직 단서는 §10 종합 판정 — P2 초안 성숙도·notion/macOS 실측·부록 A 잔여).
  진행: Cycle 1 = 안전·실행 기반(A1 python3 + T7 런처 + T14 훅) 착수.
        Cycle 2 = 도구 견고성(§4) 완료 → **G4 충족**(러너 29케이스). **G2 안전 완료**(2.1~2.5, 가드 fail-closed·종료코드 규약 통일·보호한계 README). 다음: G7·G6·G5·G1·G3·G8.
-->

# planning-kit 구축 완성 정답지 (Definition of Done)

> **이 문서의 정체**: planning-kit이 자기 자신을 검수하는 dogfooding 문서다. 킷의 종료 게이트(`completion-gate`, 종료 8조건) 사상 — "성공을 단언하지 않고 근거로 증명한다 · 값·구조가 명확한 것은 결정적 체크로 판정한다" — 을 **킷 구축 자체**에 적용한다.
> **사용 전제**: 컨텍스트가 희석돼도 *이 문서만* 보면 "무엇이 완성인가"와 "지금 무엇이 갭인가"를 측정가능하게 판정할 수 있어야 한다. 따라서 모든 완성조건은 `[ ]` 체크박스 + **검증방법(명령/관찰)** 으로만 쓴다. "적절히/잘/충분히/직관적/안정적" 같은 모호어는 이 문서에서 금지한다 — 킷의 `vague-term-lint` 규율을 문서 자신에게도 적용한다.
> **작성 근거**: 선행 감사 6대 문제 + 16개 정책결정 테마 + 캐스케이드 매트릭스 + 기계적 수정 목록. 코드 인용은 실제 파일에서 확인한 것만.

---

## 0. 목적 · 사용법 — 갭측정 사이클

### 0.1 사이클 (반복)
```
정답지(이 문서)  ──비교──▶  실제 저장소 상태
       ▲                          │
       │                     갭 식별(미충족 [ ] 수집)
   재판정 ◀── 갭 축소(기계적=즉시 / 정책=인터뷰 후) ◀──┘
```
1. **비교**: 각 조건의 검증방법을 실제 실행/관찰해 `[ ]`→`[x]` 또는 미충족으로 표시.
2. **갭 식별**: 미충족 `[ ]`를 모은다. 각 갭은 (조건번호 · 검증실패 증거 · 차단여부)로 기록.
3. **갭 축소**: 인터뷰 불요 = 부록 A의 기계적 수정으로 즉시/병렬 처리. 인터뷰 요 = §9 정책 슬롯을 사람 결정으로 채운 뒤 반영.
4. **재판정**: §10 종합 게이트를 다시 돌린다. 부분 충족이면 **'완성'을 선언하지 않고 '진행 중'으로 정직하게 표시**한다(킷의 거짓-완성 금지 규율을 킷 자신에 적용).

### 0.2 판정 원칙
- **결정적 우선**: 값·구조가 명확한 조건(파일 존재·exit 코드·정규식 매칭·문자열 일치)은 명령 실행으로 PASS/FAIL. 해석이 필요한 조건만 사람 판단(REVIEW)으로 둔다 — 단 REVIEW도 "무엇을 보고 어떻게 판정하는가"를 명시한다.
- **조용히 틀림 0**: 검증방법을 못 돌렸으면 PASS가 아니라 `[확인불가]`다. 그럴듯한 기본값으로 메우지 않는다.
- **출처 가시화**: 각 조건은 어느 감사항목/테마에서 왔는지 괄호로 표기(예: `(감사 #2, 테마: 가드 fail-open)`).

### 0.3 현재 확인된 사실(2026-06-18 기준, 본 감사에서 실측)
- `settings.json:31,42`·`hooks.json:9,15,23,32` 의 훅 명령이 `python3.claude/...`(공백 누락)으로 되어 있어 **실제 실행되지 않을 수 있다** — 읽기전용 가드가 무력. 그런데 `hooks.json:2` 주석은 "연결됨"이라 단언.
- `completion-gate.py:98` 자체의 usage 문자열도 `python3completion-gate.py`로 동일 버그.
- 오케스트레이터(`strategy-plan.md:25,27,32`)는 S4/S5/S7/S8/S9를 "(P2 — 미구축)"로 표기해 파이프라인에서 스킵. CLAUDE.md/blueprint는 "11스킬·P2완료"로 광고 → 기대-실제 불일치 확정.
- `.claude/rules/` 디렉토리가 **존재하지 않는다**(blueprint §1.1이 전제한 4종 standards 부재).
- `completion-gate.py:162` cond4는 `"high" in joined`(행 전체 substring)로 판정 → 오탐 가능. cond6(`:182-183`)은 `sc`+`10-prd-handoff.md`+`REPORT.md` 3파일만 스캔 → 범위 협소.

---

## 1. 정합성 — 미배선 스킬 / 광고-실제 일치 (감사 #1)
> 11스킬 중 4개만 배선, 나머지 5개 스킵, 문서는 "11스킬 작동"으로 광고. S6가 S4/S5 입력 없이 돈다.
> 정책 선결: §9-T1(미배선 스킬 처리) 결정 필요. 권장 = "전부 정식 배선 + 빈틈 선보강", 단 다른 테마(멈춤기준·현업자료·신호정의 등)가 선결 조건.

- [x] **1.1 광고-실제 정합** ✅ 2026-06-18 (G1, T1): orchestrator·CLAUDE.md·README·blueprint를 정직 정정 — 11스킬 전부 배선, 코어는 'MVP 실증', P2 5종은 '초안(배선됨) — 첫 실사용 고도화'(거짓 '작동' 주장 금지). "11스킬 작동/P2완료" 식 과장 제거.
  - 검증 PASS: 네 문서에서 "미구축" 토큰 0(blueprint의 서술 문구 1건 제외) + orchestrator에 11스킬 전부 호출 경로 등재(불일치 0).
- [x] **1.2 스킬 상태 어휘 통일** ✅ 2026-06-18 (G1): blueprint §5·CLAUDE.md·orchestrator·README가 P2 상태를 **"초안(배선됨)"** 동일 문구로 표기.
  - 검증 PASS: 네 문서 모두 "배선됨 + 초안/절차 골격 + 첫 실사용 고도화" 일관.
- [x] **1.3 미배선 스킬 입출력 경로 명시** ✅ 2026-06-18 (G1): S4/S5/S7/S8/S9 각 SKILL.md 산출물 섹션에 **입력 파일·산출 파일·하류 소비처** 한 줄 명시(예: S4 입력=01-problem-set→산출 03-references→하류 S6/보고서).
  - 검증 PASS: 5개 SKILL.md에 입력·산출·하류 파일명 토큰 존재(5/5).
- [x] **1.4 파이프라인 실배선(배선 분기 선택)** ✅ 2026-06-18 (G1, T1): orchestrator 단계표의 "(P2 — 미구축)"를 실제 스킬명(reference-scout·workflow-edge-map·reference-coherence·assumption-manage·mockup-elicit)으로 교체, 산출 파일과 함께 등재. 게이트 명령도 런처 형태로.
  - 검증 PASS: `strategy-plan.md` "미구축" 0건 + 11스킬 전부 단계표 등재(산출파일 동반).
- [N/A] **1.5 (배선 보류 결정 시) 결손 가시화**: T1이 **배선**을 택해 이 분기는 해당없음. 단 결손 가시화 취지는 '초안(배선됨)' 라벨 + 게이트 N/A/REVIEW(빈/얕은 산출 시 '조건부')로 충족.

---

## 2. 안전 — 훅 실제 실행 (감사 #2)
> 훅 명령 `python3.claude/...` 공백 누락으로 읽기전용 가드가 미실행. "연결됨"이라 단언됨.
> 정책: §9-T14(가드 fail-open·종료코드). 권장 = "쓰기 도구 fail-closed + 화이트리스트 + 종료코드 통일".

- [x] **2.1 훅 명령 문법 정정** ✅ 2026-06-18 (A1): settings.json=사용자 직접, hooks.json 미러=킷. 라이브 훅 2종 모두 `python3 .claude/…` 공백 포함.
  - 검증 PASS: 두 파일에서 `python3\.claude` 매칭 **0건**(grep 확인). 가드 스크립트 exit 2 동작도 검증(echo JSON | python3 …). ※ 잔여 `python3.claude`는 도구 9종 usage 주석·ensure-refmap 시드(코스메틱) → Cycle 1b에서 런처 형태로 전환.
- [x] **2.2 PreToolUse 차단 실측** ✅ 2026-06-18 (T18 검증 세션): `finalized/README.md`에 실제 Edit 시도 → `PreToolUse:Edit hook error … exit 2`로 거부 + 파일 무변경 확인(폴백 통과 아님). local-readonly-guard 분기 16케이스(Edit/Write/Bash/PowerShell × finalized/open/신규/읽기)를 stdin JSON으로 전수 통과. notion-zone-guard는 합성 finalized id로 통과/차단 로직 전수 PASS.
  - ⚠ 한계: notion-zone-guard **실제 MCP 쓰기 호출 end-to-end는 미실행**(MCP 인증 상태 불명 + 실 finalized Notion 쓰기는 비가역=ASK 바닥). matcher 연결은 local 가드가 동일 settings.json 블록·동일 `launch.sh`로 발화함이 입증돼 메커니즘상 동일. 또 현재 `finalized/`의 유일 `.refs.md`가 `_` 접두 예시뿐이라 등록 page-id=0건 → Notion 가드는 로직만 살아있고 막을 대상은 아직 없음(설계대로).
- [x] **2.3 "연결됨" 단언과 실제 일치** ✅ 2026-06-18 (T18): 2.2 로컬 가드 end-to-end PASS로 CLAUDE.md/`hooks.json`의 "연결됨/exit 2 강제" 문구가 실측과 일치(로컬 가드 한정). Notion 가드는 2.2 한계대로 '로직 검증·실 MCP 미실측' — "연결됨"은 메커니즘 근거로 유지하되 실 차단은 등록 page-id 생길 때 재실측.
- [x] **2.4 fail-open/fail-closed 정책 명시** ✅ 2026-06-18 (G2): local-readonly-guard의 JSON 파싱 실패·검사 중 내부오류 = **fail-closed(exit 2)** 로 전환(matcher가 쓰기성 도구 전부라 검사 불가 시 보수적 차단). 정상 파싱+패턴 미일치(모호/읽기)는 통과(정상 흐름). `.claude/hooks/README.md`에 "가드 보호 한계" 절 신설(셸 외 인터프리터·자식 page-id 등 미탐지 한계 명시).
  - 검증 PASS: 러너 가드 케이스 — finalized Edit→차단(2)·open Edit→통과(0)·깨진 JSON→fail-closed(2). README 보호 한계 절 존재.
  - ✅ **발견 B (2026-06-18 T18) — 해소**: 두 가드의 `block()` stderr 메시지의 em-dash(`—`)가 strict cp949에서 `UnicodeEncodeError`→`except Exception: return 0`로 **조용히 fail-open**할 수 있던 위험 + Windows 콘솔 모지바케를, `launch.sh` exec 직전 `export PYTHONIOENCODING=utf-8` 1줄로 제거(전 훅·도구 일괄). **사람 승인 2026-06-18 후 적용**(첫 시도는 거버넌스 가드가 자동 차단 → 거버넌스 정상 동작 방증). 검증: 런처 경유 `local-readonly-guard` 차단 메시지가 깨지지 않고 정상 한글 출력 + exit 2 유지, 도구 실행 exit 0 정상.
- [x] **2.5 종료코드 규약 통일** ✅ 2026-06-18 (G2): 0=정상·1=검증FAIL·2=인자오류/조건부/가드차단·3=리소스부재(파일·디렉토리 없음, 미지원형식)로 통일. "리소스 부재"가 도구마다 2·3 혼재하던 것을 **3으로 정렬**(ref-map/notion-refs/prd-handoff/inputs-extract/completion-gate). 9개 도구 전부 **알 수 없는 `--옵션` 거부(exit 2)** 추가(조용한 폴백 금지) + usage 공백 버그(A1 잔여) 정정. 매핑표 = `.claude/hooks/README.md` §3.
  - 검증 PASS: README §3 매핑표(의미 충돌 0) + 러너 29케이스 중 리소스부재(exit3)·미지옵션(exit2) 케이스 전부 통과.

---

## 3. 정책 공백 · 모호 판정기준 (감사 #5)
> 5whys 멈춤기준·현업자료 부재 동결경로·[물어봄] 임계값·adoptability 측정·T1 독립검토·inputs-extract 호출절차 등이 비어 있음. 대부분 §9 인터뷰로 채운다.

- [x] **3.1 탐색 멈춤기준 통일** ✅ 2026-06-18 (G3, T2): actionable-root 휴리스틱(통제 밖/원인 반복/해소 시 재발 안 함 중 먼저)을 5스킬에 명시 — problem-freeze(5whys)·coherence-matrix(재귀 **2차효과 필수**)·workflow-edge-map(as-is)·assumption-manage(가정)·mockup-elicit(**3라운드 초과 ASK**).
  - 검증 PASS: 5개 스킬에 멈춤기준 토큰 존재(5/5) + 재귀 2차효과·목업 3라운드 수치 기준 명시.
- [x] **3.2 현업자료 부재 동결경로** ✅ 2026-06-18 (G3, T3): problem-freeze(S2)·workflow-edge-map(S5)에 자료 부재 시 **잠정 동결 + `[현업검증=확인불가]` + S8 등재 + '조건부' 강제** 경로 추가, adoptability(S10)는 `readiness: 잠정`. completion-gate full 모드는 `[현업검증=확인불가]` 감지 시 cond9(REVIEW)로 **'완성'(exit 0) 차단**.
  - 검증 PASS: 세 스킬에 잠정/확인불가 경로 + 게이트 cond9 코드(full 모드 exit 0 차단) + 러너 회귀 무영향.
- [x] **3.3 미해결 누적 임계값** ✅ 2026-06-18 (G3, T4): guideline §14에 단일 정의(토대 3축 미해결 1건+ → 하류 blocked·'미완'; 비토대 가정 후 진행; 보조: med open ≥5 또는 토대 `[확인불가]` 1+ → '하'). completion-gate cond3(blocking)·cond4(고위험 open) FAIL + 보조 강등 코드(01·02 스캔).
  - 검증 PASS: guideline에 임계 규칙 + 게이트 cond3/4 FAIL + 강등 코드 + 러너 회귀 무영향.
- [x] **3.4 독립검토 트리거 단일정의** ✅ 2026-06-18 (G3, T5): guideline §14에 단일 정의(T2=경계/비가역/blocking/미검증가정 1+ → veto 필수·T1=권장(상한 '중')·T0=불요 + `[독립검토=완료]` 표식). coherence-auditor·prd-compose·reference-coherence가 참조. completion-gate가 표식 읽어 REVIEW→PASS 승격.
  - 검증 PASS: 정의 한 파일 1회 + 3컴포넌트 참조 + 게이트 승격 **실측**(표식 삽입 시 REVIEW 2건 승격→exit 0, 미표식 exit 2 유지).
- [x] **3.5 채택신호 정의** ✅ 2026-06-18 (G3, T11): reference-scout에 엄격 카운팅(제3자 독립 주체만 1, 벤더 자기발표/재인용 합산 1, 단종/베이퍼 제외, 모호 시 강등) + **선례0 → 핵심가정 S8 강제 등재 + 근거충분성 상한 6/10** 명시.
  - 검증 PASS: reference-scout SKILL에 신호 카운팅 규칙 + 선례0 강등(상한 6/10) 명시.
- [x] **3.6 inputs-extract 호출절차 명시** ✅ 2026-06-18 (G3): strategy-intake(S0–S1)에 비텍스트 원본(xlsx/html/csv/tsv) → `inputs-extract` 런처 호출 단계 명시(주체=strategy-intake, 시점=시작 시 입력 읽기). `.refs.md`는 기존 절차, 실패는 `[확인불가]`.
  - 검증 PASS: strategy-intake SKILL에 inputs-extract 호출 단계 존재(.refs + 일반 원본 둘 다).

---

## 4. 도구 견고성 — 회귀 테스트 + 정확도 (감사 #4)
> completion-gate cond4 행전체 substring 오탐·cond6 협소, source-tag-lint 펜스 미인식, vague-term-lint 단어경계 없음, prd-handoff-map 형식만 검사.
> 정책: §9-T15(코드펜스/단어경계). 권장 = "정규식 경계+펜스 토글+스캔범위 확대(보수적)".

- [x] **4.1 회귀 테스트 픽스처 존재** ✅ 2026-06-18 (Cycle 2): 9개 도구 전부 픽스처 + 결정적 러너 `tests/run_tests.py` 신설. 케이스 21건(도구 9종 × PASS/FAIL ≥2, ≥9×2 충족) — vague/srctag(clean 추가)·coh(empty·fail·missing)·gate(cg_fixture·cg_pass)·prd-handoff(pass·섹션누락·필드누락)·refmap(pass·fail)·notion-refs(pass·conflict)·inputs(csv·미지원·refs)·mockup(생성·인자오류).
  - 검증 PASS: `python .claude/tools/tests/run_tests.py` → 21/21 통과(종료코드 0), 각 케이스 기대 exit + 핵심 출력 토큰 대조. 러너는 `sys.executable`로 OS중립.
- [x] **4.2 vague-term-lint 단어경계** ✅ 2026-06-18 (Cycle 2): 영숫자 `\b`·한글 예외 마스킹(유연근무·비실시간)·코드펜스·인라인주석 제외·줄당 전건 보고.
  - 검증 PASS: vague_fixture → 유연근무·비실시간 미검출, '유연한'/'실시간'+'직관적'(줄당 2건)/'100%' 검출, 펜스·재정의마커 제외.
- [x] **4.3 source-tag-lint 정확도** ✅ 2026-06-18 (Cycle 2): 코드펜스(```/~~~) 블록 스킵 + 12자 임계를 명명 상수(`MIN_STATEMENT_LEN`)로. (confidence 태그 누락 경고는 보수적 보류 — T13 default대로.)
  - 검증 PASS: srctag_fixture → 펜스 내부 2줄 미검사, 무태그 진술 1줄만 FAIL, 태그줄·짧은줄 제외.
- [x] **4.4 completion-gate cond4 정확도** ✅ 2026-06-18 (Cycle 2): 리스크/상태 컬럼 헤더명으로 셀을 찾아 토큰집합 매칭(허용어 high/높음/상/critical/치명). 컬럼 식별 실패 시 행 토큰 매칭(여전히 substring 아님).
  - 검증 PASS: cg_fixture → 'high-level'(리스크=low) 미플래그, '고위험 이슈'(리스크=high·open)만 검출.
- [x] **4.5 completion-gate cond6 스캔범위** ✅ 2026-06-18 (Cycle 2): planning-dir 전체 `*.md` glob 스캔(파일명+라인 보고).
  - 검증 PASS: cg_fixture/04-workflow-edge.md의 '최적화' 검출(구 3파일 스캔은 놓쳤음).
- [x] **4.6 prd-handoff-map 실질 검사** ✅ 2026-06-18 (Cycle 2): 헤딩 키워드 존재(형식)만이 아니라, 각 소스 섹션 헤딩이 대응 feature-spec 필드 토큰(`→ fs§N`/`open-questions`)을 실제로 가리키는지 헤딩 단위로 확인. 미달은 '섹션 누락'/'필드 매핑 누락' 둘로 구분 보고하고 누락 필드명(`라벨→fs§N`)을 출력.
  - 검증 PASS: `prd_handoff_missing_field.md`(8개 섹션 헤딩은 있으나 fs 매핑 주석 전부 제거) → FAIL(exit 1) + 누락 필드명 출력. `prd_handoff_pass.md`·실제 `templates/prd-handoff.md` → PASS(exit 0, 회귀 없음). 섹션누락 픽스처 → FAIL. (강화 전엔 필드누락 픽스처가 exit 0으로 통과 = 갭이 러너에 노출됐었음.)
- [x] **4.7 coherence-check 빈 표/blocking/누락 처리** ✅ 2026-06-18 (Cycle 2): 데이터행 0이면 경고 분기('악화0을 검증된 것으로 보지 말 것'), 매트릭스 파일 없을 때 진단 메시지 출력(전엔 빈 출력), blocking은 report에 명시(completion-gate cond3가 FAIL 수신).
  - 검증 PASS: coh_empty → 경고+PASS, cg_fixture(매트릭스 없음) → 진단+exit3.

---

## 5. 산출 템플릿 · 규칙 레이어 (감사 #1/#5/#6 교차)
> 코어 토대 산출(intake·problem-set·success)에 템플릿 부재 → 구조 drift, gate 파싱 실패 위험. rules/ 4종 standards 통째 미존재.

- [x] **5.1 토대 템플릿 신설** ✅ 2026-06-18 (G5): `templates/00-intake.md`(입력유형/tier/참조맵상태)·`problem-set.md`(frozen 헤더+4필드 표)·`success.md`(①②③ 마커) 신설 — completion-gate 파싱 키와 일치.
  - 검증 PASS: 세 템플릿 존재 + **quote-automation 완주 샘플**(이 구조로 채움)이 cond1(frozen)·cond2(①②③) 통과(6.1 실측).
- [x] **5.2 rules/ SSoT 정리** ✅ 2026-06-18 (G5, T9): blueprint §1.1을 정정 — `rules/` **미존재 명시** + guideline 절(§6·§7·§9·§14)을 **잠정 SSoT**로, **모호표현 금지어 SSoT = `vague-term-lint.py` `VAGUE_TERMS`(단일 출처)** 로 표기. `_devkit-alignment`는 devkit 비활성이라 보류(open-question).
  - 검증 PASS: blueprint §1.1에 "rules/ 미생성" 명시 + 금지어 단일 출처(도구 데이터)로 지정, 본문은 예시 괄호만(canonical 목록 중복 0).
- [x] **5.3 채택검증 측정불가 해소** ✅ 2026-06-18 (G5, T10): adoptability SKILL 판정을 **AND 명시**(절차1 n≥5·30초·80% ∧ 절차2 별도행동강요=FAIL ∧ 절차3 롤아웃미정=FAIL) + 목업 전 = **`readiness: 잠정`**(PASS 금지) + 임계값 조정 근거 기록. `templates/readiness.md` 신설.
  - 검증 PASS: SKILL에 AND/FAIL/잠정 명시 + readiness 템플릿 존재 + completion-gate cond5 report 모드 **N/A 실측 확인**(6.1 게이트 출력).
- [x] **5.4 NO-GO·점수·등급 표준화** ✅ 2026-06-18 (G5, T12): prd-handoff 템플릿에 §"판정 루브릭·NO-GO" 신설 — **NO-GO 4조건**(근본원인 미해소·상호배타/blocking 잔존·S10 채택불가·신뢰성 '하') + **1–10 루브릭** + **등급 변환식**(평균 상≥8/중5–7.9/하<5, 한 항목 ≤3이면 '하' 강등) + completion-gate 교차확인. report-compose는 이를 SSoT로 참조 + **보고서 단계 채택항목 가중 0.5/(잠정)**.
  - 검증 PASS: prd 템플릿에 NO-GO·루브릭·변환식 + report-compose에 참조·가중 0.5 명시.

---

## 6. 사용자 관점 — 완주 샘플 · 매핑 · 안내 (감사 #6)
> 끝까지 채운 샘플 없음, 파일번호-단계번호 오프셋(06=S7), 기대-실제 격차, Notion 인증 안내 부재.

- [x] **6.1 완주 샘플 예시 존재** ✅ 2026-06-18 (G6): slug=`quote-automation` 완주 예시. **`docs/examples/quote-automation/`** 에 동봉(작업 디렉토리 `docs/planning/`과 분리 — 사용자 산출물 로컬 전용 정책 반영, 2026-06-18). `context.md`(입력) + `_state.md`·`00-intake`~`07-assumptions`·`REPORT.md`. G1=No 경로.
  - 검증 PASS: `completion-gate docs/examples/quote-automation --mode report` → **exit 2(보고서 생성 가능)**, FAIL 0(REVIEW 2). coherence exit 0(M1). vague 0건. (온보딩 동작확인도 이 경로.)
- [x] **6.2 파일번호↔단계번호 매핑표** ✅ 2026-06-18 (G6, =부록 A3): 오프셋(파일번호=슬롯순번 0부터=단계번호−1, 03=S4·06=S7·07=S8, S9 목업은 번호상 앞·실행은 ASK G2 후) 매핑을 `_state` 템플릿(주석)·README §4·CLAUDE.md 세 곳에 명시.
  - 검증 PASS: 세 파일에 동일 매핑 + 파일명 불변 경고.
- [x] **6.3 Notion 인증 안내** ✅ 2026-06-18 (G6): README §5에 `/mcp` 인증 3단계 + 미인증/권한없음 = `[확인불가]`(조용한 폴백 금지) + finalized 읽기전용 명시. (온보딩 HTML에도 G8에서 동일 반영)
  - 검증 PASS: README에 Notion 인증 단계 + 실패 처리 문구 존재.
- [x] **6.4 미존재 파일 참조 정정** ✅ 2026-06-18 (G6, =부록 A7): `inputs/README.md`의 technical-review-guideline·CLAUDE.fable5-lite 줄을 "*예시이며 현재 저장소엔 없음*"으로 정정, `agents/mockup-elicitor.md`의 `--design-system docs/design-system`을 "(있으면만 — 현재 없음)"으로 표기 + 런처 형태로 정정.
  - 검증 PASS: 두 파일의 죽은 참조가 "예시/있으면" 표기로 정정됨.

---

## 7. 크로스플랫폼 (Windows + macOS 50/50) (감사 #3, 테마: 플랫폼 중립·온보딩)
> 모든 도구·훅이 python3 단일 호출. Windows는 보통 `py`/`python`이라 게이트·가드가 조용히 미실행.

- [x] **7.1 OS중립 런처** ✅ 2026-06-18 (1b): `.claude/hooks/launch.sh` 신설(단일 POSIX — Git for Windows 전제, CC가 Win에서 Git Bash로 훅 실행). `python3→python→py -3` 자동탐지 + `--guard` 모드. 별도 `.cmd` 불필요(Git Bash가 .sh 실행).
  - 검증 PASS: 이 PC(Git Bash)에서 가드 차단(exit2)·통과(exit0)·도구 실행·파이썬부재 fail-closed 전부 실측.
- [x] **7.2 양 OS 동작 확인** ✅ 2026-06-18 (Win+Git Bash): 러너 29케이스 + 런처 경유 completion-gate(exit2)·coherence-check(exit1)·가드 3종 전부 Win+Git Bash 실측 통과. 코드가 OS중립(`sys.executable`·`os.path.join`·POSIX `launch.sh`)이라 macOS도 동일 동작 기대 — 단 macOS 물리 실측은 미수행(장비 부재). 기준의 "(또는 Win + Git Bash)" 충족.
  - 검증 PASS: `python .claude/tools/tests/run_tests.py` 29/29 + 런처 종료코드 일치.
- [x] **7.3 경로 분리자 처리** ✅ 2026-06-18: 경로 결합은 전부 `os.path.join`, 가드의 경로 매칭은 `replace("\\","/")` 정규화 + `[\\/]` 정규식(양 분리자 처리). 하드코딩 경로 분리자 0건.
  - 검증 PASS: 도구·가드 grep → 매치는 모두 `\n`(개행)·정규식·표시문자열, 경로 결합용 하드코딩 분리자 0건.
- [x] **7.4 인터프리터 부재 = 실패 보고** ✅ 2026-06-18 (1b): launch.sh가 python 미발견 시 가드=exit2(fail-closed)·도구=exit127 + stderr 안내(조용한 폴백 금지).
  - 검증 PASS: `env -i PATH=빈디렉토리`로 python 제거 모의 → 가드 exit2·도구 exit127 실측.
- [x] **7.5 호출 문자열 정정** ✅ 2026-06-18 (G7): 9개 도구의 헤더·런타임 usage를 OS중립 **런처 형태(`sh .claude/hooks/launch.sh .claude/tools/<tool>.py …`)로 통일**(Windows에서 `python3` 직접 호출 실패 방지). `python3<name>` 공백누락 print 버그 전부 청산.
  - 검증 PASS: 코드(.py/.json/.sh)에서 `python3<공백없이name>` 0건(docs §0.3 매치는 과거 버그 *기록* 프로즈) + 러너 29/29(usage 변경 후에도 무결).

---

## 8. 온보딩 HTML — 비개발자 진입 (감사 #3, 테마: 플랫폼 중립·온보딩)
> 비개발자용 사전 인프라(VSCode/Cursor·Claude Code·필요시 npm·Python·Notion MCP·Playwright) 통합 온보딩 부재. 의사결정/안내=HTML 규칙.

- [x] **8.1 온보딩 HTML 존재** ✅ 2026-06-18 (G8): `planning-kit-온보딩.html(루트)` 신설 — Windows/macOS **탭 분리**(JS 토글) + 양 OS 섹션.
  - 검증 PASS: 파일 존재 + win·mac 패널 둘 다.
- [x] **8.2 설치 스텝 완비** ✅ 2026-06-18 (G8): 양 OS 6스텝(에디터→Claude Code→sh(Git Bash/내장)→Python→(선택)Node+Playwright→(선택)Notion `/mcp`) + "한눈에" 표.
  - 검증 PASS: 6개 항목이 양 OS 섹션·표에 등장.
- [x] **8.3 동작확인 1줄 테스트** ✅ 2026-06-18 (G8): 각 OS에 런처로 완주 샘플(`quote-automation`)에 completion-gate `--mode report` 돌리는 복붙 명령 + 예상 출력 명시.
  - 검증 PASS: 안내 명령 **실제 실행** → `판정: 보고서 생성 가능` + **종료코드 2** 일치(HTML 예고와 동일).
- [x] **8.4 인증 실패 처리 명시** ✅ 2026-06-18 (G8): Notion 인증 실패/권한없음 = 조용한 폴백 금지 → `[확인불가]` 표시 + finalized 읽기전용을 온보딩에 명시.
  - 검증 PASS: HTML에 인증 실패 처리 문구(`[확인불가]`) 존재.

---

## 9. 정책 결정 슬롯 (✅ 확정 — 2026-06-18 인터뷰 종결)
> 각 슬롯은 §0 인터뷰 테마와 1:1. "반영지점"은 그 결정이 들어갈 파일/도구.
>
> **🔒 결정 종결 기록.** T1~T14 **14개 전부 추천안(default)으로 확정**. 결정자=사용자(biocomexecutive), 날짜=2026-06-18, 근거=전수 정책공백 스윕(run wf_9c37d54d-fd4, 후보 183건)+선행 감사. 추가 결정: `_devkit-alignment.md` 작성은 **보류**(devkit 비활성이라 비긴급) → open-question. 아래 "확정값" 열 = 잠긴 정책. 변경 시 변경요청 프로토콜(ASK→재기록).

| # | 테마 | 결정해야 할 것 | ✅ 확정값(2026-06-18) | 반영지점 | 캐스케이드 |
|---|---|---|---|---|---|
| T1 | 미배선 스킬 처리 | 5스킬 정식배선 / tier 조건부 / 광고 정직 하향 | 배선하되 배선 전 결손 명시 + 광고 "4개 배선"으로 정정 | orchestrator 단계표·CLAUDE.md·blueprint§5·README·5 SKILL 입출력 | 1,5,6,4 |
| T2 | 근본원인·탐색 멈춤기준 | actionable-root / 고정N단계 / LLM자율 | actionable-root 휴리스틱 + 분기 시 영향 큰 가지 우선 | problem-freeze·coherence-matrix·workflow-edge-map·assumption-manage·mockup-elicit SKILL | 5,1,6,4 |
| T3 | 현업자료 부재 동결경로 | 잠정동결+플래그 / 하드게이트 / AI추론동결 | 잠정 동결 + `[현업검증=확인불가]` + 조건부 강제 | problem-freeze·workflow-edge-map·adoptability-check·completion-gate | 5,1,6 |
| T4 | 미해결 누적 임계값 | 심각도(토대1+) / 절대개수 / 전부조건부 | 토대 3축 1건+ = 하류 blocked·미완 + 보조 강등룰 | CLAUDE.planning-lite·completion-gate cond3/4·coherence-check | 5,1,6,4 |
| T5 | 독립검토 트리거 T1/T2 | tier단일정의+4축 / 전PRD의무 / 신호집계 | T2=경계/비가역/blocking/미검증가정 1+, veto 필수 | guideline(또는 rules) 단일정의·coherence-auditor·prd-compose·completion-gate | 5,1,4,6 |
| T6 | 비대화형 원샷 기본분기 | 보수적정지(G1/G2 No) / G1 Yes / 시작거부 | 원샷=G1 No(보고서종료)·G2 No(Figma), 미수신 `[물어봄]` | orchestrator §2·report-compose·prd-compose | 1,5,6 |
| T7 | 플랫폼 중립·온보딩 | 런처래퍼+온보딩HTML / 한줄폴백 / Python비의존 | OS중립 런처 + 비개발자 온보딩 HTML (§7·§8) | 루트 plan-gate.cmd/.sh·전 도구 호출·planning-kit-온보딩.html(루트) | 3,2,1,6 |
| T8 | 산출 템플릿 신설 | 전용템플릿3 / 인라인 / 자유형식 | intake·problem-set·success 템플릿 신설(파싱키 일치) | templates/·completion-gate 파싱키 | 6,4,1 |
| T9 | 규칙 레이어 SSoT | guideline격상+도구데이터 / rules4종작성 / 현상유지 | guideline 절 잠정SSoT + 금지어=도구데이터, blueprint 정정 | blueprint§1.1·guideline절·vague-term-lint 데이터 | 5,1,6,4 |
| T10 | 채택검증 측정불가 | 정성체크리스트+조정 / 전부N/A / 외부설정화 | 정성 라벨 분리 + readiness:PASS는 실측만 + 임계조정 근거기록 | adoptability-check·templates(readiness)·completion-gate cond5 | 5,6,1 |
| T11 | 실사용 채택신호 정의 | 엄격(제3자) / 느슨(벤더포함) / 가중표 | 엄격: 제3자 독립 주체만 1신호, 벤더 합산1, 선례0=가정강제등재 | reference-scout SKILL/agent·guideline §7 | 5,1,4 |
| T12 | NO-GO·점수·등급 | NO-GO명시+평균강등 / 상중하만 / 자유점수 | NO-GO 4조건 + 1-10 루브릭 + 평균+≤3강등 + gate 교차확인 | prd 템플릿·report-compose·prd-compose·completion-gate | 5,6,4 |
| T13 | 코드펜스/단어경계 도구 | 정규식경계+펜스+범위확대 / 화이트리스트 / 현행유지 | 정규식 경계 + 펜스 토글 스킵 + cond4 헤더명·cond6 전체스캔 | vague/source-tag-lint·completion-gate cond4/6 | 4,6,5 |
| T14 | 가드 fail-open·종료코드 | 쓰기fail-closed+화이트리스트+코드통일 / 전면open / 전면closed | 쓰기 의심 파싱실패=exit2, 동사 단어경계, 자식prefix 차단, 코드 0/1/2/3 통일 | local-readonly-guard·notion-zone-guard·notion-refs-lint·전 도구 | 2,4,6,1 |

> **반영 규약**: 각 결정 종결 시 open-questions 원장(`_state.md` 결정 슬롯)에 결정자·날짜·근거·반영지점 4필드를 기록한다(미기록 시 completion-gate cond7 FAIL). finalized 영역에 닿는 결정은 ASK 바닥(비가역) — 적용 전 사람 확인.

---

## 10. 종합 게이트 — '킷 구축 완성' 판정
> 킷의 종료 8조건 사상을 킷 구축에 매핑한 게이트. **아래가 모두 충족돼야 '구축 완성'.** 하나라도 미충족이면 '진행 중'으로 정직하게 표시(부분 충족을 완성으로 단언 금지).

| 게이트 조건 | 매핑 출처 | PASS 기준(검증방법) | 비고 |
|---|---|---|---|
| G1 정합성 | §1 | 1.1~1.3 전부 `[x]`(+배선/보류 분기 중 택1 충족) | ✅ **충족**(2026-06-18) — 1.1~1.3 `[x]` + 1.4 배선 분기 충족(11스킬 배선, 미구축 0). 광고-실제 불일치 0 |
| G2 안전 | §2 | 2.1~2.5 전부 `[x]` + 2.2 차단 실측 PASS | ✅ **충족**(2026-06-18) — 2.1~2.5 전부 `[x]`. 로컬 가드 end-to-end 실측 + fail-closed·종료코드 규약·README 보호한계. (notion 가드 실 MCP end-to-end는 등록 id 생길 때 재실측) |
| G3 정책 공백 | §3 | 3.1~3.6 전부 `[x]`(§9 T1~T14 해당 결정 종결) | ✅ **충족**(2026-06-18) — T2~T11 정책 스킬·guideline·게이트 반영(멈춤기준·잠정동결·임계·독립검토·채택신호·extract) |
| G4 도구 견고성 | §4 | 4.1 픽스처 ≥9×2 + 4.2~4.7 PASS | ✅ **충족**(2026-06-18 Cycle 2) — `tests/run_tests.py` 21/21, 도구 9종 회귀 |
| G5 템플릿·규칙·등급 | §5 | 5.1~5.4 전부 `[x]` | ✅ **충족**(2026-06-18) — 토대 템플릿 3종·readiness 템플릿·rules SSoT 정정·NO-GO 루브릭 |
| G6 사용자 관점 | §6 | 6.1~6.4 전부 `[x]` | ✅ **충족**(2026-06-18) — quote-automation 완주 샘플(report gate exit2)·매핑표 3파일·Notion 인증 안내·죽은참조 정정 |
| G7 크로스플랫폼 | §7 | 7.1~7.5 전부 `[x]` + 양 OS 종료코드 일치 | ✅ **충족**(2026-06-18) — 7.1~7.5 `[x]`, 런처·종료코드·경로분리자 Win+Git Bash 실측. (macOS 물리 실측만 미수행, 코드 OS중립) |
| G8 온보딩 | §8 | 8.1~8.4 전부 `[x]` + 동작확인 명령 실측 PASS | ✅ **충족**(2026-06-18) — planning-kit-온보딩.html(루트·OS탭·6스텝·동작확인 exit2 실측·Notion 실패=[확인불가]) |

**판정 규칙(킷의 completion-gate 사상 차용)**:
- 8개 게이트 전부 PASS → **'킷 구축 완성'**.
- FAIL(미충족 `[ ]`) 1건+ → **'미완(진행 중)'** — 완성 선언 불가, 미충족 목록을 갭으로 명시.
- 결정 미종결(§9 슬롯 공란) = REVIEW → **'조건부'** — 사람 결정 후 재판정.
- **거짓 완성 금지**: G2(훅 실측)·G7(양 OS 실행)을 실측하지 않은 채 PASS로 표기하는 것은 "조용히 틀림"이다.

### 종합 판정 (2026-06-18)
**G1~G8 8개 게이트 전부 충족(`[x]`) → DoD 기준 '킷 구축 완성' 조건 충족.** 결정적 회귀(`run_tests.py` 29/29)·완주 샘플(report gate exit 2)·가드 실측으로 근거 확보.

> **정직 단서(거짓 완성 금지 — 완성 ≠ 무결)**: 아래는 게이트 기준은 통과했으나 실사용 전 한계로 남는다.
> 1. **G2**: notion-zone-guard는 *로직 실측*만(등록 finalized page-id 0건이라 실 MCP 쓰기 end-to-end는 미실행). 실 링크 등록 시 재실측 필요.
> 2. **G7**: macOS는 *코드 OS중립*(검증)이나 물리 실측은 Windows+Git Bash만(장비 부재).
> 3. **P2 5스킬**(reference-scout·workflow-edge-map·reference-coherence·assumption-manage·mockup-elicit): 배선·절차 골격은 완비됐으나 **MVP 실사용 검증 전** — 첫 실제 기획에서 빈틈 발견·고도화 예정.
> 4. **부록 A**: A1(부분)·A3(=6.2)·A7(=6.4)만 처리. A2·A4~A6·A8~A11은 잔여(품질 보강, 게이트 차단 아님).
> 5. completion-gate 신규 분기(cond9·강등·독립검토 승격)는 인라인+러너로 검증했으나, 다양한 실 기획 데이터로의 노출은 적다.

## 부록 A. 기계적 수정 체크리스트 (인터뷰 불요 · 즉시/병렬)
> 정책 결정과 무관하게 바로 처리 가능. **적용은 거버넌스상 사람 승인 대상**이나, 진단/제안은 즉시.

- [ ] **A1 python3 공백누락 버그 일괄 수정 (최우선 — 안전·실행 무력화 원인)**: `python3.claude/...`→`python3 .claude/...`. 대상: 전 도구 usage·print(coherence-check `:11,202`·completion-gate `:10,98`·vague-term-lint `:8,66`·source-tag-lint `:9,63`·prd-handoff-map `:5,42`·mockup-gen `:7,83`·ref-map-lint `:8,45`·inputs-extract `:6,140`·notion-refs-lint `:10,92`) + 훅 `settings.json:31,42`·`hooks.json:9,15,23,32` + `ensure-refmap.py:27` 시드. 수정 후 finalized 쓰기 시도로 exit 2 실측(→ §2.2).
  - 검증: `python3\.claude` 정규식 전 저장소 0건 + 2.2 차단 실측.
- [ ] **A2 확신도 어휘 '확실'로 통일**: reference-scout SKILL `:16,22`·agent·source-tag-lint `:22` TAG_RE vs guideline §7 `:160`·§14 `:324`('사실')을 산출물·도구 인식 어휘 '확실/추정/확인불가'로 통일. guideline의 '사실'→'확실' 정렬은 거버넌스 변경 제안으로 별도.
  - 검증: 산출 줄·도구 정규식이 동일 어휘집합.
- [ ] **A3 파일번호↔단계번호 매핑표 1회 문서화**: _state 템플릿·README·CLAUDE.md에 매핑 주석+대조표(03=S4·06=S7·07=S8, S9 위치 주의). 파일명 자체 변경은 도구 하드코딩 경로(completion-gate `07-assumptions.md` 등) 깨짐 위험이라 지양.
  - 검증: 세 파일에 동일 매핑표.
- [ ] **A4 devkit 데드 참조 주석 정리**: guideline §5 `:114`의 devkit core problem-solving 인용을 "(동일 철학, 참조·미설치)"로 명확화 — devkit 없이 실행 가능 명시.
- [ ] **A5 assumption-manage 위임대상 SSoT 정합**: SKILL `:16` vs guideline §11 `:261-262`를 비-devkit `deep-research`로 통일. §11 수정은 open-questions 등재(사람 승인 대기).
- [ ] **A6 blueprint 문서-실제 불일치 정정**: §1.2를 실제 11스킬로(S3→problem-freeze 흡수·S12→prd-compose 흡수·report-compose 추가) `:40,49`, §6.1 경로 `c:\WORKPLACE\Planning`→`Planning-kit` `:136`, §1.4 readiness 표기 `:63`, P2 어휘 `:123`를 세 문서 동일 문구로.
- [ ] **A7 미존재 파일 참조 정정**: `inputs/README.md:20-21` 없는 파일 줄 삭제/표기, `agents/mockup-elicitor.md:11` design-system 예시 "(있으면)" 표기.
- [ ] **A8 코드/도구 측 기계적 보강**: coherence-check `:103-119`(빈 표 경고 분기)·`:173-196`(blocking 항상 명시), completion-gate `:148-201`(컬럼 헤더명 매핑·위치 비의존), vague-term-lint `:47-50`(break 제거·줄당 전건 보고), source-tag-lint(코드펜스 토글 스킵).
- [ ] **A9 inputs-extract/notion-refs-lint 공유 정규식·인코딩**: Notion 호스트 목록 한 곳 정의·두 도구 공유, html/csv open `errors='replace'`, xlsx max-rows 초과 `[TRUNCATED]` 마커, page-id 추출 전 쿼리·앵커 제거(`inputs-extract.py:81-82,88,116`·`notion-refs-lint.py:23,24`).
- [ ] **A10 템플릿 결정적 후속 처리 명시**: `reference-context-map.md:39-41`(URL없는 줄 WARN 건수+확인불가), `cross-domain-analysis.md:29-33`(확정×확정 충돌=ASK 바닥·심각도 높음), `_state.md:40-49`(8조건 각 판정 소스 파일 한 줄씩).
- [ ] **A11 DRAFT 훅 동작 보완**: completion-gate-reminder `:24-27`(rc==1=미통과·0=통과·그외=실행실패 별도 리마인더), ensure-refmap `:54-59`(생성 실패 시 다음 진입 1회 확인), suggest-activation `:22`(임계·신호어 settings 노출, DRAFT 유지).

> **부록 A 완료 정의**: A1~A11 전부 `[x]` + A1·A8·A9의 코드 변경은 §4.1 회귀 픽스처로 PASS 재확인. A1은 §2(안전)·§7(플랫폼)의 선결조건이므로 가장 먼저 처리한다.


---

## 11. 교차 정책 SSoT - 전수 스윕 '누락 보완' (단일 출처가 빠진 6건)

> 스윕이 개별 항목은 다 잡았으나, 컴포넌트마다 산발돼 *단일 SSoT*가 없는 교차 정책 6건. 이게 비면 재개·원샷·동결변경에서 '조용한 스톨/무게이트 통과'가 난다. 대부분 정책결정보다 *통합 문서화*가 필요 - 권장 처리와 함께 둔다.

- [ ] **11.1 게이트 비정상종료 = 완성 차단 (안전 critical · 권장 default)**: 게이트 도구가 인터프리터 부재·예외·timeout으로 비정상 종료하면 오케스트레이터는 **'완성' 선언을 차단하고 "게이트 미실행=실패"로 보고**한다(조용한 폴백 금지). `strategy-plan §3`에 통합 규칙으로 명시.
  - 검증: 인터프리터 제거 모의 -> 오케스트레이터가 완성 선언 안 함 + 실패 보고. (※ A1 python3 버그와 결합 시 '무게이트 통과'의 직접 원인 - §2·§7의 선결.)
- [ ] **11.2 통합 원샷 종결 게이트 SSoT**: "어느 tier에서 어디까지 자동 진행하고 무엇을 [물어봄]으로 정지하나"의 단일 정책(테마 T6 결정을 오케스트레이터 한 곳에 SSoT로). 컴포넌트는 이를 참조.
  - 검증: orchestrator에 원샷 종결 정책 1곳 + 스킬들이 자체 규정 대신 참조.
- [ ] **11.3 변경요청 프로토콜 하류 재실행 배선**: 동결 변경 감지 시 영향 하류(S3·S5·S6·S7·S8·S9 중 작성분)를 **stale로 일괄 표시**하고 오케스트레이터가 포인터를 되돌려 재실행하는 단일 트리거. (현재 컴포넌트별 범위 불일치: problem-freeze=S3·S6만, guideline §5=S9까지.)
  - 검증: orchestrator에 변경요청 발동·stale 전파·포인터 되돌림 배선 존재 + 하류 범위가 한 곳에 정의.
- [ ] **11.4 tier->단계동작 단일 분기표**: tier(T0/T1/T2)가 인터뷰 강도·S4 실행여부·게이트 엄격도·동결 사람승인까지 *전 파이프라인을 어떻게 가르는가*의 매핑표 1개를 SSoT로(현재 freeze·coh·refcoh·tools·templates·agents에 흩어짐). `_state`의 tier 필드가 죽은 필드가 안 되게.
  - 검증: 'tier->각 단계 동작' 표 1곳 존재 + 스킬들이 참조.
- [ ] **11.5 참조맵 신선도 운영 SSoT**: volatility(변화 잦은 영역) 판정 주체·시점(도메인 등록 시 사람이 필드 부여) + 6개월 경과 항목 confidence '확인불가' 강등 + 강등 후 권고를 검증필요가정으로 이동하는 후속조치를 한 곳에 규정.
  - 검증: 신선도 운영 규칙 1곳 + reference-context-map 템플릿에 volatility 필드.
- [ ] **11.6 부분완성 상태 어휘 통일**: `_state`에 `skipped`(미배선 단계)·`blocked`(토대 미해결)·`provisional`(잠정 동결) 상태 어휘를 추가하고 **completion-gate 파서·재개 로직·신뢰성 등급이 동일하게 인식**. (현재 templates에만 단편적 -> 전 컴포넌트 계약으로 승격.)
  - 검증: _state 템플릿에 상태 어휘 정의 + completion-gate가 해당 상태를 등급/판정에 반영 + 재개 로직이 skipped/blocked를 구분.

> §11 처리 메모: 11.1은 안전 critical이라 A1(python3 수정)과 함께 1순위. 11.2는 T6 결정에 종속, 11.4는 T5 결정과 연동. 11.3·11.5·11.6은 통합 문서화(정책결정 경량) - 갭축소 사이클 후반에 배치.
