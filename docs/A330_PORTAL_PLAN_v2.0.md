# A330 Study Portal Plan v2.0: exact clone of as787pilot.app in the Hawaiian palette

**Target:** ha330pilot.app (repo AlohaFlyer/A330, rebuilt in place) | **Model:** as787pilot.app at v2.40, commit ff78f9a, 2026-09-11 | **Date:** 2026-09-15 | **Supersedes:** A330_PORTAL_PLAN.md Ver 1.1 for everything about layout, pages, and build order. Ver 1.1 remains valid for Drive intake, manual library, and the locked architecture decisions 1 to 9, which this plan keeps.

## Decisions taken 2026-09-15

| # | Decision | Answer |
|---|---|---|
| Q1 | Repo | Rebuild in place in AlohaFlyer/A330. CNAME, Pages, DNS, and the verified data JSON stay. Every HTML, CSS and JS file from the first attempt is replaced. |
| Q2 | Email gate | `@alaskaair.com` only, byte-identical to the B787 gate. |
| Q3 | Systems Quiz | Build the full engine, filter bar, Jeopardy, and corpus pipeline now with an empty bank. Ryan supplies the question bank and category list later; it drops into `data/systems.json` with no engine change. |
| Q4 | Pages with no obvious A330 twin | Build both: OE Workbook Trainer from the 787-321-330 Fleets OE Workbook (A330 sections only) and MCDU Preflight (PF) from A330P FCOM PRO-NOR-SOP. |

## Governing rule: fork, do not redesign

The first A330 attempt failed the "looks like the B787" test because it was written fresh against a palette file. This build does the opposite. Every file in the B787 repo is copied, then exactly three classes of change are applied, and nothing else:

1. **Palette substitution.** A fixed hex-to-hex map (section 3), applied mechanically by script. No new CSS rules, no changed sizes, radii, fonts, spacing, breakpoints, or animations.
2. **String substitution.** Fleet, airline, domain, key-prefix, manual-name and revision strings (section 4).
3. **Data substitution.** The A330 records replace the B787 records, in the same record shapes the B787 engines already consume (section 5). Engines are not rewritten.

The test that the rule held: a CSS parity diff (section 8) between the two repos, after applying the hex map and string map to the B787 side, must come back empty for every page. Any non-empty diff is a defect, not a design choice.

The one structural liberty is the locked architecture decision that data lives in `data/*.json`, not inline in HTML. That changes zero pixels. The B787 engines that read inline `const DATA=[...]` get a four-line loader (`fetch('data/x.json')`) in place of the literal; the render code after it is untouched.

## 1. What the B787 portal is (audit summary, v2.40)

24 HTML pages, two shared scripts, one service worker, nine corpus files. Five visual families share one chrome: the `.ps-homebar` home icon on every subpage and `<script src="/portal-settings.js" defer>` plus `<script src="/assist.js" defer>` at the end of every body.

| Family | Pages | Body bg | Font | Column |
|---|---|---|---|---|
| A light portal | index, flows_quiz, fom_quiz, pwa, pwa_pdf | #E8F3FA | Segoe UI, Arial | 560 / 1024 / 640 / 820 px |
| B dark drill | limitations, memory-items, triggers, weather, hot-seat, limit-or-bust, wx-alternate | #01172b | system-ui + mono | 700 / 680 / 640 px |
| C dark variants | ioe, podcast, view, systems_quiz | #0b1c2c, #01172b, #0a0d12 | mixed | 820 / 760 / full / 800 px |
| D light pale | phase_flows, cdu_preflight | #eef4f8 | Helvetica Neue / Segoe | full-screen / 760 px |
| E game | jeopardy | gradient #eaf4fc to #dcecf8 | Segoe UI | 1080 px |

