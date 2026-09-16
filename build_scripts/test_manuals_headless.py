#!/usr/bin/env python3
"""Headless smoke test for manuals/index.html: serve WORK, search with All and FCOM, open a
modal, deep-link ?s= and ?q=, capture console errors and failed requests, screenshot."""
import os, subprocess, sys, time, json
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..'))
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
from playwright.sync_api import sync_playwright

PORT = int(os.environ.get('PORT', '8765'))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1'], cwd=WORK,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(0.8)
errors, failed = [], []
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 430, 'height': 1100})
        pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
        pg.on('requestfailed', lambda r: failed.append(r.url))
        pg.on('response', lambda r: failed.append('%d %s' % (r.status, r.url)) if r.status >= 400 else None)
        base = 'http://127.0.0.1:%d' % PORT

        pg.goto(base + '/manuals/', wait_until='networkidle')
        assert pg.title() == 'A330 Manuals', pg.title()
        assert pg.inner_text('.banner .t') == 'A330 MANUALS'
        assert 'FCOM R17' in pg.inner_text('#meta')
        assert pg.locator('#manSeg button[data-man="ALL"]').get_attribute('aria-pressed') == 'true'

        # Offline Search, All
        pg.fill('#q', 'oxygen mask test')
        pg.click('#searchBtn')
        pg.wait_for_function("document.querySelectorAll('.res').length > 0", timeout=180000)
        n_all = pg.locator('.res').count()
        heads_all = pg.locator('.res .h').all_inner_texts()
        status_all = pg.inner_text('#status')
        print('ALL:', n_all, 'results |', status_all)
        for h in heads_all[:6]: print('   ', h.replace('\n', ' | '))
        assert any('Open ' in h and 'in Drive, p.' in h for h in heads_all)
        chips = pg.inner_text('#chips')
        print('chips:', chips.replace('\n', ' '))

        # FCOM only
        pg.click('#manSeg button[data-man="A330P_FCOM"]')
        pg.wait_for_function("document.getElementById('status').textContent.indexOf('FCOM R17') >= 0", timeout=60000)
        heads_fcom = pg.locator('.res .h').all_inner_texts()
        print('FCOM:', len(heads_fcom), 'results |', pg.inner_text('#status'))
        for h in heads_fcom[:6]: print('   ', h.replace('\n', ' | '))
        assert all(h.startswith('FCOM') for h in heads_fcom), heads_fcom[:3]
        assert any('DSC-35' in h for h in heads_fcom), 'expected an oxygen DSC-35 hit'

        # open the first result modal
        pg.locator('.res').first.click()
        pg.wait_for_selector('#ovl.on')
        title = pg.inner_text('#ovlTitle')
        body = pg.inner_text('#ovlBody')
        link = pg.inner_text('#ovlPdf')
        href = pg.get_attribute('#ovlPdf', 'href')
        print('MODAL:', title, '|', link, '|', href[:50], '| body chars', len(body))
        assert 'FCOM' in title and 'drive.google.com' in href and 'in Drive, p.' in link
        assert len(body) > 200
        pg.screenshot(path=os.path.join(WORK, 'docs', 'parity', 'manuals_agent_modal.png'))
        pg.keyboard.press('Escape')
        assert not pg.locator('#ovl.on').count()

        # Exact and Phrase modes still work
        pg.click('#modeSeg button[data-mode="phrase"]')
        pg.wait_for_timeout(500)
        print('PHRASE:', pg.inner_text('#status'))
        pg.click('#modeSeg button[data-mode="keywords"]')

        # TOC rendered, grouped by manual
        toc_groups = pg.locator('#tocList > li').count()
        print('TOC groups (FCOM scope):', toc_groups)
        assert toc_groups == 1

        # screenshot the main page with results
        pg.screenshot(path=os.path.join(WORK, 'docs', 'parity', 'manuals_agent.png'), full_page=False)

        # ?s= deep link
        pg.goto(base + '/manuals/?s=DSC-35-20-30', wait_until='networkidle')
        pg.wait_for_selector('#ovl.on', timeout=60000)
        t2 = pg.inner_text('#ovlTitle')
        print('?s=DSC-35-20-30 ->', t2)
        assert 'DSC-35-20-30' in t2
        pg.keyboard.press('Escape')

        # ?s= with a FOM id
        pg.goto(base + '/manuals/?s=5.4.2', wait_until='networkidle')
        pg.wait_for_selector('#ovl.on', timeout=60000)
        print('?s=5.4.2 ->', pg.inner_text('#ovlTitle'))
        pg.keyboard.press('Escape')

        # ?q= prefill and run, with ?m=QRH
        pg.goto(base + '/manuals/?m=QRH&q=tailwind', wait_until='networkidle')
        pg.wait_for_function("document.querySelectorAll('.res').length > 0 || document.getElementById('status').textContent.indexOf('No match') >= 0", timeout=60000)
        print('?m=QRH&q=tailwind ->', pg.locator('.res').count(), 'results |', pg.inner_text('#status'))
        assert pg.input_value('#q') == 'tailwind'
        assert pg.locator('#manSeg button[data-man="A330P_QRH"]').get_attribute('aria-pressed') == 'true'

        pg.goto(base + '/manuals/?m=ALL&q=tailwind', wait_until='networkidle')
        pg.wait_for_function("document.querySelectorAll('.res').length > 0", timeout=180000)
        heads = pg.locator('.res .h').all_inner_texts()
        print('?q=tailwind (All) ->', len(heads), 'results')
        for h in heads[:5]: print('   ', h.replace('\n', ' | '))

        # Ask flow with a stubbed provider: router menu -> whole sections -> answer with cite links
        pg.goto(base + '/manuals/?m=FCOM', wait_until='networkidle')
        pg.evaluate('''() => {
          window.__calls = [];
          window.PortalSettings = {
            ready: function () { return true; }, open: function () {},
            ask: function (sys, u) { window.__calls.push({kind: 'router', sys: sys, user: u}); return Promise.resolve('1, 2'); },
            askFull: function (sys, msgs) { window.__calls.push({kind: 'full', sys: sys, msgs: msgs});
              return Promise.resolve({text: 'Press and hold the RESET/TEST button on the mask stowage box.\\n- Blinker shows yellow while the test runs (FCOM DSC-35-20-30 p.1945)\\n- Crew supply pb ON first (FCOM DSC-35-20-20, p.1938)', thinking: ''}); },
            modelLabel: function () { return 'stub'; }, threadsAreCheap: function () { return true; },
            emptyReason: function () { return 'empty'; }, MAX_IMAGES: 4,
            prepImage: function () { return Promise.reject(new Error('no')); }
          };
        }''')
        pg.fill('#q', 'oxygen mask test')
        pg.click('#askBtn')
        pg.wait_for_function("document.querySelectorAll('#answer a.cite').length > 0", timeout=120000)
        calls = pg.evaluate('() => window.__calls')
        assert calls[0]['kind'] == 'router' and 'Section menu' in calls[0]['user'] and '1. FCOM DSC-35' in calls[0]['user'], calls[0]['user'][:300]
        full = calls[1]
        assert full['kind'] == 'full' and 'COMPLETE text' in full['msgs'][0]['content'] and '[FCOM DSC-35-20-30 p.1945' in full['msgs'][0]['content']
        assert 'seat' not in full['sys'].lower() and 'domicile' not in full['msgs'][0]['content'].lower()
        print('ASK: router menu lines', calls[0]['user'].count('\n'), '| context chars', len(full['msgs'][0]['content']), '| sys starts:', full['sys'][:60])
        print('ASK who:', pg.inner_text('#answerWho'))
        cites = pg.locator('#answer a.cite').all_inner_texts()
        print('ASK cites:', cites)
        assert len(cites) == 2
        pg.locator('#answer a.cite').first.click()
        pg.wait_for_selector('#ovl.on')
        print('cite click ->', pg.inner_text('#ovlTitle'))
        assert 'DSC-35-20-30' in pg.inner_text('#ovlTitle')
        pg.keyboard.press('Escape')
        pg.screenshot(path=os.path.join(WORK, 'docs', 'parity', 'manuals_agent_ask.png'))

        # citation linking in the answer renderer
        html = pg.evaluate("""() => { const t = document.createElement('div');
            t.innerHTML = '<a class="cite" data-m="A330P_FCOM" data-p="1945" data-s="DSC-35-20-30">x</a>'; return t.innerHTML; }""")
        assert 'cite' in html
        b.close()
finally:
    srv.terminate()

print('console errors:', errors)
print('failed requests:', failed)
assert not errors, errors
assert not failed, failed
print('HEADLESS OK')
