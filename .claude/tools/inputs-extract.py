#!/usr/bin/env python3
# inputs-extract — inputs/·참조맵의 원본(xlsx·html·csv·md·txt)을 텍스트로 추출 (킷 빈틈 #1, 의존성 0).
# xlsx = zip+XML 파싱(openpyxl 불필요), html = 태그 제거. PDF는 Read 도구(pages)로.
# *.refs.*(Notion 링크파일, 확장자 무관) = URL 목록만 추출(실제 fetch는 스킬 책임, 의존성 0).
#
# 사용:  sh .claude/hooks/launch.sh .claude/tools/inputs-extract.py <파일> [--max-rows N]
# 종료코드: 0 = 추출, 2 = 인자 없음, 3 = 파일 없음 또는 미지원 형식. (규약: .claude/hooks/README.md)

import html
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _ln(tag):
    return tag.split('}')[-1]


def _col(ref):
    m = re.match(r'([A-Z]+)', ref or "")
    if not m:
        return 0
    n = 0
    for ch in m.group(1):
        n = n * 26 + (ord(ch) - 64)
    return n


def extract_xlsx(path, max_rows=200):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    shared = []
    if 'xl/sharedStrings.xml' in names:
        root = ET.fromstring(z.read('xl/sharedStrings.xml'))
        for si in root:
            shared.append(''.join(t.text or '' for t in si.iter() if _ln(t.tag) == 't'))
    sheet_names = [s.get('name') for s in ET.fromstring(z.read('xl/workbook.xml')).iter() if _ln(s.tag) == 'sheet']
    out = []
    sheet_files = sorted([n for n in names if re.match(r'xl/worksheets/sheet\d+\.xml$', n)],
                         key=lambda n: int(re.search(r'(\d+)', n).group(1)))
    for i, sf in enumerate(sheet_files):
        name = sheet_names[i] if i < len(sheet_names) else sf
        out.append(f"\n##### 시트: {name} #####")
        emitted = 0
        for row in ET.fromstring(z.read(sf)).iter():
            if _ln(row.tag) != 'row':
                continue
            cells = {}
            for c in row:
                if _ln(c.tag) != 'c':
                    continue
                t, val = c.get('t'), None
                for child in c:
                    ln = _ln(child.tag)
                    if ln == 'v':
                        val = child.text
                    elif ln == 'is':
                        val = ''.join(x.text or '' for x in child.iter() if _ln(x.tag) == 't')
                if val is None:
                    continue
                if t == 's':
                    try:
                        val = shared[int(val)]
                    except (ValueError, IndexError):
                        pass
                cells[_col(c.get('r', ''))] = (val or '').strip()
            if not cells:
                continue
            line = " | ".join(cells.get(ci, '') for ci in range(1, max(cells) + 1))
            if line.strip():
                out.append(line)
                emitted += 1
                if emitted >= max_rows:
                    out.append(f"  …(시트 '{name}' {max_rows}행 초과 생략)")
                    break
    return "\n".join(out)


def extract_html(path):
    t = open(path, encoding="utf-8").read()
    t = re.sub(r'<style.*?</style>|<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<(h[1-3]|/h[1-3]|li|/li|tr|/tr|p|/p|div|br)[^>]*>', '\n', t)
    t = re.sub(r'<td[^>]*>', ' | ', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    t = re.sub(r'[ \t]+', ' ', t)
    return re.sub(r'\n\s*\n+', '\n', t).strip()


def extract_refs(path):
    """*.refs.* Notion 링크파일 → URL 목록만 추출(의존성 0, fetch 안 함).
    실제 내용 fetch는 strategy-intake/reference-coherence 스킬이 인증 확인 후 mcp__claude_ai_Notion__fetch로 수행."""
    urls, warns = [], []
    in_comment = False
    with open(path, encoding="utf-8", errors="replace") as f:
        for i, raw in enumerate(f, 1):
            s = raw.strip()
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
            m = re.search(r"https?://(?:www\.)?notion\.(?:so|site)/\S+", s)
            if m:
                urls.append(m.group(0))
            else:
                warns.append((i, s[:60]))
    out = [f"##### Notion 링크 참조 — {os.path.basename(path)} #####",
           f"URL {len(urls)}개 (Notion MCP fetch 대상 — 인증·권한 확인은 스킬이 수행):"]
    out += [f"  - {u}" for u in urls]
    if warns:
        out.append("[WARN_NO_URL] URL 없는 비주석 줄(확인 필요 — 조용한 폴백 금지):")
        out += [f"  L{i}: {s}" for i, s in warns]
    out.append("[note] inputs-extract는 URL 목록만 추출한다(의존성 0). 내용 fetch는 스킬이 mcp__claude_ai_Notion__fetch로.")
    return "\n".join(out)


def main(argv):
    bad = [a for a in argv[1:] if a.startswith("--") and a.split("=", 1)[0] not in {"--max-rows"}]
    if bad:
        print(f"[inputs-extract] 알 수 없는 옵션: {' '.join(bad)} (지원: --max-rows N)", file=sys.stderr)
        return 2
    args = [a for a in argv[1:] if not a.startswith("--")]
    max_rows = 200
    if "--max-rows" in argv:
        try:
            max_rows = int(argv[argv.index("--max-rows") + 1])
        except (ValueError, IndexError):
            pass
    if not args:
        print("사용: sh .claude/hooks/launch.sh .claude/tools/inputs-extract.py <파일> [--max-rows N]", file=sys.stderr)
        return 2
    p = args[0]
    ext = os.path.splitext(p)[1].lower()
    if not os.path.isfile(p):
        print(f"파일 없음: {p}", file=sys.stderr)
        return 3
    if ".refs." in os.path.basename(p).lower():   # Notion 링크파일(확장자 무관) — URL 목록만 추출(fetch 안 함)
        print(extract_refs(p))
        return 0
    if ext == '.xlsx':
        print(extract_xlsx(p, max_rows))
    elif ext in ('.html', '.htm'):
        print(extract_html(p))
    elif ext in ('.csv', '.md', '.txt', '.tsv'):
        print(open(p, encoding="utf-8", errors="replace").read())
    elif ext == '.pdf':
        print("PDF는 Read 도구의 pages 인자를 쓰세요(stdlib 미지원).", file=sys.stderr)
        return 3
    else:
        print(f"미지원 확장자: {ext}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
