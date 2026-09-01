#!/usr/bin/env python3
"""
PASS 3 runtime verification of the two standalone drill pages.

  python3 build_scripts/verify/pass3_runtime.py

Drives memory-items.html and limitations.html in headless Chromium via
Playwright, records pass/fail per test with evidence, and writes

  /home/claude/a330/data/PASS3_runtime.md
  /home/claude/a330/data/PASS3_failures.json

Nothing in the pages is modified. In-page state (S, current(), PROCS,
LIMITATIONS) is read for cross-checks only; every driving action goes
through the keyboard or a click, the way a user would do it.
"""
import asyncio, json, os, re, sys, time, traceback
from playwright.async_api import async_playwright

REPO = "/home/claude/a330/repo"
DATA = "/home/claude/a330/data"
PAGES = {"memory-items": "memory-items.html", "limitations": "limitations.html"}
VIEWPORTS = [(1280, 900), (390, 844), (360, 780)]
LIGHT = {"body_bg": "rgb(255, 255, 255)", "card_bg": "rgb(255, 255, 255)", "body_color": "rgb(0, 0, 0)"}

# ----------------------------------------------------------------------------
# result collection
# ----------------------------------------------------------------------------
class Results:
    def __init__(self):
        self.rows = []      # dict(page, test, name, status, evidence, repro, severity)
        self.text_hits = [] # (page, state, needle, context)
        self.state_count = 0

    def add(self, page, test, name, ok, evidence="", repro="", severity="major"):
        self.rows.append({"page": page, "test": test, "name": name,
                          "status": "PASS" if ok else "FAIL",
                          "evidence": str(evidence)[:1500], "repro": repro if not ok else "",
                          "severity": severity if not ok else ""})
        if not ok:
            print(f"  FAIL [{page}/{test}] {name}: {str(evidence)[:300]}")

    def error(self, page, test, name, exc, repro=""):
        self.rows.append({"page": page, "test": test, "name": name, "status": "FAIL",
                          "evidence": "exception: " + "".join(traceback.format_exception_only(type(exc), exc)).strip()
                                      + "\n" + traceback.format_exc()[-1200:],
                          "repro": repro, "severity": "blocker"})
        print(f"  ERROR [{page}/{test}] {name}: {exc}")


R = Results()

# ----------------------------------------------------------------------------
# page helpers
# ----------------------------------------------------------------------------
JS_OVERFLOW = """
() => {
  const vw = window.innerWidth;
  const out = [];
  const seen = new Set();
  for (const e of document.querySelectorAll('body *')) {
    const r = e.getBoundingClientRect();
    if (r.width === 0) continue;
    if (r.width > vw + 0.5 || r.right > vw + 0.5 || r.left < -0.5) {
      // is it clipped by a scrolling ancestor?
      let a = e.parentElement, clipped = false;
      while (a && a !== document.body) {
        const ox = getComputedStyle(a).overflowX;
        if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') { clipped = true; break; }
        a = a.parentElement;
      }
      const key = e.tagName + '.' + (e.className && e.className.baseVal === undefined ? e.className : '') + (clipped ? '|clipped' : '|page');
      if (seen.has(key)) continue;
      seen.add(key);
      out.push({tag: e.tagName, cls: String(e.className).slice(0, 60), id: e.id, w: Math.round(r.width), right: Math.round(r.right), left: Math.round(r.left), clipped, text: (e.textContent || '').trim().slice(0, 60)});
    }
  }
  return {vw, sw: document.documentElement.scrollWidth, bodySw: document.body.scrollWidth, items: out};
}
"""

TEXT_NEEDLES = [("undefined", r"\bundefined\b"), ("NaN", r"\bNaN\b"), ("null", r"\bnull\b"),
                ("[object", r"\[object"), ("em dash", "\u2014")]