**index.html.** Full-bleed navy banner flush to the top, padding tracks the 560 px column; logo PNG at 30 px height wrapped in a reload link; title span in lime #b1d887, 20 px, 700, letter-spacing 1 px. Email gate (h2 "Company Email Address", placeholder, Enter button, red error line) sets a 5-year cookie and logs the unlock to localStorage, flushed to a Google Apps Script collector by portal-settings.js. Menu: 12 white tiles, 2 px navy border, square corners, 18 px by 14 px padding, title 16 px 700 plus 12 px grey subtitle, right-hand arrow; hover inverts to navy. Three tinted tiles: `.phase` lime, `.podcast` #d6ecf7, `.alpa` #efe3f5. Footer: hero photo 360 px, manual revision table (5 rows), mailto contact line, gear slot, right-aligned "Ver x.y".

**portal-settings.js.** Mounts only into `#gearSlot` (index footer). Modal sections: Your profile (Seat CA/FO, Domicile HNL/SEA, Date of hire with longevity readout), Tax assumptions (state select seeded from a 2026 top-marginal table, state effective rate, federal slider), Build (running build string, Force refresh that wipes caches and the service worker), Ask Pualani (provider Claude/ChatGPT/Gemini/Grok, API key save/forget, model load), Offline (core tier about 22 MB, audio tier about 566 MB, progress bars), Portal log (owner only). Exposes `window.PortalSettings` with `profile()`, `askFull()`, `prepImage()`, `emptyReason()`, `modelLabel()`. Injects the home icon on any subpage missing it. Phone CSS: 16 px inputs, 44 px tap targets under 600 px.

**assist.js.** Per-page "Search this section" launcher (fixed bottom-right pill with Pualani avatar) opening a bottom sheet: textarea, Keywords/Exact/Phrase segment, Offline Search (BM25, k1 1.5, b 0.75, title weighted x2, phrase bonus 5), attach up to 4 images, 76 px Ask Pualani disc, profile chips, ranked results with highlighted snippets, "Pualani says" TLDR answer thread with up to 12 follow-ups and Show reasoning. Scoped to `/corpus/<key>.json` for nine pages.

**pwa.html / pwa_pdf.html.** Hawaiian 2023 Pilots Agreement. Question box, Match segment, Offline Search, Attach, Ask Pualani, profile chips, threaded answers, results with "Open PDF p.N", modal page view, "Browse by section" TOC. Router call picks up to 4 sections, then full sections (140 k char cap) go to the model with cache_control on the first message. pwa_pdf: sticky bar, iframe on `2023-pwa.pdf#page=N`, 340 px index panel with filter.

**sw.js.** Network-first for html/json/js/css with cache write and script-tag injection; cache-first for everything else; separate CORE and AUDIO caches; messages CACHE_CORE, CACHE_AUDIO, CLEAR_CORE, CLEAR_AUDIO, STATUS; PROGRESS/DONE/CLEARED/STATUS replies; 6 parallel lanes core, 4 audio; offline fallback to `/index.html` then an inline 503 page. `offline-manifest.json` lists every core URL with byte size and every audio URL.

**Drill engine (family B).** One card, `.chip` mono category, 23 px question, Reveal, then Got it K / Review R, Source button opening a verbatim-quote panel, progress bar and set label, Restart set, summary with big mono percentage. Same engine drives limitations, memory-items, triggers, weather. Keyboard: Space/Enter reveal then advance, K, R.

**Games.** hot-seat (10 injects, 20 s clock, memory items), limit-or-bust (legal / no-go, 3 lives, 8 s, generated values either side of a limit), wx-alternate (1-2-3 rule, generated weather), jeopardy (6x5 board vs Pualani and Chester, buzz, Daily Double, confetti, all-time stats).

Full per-page audit with every hex, label, control, localStorage key and record shape: `docs/B787_AUDIT_v2.40.md` in the repo (built this session from the audit report).

## 2. Page map: B787 file to A330 file

Filenames are kept identical wherever the concept survives, so every internal link, the sw manifest, the assist MAP, and the view.html whitelist port without edits.

