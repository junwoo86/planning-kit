# open/ — 검토·컨셉 · 역할 = 참고 가능한 의견

현재 보고서에 **구속력 없이 참고 반영**되는 의견(방향 제안 양방향). 확정되면 `finalized/`로 이동.
직접 넣을 때 맨 위 한 줄: `<!-- reference-context: <도메인> | status: 검토|컨셉 | source: 참조 | as-of: <날짜> -->`
사용법 = [../index.md](../index.md) · 모델 상세 = guideline §10.

## Notion 링크로 참조하기 (`.refs.md`)
이 폴더에 `<도메인>.refs.md`(예: `<도메인>.refs.md`)를 만들어 헤더 한 줄(status: 검토|컨셉) + Notion URL을 한 줄에 하나씩. 형식 예시 = `_예시-노션링크.refs.md`.
**open 링크는 기획이 진행되며 함께 조정될 수 있습니다**(양방향 수정 제안 OK). 확정되면 `finalized/`로 이동. 구조 점검 = `notion-refs-lint`.
