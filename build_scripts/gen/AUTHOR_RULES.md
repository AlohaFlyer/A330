# Systems bank authoring rules (A330 REV1 System Operational Knowledge Guide, 24JUN2024)

Input: one chunk file of the guide, sections headed "### NAME [REF] (guide page N) CATEGORY: X", bullets "- Bk (pN): text", sub-bullets "o ...", sub-sub "- ...".

Output: a JSON array written to the output path given. Each element:
{"id": "<prefix>-NNN", "system": "<CATEGORY exactly as given>", "q": "...", "a": "...", "src": "REV1 Systems Guide p.N · <REF>", "quote": "<the bullet text plus its sub-bullets verbatim, joined with ' · '>", "sec": "<section NAME>", "b": "Bk"}

Prefix: first two letters of the category lowercased by this table: Air Cond and Press=air, Auto Flight=afs, Communications=com, Electrical=ele, Fire Protection=fir, Flight Controls=fct, Fuel=fue, Hydraulics=hyd, Ice and Rain=ice, ECAM and Displays=eca, Landing Gear=lg, Navigation=nav, APU=apu, Power Plant=eng. Number sequentially within your chunk starting at the START number given (e.g. air-001).

Coverage: at least ONE question per top-level bullet. When a bullet has several distinct facts in its sub-bullets (a list of valves that close, a numbered power hierarchy, three modes), write one question per distinct fact, so a bullet may yield 2 to 6 questions. Every fact in the guide should be askable. Do not invent anything not in the text; do not add facts from your own A330 knowledge. If a bullet is empty or truncated in the source (e.g. "The igniters will automatically come on in the following cases:" with nothing under it), skip it and list it in a final "skipped" note in your reply.

Quality rules (a script checks these, so obey them):
- q: at most 25 words, exactly one ask, ends with "?". No "what do you think", no compound questions.
- a: at most 20 words, a bare fact. A yes/no question gets "Yes." or "No." first, then the fact. Numbers carry units and conditions (e.g. "25,000 ft climbing, 23,000 ft descending").
- No hedges (probably, generally, usually, may be), no other-fleet comparisons (no 787, 737, A321), at most one parenthetical per q and per a.
- Never use em dashes anywhere. Use commas or periods.
- Keep the guide's own terminology and switch names (Pb, pb-sw, FMGEC, CPC, TLA). Spell out where the guide spells out.
- Active recall, not multiple choice. Vary stems: what, how many, when, which, what happens if, what does X do.
- quote must be verbatim from the chunk (fix only obvious line-break hyphenation and doubled spaces). Keep the sub-bullets in the quote.

Reply with: total items, per-section counts, and the skipped list. Do not paste the JSON into the reply.
