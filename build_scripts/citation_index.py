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

Usage:
    python3 build_scripts/citation_index.py            # run from repo root
    python3 build_scripts/citation_index.py --root .   # explicit root
    python3 build_scripts/citation_index.py --quiet
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys

# Keys whose string values are treated as citations.
REF_KEYS = ("ref", "refs")

# Keys used, in order, as an item's stable id.
ID_KEYS = ("id", "item_id", "qid", "card_id", "step_id", "key", "slug")


def repo_root(explicit: str | None) -> str:
    """Resolve the repo root. Default is the CWD, so the tool is run from the
    repo root and reads/writes the same docs/ directory as manual_diff.py."""
    return os.path.abspath(explicit or os.getcwd())


def load_manual_codes(root: str) -> list[str]:
    """Manual codes come from manuals.json, the single source of truth."""
    path = os.path.join(root, "manuals.json")
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        sys.stderr.write(
            "warn: manuals.json not found at %s; falling back to a generic "
            "citation pattern\n" % path
        )
        return []
    return [k for k in data if not k.startswith("_")]


def build_alias_map(codes: list[str]) -> dict[str, str]:
    """Map every spelling a human might write to the canonical manual code.

    Canonical:  A330P_QRH
    Accepted:   'A330P QRH', 'A330P-QRH', and the bare tail 'QRH' only when the
                tail is unambiguous across the whole manual set (FCTM, MEL, PRC,
                AFM are unique; FCOM/QRH/PERF are not, and stay ambiguous so a
                sloppy citation fails loudly instead of landing on the wrong fleet).
    """
    aliases: dict[str, str] = {}
    for code in codes:
        aliases[code.upper()] = code
        aliases[code.replace("_", " ").upper()] = code
        aliases[code.replace("_", "-").upper()] = code

    tails: dict[str, list[str]] = {}
    for code in codes:
        tail = code.split("_", 1)[1] if "_" in code else code
        tails.setdefault(tail.upper(), []).append(code)
    for tail, owners in tails.items():
        if len(owners) == 1 and tail not in aliases:
            aliases[tail] = owners[0]
    return aliases


def citation_regex(aliases: dict[str, str]) -> re.Pattern:
    """One regex for both JSON refs and HTML markup.

    Matches: <manual alias> [optional revision token] <section token>
    Section token is the first whitespace separated chunk that looks like a
    section: digits/letters joined by dots or hyphens (5.4.1, ABN-17,
    PR-NP-SOP-160, 27-10-00).
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


def parse_refs(text: str, pattern: re.Pattern, aliases: dict[str, str]):
    """Yield (manual_code, section) for every citation found in text."""
    for m in pattern.finditer(text or ""):
        raw_manual = re.sub(r"\s+", " ", m.group("manual")).strip().upper()
        manual = aliases.get(raw_manual, raw_manual.replace(" ", "_"))
        section = normalize_section(m.group("section"))
        # A section token must contain at least one digit. Manual sections do
        # (5.4.1, ABN-17, PR-NP-SOP-160, 27-10-00); ordinary prose after a
        # manual name does not, which stops "the MEL requires ..." in a page
        # paragraph from being indexed as a citation to section REQUIRES.
        if section and any(c.isdigit() for c in section):
            yield manual, section


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


def nearest_id(stack: list) -> str | None:
    """Walk up the containing dicts and return the first usable id."""
    for node in reversed(stack):
        if isinstance(node, dict):
            for key in ID_KEYS:
                val = node.get(key)
                if isinstance(val, (str, int)) and str(val).strip():
                    return str(val)
    return None


def walk_json(node, stack, path, out):
    """Recursively collect (json_path, item_id, ref_string) from any shape.

    Shape agnostic on purpose: quiz banks, flow banks and card banks all nest
    differently, and a bank added next year should not need a code change here.
    """
    stack = stack + [node]
    if isinstance(node, dict):
        for key, val in node.items():
            child_path = f"{path}.{key}" if path else key
            if key in REF_KEYS:
                if isinstance(val, str):
                    out.append((child_path, nearest_id(stack), val))
                elif isinstance(val, list):
                    for i, entry in enumerate(val):
                        if isinstance(entry, str):
                            out.append(
                                (f"{child_path}[{i}]", nearest_id(stack), entry)
                            )
            else:
                walk_json(val, stack, child_path, out)
    elif isinstance(node, list):
        for i, entry in enumerate(node):
            walk_json(entry, stack, f"{path}[{i}]", out)


HTML_ID_RE = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""", re.IGNORECASE)


