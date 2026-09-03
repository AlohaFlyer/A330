#!/usr/bin/env python3
"""
citation_index.py - build the portal's manual citation index.

Walks the repo for study data and page markup, extracts every manual citation,
and writes two artifacts:

    docs/CITATION_INDEX.md    human readable, grouped by manual and section
    docs/citation_index.json  machine readable, consumed by manual_diff.py

WHY THIS EXISTS
---------------
When a manual revision lands, the only question that matters is "what in the
portal cited the sections that changed". That answer has to be mechanical.

TWO BUGS IN THE PREDECESSOR (B787 portal) THAT THIS TOOL FIXES
--------------------------------------------------------------
1. PATH BUG. The predecessor's index builder wrote its output to the repo root
   while the diff tool read it from build_scripts/. They worked only on the one
   machine where a stale copy happened to sit in both places; a clean clone
   silently diffed against nothing and reported "no pages affected". Here BOTH
   tools resolve paths from a single repo root (default: the current working
   directory, i.e. run from the repo root) and both use docs/citation_index.json.
   Never reintroduce a second copy of this path.

2. HTML-ONLY COVERAGE. The predecessor only parsed .html. Every quiz question,
   flow step and flashcard lives in data/*.json, so the bulk of the citations
   were invisible to the sweep. This tool walks data/*.json FIRST and treats
   HTML as the secondary source.

THE THIRD BUG, FIXED HERE: THE BARE AIRBUS IDENT
------------------------------------------------
The first version of this tool only recognised a citation that led with a
MANUAL NAME TOKEN, as in "A330P QRH ABN-17". Almost nothing in this repo is
written that way. The A330 books are cited by their Airbus Ident, which carries
no manual name at all:

    LIM-APU-10-00020218.0001001        159 of the 165 limitations
    PRO-ABN-MISC-00012261.0001001      the memory items
    DSC-52-30-20                       the oral scope areas

So 159 limitations, all 11 memory items and all 67 oral areas produced no
citation, and `manual_diff.py A330P_FCOM LIM-AFS-20` answered "Nothing to
re-verify" against twenty real citations. That failure points the wrong way:
it shortens the checklist, so it reads as good news. REVISION_PROCESS.md names
it the single most dangerous failure mode in the process.

The fix is two-sided:

  * MATCHING. A bare Ident is now recognised on its own, without a leading
    manual token. See BARE_IDENT_RE and the comment above it for the exact
    grammar and why it is shaped that way.

  * ATTRIBUTION. A bare Ident says nothing about which book it came from, and
    the Ident prefix alone is not enough to tell you: `LIM-SPD-00006064.0001001`
    is an AFM limitation, not an FCOM one, and only the record's own
    `source_book` field says so. Attribution therefore reads the RECORD's own
    fields first and falls back to the Ident prefix last. See attribute().

  * NOTHING IS DROPPED. Where a citation cannot be pinned to one manual, it is
    indexed under EVERY candidate and reported in `ambiguous_attributions`; if
    it cannot be pinned to any manual it is indexed under UNATTRIBUTED and
    reported in `unattributed`. This departs from the earlier design note
    ("ambiguous bare manual tails are rejected, not guessed"), because
    rejecting meant dropping, and a dropped citation is invisible to the sweep.
    Being loudly over-inclusive is recoverable. Being silently short is not.

COVERAGE ASSERTION
------------------
After indexing, the tool counts how many records in each data/*.json bank
produced at least one citation and how many produced none, names every record
that produced none, and writes all of it to both outputs. A record that cites
nothing is a coverage hole, and a coverage hole is now visible in the output
instead of merely absent from it. `--fail-on-gaps` turns that into a non-zero
exit for use as a gate; the default stays exit 0 so the documented
REVISION_PROCESS step 6 behaviour is unchanged.

Usage:
    python3 build_scripts/citation_index.py            # run from repo root
    python3 build_scripts/citation_index.py --root .   # explicit root
    python3 build_scripts/citation_index.py --quiet
    python3 build_scripts/citation_index.py --fail-on-gaps
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys

# Keys whose string (or list of string) values are treated as citations.
#
# "ref"/"refs" were the original two. The other three are citation fields that
# were being walked straight past:
#   fcom_ref    data/oral_scope.json, all 67 areas. The only citation those
#               records carry, and the reason the oral page indexed zero.
#   page_label  data/memory_items*.json, e.g. "PRO-ABN-MISC P1/26" (FCOM) and
#               "22.02A" (QRH). QRH differences documents are published against
#               exactly these chapter.page labels, so this is the field a QRH
#               sweep needs.
#   sub_idents  data/memory_items.json, a list of further Idents for one
#               procedure that spans several FCOM pages.
REF_KEYS = ("ref", "refs", "fcom_ref", "page_label", "sub_idents")

# Record fields that name the book a record came from. Read before any guess
# from the Ident shape: limitations lim-afm-01 cites LIM-SPD-00006064.0001001,
# which looks like an FCOM Limitations Ident but is an AFM one, and only
# source_book says so.
BOOK_HINT_KEYS = ("source_book", "book", "manual", "source_manual")

# Keys used, in order, as an item's stable id.
ID_KEYS = ("id", "item_id", "qid", "card_id", "step_id", "key", "slug")

# Airbus Ident prefixes and the book family each belongs to, taken only from
# forms actually present in data/*.json. This is the LAST resort in attribute(),
# used when the record carries no book field of its own.
#   LIM / PRO / DSC   FCOM chapters. limitations.html states the set is the
#                     "FCOM R17 Limitations chapter"; memory items carrying
#                     PRO-ABN-* Idents carry book "FCOM R17"; oral areas carry
#                     DSC-* under the key fcom_ref.
#   ABN               QRH. memory items with a bare ABN-22 / ABN-23-A Ident
#                     carry book "QRH R35".
#   EMER / NORM / APP AFM. Seen only in limitations lim-add-03/04/05, each
#                     written with an explicit "AFM " token in front of it.
#   AS                FCTM. Seen in oral_scope as "FCTM AS-CG".
#   PR                FCTM. Seen in limitations.html as
#                     "FCTM R5, PR-AEP-MISC-B-00016515.0001001".
# Do not add a prefix here that has not been seen in the data.
IDENT_PREFIX_BOOK = {
    "LIM": "FCOM",
    "PRO": "FCOM",
    "DSC": "FCOM",
    "ABN": "QRH",
    "EMER": "AFM",
    "NORM": "AFM",
    "APP": "AFM",
    "AS": "FCTM",
    "PR": "FCTM",
}

# Sentinel bucket for a citation that could not be attributed to any manual.
# It exists so such a citation is still present in the index and still shows up
# in CITATION_INDEX.md, rather than vanishing.
UNATTRIBUTED = "UNATTRIBUTED"

# A bare Airbus Ident or section token, matched with no leading manual name.
#
# Shape: two or more segments joined by "." or "-", each segment made of
# letters, digits and underscores. Every form observed in the data fits:
#
#   LIM-APU-10-00020218.0001001        limitations, the common case
#   LIM-AG-OPS-ARPT_WIND-00020102.0001001   underscore inside a segment
#   LIM-ICE_RAIN-00020129.0001001           same
#   PRO-ABN-SURV-AA-00026795.0001001   memory items
#   ABN-23-A-00017854.0001001          memory items, QRH
#   DSC-52-30-20                       oral scope
#   PRO-NOR-SOP-04, PRO-ABN-ABN-RST    oral scope, no digits at all
#   LIM-APU, LIM-ENG, AS-CG            oral scope, two segments, no digits
#   22.02A, 18.04A, 19.02A             QRH page labels
#   5.1.20, 22.4                       FOM sections
#
# The lookaround stops a partial match inside a longer token. Which of these
# actually counts as a citation is decided by is_bare_citation(), not here.
BARE_IDENT_RE = re.compile(
    r"(?<![A-Za-z0-9_.\-])"
    r"[A-Za-z0-9][A-Za-z0-9_]*(?:[.\-][A-Za-z0-9][A-Za-z0-9_]*)+"
    r"(?![A-Za-z0-9_])"
)

# Some Idents reach a page or a note through markdown, which escapes the
# underscore: LIM-AG-OPS-ARPT\_WIND, LIM-AG-F\_CTL, LIM-ICE\_RAIN. The dataset
# holds the correct unescaped form, so an escaped copy has to be folded back to
# it or the two spellings index as two different sections and a sweep on one
# misses the other.
MD_ESCAPE_RE = re.compile(r"\\([_.\-])")

# "DSC 70-35-20" and "DSC 23-20-30" appear in oral_scope alongside the usual
# hyphenated "DSC-70-35-20". Join the prefix back on so both spellings land in
# the same section bucket. The digit lookahead is deliberate: it makes it
# impossible for ordinary prose to be swallowed into an Ident.
PREFIX_SPACE_RE = re.compile(r"\b(DSC|LIM|PRO|ABN|EMER|NORM)\s+(?=[0-9])")


def unescape(text: str) -> str:
    """Undo markdown backslash escapes inside citations, then rejoin the one
    observed "PREFIX <digits>" spelling of an Ident."""
    if not text:
        return ""
    return PREFIX_SPACE_RE.sub(r"\1-", MD_ESCAPE_RE.sub(r"\1", text))


def repo_root(explicit: str | None) -> str:
    """Resolve the repo root. Default is the CWD, so the tool is run from the
    repo root and reads/writes the same docs/ directory as manual_diff.py."""
    return os.path.abspath(explicit or os.getcwd())


def load_manuals(root: str) -> dict:
    """Manual records come from manuals.json, the single source of truth."""
    path = os.path.join(root, "manuals.json")
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        sys.stderr.write(
            "warn: manuals.json not found at %s; falling back to a generic "
            "citation pattern\n" % path
        )
        return {}
    return {k: v for k, v in data.items() if not k.startswith("_")}


def build_alias_map(codes: list[str]) -> dict[str, str]:
    """Map every spelling a human might write to the canonical manual code.

    Canonical:  A330P_QRH
    Accepted:   'A330P QRH', 'A330P-QRH', and the bare tail 'QRH'.

    Unlike the first version, an ambiguous bare tail (FCOM, QRH, PERF, owned by
    both the A330P and A330F books) is NOT withheld here. It resolves to the
    tail itself and is settled later by attribute(), using the citing record's
    own `fleet` field. Withholding it meant those citations were dropped, which
    is the failure this file exists to stop. Where fleet cannot settle it, the
    citation is indexed under every candidate book and flagged as ambiguous.
    """
    aliases: dict[str, str] = {}
    for code in codes:
        aliases[code.upper()] = code
        aliases[code.replace("_", " ").upper()] = code
        aliases[code.replace("_", "-").upper()] = code
    for code in codes:
        tail = (code.split("_", 1)[1] if "_" in code else code).upper()
        aliases.setdefault(tail, tail)
    return aliases


def build_tail_map(codes: list[str]) -> dict[str, list[str]]:
    """Bare book tail -> every canonical code that owns it.

    FCTM, MEL, PRC, AFM, FOM and FODM have exactly one owner. FCOM, QRH and
    PERF have two, the A330P book and the A330F book, and those are the ones
    the citing record's `fleet` has to settle.
    """
    tails: dict[str, list[str]] = {}
    for code in codes:
        tail = (code.split("_", 1)[1] if "_" in code else code).upper()
        tails.setdefault(tail, []).append(code)
    return tails


def citation_regex(aliases: dict[str, str]) -> re.Pattern:
    """Matches an explicit "<manual> [revision] <section>" citation.

    Section token is the first whitespace separated chunk that looks like a
    section: letters/digits joined by dots or hyphens (5.4.1, ABN-17,
    PR-NP-SOP-160, 27-10-00, AS-CG).
    """
    if aliases:
        alt = "|".join(
            re.escape(a) for a in sorted(aliases, key=len, reverse=True)
        )
    else:
        alt = r"[A-Z0-9][A-Z0-9_\- ]{2,20}"
    return re.compile(
        r"\b(?P<manual>" + alt + r")"
        r"(?:[\s,:]+R[0-9][0-9A-Za-z.\-]*)?"      # optional revision token
        r"[\s,:]+"
        r"(?P<section>[0-9A-Za-z]+(?:[.\-][0-9A-Za-z]+)*)"
        r"(?![A-Za-z0-9])",
        re.IGNORECASE,
    )


def normalize_section(section: str) -> str:
    return section.strip().strip(".,;:").upper()


def segments(token: str) -> list[str]:
    return [s for s in re.split(r"[.\-]", token) if s]


def looks_like_a_date(token: str) -> bool:
    """True for an ISO date such as 2026-08-11 or 2026-09-02.

    The pages print manual issue dates right next to the manual's name
    ("A330 AFM 2026-08-11"), which reads to the citation regex exactly like a
    section. No real section in any of these books opens with a four digit
    number, so that is the discriminator.
    """
    parts = segments(token)
    return (len(parts) >= 2 and all(p.isdigit() for p in parts)
            and len(parts[0]) >= 4)


def is_explicit_section(token: str) -> bool:
    """Accept the section token that followed an explicit manual name.

    Rule one, unchanged from the original: it must contain a digit. That is what
    stops the prose line "the MEL requires a placard" indexing as section
    REQUIRES, and it is the rule the earlier test pass was written against.

    Rule two is new: an ALL-CAPS token of two or more segments also counts, even
    with no digit, because "FCTM AS-CG" and "FCOM PRO-SPO" are real citations in
    oral_scope and limitations. Requiring all caps is what keeps ordinary
    hyphenated prose ("the FCOM cross-check", "the QRH gravity-feed table") out.
    """
    if not token or looks_like_a_date(token):
        return False
    if any(c.isdigit() for c in token):
        return True
    return token == token.upper() and len(segments(token)) >= 2


def is_bare_citation(token: str, strict: bool) -> bool:
    """Accept a token found with NO manual name in front of it.

    Three rules always apply:

      * two or more segments, so "P1" out of the page label "PRO-ABN-MISC P1/26"
        and a lone "26" are not citations;
      * no lower case, because Airbus Idents are upper case, and this is what
        keeps "gravity-feed" and "cross-check" out;
      * not an ISO date, because pages print an issue date beside a book name.

    `strict` then sets how much is demanded of what is left, and it is set by
    where the text came from.

    strict=False, a citation field in a data bank. The value IS a citation, so
    anything with a digit counts. That is what admits the QRH page labels
    ("22.02A", "18.04A") and the second and third sections of a multi-section
    ref ("FOM 5.2.23, 5.6.33"). A digitless token still has to lead with a known
    Ident prefix, which is what admits LIM-APU, PRO-NOR-SUP-ADVWXR and AS-CG.

    strict=True, an HTML page. The text is prose, not a citation, so the token
    must lead with a known Airbus Ident prefix. Without that rule the pages
    hand back TRENT-772B, A330-243-B, D-180, G4-G5, MSP-1, TS-1 and 34-MSN as
    though they were manual sections. Pages are the secondary source here and
    every real citation on them is also in a data bank, so the strict rule
    costs no coverage and keeps the checklist honest.
    """
    parts = segments(token)
    if len(parts) < 2:
        return False
    if token != token.upper():
        return False
    if looks_like_a_date(token):
        return False
    if parts[0] in IDENT_PREFIX_BOOK:
        return True
    if strict:
        return False
    return any(c.isdigit() for c in token)


def book_hint_from_record(record: dict | None, aliases: dict[str, str]) -> list[str]:
    """Book tails named by the record's own fields, e.g. source_book
    "AFM 2026-08-11" -> ['AFM'], book "FCOM R17" -> ['FCOM'],
    "FCOM R17 / AFM 2026-08-11" -> ['FCOM', 'AFM']."""
    if not isinstance(record, dict):
        return []
    found: list[str] = []
    for key in BOOK_HINT_KEYS:
        val = record.get(key)
        if not isinstance(val, str):
            continue
        for word in re.split(r"[^A-Za-z0-9_\-]+", val):
            token = word.upper()
            if token in aliases and token not in found:
                found.append(aliases[token])
    return found


def book_hint_from_key(key_name: str | None, aliases: dict[str, str]) -> list[str]:
    """Book tail named by the field the citation was found in: `fcom_ref` on the
    oral scope areas says FCOM, and that is the record telling us, not a guess
    from the Ident shape."""
    if not key_name:
        return []
    head = key_name.rsplit("_", 1)[0].upper() if "_" in key_name else ""
    if head and head in aliases:
        return [aliases[head]]
    return []


def resolve_book(book: str, fleet: str | None, tails: dict[str, list[str]],
                 codes: set[str]) -> tuple[list[str], bool]:
    """Turn a book name into concrete manual codes.

    Returns (codes, ambiguous). A tail owned by one book resolves outright. A
    tail owned by both the A330P and A330F books is settled by the citing
    record's `fleet`: 'pax' takes the passenger book, 'frtr' the freighter book.
    A record whose fleet is 'both', 'shared' or missing cannot settle it, so
    every candidate is returned and the caller flags it. Returning every
    candidate rather than none is the whole point: a sweep that lists a page it
    did not need to costs an extra read, a sweep that omits one costs a missed
    revision.
    """
    book = book.upper()
    if book in codes:
        return [book], False
    owners = tails.get(book)
    if not owners:
        return [], False
    if len(owners) == 1:
        return list(owners), False
    if fleet:
        picked = [c for c in owners if (c in codes and fleet.lower() ==
                                        _fleet_of(c))]
        if len(picked) == 1:
            return picked, False
    return sorted(owners), True


_MANUAL_FLEET: dict[str, str] = {}
_MANUAL_REVISION: dict[str, set[str]] = {}


def _fleet_of(code: str) -> str:
    return _MANUAL_FLEET.get(code, "")


def is_revision_marker(section: str, book: str | None) -> bool:
    """True when the token after a manual name is that manual's revision.

    Page footers render "A330P FCOM R17" and "FOM 125.1" straight out of
    manuals.json, and to the citation regex a revision reads exactly like a
    section. Two tests, both grounded in manuals.json rather than in a guess
    about number ranges: a lone R-number ("R17", "R35"), and a token equal to a
    revision that manuals.json actually carries for the cited book ("125.1" for
    FOM, "R26-10" for the PERF volumes).
    """
    s = section.upper()
    if len(segments(s)) == 1 and re.fullmatch(r"R[0-9][0-9A-Z.\-]*", s):
        return True
    if not book:
        return False
    revs = _MANUAL_REVISION.get(book.upper(), set())
    return s in revs or s.lstrip("R") in revs


def attribute(explicit_book: str | None, record: dict | None, key_name: str | None,
              token: str, aliases: dict[str, str], tails: dict[str, list[str]],
              codes: set[str]) -> tuple[list[str], str, bool]:
    """Decide which manual a citation belongs to.

    Precedence, most trustworthy first:

      1. A manual name written in the citation string itself, or the nearest
         manual name to its left in the same string. "AFM EMER-24-00005218" and
         "FCOM LIM-AG-OPS-ENV-00021654 / AFM LIM-OPS-00005456" both resolve
         correctly this way.
      2. The record's own book field (source_book, book, manual). This has to
         outrank the Ident prefix: LIM-SPD-00006064.0001001 carries an FCOM
         style prefix but source_book says "AFM 2026-08-11", and the AFM is
         where it came from.
      3. The name of the field the citation sits in: `fcom_ref` says FCOM.
      4. The Ident prefix, from IDENT_PREFIX_BOOK, and only from prefixes seen
         in this repo's data.

    Returns (manual codes, basis, ambiguous). An empty code list means nothing
    could attribute it; the caller files it under UNATTRIBUTED and reports it.
    """
    fleet = record.get("fleet") if isinstance(record, dict) else None

    if explicit_book:
        got, amb = resolve_book(explicit_book, fleet, tails, codes)
        if got:
            return got, "manual token in citation", amb

    hints = book_hint_from_record(record, aliases)
    if hints:
        got: list[str] = []
        amb = len(hints) > 1
        for hint in hints:
            part, part_amb = resolve_book(hint, fleet, tails, codes)
            amb = amb or part_amb
            for c in part:
                if c not in got:
                    got.append(c)
        if got:
            return sorted(got), "record book field", amb

    hints = book_hint_from_key(key_name, aliases)
    if hints:
        got, amb = resolve_book(hints[0], fleet, tails, codes)
        if got:
            return got, "citation field name (%s)" % key_name, amb

    parts = segments(token)
    if parts and parts[0].upper() in IDENT_PREFIX_BOOK:
        got, amb = resolve_book(IDENT_PREFIX_BOOK[parts[0].upper()], fleet,
                                tails, codes)
        if got:
            return got, "ident prefix %s" % parts[0].upper(), amb

    return [], "none", False


def parse_citations(text: str, record: dict | None, key_name: str | None,
                    pattern: re.Pattern, aliases: dict[str, str],
                    tails: dict[str, list[str]], codes: set[str],
                    inherit_manual: bool = True, strict_bare: bool = False):
    """Yield (manual_codes, section, basis, ambiguous, matched_text) for every
    citation in `text`, explicit and bare alike.

    `inherit_manual` says whether a bare Ident may take the manual named to its
    left in the same string. That is right for a JSON ref field, which is one
    short citation ("FOM 5.2.23, 5.6.33" is two FOM sections, and
    "FOM 5.1.20 (replaces 5.4.10)" is two more). It is wrong for an HTML page,
    which is one long string where a manual named in the header would otherwise
    claim every Ident printed below it, so pages pass False and attribute from
    the Ident prefix instead.
    """
    text = unescape(text)
    if not text:
        return

    consumed: list[tuple[int, int]] = []
    explicit_at: list[tuple[int, str]] = []

    # Pass one: citations that name their manual.
    for m in pattern.finditer(text):
        raw_manual = re.sub(r"\s+", " ", m.group("manual")).strip().upper()
        book = aliases.get(raw_manual, raw_manual.replace(" ", "_"))
        explicit_at.append((m.start(), book))
        section_raw = m.group("section")
        if (not is_explicit_section(section_raw)
                or is_revision_marker(section_raw, book)):
            # Not a section, so the manual name is just prose. Leave the span
            # unconsumed; a real Ident may still follow it.
            consumed.append((m.start("manual"), m.end("manual")))
            continue
        consumed.append((m.start(), m.end()))
        got, basis, amb = attribute(book, record, key_name, section_raw,
                                    aliases, tails, codes)
        yield got, normalize_section(section_raw), basis, amb, m.group(0)

    # Pass two: bare Idents. This is the case the first version of this tool
    # could not see at all, and it is the overwhelming majority of the repo.
    for m in BARE_IDENT_RE.finditer(text):
        if any(s <= m.start() < e for s, e in consumed):
            continue
        token = m.group(0)
        if not is_bare_citation(token, strict_bare):
            continue
        nearest = None
        if inherit_manual:
            for pos, book in explicit_at:
                if pos < m.start():
                    nearest = book
        got, basis, amb = attribute(nearest, record, key_name, token,
                                    aliases, tails, codes)
        yield got, normalize_section(token), basis, amb, token


def iter_files(root: str):
    """Yield (kind, absolute_path) for every data bank and page in the repo.

    data/*.json is walked first and deliberately: the JSON banks hold most of
    the citations, and the predecessor tool missed all of them.
    """
    skip_dirs = {".git", "node_modules", "extracts", "__pycache__", ".venv"}

    data_dir = os.path.join(root, "data")
    if os.path.isdir(data_dir):
        for dirpath, dirnames, filenames in os.walk(data_dir):
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            for name in sorted(filenames):
                if name.endswith(".json"):
                    yield "json", os.path.join(dirpath, name)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for name in sorted(filenames):
            if name.endswith(".html"):
                yield "html", os.path.join(dirpath, name)


def node_id(node: dict) -> str | None:
    for key in ID_KEYS:
        val = node.get(key)
        if isinstance(val, (str, int)) and str(val).strip():
            return str(val)
    return None


def nearest_id(stack: list) -> str | None:
    """Innermost usable id, used as the citation's item id."""
    for node in reversed(stack):
        if isinstance(node, dict):
            got = node_id(node)
            if got:
                return got
    return None


def walk_json(node, stack, path, out, records, record=None):
    """Recursively collect citations and the record each one belongs to.

    Shape agnostic on purpose: quiz banks, flow banks and card banks all nest
    differently, and a bank added next year should not need a code change here.

    `record` is the OUTERMOST id bearing dict enclosing a value, which is what
    the coverage assertion counts. `nearest_id` stays the innermost id, which is
    what the re-verify checklist wants to name.
    """
    stack = stack + [node]
    if isinstance(node, dict):
        if record is None and node_id(node):
            record = node
            records.append((node_id(node), node))
        for key, val in node.items():
            child_path = f"{path}.{key}" if path else key
            if key in REF_KEYS:
                if isinstance(val, str):
                    out.append((child_path, nearest_id(stack), val, record, key))
                elif isinstance(val, list):
                    for i, entry in enumerate(val):
                        if isinstance(entry, str):
                            out.append((f"{child_path}[{i}]", nearest_id(stack),
                                        entry, record, key))
            else:
                walk_json(val, stack, child_path, out, records, record)
    elif isinstance(node, list):
        for i, entry in enumerate(node):
            walk_json(entry, stack, f"{path}[{i}]", out, records, record)


def page_fleet(text: str, manuals: dict) -> str | None:
    """The fleet an HTML page declares for itself, or None.

    An HTML page carries no `fleet` field, but every page footer renders its
    manual identity from manuals.json, so limitations.html says "A330P FCOM R17"
    and memory-items.html says "A330P FCOM ... A330P QRH". Naming a
    fleet-specific book IS the page stating its fleet, which is the same kind of
    evidence as a record's own field and not a guess from the Ident shape. Only
    a full book name counts; a bare "A330F" in prose does not, because pages
    mention the other fleet while explaining a difference. If a page names books
    from more than one fleet, it does not settle anything and returns None, and
    its citations are reported as ambiguous.
    """
    fleets = set()
    for code, meta in manuals.items():
        fleet = (meta or {}).get("fleet") if isinstance(meta, dict) else None
        if fleet not in ("pax", "frtr"):
            continue
        for spelling in (code, code.replace("_", " "), code.replace("_", "-")):
            if re.search(r"\b%s\b" % re.escape(spelling), text, re.IGNORECASE):
                fleets.add(fleet)
                break
    return fleets.pop() if len(fleets) == 1 else None


HTML_ID_RE = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""", re.IGNORECASE)


def html_id_before(text: str, pos: int) -> str | None:
    """Nearest preceding id attribute, used as the item id for an HTML citation."""
    best = None
    for m in HTML_ID_RE.finditer(text, 0, pos):
        best = m.group(1)
    return best


def collect(root: str, verbose: bool = True):
    manuals = load_manuals(root)
    codes = list(manuals)
    _MANUAL_FLEET.clear()
    _MANUAL_REVISION.clear()
    for code, meta in manuals.items():
        if not isinstance(meta, dict):
            continue
        if isinstance(meta.get("fleet"), str):
            _MANUAL_FLEET[code] = meta["fleet"].lower()
        rev = meta.get("revision")
        if isinstance(rev, str) and rev.strip():
            rev = rev.strip().upper()
            tail = (code.split("_", 1)[1] if "_" in code else code).upper()
            for key in (code.upper(), tail):
                _MANUAL_REVISION.setdefault(key, set()).add(rev)
                _MANUAL_REVISION[key].add(rev.lstrip("R"))
    aliases = build_alias_map(codes)
    tails = build_tail_map(codes)
    pattern = citation_regex(aliases)
    known = set(codes)

    index: dict[str, dict[str, list[dict]]] = {}
    unknown_manuals: dict[str, int] = {}
    ambiguous: list[dict] = []
    unattributed: list[dict] = []
    coverage: dict[str, dict] = {}
    counts = {"json_files": 0, "html_files": 0, "citations": 0,
              "data_records": 0, "records_with_citations": 0,
              "records_without_citations": 0, "ambiguous_citations": 0,
              "unattributed_citations": 0}

    for kind, abspath in iter_files(root):
        rel = os.path.relpath(abspath, root).replace(os.sep, "/")
        hits: list[tuple] = []
        records: list[tuple[str, dict]] = []
        covered_ids: set[str] = set()

        if kind == "json":
            counts["json_files"] += 1
            try:
                with open(abspath, encoding="utf-8") as fh:
                    doc = json.load(fh)
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                sys.stderr.write("warn: skipping %s (%s)\n" % (rel, exc))
                continue
            found: list = []
            walk_json(doc, [], "", found, records)
            for json_path, item_id, ref, record, key_name in found:
                hits.append((item_id, json_path, ref, record, key_name))
        else:
            counts["html_files"] += 1
            try:
                with open(abspath, encoding="utf-8") as fh:
                    text = unescape(fh.read())
            except UnicodeDecodeError as exc:
                sys.stderr.write("warn: skipping %s (%s)\n" % (rel, exc))
                continue
            # HTML carries no record fields, so a page's citations are
            # attributed from the citation text itself or the Ident prefix,
            # with the fleet the page declares for itself standing in for a
            # record's `fleet`.
            hits.append((None, None, text, {"fleet": page_fleet(text, manuals)},
                         None))
            html_text = text

        for item_id, locator, raw, record, key_name in hits:
            for got, section, basis, amb, matched in parse_citations(
                    raw, record, key_name, pattern, aliases, tails, codes=known,
                    inherit_manual=(kind == "json"),
                    strict_bare=(kind == "html")):
                if kind == "html":
                    # Recover the id and a tight raw_ref for the page case.
                    pos = html_text.find(matched)
                    item_id = html_id_before(html_text, pos) if pos >= 0 else None
                    locator = None
                    raw_ref = matched
                else:
                    raw_ref = raw.strip()

                targets = got or [UNATTRIBUTED]
                if not got:
                    counts["unattributed_citations"] += 1
                    unattributed.append({
                        "file": rel, "item_id": item_id, "section": section,
                        "raw_ref": raw_ref,
                    })
                    if verbose:
                        sys.stderr.write(
                            "warn: %s %s cites '%s' and no manual could be "
                            "attributed; filed under %s\n"
                            % (rel, item_id or "(no id)", section, UNATTRIBUTED))
                elif amb:
                    counts["ambiguous_citations"] += 1
                    ambiguous.append({
                        "file": rel, "item_id": item_id, "section": section,
                        "raw_ref": raw_ref, "candidates": targets,
                        "basis": basis,
                    })

                for manual in targets:
                    if known and manual not in known and manual != UNATTRIBUTED:
                        unknown_manuals[manual] = unknown_manuals.get(manual, 0) + 1
                    entry = {
                        "file": rel,
                        "page": os.path.basename(rel),
                        "kind": kind,
                        "item_id": item_id,
                        "locator": locator,
                        "raw_ref": raw_ref,
                        "attribution": "ambiguous" if amb else (
                            "none" if not got else "resolved"),
                        "attributed_by": basis,
                    }
                    bucket = index.setdefault(manual, {}).setdefault(section, [])
                    if entry not in bucket:
                        bucket.append(entry)
                        counts["citations"] += 1

                if kind == "json" and record is not None:
                    got_id = node_id(record)
                    if got_id:
                        covered_ids.add(got_id)

        if kind == "json":
            # COVERAGE ASSERTION. A record that produced no citation at all is a
            # hole, and a hole is reported by name. The bug this file fixes was
            # invisible precisely because uncovered records were absent from the
            # output rather than listed in it.
            all_ids = [rid for rid, _ in records]
            missing = [rid for rid in all_ids if rid not in covered_ids]
            coverage[rel] = {
                "records": len(all_ids),
                "with_citations": len(all_ids) - len(missing),
                "without_citations": len(missing),
                "uncovered_record_ids": missing,
            }
            counts["data_records"] += len(all_ids)
            counts["records_with_citations"] += len(all_ids) - len(missing)
            counts["records_without_citations"] += len(missing)

    if verbose and unknown_manuals:
        for manual, n in sorted(unknown_manuals.items()):
            sys.stderr.write(
                "warn: citation to '%s' (%d) is not a code in manuals.json\n"
                % (manual, n)
            )
    if verbose and ambiguous:
        by_book: dict[str, int] = {}
        for a in ambiguous:
            by_book["/".join(a["candidates"])] = by_book.get(
                "/".join(a["candidates"]), 0) + 1
        for books, n in sorted(by_book.items()):
            sys.stderr.write(
                "warn: %d citation(s) could not be pinned to one of %s; indexed "
                "under every candidate and listed in ambiguous_attributions\n"
                % (n, books))
    if verbose:
        for rel, cov in sorted(coverage.items()):
            if cov["without_citations"]:
                sys.stderr.write(
                    "warn: coverage hole in %s: %d of %d records cite nothing "
                    "(%s)\n" % (rel, cov["without_citations"], cov["records"],
                                ", ".join(cov["uncovered_record_ids"][:10])))

    return index, counts, sorted(unknown_manuals), coverage, ambiguous, unattributed


def section_sort_key(section: str):
    parts = re.split(r"[.\-]", section)
    return [(0, int(p)) if p.isdigit() else (1, p) for p in parts]


def write_outputs(root, index, counts, unknown, coverage, ambiguous, unattributed):
    docs_dir = os.path.join(root, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "generated": generated,
        "root": os.path.basename(root),
        "counts": counts,
        "unknown_manuals": unknown,
        "coverage": coverage,
        "ambiguous_attributions": ambiguous,
        "unattributed": unattributed,
        "index": {
            manual: {
                section: index[manual][section]
                for section in sorted(index[manual], key=section_sort_key)
            }
            for manual in sorted(index)
        },
    }
    json_path = os.path.join(docs_dir, "citation_index.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    lines = [
        "# Citation Index",
        "",
        "Generated by `build_scripts/citation_index.py` on %s." % generated,
        "Do not edit by hand. Rebuild it after any content change.",
        "",
        "Sources scanned: %d JSON data banks, %d HTML pages. "
        "Citations indexed: %d."
        % (counts["json_files"], counts["html_files"], counts["citations"]),
        "",
    ]
    if unknown:
        lines += [
            "> Warning: these cited manual codes are not in `manuals.json`: %s"
            % ", ".join(unknown),
            "",
        ]

    # Coverage first, before the index itself. A record that cites nothing is
    # the failure mode this report exists to surface, so it goes at the top.
    lines += [
        "## Coverage",
        "",
        "Records in each data bank that produced at least one citation. A record "
        "with none is a coverage hole: the sweep cannot see it, so a revision "
        "touching its section would report all clear.",
        "",
        "| Data bank | Records | Cited | Coverage holes |",
        "| --- | --- | --- | --- |",
    ]
    for rel in sorted(coverage):
        cov = coverage[rel]
        lines.append("| `%s` | %d | %d | %d |" % (
            rel, cov["records"], cov["with_citations"],
            cov["without_citations"]))
    lines += [
        "",
        "**Total: %d of %d records cite at least one manual section; %d cite "
        "nothing.**" % (counts["records_with_citations"],
                        counts["data_records"],
                        counts["records_without_citations"]),
        "",
    ]
    holes = {r: c for r, c in coverage.items() if c["without_citations"]}
    if holes:
        lines += ["### Coverage holes", ""]
        for rel in sorted(holes):
            lines.append("- `%s`: %s" % (
                rel, ", ".join("`%s`" % i
                               for i in holes[rel]["uncovered_record_ids"])))
        lines.append("")
    else:
        lines += ["Every record in every data bank cites at least one section.",
                  ""]

    if unattributed:
        lines += [
            "### Unattributed citations",
            "",
            "These citations name a section but nothing in the citation, the "
            "record or the Ident prefix says which manual owns it. They are "
            "indexed under `%s` so they are not lost." % UNATTRIBUTED,
            "",
            "| File | Item id | Section | Raw ref |",
            "| --- | --- | --- | --- |",
        ]
        for u in unattributed:
            lines.append("| `%s` | `%s` | `%s` | %s |" % (
                u["file"], u["item_id"] or "-", u["section"],
                u["raw_ref"].replace("|", "\\|")))
        lines.append("")

    if ambiguous:
        lines += [
            "### Ambiguous attributions",
            "",
            "These citations resolve to a book family but not to one book, "
            "because the citing record's `fleet` does not settle which of the "
            "A330P and A330F volumes it came from. Each is indexed under EVERY "
            "candidate so no sweep can miss it. Confirm the fleet before "
            "re-verifying.",
            "",
            "| File | Item id | Section | Candidates | Basis |",
            "| --- | --- | --- | --- | --- |",
        ]
        for a in ambiguous:
            lines.append("| `%s` | `%s` | `%s` | %s | %s |" % (
                a["file"], a["item_id"] or "-", a["section"],
                ", ".join("`%s`" % c for c in a["candidates"]), a["basis"]))
        lines.append("")

    lines += ["## Index", ""]
    if not index:
        lines += ["No citations found.", ""]
    for manual in sorted(index):
        lines += ["### %s" % manual, ""]
        for section in sorted(index[manual], key=section_sort_key):
            entries = index[manual][section]
            lines.append("#### %s  (%d citation%s)" % (
                section, len(entries), "" if len(entries) == 1 else "s"))
            lines.append("")
            lines.append("| Page | Item id | Kind | Locator | Attribution | Raw ref |")
            lines.append("| --- | --- | --- | --- | --- | --- |")
            for e in entries:
                lines.append("| `%s` | `%s` | %s | `%s` | %s | %s |" % (
                    e["file"],
                    e["item_id"] or "-",
                    e["kind"],
                    e["locator"] or "-",
                    e.get("attributed_by", "-"),
                    e["raw_ref"].replace("|", "\\|"),
                ))
            lines.append("")
    md_path = os.path.join(docs_dir, "CITATION_INDEX.md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return md_path, json_path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--root", help="repo root (default: current directory)")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--fail-on-gaps", action="store_true",
                    help="exit 1 if any data record produced no citation, or "
                         "any citation could not be attributed to a manual")
    args = ap.parse_args(argv)

    root = repo_root(args.root)
    index, counts, unknown, coverage, ambiguous, unattributed = collect(
        root, verbose=not args.quiet)
    md_path, json_path = write_outputs(root, index, counts, unknown, coverage,
                                       ambiguous, unattributed)

    if not args.quiet:
        print("scanned %d JSON data banks and %d HTML pages"
              % (counts["json_files"], counts["html_files"]))
        print("indexed %d citations across %d manuals"
              % (counts["citations"], len(index)))
        print("")
        print("COVERAGE (records citing at least one manual section)")
        for rel in sorted(coverage):
            cov = coverage[rel]
            flag = "" if not cov["without_citations"] else "   <-- %d hole%s" % (
                cov["without_citations"],
                "" if cov["without_citations"] == 1 else "s")
            print("  %-34s %4d / %-4d%s"
                  % (rel, cov["with_citations"], cov["records"], flag))
        print("  %-34s %4d / %-4d"
              % ("TOTAL", counts["records_with_citations"],
                 counts["data_records"]))
        for rel in sorted(coverage):
            cov = coverage[rel]
            if cov["without_citations"]:
                print("  hole in %s: %s"
                      % (rel, ", ".join(cov["uncovered_record_ids"])))
        if ambiguous:
            print("")
            print("%d citation(s) could not be pinned to one book and were "
                  "indexed under every candidate; see ambiguous_attributions"
                  % len(ambiguous))
        if unattributed:
            print("%d citation(s) could not be attributed to any manual and "
                  "were filed under %s" % (len(unattributed), UNATTRIBUTED))
        print("")
        print("wrote %s" % os.path.relpath(md_path, root))
        print("wrote %s" % os.path.relpath(json_path, root))

    if args.fail_on_gaps and (counts["records_without_citations"]
                              or unattributed):
        sys.stderr.write("error: citation coverage is incomplete\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
