#!/usr/bin/env python3
# ensure-refmap (SessionStart 훅) — docs/reference-context-map/ 스캐폴드를 *없으면 생성*한다.
# 실무자가 경로를 찾거나 다시 만들 필요가 없게(혼란 0). 비파괴·멱등·무출력 — 이미 있으면 손대지 않는다.

import os

ROOT = os.path.join("docs", "reference-context-map")

SEEDS = {
    os.path.join(ROOT, "index.md"): """<!-- reference-context-map index | auto-scaffolded (ensure-refmap 훅) -->
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
- 교차 분석: [cross-domain-analysis.md](cross-domain-analysis.md) · 구조 점검: `python3 .claude/tools/ref-map-lint.py docs/reference-context-map`
""",
    os.path.join(ROOT, "finalized", "README.md"): """# finalized/ — 확정 · 역할 = 고정 제약

현재 작성 중인 도메인 보고서가 **반드시 맞춰야** 하는 제약. (충돌 시 열린 쪽 조정.)
직접 넣을 때 맨 위 한 줄: `<!-- reference-context: <도메인> | status: 확정 | source: 참조 | as-of: <날짜> -->`
사용법 = [../index.md](../index.md) · 모델 상세 = guideline §10.
""",
    os.path.join(ROOT, "open", "README.md"): """# open/ — 검토·컨셉 · 역할 = 참고 가능한 의견

현재 보고서에 **구속력 없이 참고 반영**되는 의견(방향 제안 양방향). 확정되면 `finalized/`로 이동.
직접 넣을 때 맨 위 한 줄: `<!-- reference-context: <도메인> | status: 검토|컨셉 | source: 참조 | as-of: <날짜> -->`
사용법 = [../index.md](../index.md) · 모델 상세 = guideline §10.
""",
    os.path.join(ROOT, "cross-domain-analysis.md"): """<!-- cross-domain-analysis | auto-scaffolded -->
# 교차 도메인 분석 보고서

도메인이 2개 이상 등재되면 채워집니다 — 의존성/영향도 매트릭스 · 충돌 지점 · 열린 도메인 방향 수정 제안 · 선제 완성 우선순위.
(킷 생성 항목과 사람이 넣은 참조 항목을 *함께* 가로질러 분석합니다.) 템플릿: `.claude/templates/cross-domain-analysis.md`
""",
}


def main():
    os.makedirs(os.path.join(ROOT, "finalized"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "open"), exist_ok=True)
    for path, content in SEEDS.items():
        if not os.path.exists(path):
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception:
                pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
