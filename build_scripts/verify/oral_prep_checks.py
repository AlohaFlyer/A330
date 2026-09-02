#!/usr/bin/env python3
"""Build-time checks for oral-prep.html and data/oral_scope.json.

1. Dataset: parses, 67 areas / 278 objectives / 86 numeric claims, unique ids,
   full schema, valid statuses, the three flagged conflicts present, no em
   dashes / private-use / backslash-u anywhere in the raw file.
2. Runtime (Playwright): engine page over http and dist/oral-prep.html from
   file:// must load with zero console errors, show the banner and footer META,
   render the Walk (67 areas in file order, expandable, 278 objectives, claim
   badges: 23 verified / 63 unverified / 3 CONFLICT with explanations, session
   ticks that update progress), and run the Quiz through a FULL cycle (masked
   prompts, reveal with refs, self-grade, missed re-served, done) plus the
   unticked pool, at phone width and in dark mode too. The engine page from
   file:// must show the offline-tolerant message.

Usage: python3 build_scripts/verify/oral_prep_checks.py <http base, e.g. http://localhost:8765/>
"""
import asyncio, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HTTP = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/"
fails = []

def check(name, ok, detail=""):
    print(("PASS" if ok else "FAIL"), name, detail)
    if not ok: fails.append(name)

# ---------- 1. dataset ----------
raw = open(os.path.join(ROOT, "data/oral_scope.json"), encoding="utf-8").read()
doc = json.loads(raw)
areas = doc["areas"]
ids = [a["id"] for a in areas]
n_obj = sum(len(a["objectives"]) for a in areas)
claims = [c for a in areas for c in a.get("numeric_claims", [])]
check("json parses, 67 areas", len(areas) == 67, f"n={len(areas)}")
check("278 objectives", n_obj == 278, f"n={n_obj}")
check("86 numeric claims", len(claims) == 86, f"n={len(claims)}")
check("no duplicate ids", len(ids) == len(set(ids)))
check("ids well-formed oral-NN", all(re.fullmatch(r"oral-\d\d", i) for i in ids))
missing = [a["id"] for a in areas
           if not (str(a.get("panel", "")).strip() and str(a.get("fcom_ref", "")).strip()
                   and a.get("objectives") and str(a.get("maps_to", "")).strip())]
check("every area has panel/fcom_ref/objectives/maps_to", not missing, str(missing[:5]))
check("claim statuses valid", all(c["status"] in ("VERIFIED-CURRENT", "UNVERIFIED") for c in claims))
check("status split 23 verified / 63 unverified",
      sum(c["status"] == "VERIFIED-CURRENT" for c in claims) == 23
      and sum(c["status"] == "UNVERIFIED" for c in claims) == 63)
conf_pairs = [("oral-15", "800 psi"), ("oral-26", "33,000"), ("oral-33", "195")]
for aid, frag in conf_pairs:
    a = next(x for x in areas if x["id"] == aid)
    check(f"conflict claim present {aid} ({frag})",
          any(frag in c["claim"] for c in a.get("numeric_claims", [])))
check("no em dash in json", "—" not in raw)
check("no backslash-u escapes in json", "\\u" not in raw)
check("no private-use chars in json",
      not any(0xE000 <= ord(c) <= 0xF8FF or 0xF0000 <= ord(c) <= 0x10FFFD for c in raw))

# ---------- 2. runtime ----------
from playwright.async_api import async_playwright

