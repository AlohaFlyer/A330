#!/usr/bin/env python3
"""Build-time checks for fom-delta.html and data/fom_delta.json.

1. Dataset: parses, no duplicate ids, every item has before/after/ref (and the
   rest of the schema), drill shapes are sane, no em dashes / private-use /
   backslash-u anywhere in the raw file.
2. Runtime (Playwright): engine page over http and dist/fom-delta.html from
   file:// must load with zero console errors, show the banner, render both
   modes (Review grouped with before/after pairs and a working search; Drill
   through one FULL cycle: every question revealed and graded, missed ones
   re-served, session reaches done), at phone width and in dark mode too.
   The engine page from file:// must show the offline-tolerant message.

Usage: python3 build_scripts/verify/fom_delta_checks.py <http base, e.g. http://localhost:8765/>
"""
import asyncio, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HTTP = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/"
fails = []

def check(name, ok, detail=""):
    print(("PASS" if ok else "FAIL"), name, detail)
    if not ok: fails.append(name)

# ---------- 1. dataset ----------
raw = open(os.path.join(ROOT, "data/fom_delta.json"), encoding="utf-8").read()
items = json.loads(raw)
ids = [x["id"] for x in items]
check("json parses, item count", len(items) == 52, f"n={len(items)}")
check("no duplicate ids", len(ids) == len(set(ids)))
check("ids well-formed fd-NN", all(re.fullmatch(r"fd-\d\d", i) for i in ids))
missing = [x["id"] for x in items for k in ("before", "after", "ref", "fom_section", "topic",
           "change_summary", "why_it_matters", "source", "scope", "src", "fleet")
           if not str(x.get(k, "")).strip()]
check("every item has before/after/ref and full schema", not missing, str(missing[:5]))
check("source values valid", all(x["source"] in ("highlights", "diff", "both") for x in items))
check("scope values valid", all(x["scope"] in ("A330", "fleet-common") for x in items))
check("ref format", all(x["ref"].startswith("FOM ") for x in items))
drills = []
for x in items:
    d = x.get("drill")
    if not d: continue
    for qa in (d if isinstance(d, list) else [d]):
        check(f"drill shape {x['id']}", bool(str(qa.get('q','')).strip()) and bool(str(qa.get('a','')).strip()))
        drills.append(qa)
check("drill count", len(drills) == 18, f"n={len(drills)}")
check("no em dash in json", "—" not in raw)
check("no backslash-u escapes in json", "\\u" not in raw)
check("no private-use chars in json",
      not any(0xE000 <= ord(c) <= 0xF8FF or 0xF0000 <= ord(c) <= 0x10FFFD for c in raw))

# ---------- 2. runtime ----------
from playwright.async_api import async_playwright

