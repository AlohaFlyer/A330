#!/usr/bin/env python3
"""Fix-round visual checks (pass 4 items S1): dark-mode header/footer text
contrast >= 4.5:1 on both pages; at phone width no .mline value sits outside
its box on memory-items; segmented-control focus ring not clipped; gaps panels
collapsed on phone and open on desktop.
   python3 build_scripts/verify/pass4_visual_checks.py   (from the repo root)"""
import asyncio, os, re
from playwright.async_api import async_playwright
REPO = "/home/claude/a330/repo"

def lum(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def ratio(a, b):
    la, lb = lum(a), lum(b)
    if la < lb: la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)
def parse(c):
    m = re.match(r"rgba?\((\d+), (\d+), (\d+)", c)
    return tuple(int(x) for x in m.groups())

JS_BG = """(sel) => { let e = document.querySelector(sel); let el = e;
  while (el) { const bg = getComputedStyle(el).backgroundColor; if (bg && !bg.startsWith('rgba(0, 0, 0, 0')) return {fg: getComputedStyle(e).color, bg}; el = el.parentElement; }
  return {fg: getComputedStyle(e).color, bg: 'rgb(255, 255, 255)'}; }"""

async def main():
    fails = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for name in ("limitations.html", "memory-items.html"):
            for scheme in ("light", "dark"):
                ctx = await b.new_context(viewport={"width": 1280, "height": 900}, color_scheme=scheme)
                pg = await ctx.new_page()
                await pg.goto("file://" + os.path.join(REPO, name), wait_until="load")
                for sel in (".site-head h1", ".site-head .sub", "footer .id", "footer .muted", ".seg button[aria-pressed=true]", "thead th" if name == "limitations.html" else ".modes button[aria-selected=true]"):
                    if sel == "thead th":
                        await pg.click("#tabRef")
                    c = await pg.evaluate(JS_BG, sel)
                    r = ratio(parse(c["fg"]), parse(c["bg"]))
                    ok = r >= 4.5
                    fails += 0 if ok else 1
                    print(f"[{name} {scheme}] {sel:<36} {c['fg']} on {c['bg']} = {r:.2f}:1 {'PASS' if ok else 'FAIL'}")
                # focus ring on a segmented button must not be clipped: no overflow:hidden on .seg
                ov = await pg.evaluate("getComputedStyle(document.querySelector('.seg')).overflowX")
                print(f"[{name} {scheme}] .seg overflow-x = {ov} {'PASS' if ov == 'visible' else 'FAIL'}"); fails += ov != "visible"
                op = await pg.evaluate("getComputedStyle(document.querySelector('.btn .k')).opacity")
                print(f"[{name} {scheme}] .btn .k opacity = {op} {'PASS' if op == '1' else 'FAIL'}"); fails += op != "1"
                cs = await pg.evaluate("getComputedStyle(document.documentElement).colorScheme")
                print(f"[{name} {scheme}] color-scheme = {cs!r} {'PASS' if 'dark' in cs and 'light' in cs else 'FAIL'}"); fails += not ("dark" in cs and "light" in cs)
                opened = await pg.evaluate("[...document.querySelectorAll('details.gaps, details.recovered')].map(d => d.open)")
                print(f"[{name} {scheme}] desktop: info panels open = {opened} {'PASS' if all(opened) else 'FAIL'}"); fails += not all(opened)
                await ctx.close()
            # phone
            ctx = await b.new_context(viewport={"width": 390, "height": 844})
            pg = await ctx.new_page()
            await pg.goto("file://" + os.path.join(REPO, name), wait_until="load")
            opened = await pg.evaluate("[...document.querySelectorAll('details.gaps, details.recovered')].map(d => d.open)")
            print(f"[{name} phone] info panels collapsed = {[not o for o in opened]} {'PASS' if not any(opened) else 'FAIL'}"); fails += any(opened)
            sw, iw = await pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
            print(f"[{name} phone] no horizontal overflow on load: {sw <= iw} ({sw}/{iw})"); fails += sw > iw
            if name == "memory-items.html":
                # reveal every procedure in the reference tab and measure every value against its box
                await pg.click("#tabRef")
                bad = await pg.evaluate("""() => { const out = []; for (const box of document.querySelectorAll('#refList .mbox')) { const br = box.getBoundingClientRect();
                    for (const v of box.querySelectorAll('.mline .val')) { const r = v.getBoundingClientRect();
                      const it = v.parentElement.querySelector('.it').getBoundingClientRect();
                      if (r.right > br.right + 0.5 || r.left < br.left - 0.5 || r.top < br.top - 0.5 || r.bottom > br.bottom + 0.5 || r.top < it.top - 0.5)
                        out.push({val: v.textContent, item: v.parentElement.querySelector('.it').textContent}); } }
                    return {checked: document.querySelectorAll('#refList .mline .val').length, bad: out}; }""")
                print(f"[{name} phone] .mline values inside their box and not above their item: {bad['checked']} checked, {len(bad['bad'])} bad {bad['bad'][:3]} {'PASS' if not bad['bad'] else 'FAIL'}"); fails += bool(bad["bad"])
                sw, iw = await pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                print(f"[{name} phone] reference tab no horizontal overflow: {sw <= iw}"); fails += sw > iw
                await pg.click("#tabDrill")
                clipped = await pg.evaluate("(() => { const b = document.getElementById('board').getBoundingClientRect(); return [...document.querySelectorAll('#board .st')].filter(e => e.getBoundingClientRect().right > b.right + 0.5).length; })()")
                print(f"[{name} phone] scoreboard pills clipped at rest: {clipped} {'PASS' if clipped == 0 else 'FAIL'}"); fails += clipped != 0
                gut = await pg.evaluate("document.querySelectorAll('#card .gmark').length")
                await pg.keyboard.press("Enter")
                gm = await pg.evaluate("[...document.querySelectorAll('#card .gmark')].map(e => e.textContent.trim())")
                print(f"[{name} phone] gutter marks after reveal (only the cursor line carries one): {gm} {'PASS' if gm == ['grade'] else 'FAIL'}"); fails += gm != ["grade"]
            else:
                await pg.click("#tabRef"); await pg.click("#expandAll")
                await pg.wait_for_timeout(200)
                sw, iw = await pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                print(f"[{name} phone] reference, all sources expanded, no page-level horizontal overflow: {sw <= iw} ({sw}/{iw})"); fails += sw > iw
                await pg.set_viewport_size({"width": 360, "height": 780}); await pg.wait_for_timeout(100)
                sw, iw = await pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                print(f"[{name} 360px] reference, all sources expanded, no page-level horizontal overflow: {sw <= iw} ({sw}/{iw})"); fails += sw > iw
                tags = await pg.evaluate("getComputedStyle(document.querySelector('.recovered .tag')).borderStyle")
                print(f"[{name}] .recovered .tag styled (border {tags}): {'PASS' if tags == 'solid' else 'FAIL'}"); fails += tags != "solid"
                spans = await pg.evaluate("document.querySelectorAll('#statusbar > span').length")
                print(f"[{name}] status bar fragments wrapped in spans: {spans} {'PASS' if spans >= 5 else 'FAIL'}"); fails += spans < 5
            await ctx.close()
        await b.close()
    print("VISUAL CHECKS:", "ALL PASSED" if not fails else f"{fails} FAILED")
    raise SystemExit(1 if fails else 0)
asyncio.run(main())
