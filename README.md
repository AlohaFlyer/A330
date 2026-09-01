# A330 Study Portal

Study material for one A330 First Officer returning to the fleet. It is a
personal revision aid, not a company publication and not an authoritative
source. **The manuals always win.** If anything here disagrees with the FCOM,
QRH, FCTM, MEL, AFM, PRC, FOM or FODM, the manual is right and this repo has a
bug worth fixing.

The site is gated client side. That gate keeps the page out of casual view and
search results. It is not security and it is not a licence to host manual
content: it stops a stranger stumbling in, nothing more. Manual PDFs and their
text extracts are proprietary company documents and are never committed here.
See `.gitignore`.

## Architecture

**`manuals.json` drives every displayed revision.** One file at the repo root
holds the title, revision, issue date, fleet and `last_vetted` date for all
fifteen manuals. Page footers render from it. No revision string is ever typed
into HTML. The predecessor B787 portal hardcoded revisions into page footers,
which meant a revision bump was a find-and-replace across dozens of files, and
the footers drifted out of agreement with each other within a couple of cycles.
One file, one truth, one edit. Where a manual publishes no revision number
(AFM, AFM-SUPP, PRC, NPC-CB), `revision` is `null` and the issue date carries
the identity. Never invent a revision number to fill the field.

**All content lives in `data/*.json`, never inline in HTML.** Every quiz
question, flow step and flashcard is data. Pages are renderers. This is the
other lesson from the B787 portal, where content was authored directly into
markup: nothing could be linted, nothing could be indexed, and a manual revision
meant reading every page by eye to find what might be affected. Content as data
means the whole corpus is machine-checkable and machine-searchable, and a page
can be redesigned without touching a single fact.

**Every item carries `src` and `fleet`.** `src` is `manual`, `sop` or
`technique`. `fleet` is `pax`, `frtr` or `both`. These are not decoration, they
are what makes a revision sweep safe. `src` says who owns the fact: a manual
fact must be re-verified when its manual changes, an SOP note answers to the
company, and a technique is a personal method that no manual revision has any
business rewriting. `fleet` keeps A330 passenger content and A330 P2F freighter
content apart. PAX is the default view; freighter content stays available behind
a toggle and is never deleted and never blended in. PAX facts cite the A330P
books, freighter facts cite the A330F books, and the two never cross-cite. Any
item with `src: "manual"` must also carry a `ref` naming the section it came
from, and `provenance_lint.py` fails the build if it does not.

**Sweeps touch only `src: "manual"` items.** When a revision lands,
`citation_index.py` maps every citation in the repo, JSON banks included, to the
manual sections it depends on. `manual_diff.py` then turns the publisher's list
of changed sections into the exact re-verify checklist: these pages, these item
ids, nothing wider. A sweep is scoped and mechanical, not a re-read. Items that
are not `src: "manual"` are outside the sweep by design. If a manual change makes
an SOP or technique item wrong, that gets flagged to a human, never silently
rewritten.

**Audio lives in a separate repo.** Podcast and drill audio is large, binary and
regenerated often. Keeping it here would bloat every clone for no benefit. This
repo stays text.

## Layout

```
manuals.json              single source of truth for displayed revisions
data/*.json               all study content: quiz, flows, cards, limits
assets/palette.css        semantic design tokens
build_scripts/            the four gates and the index
docs/                     process, registry, generated citation index
```

## Build tooling

Run everything from the repo root. All four tools resolve paths from the current
working directory, and `citation_index.py` and `manual_diff.py` deliberately
share one canonical path for `docs/citation_index.json`. In the B787 tooling
those two disagreed, one writing to the repo root and the other reading from
`build_scripts/`, so a clean clone diffed against nothing and cheerfully
reported that no pages were affected.

| Tool | What it does | Non-zero exit means |
| --- | --- | --- |
| `citation_index.py` | Indexes every citation in `data/*.json` and `*.html` into `docs/CITATION_INDEX.md` and `docs/citation_index.json` | (writes only) |
| `manual_diff.py` | Turns changed section codes into the exact re-verify checklist, prefix matched so `5.4` catches `5.4.1` | index missing, or manual not cited |
| `provenance_lint.py` | Every item has valid `src` and `fleet`, and a `ref` when `src` is `manual` | an item is unprovenanced |
| `verify_grounding.py` | A manual-sourced answer is supported by that item's own quoted text | an answer drifted from its evidence |

```
python3 build_scripts/citation_index.py
python3 build_scripts/manual_diff.py A330P_FCOM 5.4 --json
python3 build_scripts/provenance_lint.py
python3 build_scripts/verify_grounding.py data/*.json
```

The full intake-to-publish sequence is in `docs/REVISION_PROCESS.md`. The manual
registry is `docs/MANUAL_VERSIONS.md`.

## Standing cautions

- Memory items are the highest-stakes content in this repo. Do not assemble them
  by grepping a QRH text extract. Airbus marks immediate and memorized actions
  with a graphical box, and the box does not survive text extraction. Scope comes
  from the training department worksheets plus a visual pass on the QRH pages,
  cross-checked against the FCOM and QRH text.
- Freighter content cannot be identified automatically from the extracts either.
  The A330F QRH marks it with a blue background, and background colour does not
  survive extraction. The PRC "A330F ONLY" banner text does survive and is usable.
- Never cite a section without a grep hit against the actual extract.
- No B787 material in A330 study content.
