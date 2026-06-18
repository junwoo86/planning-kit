#!/usr/bin/env python3
# notion-refs-lint — *.refs.md(Notion 링크파일)을 *결정적* 검증 + finalized 매니페스트 빌드.
#   검사: (1) finalized/·open/ 의 .refs.md 헤더 status ↔ 폴더 정합(확정→finalized / 검토·컨셉→open)
#         (2) Notion URL 형식  (3) 같은 page-id가 finalized∧open 양쪽 → '존 충돌' FAIL
#         (4) URL 없는 비주석 줄 → WARN_NO_URL(조용한 폴백 금지).
#   부수효과: --build → finalized page-id를 .claude/state/notion-finalized.tsv 로(멱등). 위반/충돌이면 빌드 거부(fail-closed).
#   판정 안 하는 것: 그 URL이 정말 '확정'인가(=사람 판단) · 링크 내용 신선도(=fetch 후 last_edited_time).
#   이름이 _·. 로 시작하는 .refs.md(예시/안내)는 검사 제외.
#
# 사용:  sh .claude/hooks/launch.sh .claude/tools/notion-refs-lint.py docs/reference-context-map [inputs] [--build]
# 종료코드: 0 = 정합, 1 = 위반(헤더/경로/충돌), 2 = 인자 없음, 3 = 경로 없음. (규약: .claude/hooks/README.md)

import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

NOTION_URL = re.compile(r"https?://(?:www\.)?notion\.(?:so|site)/\S+")
HEXID = re.compile(r"[0-9a-fA-F]{32}|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
STATUS_RE = re.compile(r"status\s*[:：]\s*(확정|검토|컨셉)")
OPEN_OK = {"검토", "컨셉"}
STATE_TSV = os.path.join(".claude", "state", "notion-finalized.tsv")


def is_refs(name):
    n = name.lower()
    return ".refs." in n and not n.startswith(("_", "."))


def page_id(url):
    ids = HEXID.findall(url)
    return ids[-1].replace("-", "").lower() if ids else None


def parse(path):
    """returns (status, [(url, id)], [(lineno, snippet)])."""
    status, links, warns = None, [], []
    in_comment = False
    with open(path, encoding="utf-8", errors="replace") as f:
        for i, raw in enumerate(f, 1):
            s = raw.strip()
            if status is None and s.startswith("<!--"):
                m = STATUS_RE.search(s)
                if m:
                    status = m.group(1)
            if in_comment:                       # 여러 줄 <!-- ... --> 주석 블록 통째로 건너뜀
                if "-->" in s:
                    in_comment = False
                continue
            if s.startswith("<!--"):
                if "-->" not in s:
                    in_comment = True
                continue
            if not s or s.startswith("#") or s.startswith("-->"):
                continue
            m = NOTION_URL.search(s)
            if m:
                links.append((m.group(0), page_id(m.group(0))))
            else:
                warns.append((i, s[:60]))
    return status, links, warns


def list_refs(folder):
    out = []
    if os.path.isdir(folder):
        for name in sorted(os.listdir(folder)):
            p = os.path.join(folder, name)
            if os.path.isfile(p) and is_refs(name):
                out.append(p)
    return out


def walk_refs(root):
    out = []
    for dp, _dns, fns in os.walk(root):
        for name in sorted(fns):
            if is_refs(name):
                out.append(os.path.join(dp, name))
    return out


def main(argv):
    bad = [a for a in argv[1:] if a.startswith("--") and a.split("=", 1)[0] not in {"--build"}]
    if bad:
        print(f"[notion-refs-lint] 알 수 없는 옵션: {' '.join(bad)} (지원: --build)", file=sys.stderr)
        return 2
    args = [a for a in argv[1:] if not a.startswith("--")]
    build = "--build" in argv
    if not args:
        print("사용: sh .claude/hooks/launch.sh .claude/tools/notion-refs-lint.py docs/reference-context-map [inputs] [--build]", file=sys.stderr)
        return 2
    refmap = args[0]
    if not os.path.isdir(refmap):
        print(f"[notion-refs-lint] 디렉토리 없음: {refmap}", file=sys.stderr)
        return 3

    fails, warns_all, count = [], [], 0
    fin_ids, open_ids = {}, {}
    print(f"[notion-refs-lint] {refmap}")

    for kind, folder, allowed in (("finalized", os.path.join(refmap, "finalized"), {"확정"}),
                                  ("open", os.path.join(refmap, "open"), OPEN_OK)):
        for p in list_refs(folder):
            count += 1
            status, links, warns = parse(p)
            rel = os.path.relpath(p, refmap)
            if status is None:
                fails.append(f"{rel}: 헤더 status(확정|검토|컨셉) 없음 (finalized/open의 .refs.md엔 필수)")
            elif status not in allowed:
                fails.append(f"{rel}: status='{status}' 인데 {kind}/ 폴더 → 경로 불일치 "
                             f"({'open/으로' if status in OPEN_OK else 'finalized/으로'} 이동)")
            else:
                print(f"  ✓ {rel}  (status: {status}, 링크 {len(links)})")
            for (url, pid) in links:
                if pid is None:
                    warns_all.append(f"{rel}: page-id 추출 실패 → {url[:50]}")
                else:
                    (fin_ids if kind == "finalized" else open_ids)[pid] = rel
            for (ln, snip) in warns:
                warns_all.append(f"{rel}:L{ln} URL 없는 줄 → {snip}")

    if len(args) > 1 and os.path.isdir(args[1]):
        for p in walk_refs(args[1]):
            count += 1
            _st, links, warns = parse(p)
            print(f"  ✓ {p}  (inputs, 링크 {len(links)})")
            for (ln, snip) in warns:
                warns_all.append(f"{p}:L{ln} URL 없는 줄 → {snip}")

    for pid in sorted(set(fin_ids) & set(open_ids)):
        fails.append(f"존 충돌: page-id …{pid[-8:]} 가 finalized({fin_ids[pid]})·open({open_ids[pid]}) 양쪽 "
                     f"— 사람 결정 필요(그 전까지 보수적으로 finalized=읽기전용 취급)")

    for w in warns_all:
        print(f"  ⚠ {w}")

    if fails:
        print()
        for f in fails:
            print(f"  ✗ {f}")
        print(f"\n결과: FAIL — {len(fails)}건. (확정→finalized · 검토·컨셉→open · 충돌은 사람 결정)")
        if build:
            print("  [build] 위반/충돌로 매니페스트 빌드 거부(fail-closed).", file=sys.stderr)
        return 1

    if build:
        os.makedirs(os.path.dirname(STATE_TSV), exist_ok=True)
        with open(STATE_TSV, "w", encoding="utf-8") as f:
            f.write("# notion-finalized | built-by notion-refs-lint.py --build | children-expanded: no\n")
            f.write("# page_id\tzone\tsource_file\n")
            for pid, rel in sorted(fin_ids.items()):
                f.write(f"{pid}\tfinalized\t{rel}\n")
        print(f"  [build] finalized page-id {len(fin_ids)}건 → {STATE_TSV}")

    print(f"\n결과: PASS — .refs.md {count}개 정합. finalized 링크 {len(fin_ids)} · open 링크 {len(open_ids)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
