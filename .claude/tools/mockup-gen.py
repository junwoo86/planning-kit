#!/usr/bin/env python3
# mockup-gen — 자족적 lo-fi HTML 목업 골격 생성기 (guideline §12, blueprint §6.4).
# *외형 전용·구현 검증 안 됨* 태그를 강제로 박는다. 최종 디자인 아님(버릴 수 있는 도출 도구).
# 기본 = 중립 lo-fi(흑백·플레이스홀더). docs/design-system/ 가 있으면 톤 참조를 배너에 표기(초안: 경로만).
#
# 사용:
#   sh .claude/hooks/launch.sh .claude/tools/mockup-gen.py <out.html> --title "견적 작성" --screens "목록,상세,작성" \
#          [--states "초기,로딩,빈,성공,에러,권한없음"] [--design-system docs/design-system]
# 종료코드: 0 = 생성, 2 = 인자 오류.

import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEFAULT_STATES = ["초기", "로딩", "빈", "성공", "에러", "권한없음"]


def opt(argv, name, default=None):
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else default


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_html(title, screens, states, ds_note):
    cards = []
    for sc in screens:
        chips = "".join(f'<button class="state">{esc(st)}</button>' for st in states)
        cards.append(f"""
    <section class="screen">
      <h2>{esc(sc)}</h2>
      <div class="states">{chips}</div>
      <div class="canvas">
        <div class="ph ph-bar"></div>
        <div class="ph ph-line"></div><div class="ph ph-line short"></div>
        <div class="ph ph-block"></div>
        <p class="hint">※ 플레이스홀더 — 상태별(초기/로딩/빈/성공/에러/권한없음) 화면을 여기에 도출</p>
      </div>
    </section>""")
    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>[목업] {esc(title)}</title>
<style>
  :root {{ --ink:#222; --mut:#888; --line:#ccc; --bg:#fafafa; }}
  * {{ box-sizing:border-box; }}
  body {{ font-family:-apple-system,'Segoe UI',sans-serif; color:var(--ink); background:var(--bg); margin:0; }}
  .banner {{ background:#222; color:#fff; padding:8px 16px; font-size:13px; position:sticky; top:0; }}
  .banner b {{ color:#ffd54a; }}
  header {{ padding:16px; border-bottom:1px solid var(--line); }}
  header h1 {{ margin:0; font-size:18px; }}
  header .ds {{ color:var(--mut); font-size:12px; margin-top:4px; }}
  main {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px; padding:16px; }}
  .screen {{ border:1px solid var(--line); border-radius:8px; background:#fff; padding:12px; }}
  .screen h2 {{ font-size:15px; margin:0 0 8px; }}
  .states {{ display:flex; flex-wrap:wrap; gap:4px; margin-bottom:8px; }}
  .state {{ font-size:11px; border:1px solid var(--line); background:#f3f3f3; border-radius:12px; padding:2px 8px; cursor:default; }}
  .canvas {{ border:1px dashed var(--line); border-radius:6px; padding:12px; min-height:140px; }}
  .ph {{ background:#eee; border-radius:4px; }}
  .ph-bar {{ height:28px; margin-bottom:10px; }}
  .ph-line {{ height:10px; margin:6px 0; }}  .ph-line.short {{ width:60%; }}
  .ph-block {{ height:56px; margin-top:10px; }}
  .hint {{ color:var(--mut); font-size:11px; margin:8px 0 0; }}
</style></head>
<body>
  <div class="banner">⚠️ <b>외형 전용 · 구현 검증 안 됨</b> — 최종 디자인 아님(버릴 수 있는 도출 도구). 암시 기능은 tech-planning 타당성 판정으로 라우팅.</div>
  <header>
    <h1>{esc(title)} <span style="color:var(--mut);font-weight:400">(lo-fi 목업)</span></h1>
    <div class="ds">{ds_note}</div>
  </header>
  <main>{''.join(cards)}
  </main>
</body></html>"""


def main(argv):
    bad = [a for a in argv[1:] if a.startswith("--") and a.split("=", 1)[0]
           not in {"--title", "--screens", "--states", "--design-system"}]
    if bad:
        print(f"[mockup-gen] 알 수 없는 옵션: {' '.join(bad)} (지원: --title --screens --states --design-system)", file=sys.stderr)
        return 2
    if len(argv) < 2 or argv[1].startswith("--"):
        print('사용: sh .claude/hooks/launch.sh .claude/tools/mockup-gen.py <out.html> --title "..." --screens "a,b,c" [--states "..."] [--design-system <dir>]',
              file=sys.stderr)
        return 2
    out = argv[1]
    title = opt(argv, "--title", "무제 화면")
    screens = [s.strip() for s in (opt(argv, "--screens", "화면1") or "").split(",") if s.strip()]
    states = [s.strip() for s in (opt(argv, "--states", ",".join(DEFAULT_STATES)) or "").split(",") if s.strip()]
    ds = opt(argv, "--design-system")
    if ds and os.path.isdir(ds):
        ds_note = f"디자인시스템 톤 참조: {ds} (색·타이포·간격을 여기에 맞춰 보강 — 초안은 중립 lo-fi)"
    else:
        ds_note = "디자인시스템 미보유 → 중립 lo-fi(흑백·플레이스홀더)"
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(build_html(title, screens, states, ds_note))
    print(f"[mockup-gen] 생성: {out}  (화면 {len(screens)} · 상태 {len(states)})")
    print("  다음: 전역 Playwright MCP로 렌더·스크린샷·검증 → 기획자 수정 프롬프트 → mockup-elicit 취합.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
