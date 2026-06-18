<!-- reference-context-map index | updated: <YYYY-MM-DD> -->
<!--
  참조 컨텍스트 맵의 *폼(format)* 템플릿. 모델 본문(역할·등재 경로·신선도 규칙)은 guideline §10이 SSoT — 여기 재서술하지 않는다.
  위치: docs/reference-context-map/ (index.md · finalized/<d>.md · open/<d>.md · cross-domain-analysis.md). 폴더 자동 보장 = ensure-refmap 훅.
-->

# 참조 컨텍스트 맵 (index)

도메인 PRD 모음집. **모델·역할·등재 규칙 = [guideline §10]** (확정→finalized=제약 · 검토·컨셉→open=참고 의견 · 등재 2경로 `source: 킷|참조`).
입구 판단·사용법은 [docs/reference-context-map/index.md](../../docs/reference-context-map/index.md)(scaffold)와 §10 참조.

## A. 도메인 인덱스 (이 표 포맷)
| 도메인 | status | source | 항목(링크) | 경로 | 최종갱신 | 신선도 |
|---|---|---|---|---|---|---|
| <domain> | 확정\|검토\|컨셉 | 킷\|참조 | [경로/<domain>.md](...) | finalized/\|open/ | <date> | 최신 |

→ 교차 분석: [cross-domain-analysis.md](cross-domain-analysis.md)

## B. 도메인 항목 포맷 (`finalized/<domain>.md` 또는 `open/<domain>.md`)
```
<!-- reference-context: <domain> | status: 확정|검토|컨셉 | source: 킷|참조 | as-of: <YYYY-MM-DD> | confidence: 상|중|하 -->
# <domain>  (status: <확정|검토|컨셉>)
- 한 줄 정의: <...>
- 동결 문제집합(요지): <...>      - 성공기준(요지): <...>      - 핵심 설계 결정: <채택/기각>
- 의존 도메인: <방향>            - 열린 결정(검토·컨셉만): <방향 제안 대상>
- 전체 PRD: <경로/inputs 링크 (작업본은 본문에 그대로 둬도 됨)>
- 출처: [<누가/어디서>] · 수집일 <date> · confidence <상|중|하>
```
> 맵 항목 = 읽을 수 있는 PRD 작업본(라이브러리). 외부 확정 PRD는 전체 문서 그대로 두고 맨 위 헤더 한 줄만 붙이면 됨. 구조 점검 = `ref-map-lint`.

## B.1 Notion 링크파일 (`<domain>.refs.md`) — 파일 대신 라이브 링크
파일을 굽지 않고 Notion 원본을 참조할 때. 파일명에 `.refs.` 표식, **위치(폴더)로 존이 갈린다**(파일 내부 마커 금지).
```
<!-- reference-context: <domain> | status: 확정|검토|컨셉 | source: 참조 | as-of: <YYYY-MM-DD> -->
# <domain> — 라이브 Notion 참조
예시 도메인 A :: https://www.notion.so/your-workspace/Example-Page-A-<32자리-page-id>
[예시 도메인 B](https://www.notion.so/your-workspace/Example-Page-B-<32자리-page-id>)
```
- 한 줄 한 URL(`라벨 :: URL` / `[라벨](URL)` / `URL`). `#`·주석 줄 무시. URL 없는 줄은 WARN(조용한 폴백 금지).
- **`finalized/<d>.refs.md` = 읽기전용**(fetch만) · **`open/<d>.refs.md` = 수정 가능**. `inputs/`에선 헤더 선택.
- 인증(MCP) 계정에 공유된 페이지만 fetch. 구조 점검 = `notion-refs-lint`. 자식 페이지·블록단위 read-fix는 페이지 단위 한계.
