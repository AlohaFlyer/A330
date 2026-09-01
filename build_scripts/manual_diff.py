#!/usr/bin/env python3
"""
manual_diff.py - turn a manual revision into an exact re-verify checklist.

Given a manual code and the section codes that changed in that revision (read
off the publisher's differences document), this prints every portal page and
item id that cites those sections. That list, and nothing wider, is the sweep.

Matching is by SECTION PREFIX on segment boundaries, so "5.4" catches "5.4.1"
and "5.4.2" but not "5.41". Segments split on "." and "-", which covers both
Airbus dotted sections (5.4.1) and ident style sections (ABN-17, PR-NP-SOP-160).

Reads docs/citation_index.json relative to the repo root, which defaults to the
current working directory. citation_index.py WRITES to that same path from that
same root. The predecessor B787 tooling had these two disagree (one wrote to the
repo root, the other read from build_scripts/) and a clean clone silently swept
nothing. Keep exactly one path.

Usage:
    python3 build_scripts/manual_diff.py A330P_QRH 5.4 ABN-17
    python3 build_scripts/manual_diff.py A330P_FCOM 27 --json
    python3 build_scripts/manual_diff.py A330_FCTM --sections-file changed.txt

Exit codes:
    0  ran fine (whether or not anything matched)
    2  the citation index is missing or unreadable; run citation_index.py
    3  the manual code is not present in the citation index
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

SEGMENT_SPLIT = re.compile(r"[.\-]")


def repo_root(explicit: str | None) -> str:
    return os.path.abspath(explicit or os.getcwd())


def index_path(root: str) -> str:
    # Single canonical location. Must match citation_index.py exactly.
    return os.path.join(root, "docs", "citation_index.json")


def segments(section: str) -> list[str]:
    return [s for s in SEGMENT_SPLIT.split(section.strip().upper()) if s]


def section_matches(changed: str, cited: str) -> bool:
    """True when `cited` is `changed` or a descendant of it.

    Prefix match on whole segments only:
        changed 5.4    cited 5.4      -> True
        changed 5.4    cited 5.4.1    -> True
        changed 5.4    cited 5.41     -> False
        changed ABN    cited ABN-17   -> True
    """
    a, b = segments(changed), segments(cited)
    if not a or len(a) > len(b):
        return False
    return b[: len(a)] == a


def load_index(root: str) -> dict:
    path = index_path(root)
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        sys.stderr.write(
            "error: %s not found.\n"
            "       Run this first, from the repo root:\n"
            "           python3 build_scripts/citation_index.py\n" % path
        )
        raise SystemExit(2)
    except json.JSONDecodeError as exc:
        sys.stderr.write("error: %s is not valid JSON (%s)\n" % (path, exc))
        raise SystemExit(2)


def collect_matches(payload: dict, manual: str, changed: list[str]):
    index = payload.get("index", {})
    if manual not in index:
        return None
    results = []
    for cited_section, entries in index[manual].items():
        hit = [c for c in changed if section_matches(c, cited_section)]
        if not hit:
            continue
        for entry in entries:
            results.append({
                "manual": manual,
                "changed_section": hit[0],
                "cited_section": cited_section,
                "file": entry.get("file"),
                "page": entry.get("page"),
                "kind": entry.get("kind"),
                "item_id": entry.get("item_id"),
                "locator": entry.get("locator"),
                "raw_ref": entry.get("raw_ref"),
            })
    results.sort(key=lambda r: (r["file"] or "", str(r["item_id"]),
                               r["cited_section"]))
    return results


def print_text(manual: str, changed: list[str], results: list[dict],
               payload: dict, root: str) -> None:
    print("RE-VERIFY CHECKLIST")
    print("manual         : %s" % manual)
    print("changed sections: %s" % ", ".join(changed))
    print("index generated : %s" % payload.get("generated", "unknown"))
    print("")
    if not results:
        print("No portal content cites those sections. Nothing to re-verify.")
        print("If that seems wrong, rebuild the index: "
              "python3 build_scripts/citation_index.py")
        return

    by_file: dict[str, list[dict]] = {}
    for r in results:
        by_file.setdefault(r["file"], []).append(r)

    for path in sorted(by_file):
        rows = by_file[path]
        print("%s  (%d item%s)" % (path, len(rows),
                                   "" if len(rows) == 1 else "s"))
        for r in rows:
            print("  [ ] %-28s %-14s %s" % (
                r["item_id"] or "(no id)",
                r["cited_section"],
                r["raw_ref"] or "",
            ))
        print("")

    pages = len(by_file)
    items = len({(r["file"], r["item_id"]) for r in results})
    print("TOTAL: %d citation%s, %d item%s, %d file%s." % (
        len(results), "" if len(results) == 1 else "s",
        items, "" if items == 1 else "s",
        pages, "" if pages == 1 else "s"))
    print("Re-verify each against the new revision, then update "
          "manuals.json last_vetted.")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Print the re-verify checklist for changed manual sections.")
    ap.add_argument("manual", help="manual code, e.g. A330P_QRH")
    ap.add_argument("sections", nargs="*",
                    help="changed section codes, e.g. 5.4 ABN-17")
    ap.add_argument("--sections-file",
                    help="file with one changed section per line "
                         "(# comments and blank lines ignored)")
    ap.add_argument("--root", help="repo root (default: current directory)")
    ap.add_argument("--json", action="store_true", dest="as_json",
                    help="emit JSON instead of the text checklist")
    args = ap.parse_args(argv)

    changed = list(args.sections)
    if args.sections_file:
        with open(args.sections_file, encoding="utf-8") as fh:
            for line in fh:
                line = line.split("#", 1)[0].strip()
                if line:
                    changed.append(line)
    if not changed:
        ap.error("give at least one changed section, or --sections-file")

    root = repo_root(args.root)
    payload = load_index(root)
    manual = args.manual.strip().upper()

    results = collect_matches(payload, manual, changed)
    if results is None:
        known = ", ".join(sorted(payload.get("index", {}))) or "(index is empty)"
        if args.as_json:
            json.dump({"manual": manual, "changed_sections": changed,
                       "error": "manual not present in citation index",
                       "known_manuals": sorted(payload.get("index", {})),
                       "results": []}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            sys.stderr.write(
                "error: '%s' has no citations in the index.\n"
                "       Manuals present: %s\n" % (manual, known))
        return 3

    if args.as_json:
        json.dump({
            "manual": manual,
            "changed_sections": changed,
            "index_generated": payload.get("generated"),
            "match_count": len(results),
            "file_count": len({r["file"] for r in results}),
            "item_count": len({(r["file"], r["item_id"]) for r in results}),
            "results": results,
        }, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print_text(manual, changed, results, payload, root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
