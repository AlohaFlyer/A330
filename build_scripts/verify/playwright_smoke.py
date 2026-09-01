import asyncio, json, os, sys
from playwright.async_api import async_playwright

REPO = "/home/claude/a330/repo"


async def load(browser, name, width=1100):
    ctx = await browser.new_context(viewport={"width": width, "height": 800})
    page = await ctx.new_page()
    errors, msgs = [], []
    page.on("console", lambda m: (msgs.append((m.type, m.text)), errors.append(m.text) if m.type == "error" else None))
    page.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
    await page.goto("file://" + os.path.join(REPO, name), wait_until="load")
    await page.wait_for_timeout(300)
    return ctx, page, errors, msgs


async def check_common(page, errors, name, banner_needle):
    scroll_y = await page.evaluate("window.scrollY")
    banner = await page.evaluate("document.querySelector(\".banner\").textContent")
    focused = await page.evaluate("document.activeElement && document.activeElement.id")
    icon = await page.get_attribute('link[rel="icon"]', "href")
    touch = await page.get_attribute('link[rel="apple-touch-icon"]', "href")
    manifest = await page.get_attribute('link[rel="manifest"]', "href")
    body_w = await page.evaluate("document.documentElement.scrollWidth")
    view_w = await page.evaluate("window.innerWidth")
    print(f"[{name}] scrollY after load: {scroll_y}")
    print(f"[{name}] focused element on load: {focused}")
    print(f"[{name}] console errors: {len(errors)} {errors[:3]}")
    print(f"[{name}] banner present: {banner_needle in banner}")
    print(f"[{name}] icon href starts with data:image/png;base64: {str(icon).startswith('data:image/png;base64,')}")
    print(f"[{name}] apple-touch-icon: {touch}   manifest: {manifest}")
    print(f"[{name}] horizontal overflow: {body_w > view_w} (scrollWidth {body_w}, innerWidth {view_w})")
    assert scroll_y == 0, "page scrolled on load"
    assert not errors, "console errors present"
    assert banner_needle in banner, "banner text missing"
    assert str(icon).startswith("data:image/png;base64,")
    assert body_w <= view_w, "horizontal overflow"
    return banner


