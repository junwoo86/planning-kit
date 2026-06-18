#!/usr/bin/env python3
# local-readonly-guard (PreToolUse 훅, L1) — reference-context-map/finalized/ 의 *기존* 내용 수정을 차단.
#   계약: stdin JSON {"tool_name":..., "tool_input":{...}}. 차단 시 stderr 사유 + exit 2
#         (PreToolUse JSON deny는 MCP 도구에 안 먹는 버그 #33106 → 로컬 도구라도 일관되게 exit 2 사용).
#   원칙: '수정'만 막고 '신규 추가'는 허용한다(사용자가 새 확정 참조를 넣는 건 정상).
#   fail 정책(T14): 이 훅의 matcher는 쓰기성 도구 전부 → 파싱/처리 실패 = '검사 불가한 쓰기' = fail-closed(exit 2).
#     단, 정상 파싱됐고 finalized 패턴에 안 걸리는 '모호/읽기성' 경우는 통과(fail-open) — 이는 예외가 아니라 정상 흐름.
#     - Edit/MultiEdit/NotebookEdit: finalized 경로 대상 → 차단(기존 파일 수정).
#     - Write: finalized 경로 *이고 이미 존재* → 차단(덮어쓰기). 없으면 통과(신규 생성).
#     - Bash/PowerShell: finalized 를 '쓰기 대상'으로 하는 패턴(리다이렉트·rm·mv 등)만 차단(읽기는 통과).

import json
import os
import re
import sys

FINAL = re.compile(r"reference-context-map[\\/]+finalized[\\/]", re.I)
STRUCT_EDIT = {"Edit", "MultiEdit", "NotebookEdit"}
RE_REDIR = re.compile(r">>?\s*\"?[^\"'|;&\n]*reference-context-map[\\/]+finalized[\\/]", re.I)
RE_DESTRUCT = re.compile(
    r"\b(rm|del|mv|cp|tee|truncate|dd|sed|Remove-Item|Move-Item|Copy-Item|Set-Content|Add-Content|Out-File|Clear-Content)\b"
    r"[^\n]*reference-context-map[\\/]+finalized[\\/]", re.I)


def is_final(p):
    return bool(p) and bool(FINAL.search(str(p).replace("\\", "/")))


def block(reason):
    sys.stderr.write(
        "[local-readonly-guard] 차단: " + reason +
        "\n  finalized/ = 확정·고정 제약(읽기전용). 내용 수정은 변경요청 프로토콜로 사람이 결정하세요."
        "\n  (새 참조 '추가'는 허용됩니다 — 기존 내용 '수정'만 막습니다.)\n")
    sys.exit(2)


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace"))
    except Exception:
        # matcher = 쓰기성 도구 전부 → 입력을 못 읽으면 '검사 불가한 쓰기'. T14: fail-closed(exit 2). 조용한 폴백 금지.
        block("훅 입력(JSON) 파싱 실패 — 쓰기 도구를 검사할 수 없어 보수적으로 차단(fail-closed)")
    try:
        tool = data.get("tool_name") or ""
        ti = data.get("tool_input") or {}
        if tool in STRUCT_EDIT:
            p = ti.get("file_path") or ti.get("notebook_path") or ""
            if is_final(p):
                block(f"{tool} → finalized 기존 파일 수정 ({p})")
        elif tool == "Write":
            p = ti.get("file_path") or ""
            if is_final(p) and os.path.exists(p):
                block(f"Write → finalized 기존 파일 덮어쓰기 ({p})")
        elif tool in ("Bash", "PowerShell"):
            cmd = ti.get("command") or ""
            if RE_REDIR.search(cmd) or RE_DESTRUCT.search(cmd):
                block(f"{tool} → finalized 쓰기 명령 감지")
    except SystemExit:
        raise
    except Exception:
        # 쓰기 도구 검사 도중 내부 오류 → 검사 미완 → fail-closed(T14).
        block("쓰기 도구 검사 중 내부 오류 — 보수적으로 차단(fail-closed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
