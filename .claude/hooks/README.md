# .claude/hooks/ — 읽기전용 가드(연결됨) + 활성화/종료 훅(DRAFT)

**읽기전용 가드 2종은 `settings.json`의 PreToolUse에 *연결돼 작동 중*입니다**(2026-06-17, 사용자 승인):
- `local-readonly-guard.py` — `reference-context-map/finalized/`의 *기존* 파일 수정(Edit/Write 덮어쓰기/Bash 쓰기)을 **exit 2로 차단**. 신규 추가·열린/inputs 수정·읽기는 통과. **파싱/처리 실패 = fail-closed(exit 2)**(T14, 2026-06-18 — matcher가 쓰기성 도구 전부라 검사 불가 시 보수적 차단).
- `notion-zone-guard.py` — Notion *쓰기* 도구가 finalized 링크(`*.refs.md`)의 page-id를 타깃하면 **exit 2로 차단**(읽기 통과). finalized id는 매번 폴더 직접 스캔(stale 0).
- 근거: PreToolUse JSON `deny`는 MCP 도구에 안 먹는 버그(#33106) → **exit 2** 사용. stdin은 UTF-8 명시 디코드(한글 경로 안전).

아래 두 훅은 **여전히 초안·미연결**입니다(런타임 행동 변경이라 의도적으로 opt-in).

## 구성
- `suggest-activation.py` — UserPromptSubmit 용. 강한 전략/전사/혁신 신호 2개+ 감지 시 `/strategy-plan` 사용을 *제안만*(거부 가능).
- `completion-gate-reminder.py` — Stop 용. 진행 중 도메인이 보고서 게이트 미통과면 *비차단 리마인더*(섣부른 '완성/확정' 선언 방지).
- `hooks.json` — 위 둘의 연결 정의(스테이징). 아직 실제 설정이 아님.

## 활성화 방법 (검증 후, 원할 때)
`update-config` 스킬로 `.claude/settings.json`의 `hooks` 키에 `hooks.json` 내용을 병합하세요. 예:
```json
{ "hooks": {
    "UserPromptSubmit": [{ "matcher": "", "hooks": [{ "type": "command", "command": "python3 .claude/hooks/suggest-activation.py" }] }],
    "Stop":            [{ "matcher": "", "hooks": [{ "type": "command", "command": "python3 .claude/hooks/completion-gate-reminder.py" }] }]
} }
```
권장: 먼저 `suggest-activation`만 켜서 노이즈를 보고, 괜찮으면 `Stop` 리마인더를 추가합니다. 하드 차단(완성 선언 막기)은 충분히 검증한 뒤에만.

---

## 가드 보호 한계 (DoD §2.4 — "절대보호 아님, 1차 방어선")

### local-readonly-guard
- **막는다**: finalized/ 의 ① 기존 파일 `Edit/MultiEdit/NotebookEdit` ② 기존 파일 `Write` 덮어쓰기 ③ `Bash`/`PowerShell`의 finalized 리다이렉트(`>`/`>>`)·파괴 동사(`rm`/`mv`/`tee`/`Set-Content`/`Out-File` 등).
- **허용한다(의도)**: finalized/ 에 *신규* 파일 추가, 모든 읽기, finalized 밖 경로.
- **fail 정책(T14)**: 입력(JSON) 파싱 실패·검사 중 내부 오류 = **fail-closed(exit 2)**. 정상 파싱 + finalized 패턴 미일치(모호/읽기성) = 통과(fail-open, 정상 흐름).
- **놓칠 수 있다(한계)**: 셸 명령 탐지는 정규식 기반 → 변수우회·인코딩·심볼릭링크·간접경로로 난독화된 쓰기, **셸 외 인터프리터**(`python -c "open(...,'w')"`) 경유 쓰기는 미탐지. 우회 가능한 1차 방어선이며, finalized 불변의 최종 책임은 사람 + 변경요청 프로토콜에 있다.

### notion-zone-guard
- **막는다**: 도구명 `mcp__…notion…__` + 쓰기 동사(update/create/append/delete/…) 이고 입력에 finalized `.refs.md` page-id가 있으면 차단.
- **놓칠 수 있다(한계)**: ① **page 단위**(블록 단위 아님) ② Notion **자식 페이지는 별도 page-id** → 부모만 등록되면 자식 쓰기 미탐지(구조적 한계) ③ 도구명 휴리스틱(실제 도구명은 인증 후 확정).
- **등록원**: `finalized/*.refs.md` 매번 직접 스캔(매니페스트 stale 0). `_`/`.` 접두 파일(예시·안내)은 제외 → 실제 등록 id가 0건이면 로직은 살아 있어도 막을 대상이 없다(설계대로).

## 종료코드 규약 (DoD §2.5 — 결정적 도구 9종 + 가드 + 런처, 의미 충돌 0)

| 코드 | 의미 | 호출자(오케스트레이터) 해석 |
|---|---|---|
| **0** | 정상 / 통과 / '완성' 선언 가능 | 진행 가능 |
| **1** | 검증 **FAIL**(판정은 났고 미충족) | 내용 결함 — 기획 보강 필요 |
| **2** | 인자/사용 오류 · 게이트 **조건부**(독립검토 대기) · **가드 차단**(PreToolUse deny) | "깨끗한 통과 아님" |
| **3** | 입력 **리소스 부재/미지원**(파일·디렉토리 없음, 미지원 형식) | 게이트 미실행 — 입력 고쳐 재실행 |
| **127** | 인프라 실패(파이썬 미발견, 런처 도구 모드) | 게이트 미실행=실패, 완성 차단(§11.1) |

| 컴포넌트 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| coherence-check | 통과 | 미해결 악화/구조결함 | 인자없음 | 매트릭스 파일 없음 |
| completion-gate | 완성가능 | 미완(FAIL) | 조건부·인자없음 | _state.md 없음 |
| vague-term-lint | 위반없음 | 위반 | 인자없음 | — |
| source-tag-lint | 통과 | 태그 누락 | 인자없음 | — |
| prd-handoff-map | 통과 | 섹션/필드 누락 | 인자없음 | 파일 없음 |
| ref-map-lint | 정합 | 불일치 | 인자없음 | 디렉토리 없음 |
| notion-refs-lint | 정합 | 위반(헤더/경로/충돌) | 인자없음 | 디렉토리 없음 |
| inputs-extract | 추출 | — | 인자없음 | 파일없음·미지원형식 |
| mockup-gen | 생성 | — | 인자오류 | — |
| local-readonly-guard | 통과 | — | 차단(파싱실패 fail-closed 포함) | — |
| notion-zone-guard | 통과 | — | 차단 | — |

**충돌 0 근거**: 같은 코드 = 한 의미 계열(0 정상 / 1 검증FAIL / 2 호출문제·조건부·차단 / 3 리소스부재). "리소스 부재"가 과거 도구마다 2·3으로 흩어졌으나 **3으로 통일**(2026-06-18). 가드의 2는 PreToolUse 'deny'(exit 2) 규약이라 도구의 2와 맥락이 달라도 호출자에겐 모두 "0 아님=깨끗한 통과 아님"으로 안전하게 수렴.

> 회귀: `python .claude/tools/tests/run_tests.py` 가 위 종료코드를 도구별 PASS/FAIL/리소스부재 + 가드 차단/통과/fail-closed 케이스로 검증.
