#!/usr/bin/env python3
"""Pass-5 polish checks. Run from the repo root."""
import asyncio, json, os, re
from playwright.async_api import async_playwright
REPO = "/home/claude/a330/repo"
html = open("limitations.html", encoding="utf-8").read()
m = re.search(r"/\* BEGIN data/limitations\.json \*/\nconst LIMITATIONS =\n(.*?);\n/\* END data/limitations\.json \*/", html, re.S)
emb = json.loads(m.group(1)); src = json.load(open("/home/claude/a330/data/limitations_v3.json", encoding="utf-8"))
def walk(o):
    if isinstance(o, str): return "\\" in o
    if isinstance(o, dict): return any(walk(v) for v in o.values())
    if isinstance(o, list): return any(walk(v) for v in o)
    return False
print("limitations embed == limitations_v3.json:", emb == src, "| items:", len(emb), "| strings with a backslash:", sum(walk(i) for i in emb))
assert emb == src and len(emb) == 160 and not any(walk(i) for i in emb)
fails = 0
async def main():
    global fails
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await (await b.new_context(viewport={"width": 1280, "height": 900})).new_page()
        await pg.goto("file://" + os.path.join(REPO, "limitations.html"))
        lab = await pg.evaluate("document.querySelector('label.check').innerText")
        print("UNCLEAR label:", repr(lab), "PASS" if "(16)" in lab else "FAIL"); fails += "(16)" not in lab
        await pg.click("#tabRef"); await pg.click("#expandAll")
        lead = await pg.evaluate("[...document.querySelectorAll('#refBody [data-vpre]')].filter(p => /^\\s/.test(p.textContent)).length")
        print("source blocks rendered with a leading space:", lead, "PASS" if lead == 0 else "FAIL"); fails += lead != 0
        wrapped = await pg.evaluate("[...document.querySelectorAll('#refBody td.ref code')].filter(c => c.getClientRects().length > 1).length")
        print("idents wrapping mid-string on desktop:", wrapped, "of", await pg.evaluate("document.querySelectorAll('#refBody td.ref code').length"), "PASS" if wrapped == 0 else "FAIL"); fails += wrapped != 0
        split = await pg.evaluate("""(() => { let n = 0; for (const p of document.querySelectorAll('#refBody [data-vpre]')) { const w = p.getBoundingClientRect().width; const r = document.createRange(); for (const t of p.childNodes) { if (t.nodeType !== 3) continue; const words = t.textContent.split(/(\\s+)/); let off = 0; for (const wd of words) { if (/^[A-Za-z]{4,}$/.test(wd)) { r.setStart(t, off); r.setEnd(t, off + wd.length); if (r.getClientRects().length > 1) n++; } off += wd.length; } } } return n; })()""")
        print("plain words split across lines in source text (desktop):", split, "PASS" if split == 0 else "FAIL"); fails += split != 0
        sw, iw = await pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]"); print("desktop overflow:", sw > iw); fails += sw > iw
        await pg.set_viewport_size({"width": 360, "height": 780}); await pg.wait_for_timeout(150)
        sw, iw = await pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]"); print("360px all sources expanded overflow:", sw > iw, f"({sw}/{iw})"); fails += sw > iw
        pg2 = await (await b.new_context(viewport={"width": 390, "height": 844})).new_page()
        await pg2.goto("file://" + os.path.join(REPO, "memory-items.html"))
        txt = await pg2.evaluate("document.getElementById('boardBody').textContent")
        print("scoreboard '1 lines':", "1 lines" in txt, "| '1 line' present:", "1 line" in txt, "PASS" if "1 lines" not in txt else "FAIL"); fails += "1 lines" in txt
        clipped = await pg2.evaluate("(() => { const b = document.getElementById('board').getBoundingClientRect(); return [...document.querySelectorAll('#board .st, #board td')].filter(e => e.getBoundingClientRect().right > b.right + 0.5).length; })()")
        print("phone scoreboard cells beyond the board edge:", clipped, "PASS" if clipped == 0 else "FAIL"); fails += clipped != 0
        await pg2.click("#styLine"); await pg2.click("#dirA2P")
        st = await pg2.evaluate("[el('styWhole').getAttribute('aria-pressed'), el('styLine').getAttribute('aria-pressed'), S.style, S.direction]")
        print("mode segment after switching to actions -> procedure:", st, "PASS" if st[0] == 'false' and st[1] == 'false' else "FAIL"); fails += not (st[0] == 'false' and st[1] == 'false')
        await pg2.click("#dirP2A"); await pg2.click("#styWhole")
        st = await pg2.evaluate("[el('styWhole').getAttribute('aria-pressed'), el('styLine').getAttribute('aria-pressed'), S.style]")
        print("mode segment after Whole procedure:", st, "PASS" if st == ['true', 'false', 'whole'] else "FAIL"); fails += st != ['true', 'false', 'whole']
        v1 = await pg.evaluate("MANUAL.version"); v2 = await pg2.evaluate("META.version")
        print("versions:", v1, v2, "PASS" if (v1, v2) == ("0.7", "0.3") else "FAIL"); fails += (v1, v2) != ("0.7", "0.3")
        await b.close()
    print("POLISH CHECKS:", "ALL PASSED" if not fails else f"{fails} FAILED"); raise SystemExit(1 if fails else 0)
asyncio.run(main())