async def run_page(browser, url, label, dark=False, phone=False):
    ctx = await browser.new_context(
        viewport={"width": 375, "height": 720} if phone else {"width": 1100, "height": 800},
        color_scheme="dark" if dark else "light")
    pg = await ctx.new_page(); errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    await pg.goto(url, wait_until="load"); await pg.wait_for_timeout(400)

    n = await pg.evaluate("Array.isArray(FOM_DELTA) ? FOM_DELTA.length : null")
    check(f"[{label}] data loaded", n == len(items), f"n={n}")
    banner = await pg.evaluate("document.getElementById('banner').textContent")
    check(f"[{label}] banner names the diff-plus-highlights method",
          "whitespace-normalized body diff" in banner and "NO Revision Highlights" in banner
          and "FOM itself is the authority" in banner.replace("The FOM itself is the authority", "FOM itself is the authority"))
    foot = await pg.evaluate("document.querySelector('footer').textContent")
    check(f"[{label}] footer META", "125.1 (8/12/26)" in foot and "123.1 (4/27/26)" in foot
          and "Generated 2026-09-02" in foot and "version 0.1" in foot)

    # REVIEW mode: grouped cards, before/after pairs, search
    cards = await pg.evaluate("document.querySelectorAll('#revList .chg').length")
    chapters = await pg.evaluate("document.querySelectorAll('#revList .chapter-h').length")
    pairs = await pg.evaluate("document.querySelectorAll('#revList .ba .before').length")
    check(f"[{label}] review renders all changes", cards == len(items), f"cards={cards}")
    check(f"[{label}] review grouped by chapter", chapters >= 10, f"chapters={chapters}")
    check(f"[{label}] before/after pair on every card", pairs == len(items), f"pairs={pairs}")
    ghosts = await pg.evaluate("document.querySelectorAll('#revList .ba .q.ghost').length")
    check(f"[{label}] only bracketed placeholders render as ghosts", ghosts == 13, f"ghosts={ghosts}")
    banner_ghost = await pg.evaluate(
        "Array.prototype.some.call(document.querySelectorAll('#revList .ba .q.ghost'),"
        "function(q){return /\\(7|\\(A3|\\(AS\\)/.test(q.textContent.slice(0,60)) && q.textContent.indexOf('(none') === -1;})")
    check(f"[{label}] no fleet-banner quote is ghosted", not banner_ghost)
    await pg.fill("#searchBox", "LAHSO")
    hits = await pg.evaluate("document.querySelectorAll('#revList .chg').length")
    check(f"[{label}] search narrows (LAHSO)", 1 <= hits < len(items), f"hits={hits}")
    await pg.fill("#searchBox", "")
    await pg.click("[data-src=\"diff\"]")
    donly = await pg.evaluate("document.querySelectorAll('#revList .chg').length")
    check(f"[{label}] diff-only filter is about 30", 25 <= donly <= 32, f"n={donly}")
    await pg.click("[data-src=\"all\"]")

    # DRILL mode: one full cycle to done (grade a couple wrong, then clean rounds)
    await pg.click("#tabDrill"); await pg.wait_for_timeout(100)
    qtotal = await pg.evaluate("DRILLS.length")
    check(f"[{label}] drill queue is the full drill list", qtotal == 18, f"n={qtotal}")
    for safety in range(200):
        phase = await pg.evaluate("S.phase")
        if phase == "done": break
        if phase == "roundbreak":
            await pg.keyboard.press(" "); continue
        await pg.keyboard.press("Enter")     # answer box focused: Enter reveals
        revealed = await pg.evaluate("S.revealed")
        if not revealed:                     # focus not in a box (post-blur): Space reveals
            await pg.keyboard.press(" ")
        if safety == 0:                      # exercise V once: show the underlying change
            await pg.keyboard.press("v")
            shown = await pg.evaluate("document.querySelectorAll('#card .srcchg .chg').length")
            check(f"[{label}] V shows the underlying change", shown == 1)
            await pg.keyboard.press("v")
        # miss the first two on round 1, get everything else
        state = await pg.evaluate("({round:S.round, idx:S.idx})")
        await pg.keyboard.press("2" if (state["round"] == 1 and state["idx"] < 2) else "1")
    final = await pg.evaluate("({phase:S.phase, round:S.round, counts:S.counts, ever:Object.keys(S.missedEver).length})")
    check(f"[{label}] full drill cycle reaches done", final["phase"] == "done", str(final))
    check(f"[{label}] missed questions were re-served in round 2+",
          final["round"] >= 2 and final["ever"] == 2 and final["counts"]["missed"] == 2, str(final))
    ok_grades = final["counts"]["got"] == 18  # 16 clean on round 1 + 2 re-served clean
    check(f"[{label}] grade bookkeeping", ok_grades, str(final["counts"]))
    check(f"[{label}] restart works", await pg.evaluate("(function(){var r=S.round; startSession(); return S.phase==='drill' && S.round===1 && S.idx===0;})()"))

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
        await run_page(b, HTTP + "fom-delta.html", "http engine")
        await run_page(b, "file://" + os.path.join(ROOT, "dist", "fom-delta.html"), "file:// dist")
        await run_page(b, HTTP + "fom-delta.html", "http engine phone", phone=True)
        await run_page(b, "file://" + os.path.join(ROOT, "dist", "fom-delta.html"), "file:// dist dark", dark=True)
        # engine from file://: fetch cannot run, the page must say so, not break
        ctx = await b.new_context(); pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file://" + os.path.join(ROOT, "fom-delta.html"), wait_until="load")
        await pg.wait_for_timeout(400)
        card = await pg.evaluate("document.getElementById('revList').textContent")
        check("[file:// engine] offline-tolerant message", "Data not loaded" in card and "dist/" in card, card.strip()[:80])
        check("[file:// engine] no page errors", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    print("FOM-DELTA CHECKS:", "ALL PASSED" if not fails else f"{len(fails)} FAILED: {fails}")
    sys.exit(1 if fails else 0)

asyncio.run(main())
