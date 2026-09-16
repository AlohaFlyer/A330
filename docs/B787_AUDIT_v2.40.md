# B787 Study Portal structural audit, v2.40 (commit ff78f9a, 2026-09-11)

Reference for the A330 clone. Every hex, label, control, localStorage key and record shape as shipped. Companion to A330_PORTAL_PLAN_v2.0.md.

## Shared chrome
- Home icon `.ps-homebar > a.ps-home` on every subpage: 34x34, radius 9, white, 2px #01416e border, shadow 0 1px 4px rgba(1,23,43,.2); hover inverts; 40x40 under 480px, 44x44 under 600px (portal-settings.js).
- Every page ends with `<script src="/portal-settings.js" defer>` and `<script src="/assist.js" defer>`; sw.js injects them into any HTML response that lacks them.
- Footer pattern on subpages: hero img 380px max 60%, mailto `ryan.pettit@alaskaair.com?subject=B787%20Study%20Portal%20-%20<Page>`, right-aligned 11px "Ver x.y". Dark pages color #b1d887, light pages #01416e. Only index and fom_quiz use the `.ver` class (rewritten at runtime to BUILD).

## index.html
- Head: robots noindex, favicon.ico/32/16, apple-touch-icon, site.webmanifest, app title "AS 787 Study", theme-color #01416e.
- Vars: --midnight #01416e, --atlas #00679c, --blue #00b2d6, --breeze #bfe9f4, --ice #E8F3FA, --good #b1d887.
- Banner full bleed, padding 12px max(20px, calc((100% - 560px)/2 + 10px)); logo PNG base64 149x44 at 30px; span #b1d887 20px 700 letter-spacing 1px "B787 STUDY PORTAL".
- Gate: h2 "Company Email Address" 22px; input placeholder first.last@alaskaair.com, 2px midnight border radius 6; button "Enter"; error #C0392B "Enter your @alaskaair.com email address."; regex ^[^\s@]+@alaskaair\.com$; cookie as787_access 5y; localStorage as787_email, as787_log_queue (cap 500), as787_log_counts.
- Menu: max 560, gap 14, padding 24px 10px; tiles white, 2px midnight border, square, padding 18px 14px, 16px 700, small 12px #555, arrow 22px; hover midnight/white; .phase bg var(--good), .podcast #d6ecf7, .alpa #efe3f5.
- Tiles in order: Flight Phase Flows; IOE Workbook Trainer; Flows Trainer; CDU Preflight (PF); Triggers; Limitations; Memory Items; Systems Quiz; FOM Quizzer; Weather; 787 Flight Deck Notes - Podcast; ALPA - Pilot Working Agreement.
- Footer: img.plane 360px max 82% aspect 1275/373 radius 6; table.revtbl 11px (FCOM R10, QRH R7, FCTM R9, FOM 125.1, MEL R5 with Drive links); .footrow contact + #gearSlot; .ver right 11px 700.

