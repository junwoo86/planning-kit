<!-- stage: S8 | status: done | updated: 2026-06-18 -->
# 가정·가설 관리 — quote-automation

> desirability·feasibility·viability × Known/Unknown × Important. Unknown+Important = 검증 필요 가정.

## 검증 필요 가정 (Unknown + Important)
| id | 가정 | 축 | 검증방법 | 상태 |
|---|---|---|---|---|
| A1 | 영업이 규칙 엔진 결과를 신뢰하고 수기 재작성을 멈춘다 | desirability | 파일럿 8주 사용률·재작성 횟수 | open [물어봄] |
| A2 | 현행 할인 한도표가 실제 승인 기준과 일치한다 | feasibility | 최근 6개월 승인 견적 표본 대조 | open [물어봄] |
| A3 | 협상 예외 비율이 규칙화로 흡수 가능한 수준이다 | viability | 예외 사유 로그 4주 분석 | open [물어봄] |

## Known (베팅 가능)
- ERP 단가 마스터 읽기 연동은 기술적으로 가능(IT 확인). [현업검증] [확실]

## 큰 베팅 경고
- A1이 깨지면(영업이 도구를 우회) 전체 채택이 무너진다 → 파일럿에서 가장 먼저 검증. [근본원인추론]