async def new_page(browser, name, viewport=(1280, 900), color_scheme=None):
    kw = {"viewport": {"width": viewport[0], "height": viewport[1]}}
    if color_scheme:
        kw["color_scheme"] = color_scheme
    ctx = await browser.new_context(**kw)
    page = await ctx.new_page()
    errors = []
    page.on("console", lambda m: errors.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
    await page.goto("file://" + os.path.join(REPO, PAGES[name]), wait_until="load")
    await page.wait_for_timeout(150)
    return ctx, page, errors


async def body_text(page):
    return await page.evaluate("document.body.innerText")


async def snap(page, name, state, overflow=True):
    """Text-integrity scan + horizontal-overflow scan of the current state."""
    R.state_count += 1
    txt = await body_text(page)
    for label, pat in TEXT_NEEDLES:
        for m in re.finditer(pat, txt):
            ctx = txt[max(0, m.start() - 50):m.end() + 50].replace("\n", " | ")
            R.text_hits.append((name, state, label, ctx))
    if overflow:
        o = await page.evaluate(JS_OVERFLOW)
        page_level = [i for i in o["items"] if not i["clipped"]]
        if o["sw"] > o["vw"] or page_level:
            R.add(name, "overflow", f"no horizontal overflow @ {o['vw']}px, state: {state}", False,
                  f"scrollWidth={o['sw']} innerWidth={o['vw']} offenders={json.dumps(page_level)[:900]}",
                  f"Open {PAGES[name]} at {o['vw']}px wide, reach state '{state}', compare documentElement.scrollWidth to innerWidth and getBoundingClientRect of the listed elements.",
                  "major")
            return False
    return True


def status_nums(txt):
    """Parse the status bar text into numbers."""
    d = {}
    for key, pat in [("round", r"Round\s+(\d+)"), ("item", r"(?:Item|Procedure)\s+(\d+)\s+of\s+(\d+)"),
                     ("queue", r"Queue\s+(\d+)"), ("got", r"(?:Lines |Names )?[Gg]ot\s+(\d+)"),
                     ("missed", r"(?:Lines |Names )?[Mm]issed\s+(\d+)"),
                     ("owed", r"(?:Still owed|Procedures owed)\s+(\d+)"),
                     ("never", r"Never missed\s+(\d+)\s+of\s+(\d+)\s+served"), ("pool", r"Pool\s+(\d+)\s+of\s+(\d+)")]:
        m = re.search(pat, txt)
        if m:
            d[key] = tuple(int(x) for x in m.groups()) if len(m.groups()) > 1 else int(m.group(1))
    return d


async def status(page):
    return status_nums(await page.evaluate("document.getElementById('statusbar').innerText"))


async def card_text(page):
    """textContent, not innerText: several elements carry CSS text-transform: uppercase,
    which would make content comparisons fail for cosmetic reasons."""
    return await page.evaluate("document.getElementById('card').textContent")


async def blur(page):
    await page.evaluate("document.activeElement && document.activeElement.blur && document.activeElement.blur()")


async def key(page, k):
    """Press a drill key the way a user who has clicked out of the answer box would."""
    await blur(page)
    await page.keyboard.press(k)


def bad_tokens(txt):
    hits = []
    for label, pat in TEXT_NEEDLES:
        if re.search(pat, txt):
            hits.append(label)
    return hits


# ----------------------------------------------------------------------------
# A / B: load checks
# ----------------------------------------------------------------------------
async def test_load(browser, name, viewport, scheme=None):
    test = "B" if scheme == "dark" else "A"
    tag = f"{viewport[0]}x{viewport[1]}" + (" dark" if scheme else "")
    ctx, page, errors = await new_page(browser, name, viewport, scheme)
    try:
        sy = await page.evaluate("window.scrollY")
        R.add(name, test, f"scrollY 0 after load @ {tag}", sy == 0, f"scrollY={sy}",
              f"Open {PAGES[name]} in a {tag} viewport and read window.scrollY after load.")
        R.add(name, test, f"zero console/page errors @ {tag}", not errors, errors or "none",
              f"Open {PAGES[name]} at {tag} with the console open.")
        bb = await page.evaluate("(() => { const b = document.querySelector('.banner'); const r = b.getBoundingClientRect(); return {top: r.top, bottom: r.bottom, h: r.height, vis: getComputedStyle(b).visibility, disp: getComputedStyle(b).display}; })()")
        ok = bb["top"] < viewport[1] and bb["top"] >= 0 and bb["h"] > 0 and bb["disp"] != "none" and bb["vis"] != "hidden"
        R.add(name, test, f"banner in initial viewport @ {tag}", ok, bb,
              f"Open {PAGES[name]} at {tag}; getBoundingClientRect() of .banner.")
        o = await page.evaluate(JS_OVERFLOW)
        page_level = [i for i in o["items"] if not i["clipped"]]
        R.add(name, test, f"no element wider than viewport @ {tag}", o["sw"] <= o["vw"] and not page_level,
              f"scrollWidth={o['sw']} innerWidth={o['vw']} offenders={json.dumps(o['items'])[:900]}",
              f"Open {PAGES[name]} at {tag}; compare documentElement.scrollWidth with innerWidth and check the listed elements.")
        if scheme == "dark":
            c = await page.evaluate("(() => ({body_bg: getComputedStyle(document.body).backgroundColor, card_bg: getComputedStyle(document.querySelector('#card .card')).backgroundColor, body_color: getComputedStyle(document.body).color, card_color: getComputedStyle(document.querySelector('#card .card')).color, scheme: matchMedia('(prefers-color-scheme: dark)').matches}))()")
            ok = c["scheme"] and c["body_bg"] != LIGHT["body_bg"] and c["card_bg"] != LIGHT["card_bg"] and c["body_color"] != LIGHT["body_color"]
            R.add(name, test, f"dark override applied @ {tag}", ok, c,
                  f"Emulate prefers-color-scheme: dark, open {PAGES[name]}, read computed background of body and #card .card and computed color of body.")
            # dark colours should be dark, light colours light
            def lum(rgb):
                m = re.findall(r"\d+", rgb)
                r, g, b = [int(x) for x in m[:3]]
                return 0.2126 * r + 0.7152 * g + 0.0722 * b
            R.add(name, test, f"dark scheme is actually dark @ {tag}", lum(c["body_bg"]) < 80 and lum(c["body_color"]) > 170,
                  c, f"As above; luminance of body background must be low and of body text high.")
        await snap(page, name, f"load {tag}")
    except Exception as e:
        R.error(name, test, f"load checks @ {tag}", e)
    finally:
        await ctx.close()


# ----------------------------------------------------------------------------
# J: icon links (static file checks + live DOM)
# ----------------------------------------------------------------------------
async def test_icons(browser, name):
    ctx, page, errors = await new_page(browser, name)
    try:
        d = await page.evaluate("""(() => {
          const q = (s) => { const e = document.querySelector(s); return e ? e.getAttribute('href') : null; };
          return {icon: q('link[rel="icon"]'), touch: q('link[rel="apple-touch-icon"]'), manifest: q('link[rel="manifest"]')};
        })()""")
        R.add(name, "J", "link rel=icon href starts with data:image/png", bool(d["icon"]) and d["icon"].startswith("data:image/png"), str(d["icon"])[:60])
        R.add(name, "J", "apple-touch-icon present", bool(d["touch"]), d["touch"])
        R.add(name, "J", "manifest present", bool(d["manifest"]), d["manifest"])
        for k in ("touch", "manifest"):
            if d[k] and not d[k].startswith("data:"):
                p = os.path.join(REPO, d[k])
                R.add(name, "J", f"{k} target file exists on disk ({d[k]})", os.path.exists(p), p, severity="minor")
    except Exception as e:
        R.error(name, "J", "icon links", e)
    finally:
        await ctx.close()


# ----------------------------------------------------------------------------
# memory-items drivers
# ----------------------------------------------------------------------------
MI_STATE = """({phase:S.phase, idx:S.idx, round:S.round, revealed:S.revealed, line:S.line, cursor:S.cursor, counts:S.counts,
  queue:S.queue.map(p=>p.pid), owed:S.missedThisRound.slice(), pid: current() && current().pid, title: current() && current().title,
  n: current() && current().gradable.length, direction:S.direction, style:S.style, missedEver:Object.keys(S.missedEver),
  boxFocused: !!(document.activeElement && document.activeElement.id === 'answerBox')})"""


async def mi_state(page):
    return await page.evaluate(MI_STATE)


async def mi_reveal(page, how):
    """Reveal the current procedure either with Enter from the focused box or with Space after blurring."""
    if how == "enter":
        focused = await page.evaluate("document.activeElement && document.activeElement.id")
        if focused != "answerBox":
            await page.focus("#answerBox")
        await page.keyboard.press("Enter")
    else:
        await page.evaluate("document.activeElement && document.activeElement.blur()")
        await page.keyboard.press(" ")


async def mi_check_status(page, name, test, model, procs, step):
    """Compare the rendered status bar with the independent python model."""
    st = await status(page)
    s = await mi_state(page)
    exp_got = sum(v["got"] for v in model["counted"].values())
    exp_missed = sum(v["missed"] for v in model["counted"].values())
    exp_owed = len(model["owed"])
    served = {pid for (rnd, pid) in model["counted"]}
    never = [pid for pid in served if pid not in model["ever"]]
    ok = (st.get("got") == exp_got and st.get("missed") == exp_missed and st.get("owed") == exp_owed
          and st.get("never") == (len(never), len(served)) and st.get("round") == model["round"])
    if s["phase"] == "drill":
        ok = ok and st.get("item") == (s["idx"] + 1, len(s["queue"]))
    if not ok:
        R.add(name, test, f"status bar consistent at {step}", False,
              f"status={st} expected got={exp_got} missed={exp_missed} owed={exp_owed} never={len(never)}/{len(served)} round={model['round']} idx={s['idx']} queue={len(s['queue'])}",
              f"Drive {PAGES[name]} to {step} and read the status bar.")
    return ok


def alt_grade(counter):
    """Alternate 1 and 2 across every graded slot, globally."""
    k = "got" if counter[0] % 2 == 0 else "missed"
    counter[0] += 1
    return k


async def mi_full_session(browser, name, test, mode, viewport=(1280, 900)):
    """mode: whole | line | a2p. Drives a whole session through to 'done'."""
    ctx, page, errors = await new_page(browser, name, viewport)
    try:
        procs = await page.evaluate("PROCS.map(p => ({pid:p.pid, title:p.title, name:p.name, actions:p.actions, gradable:p.gradable, headers:p.headers, n:p.gradable.length, unboxed: p.layout.some(g => g.kind==='box' && g.unboxed)}))")
        by_pid = {p["pid"]: p for p in procs}
        R.add(name, test, f"[{mode}] ten procedures built from eleven entries",
              len(procs) == 10 and await page.evaluate("MEMORY_ITEMS.length") == 11, f"{len(procs)} procs")
        if mode == "line":
            await page.click("#styLine")
        elif mode == "a2p":
            await page.click("#dirA2P")
        s = await mi_state(page)
        R.add(name, test, f"[{mode}] mode switch applied", (s["style"] == "line") if mode == "line" else (s["direction"] == "a2p") if mode == "a2p" else (s["style"] == "whole" and s["direction"] == "p2a"), s)
        model = {"counted": {}, "owed": [], "ever": set(), "round": 1}
        counter = [0]
        prefilled = []
        status_ok = True
        step_i = 0
        served_pids_r1 = []
        while True:
            s = await mi_state(page)
            step_i += 1
            if step_i > 400:
                R.add(name, test, f"[{mode}] session terminates", False, f"still in phase {s['phase']} after 400 steps", severity="blocker")
                break
            if s["phase"] == "roundbreak":
                ct = await card_text(page)
                n = len(model["owed"])
                m = re.search(r"Round (\d+) closed, (\d+) procedures? still owed", ct)
                R.add(name, test, f"[{mode}] round {model['round']} break card shows correct owed count",
                      bool(m) and int(m.group(1)) == model["round"] and int(m.group(2)) == n and n == len(s["owed"]),
                      f"card: {m.group(0) if m else ct[:120]!r}; model owed={n} page owed={s['owed']}",
                      f"Grade round {model['round']} in {mode} mode so that {n} procedures have a missed line; the round-break card.")
                # tally numbers
                exp_got = sum(v["got"] for v in model["counted"].values()); exp_missed = sum(v["missed"] for v in model["counted"].values())
                tally = await page.evaluate("[...document.querySelectorAll('#card .tally .n')].map(e=>e.innerText)")
                R.add(name, test, f"[{mode}] round {model['round']} break tally", tally == [str(exp_got), str(exp_missed), str(n)], f"tally={tally} expected {[exp_got, exp_missed, n]}")
                await snap(page, name, f"{mode} roundbreak r{model['round']}")
                await mi_check_status(page, name, test, model, procs, f"roundbreak r{model['round']}")
                await page.keyboard.press(" ")
                s2 = await mi_state(page)
                R.add(name, test, f"[{mode}] Space at round break re-serves exactly the missed procedures",
                      s2["phase"] == "drill" and sorted(s2["queue"]) == sorted(model["owed"]) and s2["round"] == model["round"] + 1 and s2["idx"] == 0,
                      f"queue={s2['queue']} owed={model['owed']} round={s2['round']}")
                model["round"] += 1
                model["owed"] = []
                continue
            if s["phase"] == "done":
                ct = await card_text(page)
                fp = {k: v for k, v in model["counted"].items() if k[0] == 1}
                fp_got = sum(v["got"] for v in fp.values()); fp_missed = sum(v["missed"] for v in fp.values())
                fp_clean = sum(1 for v in fp.values() if v["missed"] == 0)
                acc = round(fp_got / (fp_got + fp_missed) * 100) if (fp_got + fp_missed) else 0
                # python round() is banker's; JS Math.round rounds .5 up
                accjs = int((fp_got / (fp_got + fp_missed) * 100) + 0.5) if (fp_got + fp_missed) else 0
                served = {pid for (rnd, pid) in model["counted"]}
                never = [pid for pid in served if pid not in model["ever"]]
                tally = await page.evaluate("[...document.querySelectorAll('#card .tally .n')].map(e=>e.innerText)")
                exp = [f"{fp_clean}/{len(fp)}", f"{fp_got}/{fp_got + fp_missed}", f"{accjs}%", str(len(model["ever"])), str(len(never))]
                R.add(name, test, f"[{mode}] done card tally", tally == exp, f"tally={tally} expected={exp}",
                      f"Complete a {mode} session; the closing card tally.")
                m = re.search(r"Session closed after (\d+) rounds?", ct)
                R.add(name, test, f"[{mode}] done card round count", bool(m) and int(m.group(1)) == model["round"], m.group(0) if m else ct[:100])
                R.add(name, test, f"[{mode}] done card lists every missed procedure once",
                      all(ct.count(by_pid[pid]["title"]) >= 1 for pid in model["ever"]), f"ever={sorted(model['ever'])}")
                board = await page.evaluate("[...document.querySelectorAll('#boardBody tr')].map(tr => [...tr.querySelectorAll('td')].map(td => td.innerText))")
                bm = sum(1 for r in board if "missed at least once" in r[3].lower()); bn = sum(1 for r in board if "never missed" in r[3].lower())
                R.add(name, test, f"[{mode}] scoreboard never/missed split", bm == len(model["ever"]) and bn == len(never) and bm + bn == 10, f"board missed={bm} never={bn}")
                await snap(page, name, f"{mode} done")
                await mi_check_status(page, name, test, model, procs, "done")
                break
            # ---------------- drill ----------------
            p = by_pid[s["pid"]]
            step = f"{mode} r{s['round']} proc {s['idx'] + 1}/{len(s['queue'])} ({p['name']})"
            if s["round"] == 1:
                served_pids_r1.append(s["pid"])
            await mi_check_status(page, name, test, model, procs, step + " before reveal")
            ct = await card_text(page)
            if mode == "a2p":
                # E: boxed block shown, title hidden, before reveal
                rows = await page.evaluate("[...document.querySelectorAll('#card .mrow .mline')].map(e=>e.innerText.trim())")
                exp_rows = [p["actions"][i] for i in p["gradable"]]
                norm_rows = [re.sub(r"\s+", " ", r.replace("\n", " ")) for r in rows]
                exp_norm = [re.sub(r"\s+", " ", r.replace(" ... ", " ")) for r in exp_rows]
                R.add(name, "E", f"boxed block shown before reveal ({p['name']})",
                      len(rows) == p["n"] and all(a == b for a, b in zip(norm_rows, exp_norm)) and await page.evaluate("document.querySelectorAll('#card .mbox').length") > 0,
                      f"rows={rows[:4]} expected={exp_rows[:4]}", f"Actions -> procedure, {p['name']} before reveal.")
                no_title_el = await page.evaluate("!document.querySelector('#card .prompt') && !document.querySelector('#card .answer-value')")
                R.add(name, "E", f"title hidden before reveal ({p['name']})", p["title"] not in ct and no_title_el,
                      f"[MEM] title in card text? {p['title'] in ct}; title element present? {not no_title_el}", f"Actions -> procedure, {p['name']} before reveal; card text.")
                if p["name"] in ct:
                    R.add(name, "E", f"procedure name appears in its own boxed lines ({p['name']}), data-inherent, informational", True,
                          f"a boxed line contains the text {p['name']!r}; the FCOM prints it that way, so actions -> procedure gives this one away")
                if p["headers"]:
                    R.add(name, "E", f"condition header withheld before reveal ({p['name']})",
                          "condition withheld" in ct and not any(h in ct for h in p["headers"]), f"headers={p['headers']}")
                R.add(name, "E", f"answer box focused before reveal ({p['name']})", s["boxFocused"], s["boxFocused"])
                await mi_reveal(page, "enter" if s["idx"] % 2 == 0 else "space")
                s = await mi_state(page)
                ct = await card_text(page)
                R.add(name, "E", f"revealed ({p['name']})", s["revealed"], s)
                R.add(name, "E", f"title appears after reveal ({p['name']})", p["title"] in ct and "Trigger, as printed" in ct, ct[:200])
                if p["headers"]:
                    R.add(name, "E", f"headers shown after reveal ({p['name']})", all(h in ct for h in p["headers"]), p["headers"])
                else:
                    R.add(name, "E", f"no-header note after reveal ({p['name']})", "No condition header is printed" in ct, ct[:300])
                await snap(page, name, step + " revealed")
                await page.keyboard.press("v")
                cite = await page.evaluate("document.querySelector('#card .cite') ? document.querySelector('#card .cite').innerText : ''")
                R.add(name, "E", f"V shows source ({p['name']})", "ident" in cite and "page" in cite, cite[:160])
                await snap(page, name, step + " revealed+V", overflow=True)
                await page.keyboard.press("v")
                g = alt_grade(counter) if s["round"] == 1 else ("got" if s["idx"] % 2 == 0 or s["round"] >= 3 else "missed")
                await page.keyboard.press("1" if g == "got" else "2")
                model["counted"][(s["round"], p["pid"])] = {"got": 1 if g == "got" else 0, "missed": 0 if g == "got" else 1}
                if g == "missed":
                    model["owed"].append(p["pid"]); model["ever"].add(p["pid"])
                s3 = await mi_state(page)
                ct = await card_text(page)
                R.add(name, test, f"[{mode}] after grading, next prompt shown ({p['name']})",
                      ("Clean" in ct if g == "got" else "comes back at the end of the round" in ct) and "Next procedure" in ct, ct[-200:])
                await mi_check_status(page, name, test, model, procs, step + " graded")
                await snap(page, name, step + " graded")
                await page.keyboard.press(" ")
                continue
            if mode == "whole":
                # skeleton: no boxed line text leaks
                nlines = await page.evaluate("document.querySelectorAll('#card .mline, #card .mrow').length")
                R.add(name, test, f"[whole] no line leaks before reveal ({p['name']})", nlines == 0 and "Structure given" in ct, f"rendered lines before reveal={nlines}")
                sk = await page.evaluate("[...document.querySelectorAll('#card .mbox.skeleton')].map(e=>e.innerText)")
                R.add(name, test, f"[whole] skeleton box count line total ({p['name']})",
                      sum(int(re.match(r"(\d+)", x).group(1)) for x in sk) == p["n"], f"skeleton={sk} n={p['n']}")
                R.add(name, test, f"[whole] answer box focused before reveal ({p['name']})", s["boxFocused"], s["boxFocused"])
                pre = await page.evaluate("document.getElementById('answerBox').value")
                if pre:
                    prefilled.append((s["round"], p["name"], 0, pre[:50]))
                    await page.fill("#answerBox", "")
                # typing something so typed-match marks render on some procedures
                if s["idx"] % 3 == 0:
                    await page.focus("#answerBox")
                    await page.keyboard.type(p["actions"][p["gradable"][0]])
                    await page.keyboard.press("Enter")
                    s_mid = await mi_state(page)
                    R.add(name, test, f"[whole] Enter on a non-empty line does not reveal ({p['name']})", not s_mid["revealed"], s_mid["revealed"])
                await mi_reveal(page, "enter" if s["idx"] % 2 == 0 else "space")
                s = await mi_state(page)
                R.add(name, test, f"[whole] revealed ({p['name']})", s["revealed"], s)
                rows = await page.evaluate("[...document.querySelectorAll('#card .mrow[data-slot] .mline')].map(e=>e.innerText.trim())")
                exp_rows = [p["actions"][i] for i in p["gradable"]]
                norm_rows = [re.sub(r"\s+", " ", r.replace("\n", " ")) for r in rows]
                exp_norm = [re.sub(r"\s+", " ", r.replace(" ... ", " ")) for r in exp_rows]
                R.add(name, test, f"[whole] all boxed lines rendered in order, none empty ({p['name']})",
                      norm_rows == exp_norm and all(r for r in rows), f"rows={rows} expected={exp_rows}",
                      f"Whole-procedure mode, reveal {p['name']}, read the .mrow .mline texts.")
                empties = await page.evaluate("[...document.querySelectorAll('#card .mline')].filter(e=>!e.innerText.trim()).length")
                R.add(name, test, f"[whole] no empty action lines ({p['name']})", empties == 0, f"empty .mline={empties}")
                if p["unboxed"]:
                    R.add(name, test, f"[whole] unboxed note rendered ({p['name']})", "Printed unboxed" in await card_text(page), "")
                await snap(page, name, step + " revealed")
                await page.keyboard.press("v")
                cite = await page.evaluate("document.querySelector('#card .cite').innerText")
                R.add(name, test, f"[whole] V shows source ({p['name']})", "ident" in cite and "page" in cite, cite[:160])
                await snap(page, name, step + " revealed+V")
                await page.keyboard.press("v")
                hidden = await page.evaluate("!document.querySelector('#card .cite ul')")
                R.add(name, test, f"[whole] V hides source ({p['name']})", hidden, f"cite ul present={not hidden}")
                got = missed = 0
                for li in range(p["n"]):
                    s_l = await mi_state(page)
                    R.add(name, test, f"[whole] cursor on slot {li} ({p['name']})", s_l["cursor"] == li, s_l["cursor"]) if s_l["cursor"] != li else None
                    g = alt_grade(counter) if s["round"] == 1 else ("got" if (s["idx"] % 2 == 0 or s["round"] >= 3) else "missed")
                    await page.keyboard.press("1" if g == "got" else "2")
                    if g == "got": got += 1
                    else: missed += 1
                    marks = await page.evaluate("[...document.querySelectorAll('#card .mrow[data-slot] .gmark')].map(e=>e.textContent.trim().toLowerCase())")
                    R.add(name, test, f"[whole] gutter mark after grading slot {li} ({p['name']})", marks[li] == g, f"marks={marks}") if marks[li] != g else None
                model["counted"][(s["round"], p["pid"])] = {"got": got, "missed": missed}
                if missed:
                    model["owed"].append(p["pid"]); model["ever"].add(p["pid"])
                ct = await card_text(page)
                exp_msg = "Clean. Every line as printed." if missed == 0 else (f"{missed} line missed." if missed == 1 else f"{missed} lines missed.")
                R.add(name, test, f"[whole] procedure verdict ({p['name']})", exp_msg in ct and "Next procedure" in ct, f"want {exp_msg!r} in {ct[-260:]!r}")
                await mi_check_status(page, name, test, model, procs, step + " graded")
                await snap(page, name, step + " graded")
                # pressing 1 again after all graded must not change counts
                before = await page.evaluate("JSON.stringify(S.counts)")
                await page.keyboard.press("1")
                after = await page.evaluate("JSON.stringify(S.counts)")
                R.add(name, "H", f"1 after all lines graded is ignored ({p['name']})", before == after, f"{before} -> {after}")
                await page.keyboard.press(" ")
                continue
            if mode == "line":
                got = missed = 0
                for li in range(p["n"]):
                    s_l = await mi_state(page)
                    ct = await card_text(page)
                    R.add(name, "D", f"line {li + 1} prompt ({p['name']})", f"Line {li + 1} of {p['n']}" in ct and s_l["line"] == li and not s_l["revealed"], f"line={s_l['line']} revealed={s_l['revealed']} ct={ct[:120]!r}")
                    rows = await page.evaluate("[...document.querySelectorAll('#card .mrow[data-slot] .mline')].map(e=>e.innerText.trim())")
                    exp_rows = [p["actions"][i] for i in p["gradable"][:li]]
                    norm_rows = [re.sub(r"\s+", " ", r.replace("\n", " ")) for r in rows]
                    exp_norm = [re.sub(r"\s+", " ", r.replace(" ... ", " ")) for r in exp_rows]
                    R.add(name, "D", f"previously revealed lines stay visible and in order before line {li + 1} ({p['name']})",
                          norm_rows == exp_norm, f"rows={rows} expected={exp_rows}",
                          f"Line-by-line, {p['name']}, before revealing line {li + 1}.")
                    nxt = p["actions"][p["gradable"][li]]
                    R.add(name, "D", f"line {li + 1} not leaked before reveal ({p['name']})", len(rows) == li and await page.evaluate("document.querySelectorAll('#card .hidden-line').length") == (1 if li < p['n'] else 0), f"rows={len(rows)}")
                    R.add(name, "D", f"answer box focused before line {li + 1} ({p['name']})", s_l["boxFocused"], s_l["boxFocused"]) if not s_l["boxFocused"] else None
                    pre = await page.evaluate("document.getElementById('answerBox').value")
                    if pre:
                        prefilled.append((s["round"], p["name"], li, pre[:50]))
                        await page.fill("#answerBox", "")
                    if li % 2 == 0:
                        await page.focus("#answerBox")
                        await page.keyboard.type(nxt)
                        await page.keyboard.press("Enter")
                    else:
                        await mi_reveal(page, "space")
                    s_r = await mi_state(page)
                    ct = await card_text(page)
                    R.add(name, "D", f"line {li + 1} revealed ({p['name']})", s_r["revealed"] and s_r["line"] == li, s_r)
                    rows = await page.evaluate("[...document.querySelectorAll('#card .mrow[data-slot] .mline')].map(e=>e.innerText.trim())")
                    exp_rows = [p["actions"][i] for i in p["gradable"][:li + 1]]
                    norm_rows = [re.sub(r"\s+", " ", r.replace("\n", " ")) for r in rows]
                    exp_norm = [re.sub(r"\s+", " ", r.replace(" ... ", " ")) for r in exp_rows]
                    R.add(name, "D", f"lines 1..{li + 1} visible in order after reveal ({p['name']})", norm_rows == exp_norm and all(rows),
                          f"rows={rows} expected={exp_rows}", f"Line-by-line, {p['name']}, reveal line {li + 1}.")
                    if li % 2 == 0:
                        R.add(name, "D", f"typed-match mark for typed line {li + 1} ({p['name']})", "typed: match" in ct, ct[-300:])
                    if li == 0:
                        await page.keyboard.press("v")
                        cite = await page.evaluate("document.querySelector('#card .cite').innerText")
                        R.add(name, "D", f"V shows source in line mode ({p['name']})", "ident" in cite, cite[:120])
                        await snap(page, name, step + f" line {li + 1} revealed+V")
                        await page.keyboard.press("v")
                    g = alt_grade(counter) if s["round"] == 1 else ("got" if (s["idx"] % 2 == 0 or s["round"] >= 3) else "missed")
                    await page.keyboard.press("1" if g == "got" else "2")
                    if g == "got": got += 1
                    else: missed += 1
                    marks = await page.evaluate("[...document.querySelectorAll('#card .mrow[data-slot] .gmark')].map(e=>e.textContent.trim().toLowerCase())")
                    R.add(name, "D", f"grade mark on line {li + 1} ({p['name']})", len(marks) > li and marks[li] == g, f"marks={marks}")
                    await snap(page, name, step + f" line {li + 1} graded")
                s_e = await mi_state(page)
                ct = await card_text(page)
                model["counted"][(s["round"], p["pid"])] = {"got": got, "missed": missed}
                if missed:
                    model["owed"].append(p["pid"]); model["ever"].add(p["pid"])
                exp_msg = "Clean. Every line as printed." if missed == 0 else (f"{missed} line missed." if missed == 1 else f"{missed} lines missed.")
                R.add(name, "D", f"all lines graded verdict ({p['name']})", "All lines graded" in ct and exp_msg in ct and "Next procedure" in ct, f"want {exp_msg!r}; ct={ct[-260:]!r}")
                rows = await page.evaluate("[...document.querySelectorAll('#card .mrow[data-slot] .mline')].map(e=>e.innerText.trim())")
                R.add(name, "D", f"all {p['n']} lines visible when finished ({p['name']})", len(rows) == p["n"], len(rows))
                await mi_check_status(page, name, test, model, procs, step + " graded")
                # 1 after finished must not grade
                before = await page.evaluate("JSON.stringify(S.counts)")
                await page.keyboard.press("1")
                after = await page.evaluate("JSON.stringify(S.counts)")
                R.add(name, "H", f"1 after all lines graded is ignored, line mode ({p['name']})", before == after, f"{before} -> {after}")
                await page.keyboard.press(" ")
                continue
        R.add(name, test, f"[{mode}] re-served procedures start with an empty answer box", not prefilled,
              f"{len(prefilled)} re-served cards were pre-filled with earlier typing, e.g. {prefilled[:4]} (S.typed is not cleared in startNextRound)",
              f"{mode} mode: type a line on any procedure in round 1, grade a line 'missed', press Space at the round break: the re-served card's answer box already holds the round-1 text.", "major")
        R.add(name, test, f"[{mode}] round 1 served every procedure exactly once", sorted(served_pids_r1) == sorted(by_pid), served_pids_r1)
        R.add(name, test, f"[{mode}] zero console/page errors over the full session", not errors, errors[:5] or "none",
              f"Run a full {mode} session in {PAGES[name]} with the console open.")
    except Exception as e:
        R.error(name, test, f"[{mode}] full session", e, f"Drive a full {mode} session in {PAGES[name]}.")
    finally:
        await ctx.close()


# ----------------------------------------------------------------------------
# memory-items: reference tab (G) and keyboard edge cases (H)
# ----------------------------------------------------------------------------
async def mi_reference(browser, name):
    ctx, page, errors = await new_page(browser, name)
    try:
        procs = await page.evaluate("PROCS.map(p => ({pid:p.pid, title:p.title, n:p.gradable.length, srcs:p.sources.length}))")
        before = await mi_state(page)
        await page.click("#tabRef")
        vis = await page.evaluate("[!document.getElementById('refPane').hidden, document.getElementById('drillPane').hidden]")
        R.add(name, "G", "reference pane shown, drill hidden", vis == [True, True], vis)
        titles = await page.evaluate("[...document.querySelectorAll('#refList .refcard h3')].map(e=>e.innerText)")
        R.add(name, "G", "every procedure appears exactly once", sorted(titles) == sorted(p["title"] for p in procs) and len(titles) == len(set(titles)) == 10, titles)
        counts = await page.evaluate("[...document.querySelectorAll('#refList .refcard')].map(c => ({t: c.querySelector('h3').innerText, lines: c.querySelectorAll('.mrow .mline').length, cites: c.querySelectorAll('.cite li').length, empty: [...c.querySelectorAll('.mline')].filter(e=>!e.innerText.trim()).length}))")
        by_t = {p["title"]: p for p in procs}
        bad = [c for c in counts if c["lines"] != by_t[c["t"]]["n"] or c["cites"] != by_t[c["t"]]["srcs"] or c["empty"]]
        R.add(name, "G", "each reference card lists all lines and all citations", not bad, bad or counts)
        R.add(name, "G", "reference lists 11 citations in total", sum(c["cites"] for c in counts) == 11, sum(c["cites"] for c in counts))
        rc = await page.evaluate("document.getElementById('refCount').innerText")
        R.add(name, "G", "reference count line", "10 procedures, 11 source entries" in rc, rc)
        # search / sort / expand: not features of this page
        has = await page.evaluate("[!!document.querySelector('#refPane input[type=search]'), !!document.querySelector('#refPane [data-sort]'), document.querySelectorAll('#refPane .vbtn').length]")
        R.add(name, "G", "search/sort/expand controls (page has none; source text is shown inline)", True, f"search={has[0]} sort={has[1]} vbtns={has[2]}; N/A by design: citations are printed inline")
        await snap(page, name, "reference tab")
        # keys are inert in reference mode
        await page.keyboard.press("r"); await page.keyboard.press(" "); await page.keyboard.press("1")
        after = await mi_state(page)
        R.add(name, "G", "keys inert on the reference tab", after["queue"] == before["queue"] and after["idx"] == before["idx"], f"{before['queue'][:3]} -> {after['queue'][:3]}")
        await page.click("#tabDrill")
        vis = await page.evaluate("[document.getElementById('refPane').hidden, !document.getElementById('drillPane').hidden]")
        R.add(name, "G", "back to drill tab", vis == [True, True], vis)
        # narrow viewport reference overflow
        await page.set_viewport_size({"width": 360, "height": 780})
        await page.click("#tabRef")
        await snap(page, name, "reference tab @360")
        R.add(name, "G", "zero errors on reference tab", not errors, errors or "none")
    except Exception as e:
        R.error(name, "G", "reference tab", e)
    finally:
        await ctx.close()


async def mi_keyboard(browser, name):
    ctx, page, errors = await new_page(browser, name, (390, 844))
    try:
        # 1 / 2 before reveal, box focused (default) and blurred
        s0 = await mi_state(page)
        await page.keyboard.press("1"); await page.keyboard.press("2")
        s1 = await mi_state(page)
        v = await page.evaluate("document.getElementById('answerBox').value")
        R.add(name, "H", "1/2 before reveal with the box focused: typed, not graded", s1["counts"] == {"got": 0, "missed": 0} and v == "12" and not s1["revealed"], f"counts={s1['counts']} box={v!r}",
              "Load memory-items.html, press 1 then 2 without revealing.")
        await page.evaluate("document.getElementById('answerBox').value=''; S.typed={}; document.activeElement.blur()")
        await page.keyboard.press("1"); await page.keyboard.press("2")
        s2 = await mi_state(page)
        grades = await page.evaluate("JSON.stringify(S.grades)")
        R.add(name, "H", "1/2 before reveal with the box blurred: not graded", s2["counts"] == {"got": 0, "missed": 0} and grades in ("{}", '{"%s":[]}' % s2["pid"]) and not s2["revealed"], f"counts={s2['counts']} grades={grades}",
              "Load memory-items.html, click outside the box, press 1 then 2 without revealing.")
        # Space while textarea focused: types a space, no reveal, no scroll
        await page.focus("#answerBox")
        await page.evaluate("document.getElementById('answerBox').scrollIntoView({block:'center'})")
        await page.wait_for_timeout(50)
        sy0 = await page.evaluate("window.scrollY")
        await page.keyboard.press(" ")
        await page.wait_for_timeout(100)
        sy1 = await page.evaluate("window.scrollY")
        v = await page.evaluate("document.getElementById('answerBox').value")
        s3 = await mi_state(page)
        R.add(name, "H", "Space in the focused textarea types a space, no reveal, no scroll", v == " " and not s3["revealed"] and sy0 == sy1 and sy0 > 0,
              f"value={v!r} revealed={s3['revealed']} scrollY {sy0}->{sy1}",
              "At 390px wide, scroll so the answer box is mid-screen, focus it, press Space.")
        # Space with box blurred and page scrolled: reveals and does not scroll (preventDefault)
        await page.evaluate("document.activeElement.blur()")
        sy0 = await page.evaluate("window.scrollY")
        await page.keyboard.press(" ")
        await page.wait_for_timeout(100)
        sy1 = await page.evaluate("window.scrollY")
        s4 = await mi_state(page)
        R.add(name, "H", "Space with the box blurred reveals and does not page-scroll", s4["revealed"] and sy0 == sy1, f"revealed={s4['revealed']} scrollY {sy0}->{sy1}", severity="minor")
        # grade a couple then R
        await page.keyboard.press("1")
        g0 = await page.evaluate("(S.grades[current().pid] || [])[0]")
        R.add(name, "H", "1 after reveal grades the first slot", g0 == "got", f"slot 0 grade={g0}")
        await key(page, "r")
        s6 = await mi_state(page)
        st = await status(page)
        R.add(name, "H", "R restarts and resets counters", s6["counts"] == {"got": 0, "missed": 0} and s6["idx"] == 0 and s6["round"] == 1 and not s6["revealed"] and st.get("item") == (1, 10) and st.get("got") == 0 and st.get("missed") == 0 and st.get("owed") == 0,
              f"state={ {k: s6[k] for k in ('counts', 'idx', 'round', 'revealed')} } status={st}", "Reveal, press 1, then press R with the box blurred.")
        R.add(name, "H", "R with the box focused types r (documented behaviour)", True, "not asserted, informational")
        # arrows while the answer box holds focus (the default state of every card)
        await page.focus("#answerBox")
        idx_a = (await mi_state(page))["idx"]
        await page.keyboard.press("ArrowRight")
        idx_b = (await mi_state(page))["idx"]
        R.add(name, "H", "ArrowRight navigates while the answer box has focus (default focus state of every card; Skip button advertises the arrow key)", idx_b == idx_a + 1,
              f"idx {idx_a} -> {idx_b}; the keydown handler returns early for textarea targets, so the arrow moves the caret instead",
              "Load the page (the answer box is focused automatically), press the right arrow: nothing happens. Click outside the box first and it skips.", "minor")
        await page.keyboard.press("r")  # typed into the box, must not restart
        R.add(name, "H", "R while typing in the box does not restart", (await mi_state(page))["idx"] == idx_b, "", severity="minor")
        await page.evaluate("document.getElementById('answerBox').value=''; S.typed={}")
        await key(page, "r")
        # arrows at the ends
        await key(page, "ArrowLeft")
        s7 = await mi_state(page)
        R.add(name, "H", "ArrowLeft at the first procedure does nothing and does not throw", s7["idx"] == 0 and not errors, f"idx={s7['idx']} errors={errors}")
        for _ in range(9):
            await key(page, "ArrowRight")
        s8 = await mi_state(page)
        R.add(name, "H", "ArrowRight x9 reaches the last procedure", s8["idx"] == 9 and s8["phase"] == "drill", f"idx={s8['idx']} phase={s8['phase']}")
        await key(page, "ArrowRight")
        s9 = await mi_state(page)
        R.add(name, "H", "ArrowRight at the last procedure ends the pass (nothing graded -> done)", s9["phase"] == "done" and not errors, f"phase={s9['phase']} errors={errors}")
        ct = await card_text(page)
        R.add(name, "H", "done card after skipping everything is coherent", "Session closed after 1 round" in ct and "0/0" in ct and "0%" in ct, ct[:300], severity="minor")
        await snap(page, name, "done after skipping all")
        await key(page, "ArrowRight"); await key(page, "ArrowLeft"); await key(page, "1"); await key(page, "2"); await key(page, "v")
        s10 = await mi_state(page)
        R.add(name, "H", "keys in the done phase do not throw or change state", s10["phase"] == "done" and s10["counts"] == {"got": 0, "missed": 0} and not errors, f"{s10['phase']} {s10['counts']} {errors}")
        await key(page, " ")
        s11 = await mi_state(page)
        R.add(name, "H", "Space in the done phase restarts", s11["phase"] == "drill" and s11["idx"] == 0, s11["phase"])
        # ArrowLeft after grading: previous procedure re-opened, counts unbooked
        await page.evaluate("document.activeElement && document.activeElement.blur()")
        await key(page, " ")
        n = (await mi_state(page))["n"]
        for _ in range(n):
            await key(page, "2")
        s12 = await mi_state(page)
        await key(page, " ")
        await page.evaluate("document.activeElement && document.activeElement.blur()")
        await key(page, "ArrowLeft")
        s13 = await mi_state(page)
        st = await status(page)
        R.add(name, "H", "ArrowLeft back onto a graded procedure un-books it (counters consistent)",
              s12["counts"]["missed"] == n and s13["idx"] == 0 and s13["counts"] == {"got": 0, "missed": 0} and s13["owed"] == [] and st.get("missed") == 0 and st.get("owed") == 0 and not s13["revealed"],
              f"after grading {s12['counts']} owed={s12['owed']}; after ArrowLeft {s13['counts']} owed={s13['owed']} status={st}",
              "Reveal, grade every line 2, Space, then ArrowLeft.")
        # ArrowRight mid-procedure (skip after partial grading), on a procedure with at least two lines
        while (await mi_state(page))["n"] < 2:
            await key(page, "ArrowRight")
        idx0 = (await mi_state(page))["idx"]
        await key(page, " ")
        await key(page, "2")
        await key(page, "ArrowRight")
        s14 = await mi_state(page)
        st = await status(page)
        R.add(name, "H", "skip after a partial grade: nothing booked, no owed", s14["idx"] == idx0 + 1 and s14["counts"] == {"got": 0, "missed": 0} and st.get("owed") == 0 and not errors,
              f"{s14['counts']} owed={s14['owed']} status={st} errors={errors}", "Reveal, press 2 once, then ArrowRight.", severity="minor")
        # filter chips: None -> empty phase; All -> back
        await page.click("#noProc")
        s15 = await mi_state(page)
        ct = await card_text(page)
        R.add(name, "H", "None filter gives the empty card", s15["phase"] == "empty" and "No procedures selected" in ct, s15["phase"])
        await snap(page, name, "empty pool")
        await key(page, " "); await key(page, "1"); await key(page, "ArrowRight")
        R.add(name, "H", "keys on the empty card do not throw", not errors, errors)
        await page.click("#allProc")
        s16 = await mi_state(page)
        R.add(name, "H", "All filter restores 10", len(s16["queue"]) == 10 and s16["phase"] == "drill", len(s16["queue"]))
        # single chip toggle -> pool 9
        await page.click("#procChips .chip >> nth=0")
        s17 = await mi_state(page)
        st = await status(page)
        R.add(name, "H", "toggling one chip reduces the pool to 9", len(s17["queue"]) == 9 and st.get("pool") == (9, 10), f"queue={len(s17['queue'])} status={st}")
        board = await page.evaluate("[...document.querySelectorAll('#boardBody tr')].filter(tr => tr.textContent.toLowerCase().includes('filtered out')).length")
        R.add(name, "H", "scoreboard shows the filtered procedure", board == 1, board, severity="minor")
        await snap(page, name, "one chip off")
        # Ctrl+Enter reveals from anywhere
        await page.click("#allProc")
        await page.focus("#answerBox")
        await page.keyboard.type("abc")
        await page.keyboard.press("Control+Enter")
        s18 = await mi_state(page)
        R.add(name, "H", "Ctrl+Enter reveals from the box", s18["revealed"], s18["revealed"], severity="minor")
        R.add(name, "H", "zero errors during keyboard edge cases", not errors, errors or "none")
    except Exception as e:
        R.error(name, "H", "keyboard edge cases", e)
    finally:
        await ctx.close()


# ----------------------------------------------------------------------------
# limitations drivers
# ----------------------------------------------------------------------------
LI_STATE = """({phase:S.phase, idx:S.idx, round:S.round, revealed:S.revealed, counts:S.counts, queue:S.queue.map(i=>i.id),
  owed:S.missedThisRound.slice(), id: current() && current().id, direction:S.direction, missedEver:Object.keys(S.missedEver),
  boxFocused: !!(document.activeElement && document.activeElement.id === 'answerBox'), includeUnclear:S.includeUnclear})"""


async def li_state(page):
    return await page.evaluate(LI_STATE)


async def li_full_session(browser, name, direction, viewport=(1280, 900), show_source=False):
    ctx, page, errors = await new_page(browser, name, viewport)
    test = "F"
    tag = f"{direction} @{viewport[0]}"
    try:
        items = await page.evaluate("LIMITATIONS.map(i => ({id:i.id, parameter:i.parameter, limit:i.limit, condition:i.condition||'', system:i.system, confidence:i.confidence, ref:i.ref, verbatim:i.verbatim, source_book:i.source_book||null, note:i.note||null}))")
        by_id = {i["id"]: i for i in items}
        R.add(name, test, f"[{tag}] 160 items, ids unique", len(items) == 160 and len(by_id) == 160, len(items))
        if direction == "l2p":
            await page.click("#dirL2P")
        s = await li_state(page)
        R.add(name, test, f"[{tag}] direction set", s["direction"] == direction and len(s["queue"]) == 160 and s["idx"] == 0, s["direction"])
        model = {"got": 0, "missed": 0, "owed": [], "ever": set(), "round": 1, "fp_got": 0, "fp_missed": 0, "latest": {}}
        counter = [0]
        served_r1 = []
        reserve_pill, prefilled = [], []
        R.add(name, test, f"[{tag}] counter semantics note (informational)", True,
              "limitations counts the LATEST grade per item (S.graded persists across rounds, so a round-2 'got' moves an item from Missed to Got); memory-items counts cumulatively per served procedure. Modelled accordingly.")
        step_i = 0
        checked_source = 0
        while True:
            s = await li_state(page)
            step_i += 1
            if step_i > 800:
                R.add(name, test, f"[{tag}] session terminates", False, f"phase {s['phase']} after 800 steps", severity="blocker")
                break
            st = await status(page)
            if s["phase"] == "roundbreak":
                ct = await card_text(page)
                n = len(model["owed"])
                m = re.search(r"Round (\d+) closed, (\d+) items? still owed", ct)
                R.add(name, test, f"[{tag}] round {model['round']} break card owed count", bool(m) and int(m.group(1)) == model["round"] and int(m.group(2)) == n and sorted(s["owed"]) == sorted(model["owed"]),
                      f"{m.group(0) if m else ct[:100]!r} model owed={n}", f"Grade {n} items 'missed' in round {model['round']} ({direction}); round-break card.")
                tally = await page.evaluate("[...document.querySelectorAll('#card .tally .n')].map(e=>e.innerText)")
                R.add(name, test, f"[{tag}] round {model['round']} break tally", tally == [str(model["got"]), str(model["missed"]), str(n)], f"{tally} vs {[model['got'], model['missed'], n]}")
                ok = st.get("got") == model["got"] and st.get("missed") == model["missed"] and st.get("owed") == n and st.get("round") == model["round"]
                R.add(name, test, f"[{tag}] status at round {model['round']} break", ok, f"{st} model={model['got']}/{model['missed']}/{n}") if not ok else None
                lis = await page.evaluate("[...document.querySelectorAll('#card .misslist li')].length")
                R.add(name, test, f"[{tag}] round-break list has one entry per owed item", lis == n, f"{lis} vs {n}")
                await snap(page, name, f"{tag} roundbreak r{model['round']}")
                await page.keyboard.press(" ")
                s2 = await li_state(page)
                R.add(name, test, f"[{tag}] Space at round break re-serves exactly the missed items", s2["phase"] == "drill" and sorted(s2["queue"]) == sorted(model["owed"]) and s2["round"] == model["round"] + 1 and s2["idx"] == 0 and not s2["revealed"],
                      f"queue={len(s2['queue'])} owed={len(model['owed'])} round={s2['round']}")
                model["round"] += 1
                model["owed"] = []
                continue
            if s["phase"] == "done":
                ct = await card_text(page)
                fpt = model["fp_got"] + model["fp_missed"]
                accjs = int(model["fp_got"] / fpt * 100 + 0.5) if fpt else 0
                tally = await page.evaluate("[...document.querySelectorAll('#card .tally .n')].map(e=>e.innerText)")
                exp = [f"{model['fp_got']}/{fpt}", f"{accjs}%", str(len(model["ever"])), str(model["got"])]
                R.add(name, test, f"[{tag}] done card tally", tally == exp, f"{tally} vs {exp}", f"Complete a full {direction} session; closing card.")
                m = re.search(r"Session closed after (\d+) rounds?", ct)
                R.add(name, test, f"[{tag}] done card round count", bool(m) and int(m.group(1)) == model["round"], m.group(0) if m else ct[:80])
                lis = await page.evaluate("[...document.querySelectorAll('#card .misslist li')].length")
                R.add(name, test, f"[{tag}] done card lists every ever-missed item once", lis == len(model["ever"]), f"{lis} vs {len(model['ever'])}")
                ok = st.get("got") == model["got"] and st.get("missed") == model["missed"] and st.get("owed") == 0 and st.get("queue") is not None
                R.add(name, test, f"[{tag}] status at done", ok, st) if not ok else None
                await snap(page, name, f"{tag} done")
                break
            # ---------- drill ----------
            it = by_id[s["id"]]
            if s["round"] == 1:
                served_r1.append(s["id"])
            step = f"{tag} r{s['round']} item {s['idx'] + 1}/{len(s['queue'])} ({it['id']})"
            ok = (st.get("item") == (s["idx"] + 1, len(s["queue"])) and st.get("got") == model["got"] and st.get("missed") == model["missed"]
                  and st.get("owed") == len(model["owed"]) and st.get("round") == model["round"] and st.get("pool") == (160, 160))
            if not ok:
                R.add(name, test, f"[{tag}] status consistent at {step}", False, f"{st} vs model got={model['got']} missed={model['missed']} owed={len(model['owed'])} round={model['round']}",
                      f"Drive a {direction} session to {step}.")
            ct = await card_text(page)
            if s["round"] >= 2:
                if "Graded:" in ct:
                    reserve_pill.append(it["id"])
                pre = await page.evaluate("document.getElementById('answerBox').value")
                if pre:
                    prefilled.append((s["round"], it["id"], pre[:60]))
                    await page.fill("#answerBox", "")
            if direction == "p2l":
                R.add(name, test, f"[{tag}] prompt is the parameter, limit hidden ({it['id']})", it["parameter"] in ct and it["limit"] not in ct and not s["revealed"],
                      f"limit {it['limit']!r} in card: {it['limit'] in ct}", f"Parameter -> limit, item {it['id']} before reveal.") if not (it["parameter"] in ct and it["limit"] not in ct) else None
            else:
                if not (it["limit"] in ct and it["parameter"] not in ct):
                    where = await page.evaluate("(p) => [...document.querySelectorAll('#card *')].filter(e => e.textContent.includes(p) && ![...e.children].some(c => c.textContent.includes(p))).map(e => e.tagName + '.' + e.className + ': ' + e.textContent.slice(0, 160))", it["parameter"])
                    R.add(name, test, f"[{tag}] prompt is the limit, parameter hidden ({it['id']})", False,
                          f"parameter {it['parameter']!r} shown before reveal in: {where}", f"Limit -> parameter, item {it['id']} ({it['parameter']}) before reveal.", "minor")
            if it["confidence"] == "UNCLEAR":
                R.add(name, test, f"[{tag}] UNCLEAR item carries its warning ({it['id']})", "Unclear, mapping not provable" in ct and "UNCLEAR, do not commit" in ct, ct[:200]) if "UNCLEAR, do not commit" not in ct else None
            if not s["boxFocused"]:
                R.add(name, test, f"[{tag}] answer box focused before reveal ({it['id']})", False, s)
            # type a number for the number check on some items
            typed = None
            if s["idx"] % 4 == 0 and direction == "p2l":
                typed = it["limit"]
                await page.focus("#answerBox")
                await page.keyboard.type(typed)
            if s["idx"] % 2 == 0:
                await page.focus("#answerBox")
                await page.keyboard.press("Enter")
            else:
                await page.evaluate("document.activeElement && document.activeElement.blur()")
                await page.keyboard.press(" ")
            s = await li_state(page)
            ct = await card_text(page)
            if not s["revealed"]:
                R.add(name, test, f"[{tag}] reveal ({it['id']})", False, s, f"Item {it['id']}, press Enter in the box or Space with it blurred.")
            av = await page.evaluate("document.querySelector('#card .answer-value') ? document.querySelector('#card .answer-value').innerText : null")
            want = it["limit"] if direction == "p2l" else it["parameter"]
            if av != want:
                R.add(name, test, f"[{tag}] revealed answer matches data ({it['id']})", False, f"shown={av!r} want={want!r}")
            if direction == "l2p" and it["system"] not in ct:
                R.add(name, test, f"[{tag}] system shown after reveal ({it['id']})", False, ct[:200])
            cond_ok = (it["condition"] in ct) if it["condition"] else ("None stated in the source" in ct)
            if not cond_ok:
                R.add(name, test, f"[{tag}] condition shown after reveal ({it['id']})", False, f"cond={it['condition']!r}")
            if it["source_book"] and ("Different book" not in ct or it["source_book"] not in ct):
                R.add(name, test, f"[{tag}] off-book note shown ({it['id']})", False, ct[:300])
            if typed is not None:
                nc = await page.evaluate("document.querySelector('#numCheck') ? document.querySelector('#numCheck').innerText : ''")
                nums = await page.evaluate("numbersIn(current().limit).length")
                if nums and not re.search(rf"Numbers {nums} of {nums} present", nc):
                    R.add(name, test, f"[{tag}] number check passes when the exact limit is typed ({it['id']})", False, f"typed={typed!r} numcheck={nc!r}",
                          f"Parameter -> limit, item {it['id']}: type the limit verbatim, reveal.", "minor")
            if "ident" in ct and False:
                pass
            if it["ref"] not in ct:
                R.add(name, test, f"[{tag}] citation ref shown ({it['id']})", False, ct[-300:])
            # source text
            if show_source or s["idx"] % 5 == 0:
                await page.keyboard.press("v")
                pre = await page.evaluate("document.getElementById('vPre') ? document.getElementById('vPre').innerText : null")
                if pre is None or pre.strip() != it["verbatim"].strip():
                    R.add(name, test, f"[{tag}] V shows the verbatim source text ({it['id']})", False, f"pre={str(pre)[:100]!r}", f"Item {it['id']}, reveal, press V.")
                checked_source += 1
                await snap(page, name, step + " revealed+V")
                await page.keyboard.press("v")
                pre = await page.evaluate("!!document.getElementById('vPre')")
                if pre:
                    R.add(name, test, f"[{tag}] V hides the source text again ({it['id']})", False, "vPre still present")
            else:
                await snap(page, name, step + " revealed")
            g = alt_grade(counter)
            await page.keyboard.press("1" if g == "got" else "2")
            prevg = model["latest"].get(it["id"])
            if prevg != g:
                if prevg:
                    model[prevg] -= 1
                model[g] += 1
                model["latest"][it["id"]] = g
            if s["round"] == 1:
                model["fp_" + g] += 1
            if g == "missed":
                model["owed"].append(it["id"]); model["ever"].add(it["id"])
            s3 = await li_state(page)
            if s3["phase"] == "drill" and not (s3["idx"] == s["idx"] + 1 and not s3["revealed"]):
                R.add(name, test, f"[{tag}] grading auto-advances ({it['id']})", False, s3)
        R.add(name, test, f"[{tag}] re-served items do not show their previous grade before reveal", not reserve_pill,
              f"{len(reserve_pill)} re-served cards carried a 'Graded: missed' pill before reveal, e.g. {reserve_pill[:5]} (S.graded is not cleared in startNextRound)",
              "Miss any item in round 1, press Space at the round break: the re-served card shows a 'Graded: missed' pill above the question before you reveal.", "minor")
        R.add(name, test, f"[{tag}] re-served items start with an empty answer box", not prefilled,
              f"{len(prefilled)} re-served cards were pre-filled with the round-1 typing, e.g. {prefilled[:4]} (S.typed is not cleared in startNextRound)",
              "Type an answer on any item in round 1, grade it 'missed', press Space at the round break: the re-served card's answer box already contains what you typed in round 1.", "major")
        R.add(name, test, f"[{tag}] round 1 served each of the 160 items exactly once", sorted(served_r1) == sorted(by_id), f"{len(served_r1)} served, {len(set(served_r1))} unique")
        R.add(name, test, f"[{tag}] source text checked on {checked_source} items", checked_source > 0, checked_source)
        R.add(name, test, f"[{tag}] zero console/page errors over the full session", not errors, errors[:5] or "none")
    except Exception as e:
        R.error(name, test, f"[{tag}] full session", e)
    finally:
        await ctx.close()


async def li_filters(browser, name):
    ctx, page, errors = await new_page(browser, name)
    try:
        items = await page.evaluate("LIMITATIONS.map(i => ({id:i.id, system:i.system, confidence:i.confidence}))")
        NV = sum(1 for i in items if i["confidence"] != "UNCLEAR")   # VERIFIED count, from the data (139 on v2, 144 on v3)
        # UNCLEAR off
        await page.click("#incUnclear")
        s = await li_state(page)
        st = await status(page)
        R.add(name, "F", f"UNCLEAR off reduces the pool to {NV}", len(s["queue"]) == NV and st.get("pool") == (NV, 160) and st.get("item") == (1, NV), f"queue={len(s['queue'])} status={st}",
              "Untick 'Include UNCLEAR items'.")
        conf = {i["id"]: i["confidence"] for i in items}
        R.add(name, "F", "every queued item is VERIFIED with UNCLEAR off", all(conf[i] == "VERIFIED" for i in s["queue"]), sorted({conf[i] for i in s["queue"]}))
        # serve every one of them by keyboard and check the face of the card
        seen = []
        bad = []
        for k in range(NV):
            s = await li_state(page)
            ct = await card_text(page)
            seen.append(s["id"])
            if conf[s["id"]] != "VERIFIED" or "Unclear, mapping" in ct or "UNCLEAR, do not commit" in ct:
                bad.append(s["id"])
            await page.evaluate("document.activeElement && document.activeElement.blur()")
            if k % 10 == 0:
                await page.keyboard.press(" ")
                ct2 = await card_text(page)
                if "VERIFIED" not in ct2:
                    bad.append(s["id"] + ":no VERIFIED on cite")
                await snap(page, name, f"unclear-off item {k + 1} revealed")
            await page.keyboard.press("ArrowRight")
        R.add(name, "F", f"served all {NV} items with UNCLEAR off; every served item VERIFIED", len(set(seen)) == NV and not bad, f"unique={len(set(seen))} bad={bad}")
        s = await li_state(page)
        R.add(name, "F", f"ArrowRight past the last of {NV} ends the pass (done)", s["phase"] == "done" and not errors, f"{s['phase']} {errors}")
        await snap(page, name, "unclear-off done")
        # UNCLEAR back on
        await page.click("#incUnclear")
        s = await li_state(page)
        R.add(name, "F", "UNCLEAR on restores 160", len(s["queue"]) == 160 and s["phase"] == "drill", len(s["queue"]))
        # system chips
        chips = await page.evaluate("[...document.querySelectorAll('#sysChips .chip')].map(b => ({sys: b.getAttribute('data-sys'), label: b.innerText, n: b.querySelector('.n').innerText}))")
        R.add(name, "F", "17 system chips", len(chips) == 17, len(chips))
        from collections import Counter
        cnt = Counter(i["system"] for i in items)
        ucnt = Counter(i["system"] for i in items if i["confidence"] == "UNCLEAR")
        R.add(name, "F", "chip counts equal data counts", all(int(re.match(r"(\d+)", c["n"]).group(1)) == cnt[c["sys"]] for c in chips) and sum(cnt.values()) == 160, [(c["sys"], c["n"], cnt[c["sys"]]) for c in chips])
        R.add(name, "F", "chip UNCLEAR sub-count equals data", all((("/ %d?" % ucnt[c["sys"]]) in c["n"]) == (ucnt[c["sys"]] > 0) for c in chips), [(c["sys"], c["n"]) for c in chips if ucnt[c["sys"]]])
        # one chip off from all -> 160 - n
        c0 = chips[0]
        await page.click(f"#sysChips .chip[data-sys=\"{c0['sys']}\"]")
        s = await li_state(page); st = await status(page)
        R.add(name, "F", f"one chip off ({c0['sys']}) -> pool {160 - cnt[c0['sys']]}", len(s["queue"]) == 160 - cnt[c0["sys"]] and st.get("pool") == (160 - cnt[c0["sys"]], 160), f"{len(s['queue'])} {st}")
        R.add(name, "F", "chip aria-pressed reflects the toggle", await page.evaluate(f"document.querySelector('#sysChips .chip[data-sys=\"{c0['sys']}\"]').getAttribute('aria-pressed')") == "false", "")
        # None then each chip alone
        await page.click("#noSys")
        s = await li_state(page); ct = await card_text(page)
        R.add(name, "F", "None -> empty card", s["phase"] == "empty" and "No items selected" in ct, s["phase"])
        await snap(page, name, "no systems")
        await page.keyboard.press(" "); await page.keyboard.press("1"); await page.keyboard.press("ArrowRight"); await page.keyboard.press("v")
        R.add(name, "F", "keys on the empty card do not throw", not errors, errors)
        bad = []
        for c in chips:
            await page.click(f"#sysChips .chip[data-sys=\"{c['sys']}\"]")
            s = await li_state(page); st = await status(page)
            sysn = cnt[c["sys"]]
            if not (len(s["queue"]) == sysn and st.get("pool") == (sysn, 160) and all(next(i for i in items if i["id"] == q)["system"] == c["sys"] for q in s["queue"])):
                bad.append((c["sys"], len(s["queue"]), st.get("pool"), sysn))
            # with unclear off as well
            await page.click("#incUnclear")
            s2 = await li_state(page); st2 = await status(page)
            exp2 = sysn - ucnt[c["sys"]]
            if not (len(s2["queue"]) == exp2 and st2.get("pool") == (exp2, 160)) and not (exp2 == 0 and s2["phase"] == "empty"):
                bad.append((c["sys"] + " unclear-off", len(s2["queue"]), st2.get("pool"), exp2))
            if exp2 == 0 and s2["phase"] != "empty":
                bad.append((c["sys"] + " unclear-off should be empty", s2["phase"]))
            await page.click("#incUnclear")
            await page.click(f"#sysChips .chip[data-sys=\"{c['sys']}\"]")
        R.add(name, "F", "each system alone gives the chip's count (with and without UNCLEAR)", not bad, bad or "all 17 ok",
              "Click None, then one chip at a time; compare the status Pool to the chip count.")
        await page.click("#allSys")
        s = await li_state(page)
        R.add(name, "F", "All restores 160", len(s["queue"]) == 160, len(s["queue"]))
        R.add(name, "F", "zero errors during filter tests", not errors, errors or "none")
    except Exception as e:
        R.error(name, "F", "filters", e)
    finally:
        await ctx.close()


async def li_reference(browser, name):
    ctx, page, errors = await new_page(browser, name)
    try:
        items = await page.evaluate("LIMITATIONS.map(i => ({id:i.id, parameter:i.parameter, limit:i.limit, condition:i.condition||'', system:i.system, confidence:i.confidence, ref:i.ref, verbatim:i.verbatim}))")
        before = await li_state(page)
        await page.click("#tabRef")
        vis = await page.evaluate("[!document.getElementById('refPane').hidden, document.getElementById('drillPane').hidden]")
        R.add(name, "G", "reference pane shown, drill hidden", vis == [True, True], vis)
        ids = await page.evaluate("[...document.querySelectorAll('#refBody [data-vid]')].map(b => b.getAttribute('data-vid'))")
        R.add(name, "G", "every item appears exactly once", len(ids) == 160 and len(set(ids)) == 160 and set(ids) == {i["id"] for i in items}, f"{len(ids)} rows, {len(set(ids))} unique")
        rc = await page.evaluate("document.getElementById('rowCount').innerText")
        R.add(name, "G", "row count line", rc.startswith("160 of 160 items shown"), rc)
        rows = await page.evaluate("[...document.querySelectorAll('#refBody tr')].map(tr => [...tr.querySelectorAll('td')].map(td => td.innerText.trim()))")
        R.add(name, "G", "no empty cells in the reference table", all(len(r) == 4 and all(c for c in r) for r in rows), [r for r in rows if not all(r)][:3])
        # default sort: system then parameter
        order = await page.evaluate("[...document.querySelectorAll('#refBody tr')].map(tr => tr.querySelector('[data-vid]').getAttribute('data-vid'))")
        exp = await page.evaluate("LIMITATIONS.slice().sort((a,b) => (a.system+'|'+a.parameter).localeCompare(b.system+'|'+b.parameter, 'en', {numeric:true})).map(i=>i.id)")
        R.add(name, "G", "default sort is system then parameter", order == exp, f"first={order[:3]} exp={exp[:3]}")
        await snap(page, name, "reference tab")
        # search
        await page.fill("#search", "APU")
        n = await page.evaluate("document.querySelectorAll('#refBody tr').length")
        exp_n = sum(1 for i in items if "apu" in (i["parameter"] + " " + i["limit"] + " " + i["condition"] + " " + i["ref"] + " " + i["system"] + " " + i["verbatim"] + " " + i["id"]).lower())
        R.add(name, "G", "search 'APU' narrows", n == exp_n and 0 < n < 160, f"{n} rows, expected {exp_n}")
        rc = await page.evaluate("document.getElementById('rowCount').innerText")
        R.add(name, "G", "row count follows the search", rc.startswith(f"{n} of 160"), rc)
        await page.fill("#search", "zzzzqqq")
        n0 = await page.evaluate("document.querySelectorAll('#refBody tr').length")
        R.add(name, "G", "search with no hits shows zero rows", n0 == 0, n0)
        await snap(page, name, "reference search no hits")
        await page.fill("#search", "")
        n1 = await page.evaluate("document.querySelectorAll('#refBody tr').length")
        R.add(name, "G", "clearing the search restores 160", n1 == 160, n1)
        # '/' focuses the search
        await page.evaluate("document.activeElement && document.activeElement.blur()")
        await page.keyboard.press("/")
        R.add(name, "G", "/ focuses the search box", await page.evaluate("document.activeElement.id") == "search", await page.evaluate("document.activeElement.id"), severity="minor")
        await page.evaluate("document.activeElement.blur()")
        # sort by each column, both directions
        for key in ("limit", "parameter", "confidence", "system"):
            await page.click(f"thead [data-sort=\"{key}\"]")
            order = await page.evaluate("[...document.querySelectorAll('#refBody tr')].map(tr => tr.querySelector('[data-vid]').getAttribute('data-vid'))")
            cmp = {"limit": "a.limit.localeCompare(b.limit,'en',{numeric:true})", "parameter": "a.parameter.localeCompare(b.parameter,'en',{numeric:true})",
                   "confidence": "(a.confidence+a.system+a.parameter).localeCompare(b.confidence+b.system+b.parameter,'en',{numeric:true})",
                   "system": "(a.system+'|'+a.parameter).localeCompare(b.system+'|'+b.parameter,'en',{numeric:true})"}[key]
            # independent check: adjacent pairs are non-decreasing under the same collation
            mono = await page.evaluate("(order) => { const by = {}; LIMITATIONS.forEach(i => by[i.id] = i); let bad = 0; for (let k = 1; k < order.length; k++) { const a = by[order[k-1]], b = by[order[k]]; if ((%s) > 0) bad++; } return bad; }" % cmp, order)
            rc = await page.evaluate("document.getElementById('rowCount').innerText")
            R.add(name, "G", f"sort by {key} ascending", mono == 0 and len(order) == 160 and f"sorted by {key} ascending" in rc, f"out-of-order pairs={mono} rc={rc}", f"Reference tab, click the {key} header once.")
            await page.click(f"thead [data-sort=\"{key}\"]")
            order = await page.evaluate("[...document.querySelectorAll('#refBody tr')].map(tr => tr.querySelector('[data-vid]').getAttribute('data-vid'))")
            mono = await page.evaluate("(order) => { const by = {}; LIMITATIONS.forEach(i => by[i.id] = i); let bad = 0; for (let k = 1; k < order.length; k++) { const a = by[order[k-1]], b = by[order[k]]; if ((%s) < 0) bad++; } return bad; }" % cmp, order)
            rc = await page.evaluate("document.getElementById('rowCount').innerText")
            R.add(name, "G", f"sort by {key} descending", mono == 0 and f"sorted by {key} descending" in rc, f"out-of-order pairs={mono} rc={rc}")
        # expand one
        first = await page.evaluate("document.querySelector('#refBody [data-vid]').getAttribute('data-vid')")
        await page.click("#refBody [data-vid] >> nth=0")
        pre = await page.evaluate(f"(document.querySelector('#refBody [data-vpre=\"{first}\"]') || {{}}).innerText")
        want = next(i for i in items if i["id"] == first)["verbatim"]
        R.add(name, "G", "source text expands for one row", (pre or "").strip() == want.strip(), f"pre={str(pre)[:80]!r}")
        R.add(name, "G", "only one row expanded", await page.evaluate("document.querySelectorAll('#refBody [data-vpre]').length") == 1, "")
        await snap(page, name, "reference one source expanded")
        await page.click(f"#refBody [data-vid=\"{first}\"]")
        R.add(name, "G", "source text collapses again", await page.evaluate("document.querySelectorAll('#refBody [data-vpre]').length") == 0, "")
        # expand all
        await page.click("#expandAll")
        n = await page.evaluate("document.querySelectorAll('#refBody [data-vpre]').length")
        allok = await page.evaluate("[...document.querySelectorAll('#refBody [data-vpre]')].every(p => p.innerText.trim() === LIMITATIONS.find(i => i.id === p.getAttribute('data-vpre')).verbatim.trim())")
        R.add(name, "G", "Show all source text expands all 160 with the right text", n == 160 and allok and await page.evaluate("document.getElementById('expandAll').innerText") == "Hide all source text", f"{n} pres, texts ok={allok}")
        await snap(page, name, "reference all sources expanded")
        # collapse one while expanded-all: others stay open
        await page.click(f"#refBody [data-vid=\"{first}\"]")
        n = await page.evaluate("document.querySelectorAll('#refBody [data-vpre]').length")
        R.add(name, "G", "collapsing one row after expand-all leaves 159 open", n == 159, n, severity="minor")
        label = await page.evaluate("document.getElementById('expandAll').textContent")
        await page.click("#expandAll")
        n2 = await page.evaluate("document.querySelectorAll('#refBody [data-vpre]').length")
        label2 = await page.evaluate("document.getElementById('expandAll').textContent")
        R.add(name, "G", "expand-all button stays truthful after one row is collapsed (label + click hides the rest)", label == "Show all source text" or n2 == 0,
              f"label after collapsing one row={label!r} (159 still open); clicking it -> {n2} open, label {label2!r}",
              "Reference tab: click 'Show all source text', then click one row's 'Hide source text', then click the top button again: it re-opens the collapsed row instead of hiding all, and its label never changed.", "minor")
        if n2:
            await page.click("#expandAll")
        n = await page.evaluate("document.querySelectorAll('#refBody [data-vpre]').length")
        R.add(name, "G", "Hide all source text collapses all", n == 0, n, severity="minor")
        # unclear toggle on reference
        await page.click("#refUnclear")
        n = await page.evaluate("document.querySelectorAll('#refBody tr').length")
        NV = sum(1 for i in items if i["confidence"] != "UNCLEAR")
        R.add(name, "G", f"reference Show UNCLEAR off -> {NV} rows", n == NV, n)
        await page.click("#refUnclear")
        # reference chips
        await page.click("#refChips .chip >> nth=0")
        n = await page.evaluate("document.querySelectorAll('#refBody tr').length")
        sys0 = await page.evaluate("document.querySelector('#refChips .chip').getAttribute('data-sys')")
        exp_n = 160 - sum(1 for i in items if i["system"] == sys0)
        R.add(name, "G", f"reference chip toggle ({sys0}) filters rows", n == exp_n, f"{n} vs {exp_n}")
        await page.click("#refChips .chip >> nth=0")
        # keys inert on reference tab
        await page.keyboard.press("r"); await page.keyboard.press(" "); await page.keyboard.press("1")
        after = await li_state(page)
        R.add(name, "G", "keys inert on the reference tab", after["queue"] == before["queue"] and after["idx"] == before["idx"] and not after["revealed"], "")
        # reference at phone width
        await page.set_viewport_size({"width": 360, "height": 780})
        await page.wait_for_timeout(100)
        await snap(page, name, "reference tab @360")
        await page.click("#expandAll")
        R.add(name, "G", "expand-all state reached @360", await page.evaluate("document.querySelectorAll('#refBody [data-vpre]').length") == 160, "")
        await snap(page, name, "reference all sources expanded @360")
        await page.click("#expandAll")
        await page.click("#refBody [data-vid] >> nth=0")
        await snap(page, name, "reference one source expanded @360 (" + first + ")")
        # single-row expansion of the item with the longest dot-leader run
        await page.fill("#search", "lim-afs-24")
        await page.click("#refBody [data-vid] >> nth=0")
        await snap(page, name, "reference single row lim-afs-24 expanded @360")
        await page.fill("#search", "")
        await page.click("#tabDrill")
        vis = await page.evaluate("[document.getElementById('refPane').hidden, !document.getElementById('drillPane').hidden]")
        R.add(name, "G", "back to drill tab", vis == [True, True], vis)
        R.add(name, "G", "zero errors on the reference tab", not errors, errors or "none")
    except Exception as e:
        R.error(name, "G", "reference tab", e)
    finally:
        await ctx.close()


async def li_keyboard(browser, name):
    ctx, page, errors = await new_page(browser, name, (390, 844))
    try:
        s0 = await li_state(page)
        await page.keyboard.press("1"); await page.keyboard.press("2")
        s1 = await li_state(page)
        v = await page.evaluate("document.getElementById('answerBox').value")
        R.add(name, "H", "1/2 before reveal with the box focused: typed, not graded", s1["counts"] == {"got": 0, "missed": 0} and v == "12" and s1["idx"] == 0 and not s1["revealed"], f"counts={s1['counts']} box={v!r} idx={s1['idx']}",
              "Load limitations.html, press 1 then 2 without revealing.")
        await page.evaluate("document.getElementById('answerBox').value=''; S.typed={}; document.activeElement.blur()")
        await page.keyboard.press("1"); await page.keyboard.press("2")
        s2 = await li_state(page)
        R.add(name, "H", "1/2 before reveal with the box blurred: not graded, no advance", s2["counts"] == {"got": 0, "missed": 0} and s2["idx"] == 0 and not s2["revealed"] and await page.evaluate("JSON.stringify(S.graded)") == "{}", f"counts={s2['counts']} idx={s2['idx']}",
              "Load limitations.html, click outside the box, press 1 then 2 without revealing.")
        await page.focus("#answerBox")
        await page.evaluate("document.getElementById('answerBox').scrollIntoView({block:'center'})")
        await page.wait_for_timeout(50)
        sy0 = await page.evaluate("window.scrollY")
        await page.keyboard.press(" ")
        await page.wait_for_timeout(100)
        sy1 = await page.evaluate("window.scrollY")
        v = await page.evaluate("document.getElementById('answerBox').value")
        s3 = await li_state(page)
        R.add(name, "H", "Space in the focused textarea types a space, no reveal, no scroll", v == " " and not s3["revealed"] and sy0 == sy1 and sy0 > 0,
              f"value={v!r} revealed={s3['revealed']} scrollY {sy0}->{sy1}", "At 390px wide, scroll so the answer box is mid-screen, focus it, press Space.")
        await page.evaluate("document.activeElement.blur()")
        sy0 = await page.evaluate("window.scrollY")
        await page.keyboard.press(" ")
        await page.wait_for_timeout(100)
        sy1 = await page.evaluate("window.scrollY")
        s4 = await li_state(page)
        R.add(name, "H", "Space with the box blurred reveals and does not page-scroll", s4["revealed"] and sy0 == sy1, f"revealed={s4['revealed']} scrollY {sy0}->{sy1}", severity="minor")
        await page.keyboard.press("2")
        s5 = await li_state(page)
        st = await status(page)
        R.add(name, "H", "2 after reveal grades missed and advances", s5["counts"]["missed"] == 1 and s5["idx"] == 1 and st.get("owed") == 1, f"{s5['counts']} idx={s5['idx']} {st}")
        # go back with ArrowLeft, the graded pill shows, re-grade to got adjusts counts
        await page.evaluate("document.activeElement && document.activeElement.blur()")
        await key(page, "ArrowLeft")
        s6 = await li_state(page)
        ct = await card_text(page)
        R.add(name, "H", "ArrowLeft returns to the graded item and shows its grade", s6["idx"] == 0 and "Graded: missed" in ct and not s6["revealed"], f"idx={s6['idx']} {ct[:120]!r}")
        await key(page, " ")
        await key(page, "1")
        s7 = await li_state(page)
        st = await status(page)
        R.add(name, "H", "re-grading missed -> got moves the counters and clears the owed entry", s7["counts"] == {"got": 1, "missed": 0} and s7["owed"] == [] and st.get("got") == 1 and st.get("missed") == 0 and st.get("owed") == 0, f"{s7['counts']} owed={s7['owed']} {st}",
              "Reveal, press 2, ArrowLeft, Space, press 1.")
        # R restarts
        await key(page, "r")
        s8 = await li_state(page); st = await status(page)
        R.add(name, "H", "R restarts and resets counters", s8["counts"] == {"got": 0, "missed": 0} and s8["idx"] == 0 and s8["round"] == 1 and not s8["revealed"] and st.get("item") == (1, 160) and st.get("got") == 0 and st.get("owed") == 0, f"{s8['counts']} idx={s8['idx']} {st}")
        # arrows while the answer box holds focus (the default state of every card)
        await page.focus("#answerBox")
        idx_a = (await li_state(page))["idx"]
        await page.keyboard.press("ArrowRight")
        idx_b = (await li_state(page))["idx"]
        R.add(name, "H", "ArrowRight navigates while the answer box has focus (default focus state of every card; Skip button advertises the arrow key)", idx_b == idx_a + 1,
              f"idx {idx_a} -> {idx_b}; the keydown handler returns early for textarea targets, so the arrow moves the caret instead",
              "Load the page (the answer box is focused automatically), press the right arrow: nothing happens. Click outside the box first and it skips.", "minor")
        await page.keyboard.press("r")  # typed into the box, must not restart
        R.add(name, "H", "R while typing in the box does not restart", (await li_state(page))["idx"] == idx_b, "", severity="minor")
        await page.evaluate("document.getElementById('answerBox').value=''; S.typed={}")
        await key(page, "r")
        # arrows at ends
        await key(page, "ArrowLeft")
        s9 = await li_state(page)
        R.add(name, "H", "ArrowLeft at the first item does nothing and does not throw", s9["idx"] == 0 and not errors, f"idx={s9['idx']} {errors}")
        for _ in range(159):
            await key(page, "ArrowRight")
        s10 = await li_state(page)
        R.add(name, "H", "ArrowRight x159 reaches item 160", s10["idx"] == 159 and s10["phase"] == "drill", s10["idx"])
        await key(page, "ArrowRight")
        s11 = await li_state(page)
        R.add(name, "H", "ArrowRight at the last item ends the pass (nothing graded -> done)", s11["phase"] == "done" and not errors, f"{s11['phase']} {errors}")
        ct = await card_text(page)
        R.add(name, "H", "done card after skipping all is coherent", "Session closed after 1 round" in ct and "0/0" in ct and "0%" in ct and "Nothing was missed" in ct, ct[:300], severity="minor")
        await snap(page, name, "done after skipping all")
        await key(page, "ArrowRight"); await key(page, "ArrowLeft"); await key(page, "1"); await key(page, "2"); await key(page, "v")
        s12 = await li_state(page)
        R.add(name, "H", "keys in the done phase do not throw or change state", s12["phase"] == "done" and s12["counts"] == {"got": 0, "missed": 0} and not errors, f"{s12['phase']} {s12['counts']} {errors}")
        await key(page, " ")
        s13 = await li_state(page)
        R.add(name, "H", "Space in the done phase restarts", s13["phase"] == "drill" and s13["idx"] == 0 and s13["round"] == 1, s13["phase"])
        # 1 / 2 in round break must not grade or throw
        await page.evaluate("document.activeElement && document.activeElement.blur()")
        await key(page, " "); await key(page, "2")
        for _ in range(158):
            await key(page, "ArrowRight")
        s14 = await li_state(page)
        await key(page, "ArrowRight")
        s15 = await li_state(page)
        R.add(name, "H", "one miss then skip to the end -> round break", s14["idx"] == 159 and s15["phase"] == "roundbreak" and s15["owed"] and len(s15["owed"]) == 1, f"idx={s14['idx']} phase={s15['phase']} owed={s15['owed']}")
        await key(page, "1"); await key(page, "2"); await key(page, "ArrowRight"); await key(page, "ArrowLeft")
        s16 = await li_state(page)
        R.add(name, "H", "1/2/arrows in the round break do not grade, advance or throw", s16["phase"] == "roundbreak" and s16["counts"] == {"got": 0, "missed": 1} and not errors, f"{s16['phase']} {s16['counts']} {errors}")
        await snap(page, name, "roundbreak 1 owed")
        await key(page, " ")
        s17 = await li_state(page)
        R.add(name, "H", "Space starts round 2 with the one owed item", s17["phase"] == "drill" and s17["round"] == 2 and len(s17["queue"]) == 1 and s17["queue"][0] == s15["owed"][0], f"{s17}")
        ct = await card_text(page)
        R.add(name, "H", "re-served item in round 2 does not still show the old grade pill", "Graded:" not in ct, ct[:160], severity="minor")
        await page.evaluate("document.activeElement && document.activeElement.blur()")
        await key(page, " "); await key(page, "1")
        s18 = await li_state(page)
        st = await status(page)
        R.add(name, "H", "getting the re-served item closes the session", s18["phase"] == "done" and s18["counts"] == {"got": 1, "missed": 0} and st.get("owed") == 0, f"{s18['phase']} {s18['counts']} {st} (latest-grade semantics: the round-2 got replaces the round-1 missed)")
        tally = await page.evaluate("[...document.querySelectorAll('#card .tally .n')].map(e=>e.innerText)")
        R.add(name, "H", "done tally after 1 miss + skip-all: first pass 0/1, 0%, 1 missed, 1 total got", tally == ["0/1", "0%", "1", "1"], tally)
        await snap(page, name, "done after 2 rounds")
        # direction switch restarts
        await page.click("#dirL2P")
        s19 = await li_state(page)
        R.add(name, "H", "direction toggle restarts the session", s19["direction"] == "l2p" and s19["round"] == 1 and s19["idx"] == 0 and s19["counts"] == {"got": 0, "missed": 0}, s19["direction"])
        R.add(name, "H", "zero errors during keyboard edge cases", not errors, errors or "none")
    except Exception as e:
        R.error(name, "H", "keyboard edge cases", e)
    finally:
        await ctx.close()


# ----------------------------------------------------------------------------
# narrow-viewport state sweeps (overflow + text) for both pages
# ----------------------------------------------------------------------------
async def narrow_sweep(browser, name):
    for (w, h) in ((360, 780), (390, 844)):
        ctx, page, errors = await new_page(browser, name, (w, h))
        try:
            tag = f"@{w}"
            if name == "memory-items":
                procs = await page.evaluate("PROCS.length")
                for k in range(procs):
                    await page.evaluate("document.activeElement && document.activeElement.blur()")
                    await page.keyboard.press(" ")
                    await page.keyboard.press("v")
                    await snap(page, name, f"{tag} whole revealed+V proc {k + 1}")
                    await page.keyboard.press("ArrowRight")
                await page.click("#dirA2P")
                for k in range(procs):
                    await snap(page, name, f"{tag} a2p before reveal proc {k + 1}")
                    await page.evaluate("document.activeElement && document.activeElement.blur()")
                    await page.keyboard.press(" ")
                    await page.keyboard.press("v")
                    await snap(page, name, f"{tag} a2p revealed+V proc {k + 1}")
                    await page.keyboard.press("ArrowRight")
                await page.click("#dirP2A"); await page.click("#styLine")
                await page.evaluate("document.activeElement && document.activeElement.blur()")
                await page.keyboard.press(" ")
                await snap(page, name, f"{tag} line mode line 1 revealed")
            else:
                n = await page.evaluate("S.queue.length")
                for k in range(n):
                    await page.evaluate("document.activeElement && document.activeElement.blur()")
                    await page.keyboard.press(" ")
                    await page.keyboard.press("v")
                    await snap(page, name, f"{tag} p2l revealed+V item {k + 1}")
                    await page.keyboard.press("ArrowRight")
                await page.click("#dirL2P")
                for k in range(n):
                    await page.evaluate("document.activeElement && document.activeElement.blur()")
                    await snap(page, name, f"{tag} l2p before reveal item {k + 1}", overflow=(k % 4 == 0))
                    await page.keyboard.press(" ")
                    await snap(page, name, f"{tag} l2p revealed item {k + 1}")
                    await page.keyboard.press("ArrowRight")
            R.add(name, "A", f"narrow sweep {tag}: zero errors", not errors, errors or "none")
        except Exception as e:
            R.error(name, "A", f"narrow sweep @{w}", e)
        finally:
            await ctx.close()


# ----------------------------------------------------------------------------
# report
# ----------------------------------------------------------------------------
# Root causes for the defects this harness is known to surface, keyed by a stable
# fragment of the check name. Everything else in the failure list is reported as found.
ROOT_CAUSES = {
    "start with an empty answer box": "S.typed is reset only in startSession(); startNextRound() keeps it, and renderCard() does box.value = S.typed[key] || \"\" (memory-items.html ~line 1661, limitations.html ~line 2961). The re-served card is pre-filled with the round-1 typing, i.e. the answer the drill is meant to withhold.",
    "re-served items do not show their previous grade": "limitations.html: S.graded is not cleared in startNextRound(), and renderCard() prints a 'Graded: missed' pill from S.graded[it.id] before reveal (~line 2902). Same root as the latest-grade counter semantics.",
    "does not still show the old grade pill": "limitations.html: S.graded persists across rounds (see startNextRound ~line 2760); the pill at ~line 2902 renders before reveal.",
    "no horizontal overflow @ 360px, state: reference": "limitations.html: dot-leader runs of 130+ characters in `verbatim` (e.g. lim-afs-24 'height....') set the table's min-content width; `.verbatim` has word-wrap: break-word which does not shrink table min-content. Below 640px `.tablewrap` is overflow-x: visible (CSS ~line 416), so the whole page scrolls sideways to ~1148px whenever a row with such a run is expanded. At >=641px the same content forces a ~1618px-wide table inside the scrolling .tablewrap.",
    "prompt is the limit, parameter hidden": "limitations.html: in Limit -> parameter the UNCLEAR note (unclearReason(), ~line 2916) is printed before reveal, and the UNCLEAR_REASONS texts open with the parameter name ('Minimum flight crew oxygen bottle pressure.', 'Fuel specification freezing points.', also 'Maximum flaps/slats speeds.', 'Centre of gravity envelope.', 'Fuel imbalance table.' etc.), giving the answer away.",
    "ArrowRight navigates while the answer box has focus": "Both pages focus the answer box on every new card (box.focus) and the keydown handler returns early for textarea targets, so the arrow keys advertised on the Skip button only work after clicking out of the box.",
    "expand-all button stays truthful": "limitations.html: the per-row source-text handler sets S.ref.expandAll = false and opens every row individually (~line 3055) but never updates the #expandAll label; the next click on the button re-enables expand-all instead of hiding.",
}


def root_cause(name):
    for k, v in ROOT_CAUSES.items():
        if k in name:
            return v
    return ""


def write_reports():
    rows = R.rows
    # text integrity as its own test rows
    for pg in PAGES:
        hits = [h for h in R.text_hits if h[0] == pg]
        R.add(pg, "I", f"no 'undefined' / 'NaN' / 'null' / '[object' / em dash in any visited state ({sum(1 for _ in hits)} hits over states)",
              not hits, "; ".join(f"[{h[1]}] {h[2]}: ...{h[3]}..." for h in hits[:20]) or "clean",
              "See the listed state; document.body.innerText contains the token.", "major")
    total = len(rows)
    passed = sum(1 for r in rows if r["status"] == "PASS")
    failed = [r for r in rows if r["status"] == "FAIL"]
    # collapse repeated failures with the same (page, test, symptom prefix)
    fail_json, seen_keys = [], {}
    for r in failed:
        key = (r["page"], re.sub(r"\(lim-[a-z]+-\d+\)|\[(p2l|l2p|whole|line|a2p)[^\]]*\]|round \d+|state: reference.*$", "", r["name"]).strip())
        if key in seen_keys:
            seen_keys[key]["occurrences"] += 1
            continue
        entry = {"page": PAGES[r["page"]], "test": r["test"], "symptom": r["name"] + " :: " + r["evidence"][:600],
                 "repro": r["repro"] or "Run build_scripts/verify/pass3_runtime.py and see the named check.", "severity": r["severity"] or "major",
                 "root_cause": root_cause(r["name"]), "occurrences": 1}
        seen_keys[key] = entry
        fail_json.append(entry)
    fail_json.sort(key=lambda e: {"blocker": 0, "major": 1, "minor": 2}.get(e["severity"], 3))
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "PASS3_failures.json"), "w") as f:
        json.dump(fail_json, f, indent=2, ensure_ascii=False)
    # markdown matrix
    tests = {"A": "Load (scroll, errors, banner, overflow) at 1280x900 / 390x844 / 360x780 + narrow state sweeps",
             "B": "Dark scheme load checks + computed colours",
             "C": "memory-items whole-procedure full session incl. re-serve",
             "D": "memory-items line-by-line full session",
             "E": "memory-items actions -> procedure direction",
             "F": "limitations full sessions (both directions), UNCLEAR toggle, system filters",
             "G": "Reference tabs",
             "H": "Keyboard edge cases",
             "I": "Text integrity across visited states",
             "J": "Icon links",
             "overflow": "Per-state horizontal overflow (recorded from state snapshots)"}
    L = []
    L.append("# PASS 3, runtime verification of memory-items.html and limitations.html\n")
    L.append(f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')} by `build_scripts/verify/pass3_runtime.py` (Playwright, headless Chromium, file://).\n")
    L.append(f"**Checks recorded: {total}. Pass: {passed}. Fail: {len(failed)}. States scanned for text integrity and overflow: {R.state_count}.**\n")
    L.append("## Matrix\n")
    L.append("| Test | Scope | memory-items | limitations |")
    L.append("|---|---|---|---|")
    for t, desc in tests.items():
        cells = []
        for pg in PAGES:
            sub = [r for r in rows if r["page"] == pg and r["test"] == t]
            if not sub:
                cells.append("n/a")
            else:
                f = sum(1 for r in sub if r["status"] == "FAIL")
                cells.append(f"{'PASS' if f == 0 else 'FAIL'} ({len(sub) - f}/{len(sub)})")
        L.append(f"| {t} | {desc} | {cells[0]} | {cells[1]} |")
    L.append("")
    L.append("## Distinct defects, with reproduction steps\n")
    L.append(f"{len(fail_json)} distinct defects from {len(failed)} failing checks (duplicates across items/rounds/directions collapsed).\n")
    if not fail_json:
        L.append("None.\n")
    for i, e in enumerate(fail_json, 1):
        L.append(f"### D{i}. [{e['page']}] test {e['test']}, **{e['severity']}** ({e['occurrences']} occurrence{'s' if e['occurrences'] != 1 else ''})\n")
        L.append(f"**Symptom:** {e['symptom'][:900]}\n")
        L.append(f"**Repro:** {e['repro']}\n")
        if e["root_cause"]:
            L.append(f"**Root cause:** {e['root_cause']}\n")
    L.append("## Observations that are not failures\n")
    L.append("- memory-items.html: the warning banner is 655px tall at 360x780 (84% of the first screen) and 596px at 390x844. It is in the initial viewport as required, but the drill itself starts two screens down on a phone.")
    L.append("- memory-items.html: in Actions -> procedure, EMER DESCENT's first boxed line reads 'EMER DESCENT ... INITIATE', so the block names its own procedure. That is how the FCOM prints it; recorded as informational, not a page defect.")
    L.append("- limitations.html counts the latest grade per item (a round-2 'got' moves an item from Missed to Got); memory-items.html counts cumulatively per served procedure. Each page is internally consistent, but the two 'Missed' counters mean different things.")
    L.append("- memory-items.html has no search, sort or collapse controls on its Reference tab (citations are printed inline); those parts of test G are n/a there.")
    L.append("")
    L.append("## Text-integrity hits\n")
    if not R.text_hits:
        L.append("None in any visited state.\n")
    else:
        for h in R.text_hits[:200]:
            L.append(f"- [{h[0]}] state `{h[1]}`: **{h[2]}** ...{h[3]}...")
        L.append("")
    L.append("## Every check\n")
    L.append("| Page | Test | Status | Check | Evidence |")
    L.append("|---|---|---|---|---|")
    for r in rows:
        ev = r["evidence"].replace("|", "\\|").replace("\n", " ")[:160]
        L.append(f"| {r['page']} | {r['test']} | {r['status']} | {r['name'].replace('|', '/')} | {ev} |")
    with open(os.path.join(DATA, "PASS3_runtime.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    return total, passed, failed


async def main():
    t0 = time.time()
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for name in PAGES:
            print(f"== {name}: A/B load checks")
            for vp in VIEWPORTS:
                await test_load(browser, name, vp)
                await test_load(browser, name, vp, "dark")
            await test_icons(browser, name)
        print("== memory-items: C whole")
        await mi_full_session(browser, "memory-items", "C", "whole")
        print("== memory-items: D line")
        await mi_full_session(browser, "memory-items", "D", "line")
        print("== memory-items: E a2p")
        await mi_full_session(browser, "memory-items", "E", "a2p")
        print("== memory-items: G reference")
        await mi_reference(browser, "memory-items")
        print("== memory-items: H keyboard")
        await mi_keyboard(browser, "memory-items")
        print("== limitations: F p2l full session")
        await li_full_session(browser, "limitations", "p2l")
        print("== limitations: F l2p full session")
        await li_full_session(browser, "limitations", "l2p")
        print("== limitations: F filters")
        await li_filters(browser, "limitations")
        print("== limitations: G reference")
        await li_reference(browser, "limitations")
        print("== limitations: H keyboard")
        await li_keyboard(browser, "limitations")
        print("== narrow sweeps")
        await narrow_sweep(browser, "memory-items")
        await narrow_sweep(browser, "limitations")
        await browser.close()
    total, passed, failed = write_reports()
    print(f"\nchecks={total} pass={passed} fail={len(failed)} states={R.state_count} time={time.time() - t0:.0f}s")
    for r in failed:
        print(f" - [{r['page']}/{r['test']}/{r['severity']}] {r['name']}")


if __name__ == "__main__":
    asyncio.run(main())
