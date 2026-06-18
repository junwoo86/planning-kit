<!-- planning-state | slug: <SLUG> | updated: <YYYY-MM-DD> -->
<!--
  _state.md = 재개 앵커(필수). 세션 시작 시 이 파일을 *먼저* 읽고 "현재 포인터 → 다음 액션"부터 이어간다.
  포맷은 도구(completion-gate.py)가 결정적으로 파싱한다 — 표 구조·컬럼명·상태 어휘를 임의로 바꾸지 말 것.
  상태 어휘: pending · in-progress · done · frozen(S2 문제집합·동결된 산출 전용).
-->

# 진행 상태 — <SLUG>

## 단계 상태
<!-- 상태 = pending|in-progress|done|frozen. 산출물 = 약속된 파일명(없으면 "(인라인)"). -->
| 단계 | 이름 | 상태 | 산출물 |
|---|---|---|---|
| S0 | 세션 시작(입력유형·tier·참조맵) | pending | (인라인) |
| S1 | 적응형 인테이크 | pending | 00-intake.md |
| S2 | 문제 정의 & 동결 | pending | 01-problem-set.md |
| S3 | 성공기준(계층형 3층) | pending | 02-success.md |
| S4 | 레퍼런스 인지 주입 | pending | 03-references.md |
| S5 | 워크플로/엣지 | pending | 04-workflow-edge.md |
| S6 | 해법 설계 + 정합성 매트릭스 | pending | 05-coherence-matrix.md |
| S7 | 참조 정합·교차 도메인 | pending | 06-cross-domain.md + 참조맵 |
| S8 | 가정·가설 관리 | pending | 07-assumptions.md |
| (보고서) | S8 검토 보고서 + ASK G1 | pending | REPORT.md |
| S9 | 목업 UI/UX 루프(opt-in, ASK G2) | pending | 08-mockups/ |
| S10 | 채택(readiness) 선검증 | pending | 09-readiness.md |
| S11 | PRD 산출 + 무결성 게이트 | pending | 10-prd.html · 10-prd-handoff.md |
| S12 | 개발 핸드오프 | pending | 11-handoff.md |

<!-- 파일번호↔단계번호 매핑(헷갈림 주의): 파일 번호 = 산출 *슬롯 순번*(0부터)이라 대체로 **파일번호 = 단계번호 − 1**
     (S1→00 … S8→07 … S12→11). 예외 인지: 03=S4·06=S7·07=S8. S9(목업)는 번호상 08이지만 *실행*은 ASK G2 "Yes" 때만(PRD보다 앞 번호여도 나중 실행).
     파일명은 completion-gate 등 도구가 하드코딩 참조하므로 **임의 변경 금지**. 동일 표 = 루트 README·CLAUDE.md. -->

## 현재 포인터
- 현재 단계: S0
- 다음 액션: <한 줄로 — 돌아온 사람이 바로 무엇을 할지>
- tier: <T0|T1|T2 (S0에서 확정)>
- 입력유형: <a 녹취 | b 문제+방향 | c 제로베이스 | d 기존문서 | 혼합>
- 참조맵 상태: <최신 | 낡음 | 비어있음>

## Open-Questions & 결정 원장
<!-- 단일 원장(흩어진 메모 금지). completion-gate.py가 이 두 표를 결정적으로 검사한다. -->

### 미해결 (open-questions)
<!-- 리스크 = high|med|low. 상태 = open|resolved. 고위험(high)이 open이면 종료 게이트 cond4 FAIL. -->
| id | 항목 | 리스크 | 상태 | 비고 |
|---|---|---|---|---|
| Q1 | <예: 재무 단가 SSoT와 충돌 가능성> | high | open | <검증 방법/링크> |

### 결정 (decisions)
<!-- 결정 종결 = 결정자·날짜·근거·반영지점 모두 기록. 빈 칸 있으면 종료 게이트 cond7(미기록 결정) FAIL. -->
| id | 결정 | 결정자 | 날짜 | 근거 | 반영지점 |
|---|---|---|---|---|---|
| D1 | <무엇을 결정> | <누가> | <YYYY-MM-DD> | <왜> | <파일#앵커> |

## 변경 이력(provenance)
<!-- 동결 이후 문제집합/성공기준이 바뀌면 변경요청 프로토콜(guideline §5) 기록을 여기 남긴다. -->
- <YYYY-MM-DD> 최초 생성.