def html_id_before(text: str, pos: int) -> str | None:
    """Nearest preceding id attribute, used as the item id for an HTML citation."""
    best = None
    for m in HTML_ID_RE.finditer(text, 0, pos):
        best = m.group(1)
    return best


def collect(root: str, verbose: bool = True):
    codes = load_manual_codes(root)
    aliases = build_alias_map(codes)
    pattern = citation_regex(aliases)
    known = set(codes)

    index: dict[str, dict[str, list[dict]]] = {}
    unknown_manuals: dict[str, int] = {}
    counts = {"json_files": 0, "html_files": 0, "citations": 0}

    for kind, abspath in iter_files(root):
        rel = os.path.relpath(abspath, root)
        hits: list[tuple[str | None, str | None, str]] = []

        if kind == "json":
            counts["json_files"] += 1
            try:
                with open(abspath, encoding="utf-8") as fh:
                    doc = json.load(fh)
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                sys.stderr.write("warn: skipping %s (%s)\n" % (rel, exc))
                continue
            found: list = []
            walk_json(doc, [], "", found)
            for json_path, item_id, ref in found:
                hits.append((item_id, json_path, ref))
        else:
            counts["html_files"] += 1
            try:
                with open(abspath, encoding="utf-8") as fh:
                    text = fh.read()
            except UnicodeDecodeError as exc:
                sys.stderr.write("warn: skipping %s (%s)\n" % (rel, exc))
                continue
            for m in pattern.finditer(text):
                hits.append((html_id_before(text, m.start()), None, m.group(0)))

        for item_id, locator, raw in hits:
            for manual, section in parse_refs(raw, pattern, aliases):
                if known and manual not in known:
                    unknown_manuals[manual] = unknown_manuals.get(manual, 0) + 1
                entry = {
                    "file": rel.replace(os.sep, "/"),
                    "page": os.path.basename(rel),
                    "kind": kind,
                    "item_id": item_id,
                    "locator": locator,
                    "raw_ref": raw.strip(),
                }
                bucket = index.setdefault(manual, {}).setdefault(section, [])
                if entry not in bucket:
                    bucket.append(entry)
                    counts["citations"] += 1

    if verbose and unknown_manuals:
        for manual, n in sorted(unknown_manuals.items()):
            sys.stderr.write(
                "warn: citation to '%s' (%d) is not a code in manuals.json\n"
                % (manual, n)
            )
    return index, counts, sorted(unknown_manuals)


def section_sort_key(section: str):
    parts = re.split(r"[.\-]", section)
    return [(0, int(p)) if p.isdigit() else (1, p) for p in parts]


def write_outputs(root: str, index, counts, unknown):
    docs_dir = os.path.join(root, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "generated": generated,
        "root": os.path.basename(root),
        "counts": counts,
        "unknown_manuals": unknown,
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
    if not index:
        lines += ["No citations found.", ""]
    for manual in sorted(index):
        lines += ["## %s" % manual, ""]
        for section in sorted(index[manual], key=section_sort_key):
            entries = index[manual][section]
            lines.append("### %s  (%d citation%s)" % (
                section, len(entries), "" if len(entries) == 1 else "s"))
            lines.append("")
            lines.append("| Page | Item id | Kind | Locator | Raw ref |")
            lines.append("| --- | --- | --- | --- | --- |")
            for e in entries:
                lines.append("| `%s` | `%s` | %s | `%s` | %s |" % (
                    e["file"],
                    e["item_id"] or "-",
                    e["kind"],
                    e["locator"] or "-",
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
    args = ap.parse_args(argv)

    root = repo_root(args.root)
    index, counts, unknown = collect(root, verbose=not args.quiet)
    md_path, json_path = write_outputs(root, index, counts, unknown)

    if not args.quiet:
        print("scanned %d JSON data banks and %d HTML pages"
              % (counts["json_files"], counts["html_files"]))
        print("indexed %d citations across %d manuals"
              % (counts["citations"], len(index)))
        print("wrote %s" % os.path.relpath(md_path, root))
        print("wrote %s" % os.path.relpath(json_path, root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
