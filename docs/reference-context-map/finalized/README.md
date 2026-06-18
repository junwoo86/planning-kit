# finalized/ — 확정 · 역할 = 고정 제약

현재 작성 중인 도메인 보고서가 **반드시 맞춰야** 하는 제약. (충돌 시 열린 쪽 조정.)
직접 넣을 때 맨 위 한 줄: `<!-- reference-context: <도메인> | status: 확정 | source: 참조 | as-of: <날짜> -->`
사용법 = [../index.md](../index.md) · 모델 상세 = guideline §10.

## Notion 링크로 참조하기 (`.refs.md`)
파일 대신 **Notion 문서 링크**를 연결하려면, 이 폴더에 `<도메인>.refs.md`(예: `기록_수면.refs.md`)를 만들어 맨 위 헤더 한 줄(status: 확정) + Notion URL을 한 줄에 하나씩 적으세요. 형식 예시 = `_예시-노션링크.refs.md`.
**finalized 링크가 가리키는 Notion 문서는 '읽기 전용'**입니다(킷이 수정하지 않음). 구조 점검 = `python3 ../../../.claude/tools/notion-refs-lint.py docs/reference-context-map`.