| # | B787 file | A330 file | Tile title on index | A330 data source | Status at launch |
|---|---|---|---|---|---|
| 1 | phase_flows.html | phase_flows.html | Flight Phase Flows | data/flows.json (15 phases, 143 steps, 11 checklists, 80 callouts, verified) reshaped into the B787 phase record | Full |
| 2 | ioe.html | ioe.html | OE Workbook Trainer | 787-321-330 Fleets OE Workbook PDF, A330 sections only, in AS - Boeing 787 | Full |
| 3 | flows_quiz.html | flows_quiz.html | Flows Trainer | data/flows.json plus A330 PAX Interactive Flows PDF for x,y dot placement | Full |
| 4 | cdu_preflight.html | mcdu_preflight.html | MCDU Preflight (PF) | A330P FCOM R17 PRO-NOR-SOP cockpit preparation and FMGS pages; 1-page handout PDF built by script | Full |
| 5 | triggers.html | triggers.html | Triggers | FCOM PRO-NOR-SOP trigger events plus PRC; 30-record target | Full |
| 6 | limitations.html | limitations.html | Limitations | data/limitations.json, 168 verified; `mem:true` subset defines the drill set | Full |
| 7 | memory-items.html | memory-items.html | Memory Items | data/memory_items.json, 10 [MEM] procedures, 11 entries, visually verified | Full |
| 8 | systems_quiz.html | systems_quiz.html | Systems Quiz | data/systems.json, empty bank, categories placeholder | Engine live, bank pending Ryan |
| 9 | fom_quiz.html | fom_quiz.html | FOM Quizzer | FOM 125.1 shared; B787 fom_q bank scrubbed of 787-only items, A330 items added from FOM_DELTA and fleet banners | Full |
| 10 | weather.html | weather.html | Weather | FOM 125.1 weather and alternate rules, A330 figures | Full |
| 11 | podcast.html | podcast.html | 330 Flight Deck Notes - Podcast | Episode list empty at launch; audio on a media origin (section 6) | Shell live, episodes later |
| 12 | pwa.html | pwa.html | ALPA - Pilot Working Agreement | 2023-pwa.pdf, pwa_index.json, pwa_toc.json, pwa_prompt.json copied verbatim | Full, day one |
| | pwa_pdf.html | pwa_pdf.html | (from pwa) | same | Full |
| | view.html | view.html | (handout viewer) | whitelist: A330_Weather_Requirements.pdf, A330_Memory_Limitations.pdf, A330_QRH_Memory_Items.pdf, A330_OE_Workbook_Answered.pdf | Full |
| | hot-seat.html | hot-seat.html | (game from memory-items) | memory_items.json plus scenario map | Full |
| | limit-or-bust.html | limit-or-bust.html | (game from limitations) | limitations.json NUM and BOOL subsets | Full |
| | wx-alternate.html | wx-alternate.html | (game from weather) | generated, FOM 8.2.3 rule unchanged | Full |
| | jeopardy.html | jeopardy.html | (game from systems) | pool derived from systems.json | Engine live, empty until bank lands |

Tile order, tints and subtitles follow the B787 index exactly: tile 1 `.phase`, tile 11 `.podcast`, tile 12 `.alpa`. Subtitle text is rewritten for the A330 counts (for example "160 memory-flagged and reference limitations, FCOM R17 LIM") and regenerated by the build script from the data files so the numbers never drift.

## 3. Palette map: Alaska hex to Hawaiian hex