async def drive_memory_items(page):
    # state introspection helpers
    st = lambda: page.evaluate("({phase:S.phase, idx:S.idx, revealed:S.revealed, cursor:S.cursor, line:S.line, counts:S.counts, queue:S.queue.length, owed:S.missedThisRound.length, pid: current() && current().pid, title: current() && current().title, n: current() && current().gradable.length})")
    procs = await page.evaluate("PROCS.map(function(p){return {pid:p.pid, title:p.title, lines:p.gradable.length, books:p.books, headers:p.headers.length}})")
    print(f"[memory-items] procedures built at load: {len(procs)}")
    for p in procs:
        print("   ", p["pid"], p["title"], "lines=", p["lines"], "books=", p["books"], "headers=", p["headers"])
    assert len(procs) == 10
    emer = [p for p in procs if "EMER DESCENT" in p["title"]]
    assert len(emer) == 1 and emer[0]["books"] == ["FCOM R17", "QRH R35"], "EMER DESCENT must be one item with both citations"
    warnings = await page.evaluate("DATA_WARNINGS")
    print(f"[memory-items] DATA_WARNINGS: {warnings}")
    assert warnings == []

    # --- whole-procedure mode: drive procedure 1 with the keyboard ---
    s0 = await st()
    print(f"[memory-items] whole mode, procedure 1: {s0['title']} ({s0['n']} lines), focused box: ", await page.evaluate("document.activeElement.id"))
    # skeleton must not leak the boxed lines before reveal
    card_before = await page.locator("#card").inner_text()
    first_line = await page.evaluate("current().actions[current().gradable[0]]")
    assert first_line not in card_before, "boxed line leaked before reveal"
    # type one correct line, then Enter on an empty line to reveal
    await page.keyboard.type(first_line)
    await page.keyboard.press("Enter")   # newline (line not empty)
    assert not (await st())["revealed"], "Enter on a non-empty line must not reveal in whole mode"
    await page.keyboard.press("Enter")   # empty line -> reveal
    s1 = await st()
    assert s1["revealed"], "Enter on an empty line should reveal"
    card_after = await page.locator("#card").inner_text()
    assert first_line.split(" ... ")[0] in card_after, "revealed block missing the first item"
    assert "typed: match" in card_after, "typed-match mark missing for the typed line"
    assert "Paraphrase is a miss" in card_after, "grading copy must state paraphrase is a miss"
    # source on demand
    await page.keyboard.press("v")
    src = await page.locator("#card .cite").inner_text()
    assert "ident" in src and "page" in src, "source details missing after V"
    print("[memory-items] V shows source:", src.splitlines()[1][:110] if len(src.splitlines()) > 1 else src[:110])
    # grade every line: 1 for all but the last, 2 for the last
    n = s1["n"]
    for i in range(n):
        await page.keyboard.press("1" if i < n - 1 else "2")
    s2 = await st()
    print(f"[memory-items] after grading {n} lines: counts={s2['counts']} owed={s2['owed']}")
    assert s2["counts"] == {"got": n - 1, "missed": 1}
    assert s2["owed"] == 1, "procedure with a missed line must be queued"
    assert "comes back at the end of the round" in await page.locator("#card").inner_text()
    board = await page.evaluate("document.getElementById(\"boardBody\").textContent")
    assert "missed at least once" in board
    # Space -> next procedure
    await page.keyboard.press(" ")
    s3 = await st()
    assert s3["idx"] == 1 and not s3["revealed"], "Space after a fully graded procedure should advance"
    print(f"[memory-items] advanced to procedure 2: {s3['title']}")
    # grade the rest of round 1 clean using Space + 1s, then check round break appears
    guard = 0
    while (await st())["phase"] == "drill":
        guard += 1
        assert guard < 40, "drill loop did not terminate"
        s = await st()
        if not s["revealed"]:
            await page.keyboard.press("Enter")   # box is focused and empty: Enter reveals
        else:
            for _ in range(s["n"]):
                await page.keyboard.press("1")
            await page.keyboard.press(" ")
    s4 = await st()
    print(f"[memory-items] end of round 1: phase={s4['phase']} counts={s4['counts']}")
    assert s4["phase"] == "roundbreak"
    assert "still owed" in await page.locator("#card").inner_text()
    await page.keyboard.press(" ")  # start round 2 with the one missed procedure
    s5 = await st()
    assert s5["phase"] == "drill" and s5["queue"] == 1 and s5["pid"] == s0["pid"], "round 2 must re-serve the missed procedure"
    print(f"[memory-items] round 2 re-serves: {s5['title']}")
    await page.keyboard.press("Enter")
    for _ in range(s5["n"]):
        await page.keyboard.press("1")
    await page.keyboard.press(" ")
    s6 = await st()
    done_text = await page.locator("#card").inner_text()
    print(f"[memory-items] phase after round 2: {s6['phase']}")
    assert s6["phase"] == "done" and "Never missed" in done_text and "Missed at least once" in done_text
    board = await page.evaluate("document.getElementById(\"boardBody\").textContent")
    assert board.count("never missed") == 9 and board.count("missed at least once") == 1, board
    print("[memory-items] scoreboard: 9 never missed, 1 missed at least once")

    # --- line-by-line mode ---
    await page.keyboard.press("r")
    await page.click("#styLine")
    s7 = await st()
    print(f"[memory-items] line-by-line, procedure: {s7['title']} ({s7['n']} lines)")
    for i in range(s7["n"]):
        before = await page.locator("#card").inner_text()
        nxt = await page.evaluate("current().actions[current().gradable[S.line]]")
        assert nxt.split(" ... ")[0] not in before or i > 0, "next line leaked before reveal"
        await page.keyboard.type(nxt)
        await page.keyboard.press("Enter")   # single-line box: Enter reveals
        s = await st()
        assert s["revealed"] and s["line"] == i
        shown = await page.locator("#card").inner_text()
        assert "typed: match" in shown
        await page.keyboard.press("1")
    s8 = await st()
    assert "Clean" in await page.locator("#card").inner_text()
    assert s8["counts"]["got"] == s7["n"]
    print(f"[memory-items] line-by-line completed clean: counts={s8['counts']}")

    # --- actions -> procedure ---
    await page.click("#dirA2P")
    disabled = await page.evaluate("el('styWhole').disabled && el('styLine').disabled")
    assert disabled, "mode buttons must be disabled in actions -> procedure"
    s9 = await st()
    card = await page.locator("#card").inner_text()
    assert s9["title"] not in card, "procedure title leaked in actions -> procedure before reveal"
    await page.keyboard.press("Enter")
    card = await page.evaluate("document.getElementById(\"card\").textContent")
    assert s9["title"] in card and "Trigger, as printed" in card
    await page.keyboard.press("1")
    s10 = await st()
    assert s10["counts"] == {"got": 1, "missed": 0}
    print(f"[memory-items] actions -> procedure: revealed {s9['title']}, graded got; counts={s10['counts']}")

    # --- reference tab renders all ten with citations ---
    await page.click("#tabRef")
    ref = await page.locator("#refList").inner_text()
    assert ref.count("ident") >= 11, "reference should list all 11 citations"
    assert "Printed unboxed" in ref, "TCAS CAUTION unboxed note missing in reference"
    print("[memory-items] reference tab: 11 citations listed, TCAS CAUTION marked printed unboxed")


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        # limitations.html
        ctx, page, errors, msgs = await load(browser, "limitations.html")
        await check_common(page, errors, "limitations", "Study aid only, not a source document")
        ver = await page.locator("#footGen").inner_text()
        print("[limitations] footer:", ver)
        assert "page version 0.7" in ver
        await ctx.close()
        # memory-items.html, desktop
        ctx, page, errors, msgs = await load(browser, "memory-items.html")
        await check_common(page, errors, "memory-items", "NOT yet been cross-checked against the training-department")
        banner = await page.evaluate("document.querySelector(\".banner\").textContent")
        assert "TCAS CAUTION" in banner and "unboxed" in banner and "3164" in banner and "At-ANY-TIME" in banner
        print("[memory-items] banner carries the TCAS CAUTION unboxed fact and the Smoke/Fumes p3164 At-ANY-TIME fact: True")
        foot = await page.locator("footer").inner_text()
        assert "A330P FCOM R17, issue 15 MAY 26" in foot and "A330P QRH R35, issue 26 JUN 26" in foot and "Generated 2026-09-01" in foot and "page version 0.3" in foot
        print("[memory-items] footer:", " | ".join(foot.splitlines()[:3]))
        await drive_memory_items(page)
        assert not errors, errors
        print(f"[memory-items] console errors after full drive: {len(errors)}")
        await ctx.close()
        # memory-items.html, phone width, dark scheme
        ctx = await browser.new_context(viewport={"width": 375, "height": 720}, color_scheme="dark")
        page = await ctx.new_page()
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        await page.goto("file://" + os.path.join(REPO, "memory-items.html"), wait_until="load")
        await page.wait_for_timeout(200)
        sw, iw = await page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
        bg = await page.evaluate("getComputedStyle(document.body).backgroundColor")
        sy = await page.evaluate("window.scrollY")
        print(f"[memory-items phone/dark] scrollY={sy} overflow={sw > iw} (scrollWidth {sw}, innerWidth {iw}) body bg={bg} errors={errs}")
        assert sw <= iw and sy == 0 and not errs
        assert bg == "rgb(21, 19, 28)", "dark palette not applied"
        await page.screenshot(path="/tmp/mi_phone_dark.png", full_page=False)
        await ctx.close()
        # desktop light screenshot after reveal, for a visual look
        ctx, page, errors, msgs = await load(browser, "memory-items.html")
        await page.keyboard.press(" ")
        await page.screenshot(path="/tmp/mi_desktop_revealed.png", full_page=True)
        await ctx.close()
        await browser.close()
    print("ALL PLAYWRIGHT CHECKS PASSED")


asyncio.run(main())
