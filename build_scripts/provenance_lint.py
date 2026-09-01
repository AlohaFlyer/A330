#!/usr/bin/env python3
"""
provenance_lint.py - enforce provenance on every study item.

Every item in every data/*.json bank must declare where it came from and who it
applies to. Without that, a revision sweep cannot tell a manual fact (which must
be re-verified against the new PDF) from an SOP note or a personal technique
(which must not be silently rewritten), and PAX content can drift into freighter
content.

RULES (all failures are hard, exit code 1):
  R1  src is present and is one of: manual | sop | technique
  R2  fleet is present and is one of: pax | frtr | both
  R3  src == "manual" requires a non-empty ref

Usage:
    python3 build_scripts/provenance_lint.py                 # all data/*.json
    python3 build_scripts/provenance_lint.py data/limits.json
    python3 build_scripts/provenance_lint.py --root . --quiet

Exit codes:
    0  every item passed
    1  at least one item failed a rule
    2  nothing to lint, or a file could not be parsed
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

VALID_SRC = ("manual", "sop", "technique")
VALID_FLEET = ("pax", "frtr", "both")

ID_KEYS = ("id", "item_id", "qid", "card_id", "step_id", "key", "slug")
# A dict is treated as a study item when it carries any of these. Keeps the
# linter off metadata blocks, nav config and other non-item structure.
ITEM_MARKERS = ("src", "fleet", "answer", "question", "limit", "verbatim",
                "prompt", "front", "back", "step", "ref")


def repo_root(explicit: str | None) -> str:
    return os.path.abspath(explicit or os.getcwd())


def item_id(node: dict, path: str) -> str:
    for key in ID_KEYS:
        val = node.get(key)
        if isinstance(val, (str, int)) and str(val).strip():
            return str(val)
    return "(no id) at %s" % (path or "<root>")


def looks_like_item(node: dict) -> bool:
    if node.get("_meta") or node.get("_comment"):
        return False
    return any(k in node for k in ITEM_MARKERS)


def find_items(node, path="", out=None):
    """Collect (json_path, dict) for every study item, at any nesting depth."""
    if out is None:
        out = []
    if isinstance(node, dict):
        if looks_like_item(node):
            out.append((path, node))
        for key, val in node.items():
            child = f"{path}.{key}" if path else key
            if isinstance(val, (dict, list)):
                find_items(val, child, out)
    elif isinstance(node, list):
        for i, entry in enumerate(node):
            find_items(entry, f"{path}[{i}]", out)
    return out


def check_item(node: dict) -> list[str]:
    errors = []

    src = node.get("src")
    if src is None or (isinstance(src, str) and not src.strip()):
        errors.append("R1 missing 'src' (expected one of: %s)"
                      % "|".join(VALID_SRC))
        src = None
    elif not isinstance(src, str) or src.strip().lower() not in VALID_SRC:
        errors.append("R1 invalid src %r (expected one of: %s)"
                      % (src, "|".join(VALID_SRC)))
        src = None
    else:
        src = src.strip().lower()

    fleet = node.get("fleet")
    if fleet is None or (isinstance(fleet, str) and not fleet.strip()):
        errors.append("R2 missing 'fleet' (expected one of: %s)"
                      % "|".join(VALID_FLEET))
    elif not isinstance(fleet, str) or fleet.strip().lower() not in VALID_FLEET:
        errors.append("R2 invalid fleet %r (expected one of: %s)"
                      % (fleet, "|".join(VALID_FLEET)))

    if src == "manual":
        ref = node.get("ref")
        if isinstance(ref, list):
            ok = any(isinstance(r, str) and r.strip() for r in ref)
        else:
            ok = isinstance(ref, str) and bool(ref.strip())
        if not ok:
            errors.append("R3 src is 'manual' but 'ref' is missing or empty; "
                          "a manual fact must cite the manual section it came from")
    return errors


def target_files(root: str, explicit: list[str]) -> list[str]:
    if explicit:
        return [os.path.abspath(p) for p in explicit]
    return sorted(glob.glob(os.path.join(root, "data", "*.json")))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Fail if any study item lacks src, fleet, or a manual ref.")
    ap.add_argument("files", nargs="*", help="data files (default: data/*.json)")
    ap.add_argument("--root", help="repo root (default: current directory)")
    ap.add_argument("--quiet", action="store_true",
                    help="print only failures and the summary line")
    args = ap.parse_args(argv)

    root = repo_root(args.root)
    files = target_files(root, args.files)
    if not files:
        sys.stderr.write("error: no data files found under %s\n"
                         % os.path.join(root, "data"))
        return 2

    total_items = 0
    total_errors = 0
    files_with_errors = 0
    parse_failures = 0

    for path in files:
        rel = os.path.relpath(path, root)
        try:
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            sys.stderr.write("PARSE FAIL %s: %s\n" % (rel, exc))
            parse_failures += 1
            continue

        items = find_items(doc)
        total_items += len(items)
        file_errors = []
        for json_path, node in items:
            errs = check_item(node)
            if errs:
                file_errors.append((item_id(node, json_path), json_path, errs))

        if file_errors:
            files_with_errors += 1
            print("FAIL %s  (%d of %d item%s)"
                  % (rel, len(file_errors), len(items),
                     "" if len(items) == 1 else "s"))
            for iid, json_path, errs in file_errors:
                print("  item: %s" % iid)
                print("    at: %s" % (json_path or "<root>"))
                for err in errs:
                    print("    - %s" % err)
                    total_errors += 1
            print("")
        elif not args.quiet:
            print("ok   %s  (%d item%s)"
                  % (rel, len(items), "" if len(items) == 1 else "s"))

    print("")
    print("provenance lint: %d item%s across %d file%s; %d error%s in %d file%s."
          % (total_items, "" if total_items == 1 else "s",
             len(files) - parse_failures,
             "" if len(files) - parse_failures == 1 else "s",
             total_errors, "" if total_errors == 1 else "s",
             files_with_errors, "" if files_with_errors == 1 else "s"))

    if parse_failures:
        return 2
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
