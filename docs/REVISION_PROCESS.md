# Revision Process

How a new manual revision gets from the inbox to the live portal. Follow it in
order. Every step has a done-criterion you can check.

The whole point of this sequence is that a revision sweep is **scoped and
mechanical**, not a re-read of the portal. The citation index tells you exactly
which pages and items depend on the sections that changed. You re-verify those
and nothing else.

---

## 0. Precondition

Work from the repo root. Every tool here resolves its paths from the current
working directory, so `cd` to the repo root once and stay there.

```
cd <repo root>
```

---

## 1. Intake and verification

1. The new manual lands in `_incoming`.
2. Verify the revision **off the document itself**, not off the filename or the
   email that carried it.
   - Trap: the HAL A330 FCOM and FCTM put no revision number on the cover, only
     an issue date. The number is on the Revision Summary page, around page 45.
   - Trap: some manuals publish no revision number at all (AFM, AFM-SUPP, PRC,
     NPC-CB). Those are identified by issue date. Never invent a revision number
     to fill the field.
3. Rename to `<FLEET>_<MANUAL>_R<rev>.pdf`, or `_<YYYY-MM-DD>.pdf` when there is
   no revision number.
4. File it to the fleet folder or `_shared_manuals`. Move the prior revision to
   `_superseded` as the single fallback.
5. Regenerate the `.md` extract and verify the page count.
6. Log it in `MANUAL_LOG.md`.

**Done when:** the new PDF and its extract are filed, exactly one prior revision
remains as fallback, and `_incoming` is empty.

**Never:** commit the PDF or the extract to this repo. See `.gitignore`.

---

## 2. Update the single source of truth

Edit `manuals.json` at the repo root. Change `revision` and `date` for that
manual code. Leave `last_vetted` alone for now: it still records the last
revision a human actually checked the content against, and it is about to be
stale on purpose.

`manuals.json` is the **only** place a displayed revision string lives. Page
footers render from it. If you find a revision hardcoded in HTML, that is a bug;
fix it by pointing the footer at `manuals.json`.

**Done when:** `manuals.json` parses as JSON and shows the new revision and date.

---

## 3. Rebuild the citation index

```
python3 build_scripts/citation_index.py
```

This walks `data/*.json` and every `*.html` and rewrites `docs/CITATION_INDEX.md`
and `docs/citation_index.json`.

Rebuild it **before** the diff, every time. A stale index is the single most
dangerous failure mode in this process, because it produces a short checklist
that looks like good news.

**Done when:** the tool reports a non-zero citation count and both output files
have today's timestamp.

---

## 4. Scope the sweep from the differences document

Read the publisher's list of changed sections for that revision. Turn it into
section codes, then:

```
python3 build_scripts/manual_diff.py A330P_FCOM 5.4 27-10 ABN-17
```

or, for a long list:

```
python3 build_scripts/manual_diff.py A330P_FCOM --sections-file changed.txt
python3 build_scripts/manual_diff.py A330P_FCOM --sections-file changed.txt --json
```

Matching is by section prefix on segment boundaries, so `5.4` catches `5.4.1`
and `5.4.2` and does not catch `5.41`.

The output is the re-verify checklist: every page and item id that cites those
sections. That list is the sweep.

**Done when:** you have a written checklist with a count on it.

---

## 5. Re-verify each item on the checklist

For every item, open the new extract, find the cited section, and confirm the
item still matches.

Rules:

- **Only `src: "manual"` items are re-verified against the manual.** Items with
  `src: "sop"` or `src: "technique"` are not the manual's to change. If a manual
  change makes an SOP or technique item wrong, that is a human decision, so flag
  it, do not silently rewrite it.
- Never cite a section without a grep hit against the actual extract.
- PAX facts come from the A330P books, freighter facts from the A330F books.
  Never cross-cite.
- If a number changed, change the number **and** the `verbatim`, together. An
  answer updated without its evidence is exactly what `verify_grounding.py`
  catches, and catching it there means it already shipped once.
- If the cited section was renumbered, update the `ref`.
- If the cited section was deleted, do not guess a replacement. Flag the item.

**Done when:** every line on the checklist is ticked or explicitly flagged.

---

## 6. Run the gates

```
python3 build_scripts/provenance_lint.py
python3 build_scripts/verify_grounding.py data/*.json
python3 build_scripts/citation_index.py
```

All three must pass. `provenance_lint.py` exits non-zero if any item lacks
`src` or `fleet`, or claims `src: "manual"` without a `ref`.
`verify_grounding.py` exits non-zero if a manual-sourced answer says things its
own cited text does not support. Re-run `citation_index.py` last because step 5
may have changed refs.

**Done when:** all three exit 0.

---

## 7. Stamp and publish

1. Set `last_vetted` in `manuals.json` to today's date for the manual you swept.
   This is the only step that records that a human, not a script, checked it.
2. Update the row in `docs/MANUAL_VERSIONS.md`.
3. Commit. The diff should contain `manuals.json`, the touched `data/*.json`,
   the regenerated `docs/` files, and nothing with a `.pdf` or `_extract.md` in
   the path.
4. Publish.
5. Spot check a live page footer and confirm it shows the new revision.

**Done when:** the live site footer shows the new revision and `last_vetted` is
today.

---

## Failure modes worth remembering

| Symptom | Real cause |
| --- | --- |
| Diff reports "nothing to re-verify" on a big revision | Index was never rebuilt, or was rebuilt from a different directory |
| Footer shows the old revision after publish | A revision string is hardcoded in HTML instead of read from `manuals.json` |
| An item's number is right but its quote is not | Step 5 was done on the answer only; run `verify_grounding.py` |
| A freighter limit appears in PAX study content | An item has the wrong `fleet`, or a ref crossed A330P and A330F books |
| Sweep silently rewrote a personal technique | An item was mis-tagged `src: "manual"` |