## portal-settings.js (BUILD v2.40)
- Modal .ps-modal white 2px #01416e max 560; header #01416e text #b1d887 "PORTAL SETTINGS"; scrim rgba(1,23,43,.72).
- Sections: Your profile (Seat CA/FO, Domicile HNL/SEA, Date of hire, "Fleet is B787."), Tax assumptions (state select 2026 top marginal table, state effective rate + Reset, federal slider 0-50), Build (readonly build, Force refresh), Ask Pualani (provider claude/openai/gemini/grok, key Save/Forget, model Load, "Keys stay in this browser"), Offline (Make Available Offline ~22 MB, Include podcast audio ~566 MB, progress bars #b1d887), Portal log (owner only, Apps Script collector).
- Keys: pwa_seat, pwa_base, pwa_doh (2011-10-05), pwa_state (NV), pwa_state_rate, pwa_fed_rate (35), pwa_provider, pwa_key_<p>, pwa_model_<p>, as787_off_core, as787_off_audio, as787_log_key.
- API: profile(), build(), providerName(), ready(), askFull(sys,msgs), askThread, ask, MAX_IMAGES 4, prepImage (1568px PNG), emptyReason, threadsAreCheap, modelLabel. Event portalsettings:ready.
- Phone CSS under 600px: inputs 16px; .filter-btn,.gamebtn,.srcbtn,.catbtn,.navbtn,.btn,a.back,.portal-back,.reset-link,.bar a,.bar button,.mini,.ps-mini min-height 44px.
- Claude call: max_tokens 8000, cache_control ephemeral on first user text block, anthropic-dangerous-direct-browser-access.

## assist.js
- MAP: ioe, flows, cdu, triggers, limitations, memory, systems, fom, weather -> /corpus/<key>.json.
- BM25 k1 1.5 b 0.75, title x2, phrase bonus 5; modes Keywords/Exact/Phrase (as787_assist_mode).
- Launcher #as-launch fixed right 14 bottom 14, #01416e, 2px #b1d887 border, pill, 30px avatar /assets/pualani-2001.png, "Search this section".
- Panel bottom sheet max 88vh, bg #E8F3FA, top border 3px #01416e; header #01416e/#b1d887 corpus title uppercased; textarea "Ask about this section"; Offline Search full width; attach; 76px Ask Pualani disc; chips scope (green) + seat, fleet, base, state, years; results white, left 6px #007cba, mark #b1d887; answer left 8px #b1d887 "Pualani says", 12 follow-ups, Show reasoning.
- System prompt: TLDR format, excerpts only, no em dashes, units and conditions, "Not in this section."

## Family B drill pages (limitations, memory-items, triggers, weather, hot-seat, limit-or-bust, wx-alternate)
- Vars: --bg #01172b, --panel #062b46, --panel2 #0a3556, --line #13486e, --ink #eaf3fb, --muted #8fb3cf, --mid #01426A, --atlas #0074C8, --breeze #00C7E6, --green #C0E585, --amber #f2a65a, --red #ff6b6b.
- .wrap 700; card radius 8 padding 24px 22px min-height 240; .chip mono 10.5px breeze; .q 23px 700 (19px under 480); buttons 14px 600 radius 6 padding 11px 18px; .primary atlas; .knew green outline; .rev amber outline; .srcbtn atlas border breeze text; .srcpanel #01233b; .bar track/fill atlas; summary .big mono 46px green.
- Keys: Space/Enter reveal then advance, K got it, R review. handrow: handout PDF link (view.html?f=) + "GAME" link.
- limitations: 46 records {s,q,a,ref,mem,src}, drills mem:true only, "FCOM Source" panel. memory-items: 10 records {name,ref,cond,fctm?,steps:[{t,n,h}]}. triggers: 30 {s,who,q,a,tech,ref,src,flow}, categories All/Phase Triggers/Approach Setup/Go-Around Brief/Checklist Order, game 20s, trig_best. weather: 22 {cat,ref,q,a[],src,tbl?}.
- hot-seat: 10 injects, 20s, hs_best. limit-or-bust: NUM {p,v,u,k,ref,step,spread} BOOL {p,legal,ref,lim}, 3 lives 8s, lob_best. wx-alternate: 1-2-3 rule generator, aon_best.

## Other pages
- phase_flows: light vars --head #01426A, --bg #eef4f8, --ink #15314a, --cl #7b2fb0, --trig #e8590c, --say #c0392b; body.dark set; 100vh app, header + purple gate bar + multicol main (1/2/3/4 cols at 600/820/1100) + bottom nav; toggles NOTES, CA/FO, PF/PM, ILS/IAN/RNP AR, CAT I/II/III, BOTH/MINE, day/night; keys b787state, b787dark; inline phase records with box/trig/cl/S builders; NORMAL 12 phases, NON-NORMAL 11.
- ioe: vars --bg #0b1c2c --card #12293d --line #1e3d57 --accent #b1d887; 342 records; filters topic/section/kind; game 20s; ioe_best, ioe_offline; source panel with ref, quote, ICAO amber box.
- flows_quiz: light vars + --red #C8102E; grid minmax(280px,45%) 1fr max 1024; modes Sequence Drill/Full Flows/Poster; CA/FO PF/PM; phasebar; SVG map viewBox 300x437 over base64 cockpit JPEG; dot colors CA #4B2D89 FO #CE0C88 PF #007cba PM #00b2d6; trace #F9423A; Space/D keys; 24 flows.
- cdu_preflight: header #01426A, .wrap 760, cards white 1px #d7e1ea radius 10, a.pdf #0074C8, inline SVG page flow.
- systems_quiz: vars --bg #0a0d12 --surface #141820 --surface2 #1c2230 --border #2a3344 --green #4caf73 --amber #f0a030 --red #e05050 --blue #5090d0 --text #d8dde8 --text-dim #7a8899 --magenta #d060b0; sticky .portal-bar #01416e; 100-card session, filter pills with n/m, mastered/remaining/recycle, streak; b787_sysquiz_v2; 1515 {id,system,q,a,src} + SOURCE_DETAIL.
- fom_quiz: light vars + --amber #f0a030 --red #d9534f; .wrap 640; card radius 12; Game Off/On with 10/15/20/30s timer; chapter pills; fom_mastered_v1; keys Space/K/M; ?chapter= ?game=1; manifest fom_questions.json + fom_q/chNN.json.
- podcast: body #01172b, .wrap 760, .bar #01426A title #b1d887; tabs Systems #3a9ee0/#062b46, Procedures #a07bd6/#1d1736, FFS #e0687a/#2c1218, Maneuvers #e07b3a/#301c0d, LOFT #3ecf8e/#0f2e22, Operations #2bb59a/#052b25, FOM #c58be0/#241a33, Review #e0a648/#2c2310; episode rows left 4px accent; heard/offline checkboxes; fdn_tab, fdn_heard_<n>, fdn_offline_<n>; ?ep=N.
- pwa: family A, .wrap 820, banner "ALPA PILOT WORKING AGREEMENT"; textarea, Match segment, Offline Search, Attach, 96px Pualani disc, chips, threads, results with "Open PDF p.N", modal, TOC details; pwa_index.json {meta,toc,docs[{p,s,t,cp,x}]}, pwa_prompt.json v4; router then 140k-char sections with cache_control.
- pwa_pdf: sticky bar, iframe 2023-pwa.pdf#page=N&view=FitH, 340px index panel, pwa_toc.json.
- view.html: whitelist B787_Weather_Requirements, B787_Memory_Limitations, B787_QRH_Memory_Items, B787_IOE_Workbook_Answered; iframe #view=FitH.
- jeopardy: vars --board2 #060CE9 --tile #0a1fd6 --tilehi #1838ff --gold #f3c44b; 6x5 board; vs Pualani/Chester; buzz 2.5s; Daily Double; b787_jeopardy_stats.

## Infrastructure
- sw.js VERSION v4, caches b787-core-v4 / b787-audio-v4; network-first html/json/js/css, cache-first else; messages CACHE_CORE/CACHE_AUDIO/CLEAR_CORE/CLEAR_AUDIO/STATUS; replies PROGRESS/DONE/CLEARED/STATUS; 6 lanes core 4 audio; fallback /index.html then inline 503.
- offline-manifest.json {version,built,coreBytes,audioBytes,core[{u,b}],audio[{u,b}]}; stale bytes for assist.js/portal-settings.js; lists missing B787_Aircraft_Setup.pdf.
- site.webmanifest name "AS 787 Study Portal" short "AS 787 Study", icons 192/512 any maskable, theme #01416e, bg #E8F3FA, standalone.
- corpus/*.json {title,page,built,docs[{t,x,r}]}: limitations 46, memory 10, flows 226, triggers 30, systems 1515, fom 438, weather 22, cdu 18, ioe 342.
- build_scripts: citation_index.py, manual_diff.py, build_ioe_pdf.py, verify_ioe.py, parse_ep.py, master_ep.sh; docs: CITATION_INDEX, MANUAL_VERSIONS, QUARTERLY_UPDATE, REVISION_PROCESS.

## Inconsistencies collapsed in the A330 clone
1. Two navies #01416e / #01426A and two atlases #00679c / #0074C8 -> one value each.
2. Two greens #b1d887 (brand) / #C0E585 (correct) -> brand coral tint vs success green.
3. Version strings hand-edited per page -> generated.
4. Dead CSS (a.back, a.portal-bar, .banner a.home) -> removed only if parity_diff treats it as no-op; otherwise kept.
5. Missing B787_Aircraft_Setup.pdf in manifest -> manifest generated from disk.