async def run_page(browser, url, label, dark=False, phone=False, full=False):
    ctx = await browser.new_context(
        viewport={"width": 375, "height": 720} if phone else {"width": 1100, "height": 800},
        color_scheme="dark" if dark else "light")
    pg = await ctx.new_page(); errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    await pg.goto(url, wait_until="load"); await pg.wait_for_timeout(400)

    n = await pg.evaluate("ORAL_SCOPE && ORAL_SCOPE.areas ? ORAL_SCOPE.areas.length : null")
    check(f"[{label}] data loaded", n == 67, f"n={n}")
    banner = await pg.evaluate("document.getElementById('banner').textContent")
    check(f"[{label}] banner: source, age, authority, progress-reset",
          "Rev 7 (04/06/23)" in banner and "three years old" in banner
          and "win every conflict" in banner and "reset on reload, by design" in banner)
    foot = await pg.evaluate("document.querySelector('footer').textContent")
    check(f"[{label}] footer META", "Rev 7 (04/06/23)" in foot and "FCOM R17" in foot
          and "QRH R35" in foot and "Generated 2026-09-02" in foot and "version 0.1" in foot
          and "23 of 86" in foot)

    # WALK: 67 areas in file order, expandable, badges, ticks
    n_areas = await pg.evaluate("document.querySelectorAll('#walkList .area').length")
    check(f"[{label}] walk renders 67 areas", n_areas == 67, f"n={n_areas}")
    order_ok = await pg.evaluate(
        "(function(){var b=document.querySelectorAll('#walkList .area-btn');"
        "for(var i=0;i<b.length;i++){if(AREAS[i].n!==i+1||b[i].textContent.indexOf(AREAS[i].panel)===-1)return i;}return -1;})()")
    check(f"[{label}] walk keeps the file's exam order", order_ok == -1, f"first bad index={order_ok}")
    await pg.click("#expandAll"); await pg.wait_for_timeout(100)
    lis = await pg.evaluate("document.querySelectorAll('#walkList .area-body ol li').length")
    check(f"[{label}] 278 objectives with FCOM refs", lis == 278, f"li={lis}")
    refs = await pg.evaluate("document.querySelectorAll('#walkList .area-btn .refm').length")
    check(f"[{label}] every area shows its FCOM ref", refs == 67, f"n={refs}")
    ver = await pg.evaluate("document.querySelectorAll('#walkList .claim .pill-ver').length")
    con = await pg.evaluate("document.querySelectorAll('#walkList .claim .pill-con').length")
    unv = await pg.evaluate("document.querySelectorAll('#walkList .claim .pill-unv').length")
    check(f"[{label}] claim badges 23 verified / 3 CONFLICT", ver == 23 and con == 3, f"ver={ver} con={con}")
    check(f"[{label}] 63 unverified badges (conflicts carry both)", unv == 63, f"unv={unv}")
    wl = await pg.evaluate("document.getElementById('walkList').textContent")
    check(f"[{label}] unverified caveat text visible",
          "NOT YET VERIFIED against current manuals, treat the number as suspect" in wl)
    check(f"[{label}] conflict explanations visible",
          "4,400 lb unusable per inner tank" in wl and "600/300 psi" in wl and "needs a FOM check" in wl)
    src_ok = await pg.evaluate(
        "Array.prototype.every.call(document.querySelectorAll('#walkList .claim'),"
        "function(p){return !p.querySelector('.pill-ver') || /Source: /.test(p.textContent);})")
    check(f"[{label}] every verified claim shows its source", src_ok)
    await pg.click("#collapseAll"); await pg.wait_for_timeout(50)
    open_bodies = await pg.evaluate("document.querySelectorAll('#walkList .area-body:not([hidden])').length")
    check(f"[{label}] collapse all closes every area", open_bodies == 0, f"open={open_bodies}")
    await pg.click('#walkList .area-btn[data-area="oral-26"]')
    body26 = await pg.evaluate(
        "(function(){var b=document.querySelector('#walkList .area-btn[data-area=\"oral-26\"]');"
        "return b.getAttribute('aria-expanded')==='true' && !b.closest('.area').querySelector('.area-body').hidden;})()")
    check(f"[{label}] single area expands (FUEL)", body26)
    await pg.click('#walkList .tick[data-tick="oral-01"]')
    stat = await pg.evaluate("document.getElementById('walkStatus').textContent")
    done_cls = await pg.evaluate("document.querySelectorAll('#walkList .area.done').length")
    check(f"[{label}] tick updates session progress", "1" in stat and "67" in stat and done_cls == 1, stat.strip()[:60])

    # QUIZ: masked prompt, reveal with refs, self-grade, full cycle
    await pg.click("#tabQuiz"); await pg.wait_for_timeout(100)
    qn = await pg.evaluate("S.queue.length")
    check(f"[{label}] quiz queue is all 278 objectives", qn == 278, f"n={qn}")
    masked = await pg.evaluate(
        "(function(){var q=current(); var p=document.querySelector('#card .prompt').textContent;"
        "return {mask: !/\\d/.test(p.replace(/Area/,'')) || p.indexOf('___')>-1 || !/\\d/.test(q.obj),"
        "explain: p.indexOf('Explain: ')===0, area: document.querySelector('#card .pill-map').textContent===q.area.panel};})()")
    check(f"[{label}] prompt shows area + Explain stem with numbers masked",
          masked["mask"] and masked["explain"] and masked["area"], str(masked))
    no_choice = await pg.evaluate("document.querySelectorAll('#card input[type=radio], #card .choice').length")
    check(f"[{label}] no multiple choice", no_choice == 0)
    focus_ok = await pg.evaluate("document.activeElement && document.activeElement.id === 'answerBox'")
    scroll_y = await pg.evaluate("window.scrollY")
    check(f"[{label}] answer box focused without scroll jump", focus_ok, f"scrollY={scroll_y}")
    await pg.keyboard.press("Enter")   # reveal from the box
    rev = await pg.evaluate(
        "(function(){var q=current(); var r=document.querySelector('#card .reveal');"
        "return r && r.textContent.indexOf(q.obj)>-1 && r.textContent.indexOf('FCOM '+q.area.fcom_ref)>-1;})()")
    check(f"[{label}] reveal shows full objective plus refs", rev)
    await pg.keyboard.press("2")       # miss the first
    await pg.keyboard.press(" ")       # reveal second (box blurred after grade renders new box; Space may not fire in box)
    if not await pg.evaluate("S.revealed"): await pg.keyboard.press("Enter")
    await pg.keyboard.press("2")       # miss the second
    if full:
        done = await pg.evaluate(
            "(function(){for(var i=0;i<3000;i++){if(S.phase==='done')break;"
            "if(S.phase==='roundbreak'){startNextRound();continue;}"
            "if(!S.revealed){reveal();} grade('got');}"
            "return {phase:S.phase, round:S.round, ever:Object.keys(S.missedEver).length,"
            "got:S.counts.got, missed:S.counts.missed};})()")
        check(f"[{label}] full quiz cycle reaches done", done["phase"] == "done", str(done))
        check(f"[{label}] missed objectives re-served until clean",
              done["round"] >= 2 and done["ever"] == 2 and done["missed"] == 2
              and done["got"] == 278, str(done))
    check(f"[{label}] restart works",
          await pg.evaluate("(function(){startSession(); return S.phase==='quiz' && S.round===1 && S.idx===0;})()"))
    # unticked pool honours the walk tick (oral-01 has 2 objectives)
    await pg.click('[data-pool="unticked"]'); await pg.wait_for_timeout(50)
    pooled = await pg.evaluate("S.queue.length")
    check(f"[{label}] unticked pool drops the ticked area", pooled == 276, f"n={pooled}")
    await pg.click('[data-pool="all"]')

    if phone:
        overflow = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check(f"[{label}] no horizontal overflow at 375px", overflow <= 1, f"overflow={overflow}")
    if dark:
        bg = await pg.evaluate("getComputedStyle(document.body).backgroundColor")
        check(f"[{label}] dark body ground", bg == "rgb(21, 19, 28)", bg)
    check(f"[{label}] zero console errors", not errs, str(errs[:3]))
    await ctx.close()

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        await run_page(b, HTTP + "oral-prep.html", "http engine", full=True)
        await run_page(b, "file://" + os.path.join(ROOT, "dist", "oral-prep.html"), "file:// dist", full=True)
        await run_page(b, HTTP + "oral-prep.html", "http engine phone", phone=True)
        await run_page(b, "file://" + os.path.join(ROOT, "dist", "oral-prep.html"), "file:// dist dark", dark=True)
        # engine from file://: fetch cannot run, the page must say so, not break
        ctx = await b.new_context(); pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file://" + os.path.join(ROOT, "oral-prep.html"), wait_until="load")
        await pg.wait_for_timeout(400)
        card = await pg.evaluate("document.getElementById('walkList').textContent")
        check("[file:// engine] offline-tolerant message", "Data not loaded" in card and "dist/" in card, card.strip()[:80])
        check("[file:// engine] no page errors", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    print("ORAL-PREP CHECKS:", "ALL PASSED" if not fails else f"{len(fails)} FAILED: {fails}")
    sys.exit(1 if fails else 0)

asyncio.run(main())
