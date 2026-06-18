#!/usr/bin/env python3
# notion-zone-guard (PreToolUse 훅, L2) — Notion *쓰기* 도구가 finalized 링크의 page-id를 타깃하면 차단.
#   계약: stdin JSON {"tool_name":..., "tool_input":{...}}. 차단 = exit 2
#         (PreToolUse JSON permissionDecision:"deny"는 MCP 도구에 안 먹는 버그 #33106 → 반드시 exit 2).
#   동작: 읽기(search/fetch/get/list/query 등 = 쓰기 동사 없음)는 통과. 쓰기인데 입력에 finalized page-id가
#         있으면 차단(denylist). finalized id = reference-context-map/finalized/*.refs.md 를 매번 직접 스캔
#         (매니페스트 stale 창 0). 서버명/도구명은 'mcp__...notion...__' + 쓰기 동사로 느슨히 매칭(실제 도구명은 인증 후 확정).
#   한계: Notion 자식 페이지는 별도 page-id라 부모만 등록되면 못 막음(문서화). 블록단위 아닌 페이지단위.

import json
import os
import re
import sys

NOTION_URL = re.compile(r"https?://(?:www\.)?notion\.(?:so|site)/\S+")
HEXID = re.compile(r"[0-9a-fA-F]{32}|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
WRITE = re.compile(r"(update|create|append|insert|delete|archive|add|move|duplicate|patch|replace|write)", re.I)
FIN_DIR = os.path.join("docs", "reference-context-map", "finalized")


def norm(raw):
    return raw.replace("-", "").lower()


def finalized_ids():
    ids = set()
    if not os.path.isdir(FIN_DIR):
        return ids
    for name in os.listdir(FIN_DIR):
        n = name.lower()
        if ".refs." not in n or n.startswith(("_", ".")):
            continue
        try:
            in_comment = False
            with open(os.path.join(FIN_DIR, name), encoding="utf-8", errors="replace") as f:
                for line in f:
                    s = line.strip()
                    if in_comment:                   # 여러 줄 <!-- ... --> 주석 통째로 건너뜀
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
                        hx = HEXID.findall(m.group(0))
                        if hx:
                            ids.add(norm(hx[-1]))
        except Exception:
            continue
    return ids


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace"))
    except Exception:
        return 0
    try:
        tool = (data.get("tool_name") or "")
        low = tool.lower()
        if not low.startswith("mcp__") or "notion" not in low:
            return 0
        if not WRITE.search(low):
            return 0  # 읽기/알수없음 → 통과(권한 프롬프트가 사람 게이트)
        fin = finalized_ids()
        if not fin:
            return 0
        try:
            blob = json.dumps(data.get("tool_input") or {}, ensure_ascii=False)
        except Exception:
            blob = str(data.get("tool_input"))
        target = {norm(x) for x in HEXID.findall(blob)}
        hit = sorted(target & fin)
        if hit:
            sys.stderr.write(
                "[notion-zone-guard] 차단: Notion 쓰기 도구가 finalized 링크 페이지를 타깃합니다 "
                f"(page-id …{hit[0][-8:]}).\n"
                "  finalized = 확정·고정 제약 → 읽기전용. 수정 금지(변경요청 프로토콜로 사람이 결정).\n")
            sys.exit(2)
    except SystemExit:
        raise
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