Source palette is the Auro design-token Hawaiian theme already verified 2026-09-01 (purple #463C8F, fuchsia #CE0C88, coral #EE453D, deep fuchsia #831A57, pale purple #EAE5F4, success #447A1F). Ryan's decision: Hawaiian only, coral never as body text on white.

The map is role-based, applied by `build_scripts/apply_palette.py` across every HTML, JS and inline-style occurrence. Two B787 shades that were accidental variants (navy #01416e vs #01426A, atlas #00679c vs #0074C8) collapse to one Hawaiian value each. Semantic colors (red, amber, success green, per-phase flow colors, podcast tab accents, Jeopardy board blue and gold) are kept as they are, because they carry meaning, not brand.

| Role | B787 hex | Where it appears | A330 hex | Note |
|---|---|---|---|---|
| Brand dark (banner, borders, buttons, modal header) | #01416e, #01426A | everywhere | #463C8F | purple |
| Brand dark hover | #00679c (index gate hover) | buttons | #31295C | purple bold |
| Link and accent (atlas) | #00679c, #0074C8, #007cba | links, result borders, hover | #CE0C88 | fuchsia |
| Accent hover | #007cba on #01416e | search buttons | #831A57 | deep fuchsia |
| Secondary accent (blue) | #00b2d6 | mode borders, mini hover | #E26DB8 | fuchsia tint |
| Pale tint (breeze) | #bfe9f4 | borders, dividers, chips | #EAE5F4 | pale purple |
| Page background (ice) | #E8F3FA, #E8F2F9 | family A bodies, assist panel | #F4F1F9 | purple tint, 3% |
| Pale page (family D) | #eef4f8 | phase_flows, mcdu | #F1EEF6 | |
| Signature accent as text on dark (lime) | #b1d887 | banner title, version lines, modal header text, footer links on dark | #FF9080 | coral tint, 4.3:1 on #463C8F, passes AA large and normal at 20 px 700 |
| Signature accent as fill on light (lime) | #b1d887 | `.phase` tile, gear hover, progress fills, marks, answer borders | #FFC9BF | coral pale, text on it stays purple |
| Signature accent as text on light | #b1d887 in `.ps-logbtn` etc. | rare | #97322A | coral text-safe |
| Dark drill background | #01172b | family B body | #1A1630 | purple black |
| Dark drill panel | #062b46 | cards | #2A2440 | |
| Dark drill panel 2 | #0a3556 | buttons | #332E44 | |
| Dark drill line | #13486e | borders | #453F58 | |
| Dark drill muted | #8fb3cf | secondary text | #C3BED0 | |
| Dark drill breeze | #00C7E6 | chips, category on | #E26DB8 | |
| Dark drill green (answers, got it) | #C0E585 | answers | #8EC891 | success tint, kept green because it means correct |
| Dark ioe bg / card / line | #0b1c2c, #12293d, #1e3d57 | ioe | #1A1630, #2A2440, #453F58 | same family as drills |
| Systems quiz dark | #0a0d12, #141820, #1c2230, #2a3344 | systems | #15131C, #211D2E, #2A2440, #453F58 | |
| Podcast tile | #d6ecf7 | index | #FDF1F8 | pale fuchsia |
| ALPA tile | #efe3f5 | index | #EAE5F4 | pale purple |
| Jeopardy tint | #eaf4fc to #dcecf8 | body gradient | #F4F1F9 to #EAE5F4 | |
| Overlay scrim | rgba(1,23,43,.72) | modals | rgba(21,19,28,.72) | |
| Shadows | rgba(1,65,110,.25), rgba(1,23,43,.45) | | rgba(70,60,143,.25), rgba(21,19,28,.45) | |
| Success (light) | #00805E, #4a7a1f | | #447A1F | Hawaiian success |
| Red, amber, magenta, flow phase colors, podcast tab accents, Jeopardy #060CE9 / #f3c44b | unchanged | | unchanged | semantic |

Every pair is validated at build by `build_scripts/contrast_check.py` (WCAG AA: 4.5:1 normal text, 3:1 large text and UI). Any pair that fails is adjusted toward the nearest passing tint and the change logged in `docs/PALETTE_MAP.md`. The two open tuning points are the coral tint on purple (#FF9080 computed at 4.3:1) and the pale coral fill for `.phase` (purple text on #FFC9BF, computed at 6.1:1). Both pass; both get a visual check on the phone.

## 4. String map

Applied by `build_scripts/apply_strings.py`, in this order, whole-word and case-sensitive:

| B787 string | A330 string |
|---|---|
| `B787 STUDY PORTAL`, `B787 Study Portal` | `A330 STUDY PORTAL`, `A330 Study Portal` |
| `AS 787 Study`, `AS 787 Study Portal` | `HA 330 Study`, `HA 330 Study Portal` |
| `787 Flight Deck Notes` | `330 Flight Deck Notes` |
| `B787` (fleet label in profile, chips, prompts, page h1s) | `A330` |
| `as787pilot.app` | `ha330pilot.app` |
| `as787_` (cookie and localStorage prefix) | `ha330_` |
| `b787-core-`, `b787-audio-` (cache names) | `ha330-core-`, `ha330-audio-` |
| `b787state`, `b787dark`, `b787_sysquiz_v2`, `b787_jeopardy_stats` | `a330state`, `a330dark`, `a330_sysquiz_v2`, `a330_jeopardy_stats` |
| `B787_night.jpg` | `A330_hero.jpg` |
| `alaska_787.svg`, Alaska logo base64 PNG | `hawaiian_a330.svg`, Hawaiian logo base64 PNG (Ryan supplies) |
| `FCOM R10`, `QRH R7`, `FCTM R9`, `MEL R5`, `FOM 125.1` | read from `manuals.json` at build: `FCOM R17`, `QRH R35`, `FCTM R5`, `MEL R59`, `FOM 125.1`, plus `AFM 11 AUG 26` |
| `CDU`, `cdu_preflight.html`, `cdu` corpus key | `MCDU`, `mcdu_preflight.html`, `mcdu` |
| `IOE Workbook Trainer`, `OE Workbook V3, 787 only` | `OE Workbook Trainer`, `Fleets OE Workbook, A330 sections` |
| `Fleet is B787.` | `Fleet is A330.` |
| Default seat `CA` | `FO` |
| `ryan.pettit@alaskaair.com?subject=B787%20Study%20Portal` | same address, `A330%20Study%20Portal` |
| BUILD `v2.40` | `v1.0` |
| Banner alt `Alaska Airlines` | `Hawaiian Airlines` |

What does not change: Pualani as the assistant name and avatar (`/assets/pualani-2001.png`, copied), the podcast hosts Pualani, Chester, Otto, the `@alaskaair.com` gate, the owner address for the portal log, the provider list, the tax table, the HNL/SEA domicile segment, the collector URL (see section 6 for the one-field change).

The index footer revision table and every page's `.src` revision label are generated from `manuals.json` so the strings never go stale; the B787 hand-edited them per page and drifted (index said Ver 2.27 while BUILD said v2.40).

## 5. Data layer: record shapes the engines consume

Data is external (`data/*.json`) per locked decision 3, but in the exact B787 record shapes so the engine code is untouched. Where the verified A330 files already exist in a richer shape (limitations.json with `verbatim`, `confidence`, `fleet`), a build step projects them to the engine shape and keeps the rich file as the source of truth. Every record carries `src` (manual | sop | technique) and `fleet` (pax | frtr | both) per decisions 2 and the PAX rule; the engines filter `fleet !== 'frtr'` by default.

| Engine | B787 shape (kept) | A330 source file | Projection |
|---|---|---|---|
| limitations drill, limit-or-bust | `{s,q,a,ref,mem,src}` and `NUM {p,v,u,k,ref,step,spread}` / `BOOL {p,legal,ref,lim}` | data/limitations.json (168) | `s`=system, `q`=parameter phrased as a question, `a`=limit + condition, `mem` from the memorize flag Ryan marks, `src`=verbatim. NUM/BOOL derived from numeric vs prohibited items. |
| memory items, hot-seat | `{name,ref,cond,fctm?,steps:[{t:'n'|'s'|'b',n?,h}]}` | data/memory_items.json (11) | `name`=procedure, `ref`=Airbus ident, `cond` from evidence, `steps` from `actions` with action text bolded; scenario map `SCN` written per procedure. |
| triggers | `{s,who,q,a,tech,ref,src,flow:{n,i[]}}` | new data/triggers.json | 30 records from FCOM SOP and PRC. |
| phase flows | `{id,label,kind,title,src,sections:[S(h,color,items,cite,appr)]}` with box/trig/cl builders | data/flows.json | reshape 15 phases; NORMAL list is the A330 SOP sequence; NON-NORMAL list: Go-Around, Diversion, ETOPS Divert, Oceanic Contingency, Depress, Rejected T/O, Eng Fail T/O, Emer Descent, Holding, Memory Items, Limitations; approach toggle ILS / RNP / NPA (FLS) and CAT I / II / III. |
| flows trainer | `FLOWS [{n,who,ref,phase,items:[{item,act,role,x,y,d,cl,...}],shape,mnemonic,trig}]` | data/flows.json plus the Interactive Flows PDF | x,y placed on the A330 cockpit map SVG (viewBox 300x437 kept; base image swapped). Role set CA/FO/BOTH/PF/PM; IRO retained for augmented crews. |
| OE workbook | `{id,sec,secTitle,group,coi,status,kind,topic,q,a,qOrig,detail,ref,quote,note}` | new data/oe.json | from the Fleets OE Workbook, A330 sections; `verify_oe.py` (B787 verify_ioe generalized) checks every quote against the extracts. |
| systems quiz, jeopardy | `{id,system,q,a,src}` plus `SOURCE_DETAIL {id:[{ref,quote,note}]}` | data/systems.json (empty) | category list read from the file's `systems` array so Ryan's bank defines the filter pills. |
| FOM quizzer | manifest `{rev,generated,chapters:[{chapter,name,file,count}]}` plus `fom_q/chNN.json` | B787 fom_q copied, scrubbed, extended | FOM_REBUILD.md process, fleet scrub replaces the 787-only scrub. |
| weather, wx-alternate | `{cat,ref,q,a:[html],src,tbl?}` | new data/weather.json | A330 takeoff alternate distance, ETOPS figures from FOM 6. |
| MCDU preflight | static page plus corpus | FCOM PRO-NOR-SOP | SVG page-flow diagram regenerated for the MCDU pages. |
| podcast | `EPISODES [{n,group,title,topic,len,audio,quiz}]` | data/episodes.json (empty) | tabs and accents unchanged. |
| PWA | pwa_index.json, pwa_toc.json, pwa_prompt.json | copied | prompt fleet string only. |
| corpus/*.json | `{title,page,built,docs:[{t,x,r}]}` | generated | `build_scripts/build_corpus.py` derives all nine from data/*.json so Search this section and Ask Pualani work the day a page ships. |

## 6. Infrastructure carried over, and the four things that must differ

Carried over unchanged: portal-settings.js, assist.js, sw.js, site.webmanifest (name and colors mapped), robots.txt, CNAME, view.html, the favicon set (A330 icons already in `assets/icons/`, moved to the B787 root filenames), offline-manifest.json (regenerated by `build_scripts/build_offline_manifest.py` with real byte counts, fixing the B787's stale entries and its missing `B787_Aircraft_Setup.pdf`).

1. **Audio origin.** Locked decision 6 keeps mp3s out of the content repo. A second repo `AlohaFlyer/A330-media` publishes to `media.ha330pilot.app`. sw.js gets one addition: the audio tier fetches from that origin (CORS enabled by Pages), cached under `ha330-audio-`. The Offline modal, progress bars and podcast offline checkbox behave identically. Until the first episode exists the audio tier reports 0 files, same as the B787 behaves with an empty manifest.
2. **Unlock log collector.** The Apps Script deployment stores rows keyed on timestamp plus email. The A330 index posts the same rows with one extra field `portal:"ha330"`. Ryan redeploys the script once with that column (or accepts a shared log; the owner view then shows both portals). This is the only non-repo change.
3. **Banner logo and hero photo.** Two binary assets Ryan supplies: a Hawaiian Airlines wordmark PNG rendering at 30 px height (inlined as base64 like the Alaska one) and an A330 hero photo at 1275x373 aspect (the B787 `footer .plane` ratio). Placeholders ship in v1.0 so nothing blocks.
4. **Flows Trainer cockpit image.** The B787 embeds a 1.26 MB base64 cockpit JPEG. The A330 uses `assets/a330_cockpit.jpg` from the "A330 All Panels FULL SIZE.pdf" render, referenced by URL, listed in the offline manifest. No visual difference.

## 7. Build order and sessions

Each step is one Cowork session, ends with a push, a Pages deploy, a phone check, and a register note. Version footers start at Ver 1.0 per page and increment by 0.1 per file change, same convention as the B787.

| Step | Scope | Exit test |
|---|---|---|
| 1 | Repo reset: delete every html/css/js from the first attempt, keep data/, docs/, manuals.json, CNAME, icons. Copy the B787 tree minus mp3s, PDFs and corpus. Run apply_palette.py and apply_strings.py. Push. | ha330pilot.app renders the B787 layout in purple with B787 data still inside. CSS parity diff empty. |
| 2 | Shared chrome: index (tiles, gate, footer from manuals.json, gear), portal-settings.js, assist.js, sw.js, manifests, icons, placeholders for logo and hero. | Gate, settings modal, offline core download, force refresh, install to iPhone home screen all work. |
| 3 | Limitations, memory items, hot-seat, limit-or-bust from the verified JSON. Handout PDFs built by script and wired through view.html. | Drill engines identical in behavior; grounding verify passes; corpus generated. |
| 4 | Phase flows and flows trainer from flows.json; cockpit map. | 15 phases navigable, seat/duty/approach toggles, checklist overlays, poster mode. |
| 5 | Triggers, weather, wx-alternate, MCDU preflight with handout. | 30 triggers, weather set, generated games, corpus. |
| 6 | OE Workbook Trainer from the Fleets OE Workbook A330 sections; verify_oe.py; answered-workbook PDF. | All cards answered or marked "ask the check airman"; every quote verified. |
| 7 | FOM quizzer: copy fom_q, scrub 787-only, add A330 items from FOM_DELTA; systems quiz and jeopardy engines with empty bank; podcast shell; media repo and sw audio origin. | FOM chapters pass grounding; systems and podcast shells render their empty state cleanly. |
| 8 | PWA pages copied verbatim; Ask Pualani end to end on all nine corpus pages; final parity pass; docs (MANUAL_VERSIONS, REVISION_PROCESS, CITATION_INDEX regenerated). Ver 1.0 tagged. | Section 8 verification all green; register task closed. |

Later, on Ryan's inputs: systems bank drop-in (data only), podcast episodes (pipeline already in build_scripts), logo and hero swap (two files).

## 8. Verification (every step, and the final gate)

1. **CSS parity diff.** `build_scripts/parity_diff.py` extracts every `<style>` block, inline `style=` attribute, and CSS string in JS from the B787 file and its A330 twin, applies the hex and string maps to the B787 side, normalizes whitespace, and diffs. Must be empty per page. Runs pre-commit.
2. **DOM parity.** Same script compares the tag and class skeleton (element names, class lists, ids) with text nodes stripped. Must be empty for chrome pages (index, settings modal, assist panel, drill pages); data-driven pages are compared on their first-card render.
3. **Screenshot pairs.** Playwright renders each page pair at 390x844 and 1280x800, converts both to greyscale, and reports structural similarity. Threshold 0.97; below it is a defect. Contact sheets are saved to `docs/parity/` and one composite is sent to Ryan per step.
4. **Runtime harness.** The B787's engines get the A330 data through the same checks used in the first attempt (pass3_runtime.py, playwright_smoke.py, reused as-is).
5. **Grounding.** `verify_grounding.py` per bank: every `src` quote is a literal substring of the matching extract in `HA - Airbus A330/extracts`. Zero tolerance.
6. **Contrast.** `contrast_check.py` over the palette map. All pairs AA.
7. **PWA.** Lighthouse installable, service worker registered, offline reload of every page after "Make Available Offline".
8. **Phone.** Ryan opens the portal on the iPhone, installs it, runs one drill offline. His word is the last check.

## 9. Inputs from Ryan (none blocking step 1)

- Hawaiian Airlines wordmark PNG for the banner (30 px height render) and an A330 hero photo.
- Systems quiz bank and category list, any format; the engine reads `data/systems.json`.
- Confirmation the 787-321-330 Fleets OE Workbook in AS - Boeing 787 is the current A330 OE workbook.
- One Apps Script redeploy adding the `portal` column, or a nod to share the log.
- Memorize-set marking on the limitations bank (which of the 168 are "know cold" for the drill). Default until then: every item with `confidence: VERIFIED` and a numeric limit.

## 10. What this plan deliberately does not do

- No new pages, features, or layouts that the B787 does not have.
- No Alaska blend in the palette.
- No B787 study content anywhere in the A330 data.
- No manual PDFs or extracts in the public repo.
- No inline data blobs; every bank is a JSON file the revision skill can index.
