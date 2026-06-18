<!-- reference-context-map index | auto-scaffolded (ensure-refmap 훅) -->
# 참조 컨텍스트 맵 (index)

도메인 PRD를 모아 의존성·충돌·우선순위를 보는 **참조 라이브러리**입니다. 항목은 두 경로로 들어옵니다:
- **킷 생성(source: 킷)**: `inputs/<주제>/`로 올려 기획/보고서를 만든 도메인 → 킷이 자동 등재.
- **사람 직접(source: 참조)**: 이미 확정됐거나 다른 데서 진행 중이라 *참조만* 할 자료 → `finalized/`·`open/`에 직접.

> 한 질문으로 갈립니다 — **"이 도메인을 킷으로 기획/보고서 생성할 건가?"** → 응 = `inputs/` · 아니(참조만) = 여기 직접.

## 도메인 인덱스
<!-- status = 확정 | 검토 | 컨셉 · source = 킷 | 참조 -->
| 도메인 | status | source | 항목(링크) | 경로 | 최종갱신 |
|---|---|---|---|---|---|
| (아직 없음) | | | | | |

- `finalized/` = 확정(고정 제약) · `open/` = 검토·컨셉(열림)
- **직접 넣을 때**: 문서 맨 위에 한 줄만 → `<!-- reference-context: <도메인> | status: 확정|검토|컨셉 | source: 참조 | as-of: <날짜> -->`
- **Notion 링크로**: `<도메인>.refs.md`(URL 한 줄씩) — finalized=읽기전용 · open=조정 가능. 형식 예시 = 각 폴더의 `_예시-노션링크.refs.md`.
- 교차 분석: [cross-domain-analysis.md](cross-domain-analysis.md) · 구조 점검: `python3 .claude/tools/ref-map-lint.py docs/reference-context-map` · Notion 링크 점검: `python3 .claude/tools/notion-refs-lint.py docs/reference-context-map`
