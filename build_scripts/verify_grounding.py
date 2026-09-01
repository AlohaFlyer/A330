#!/usr/bin/env python3
"""
verify_grounding.py - check that a manual-sourced answer is actually supported
by the text that item itself cites.

provenance_lint.py proves an item CLAIMS a manual source. This proves the claim
holds up: for every item with src == "manual", the substantive keywords in its
answer/limit field must appear somewhere in that same item's own quoted
evidence (verbatim, quote, ref, detail). An item whose answer says things its
own cited text never says is either paraphrased past the source or drifted from
it during an earlier revision sweep. Both are how a wrong number reaches a
checkride.

This is a smoke test, not a proof. It cannot know whether the citation is the
right section, only whether the answer and the evidence talk about the same
things. Numbers are weighted hardest, because numbers are what kill.

The data file is an argument, so it generalizes across banks (limits, memory
items, flows, quiz, cards).

Usage:
    python3 build_scripts/verify_grounding.py data/limits.json
    python3 build_scripts/verify_grounding.py data/*.json --threshold 0.75
    python3 build_scripts/verify_grounding.py data/limits.json --json
    python3 build_scripts/verify_grounding.py data/limits.json --report-only

Exit codes:
    0  every manual item is grounded (or --report-only)
    1  at least one manual item is not grounded
    2  bad input
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

# Fields that hold the claim being made.
ANSWER_FIELDS = ("answer", "limit", "value", "back", "a", "response",
                 "correct_answer", "limitation")
# Fields that hold the evidence the item cites for itself.
EVIDENCE_FIELDS = ("verbatim", "quote", "ref", "refs", "detail", "details",
                   "source_text", "excerpt", "note", "explanation")

ID_KEYS = ("id", "item_id", "qid", "card_id", "step_id", "key", "slug")

# Words carrying no evidentiary weight. Kept deliberately small: in manual text
# almost every content word matters.
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "must", "may", "are",
    "is", "be", "of", "to", "in", "on", "at", "or", "a", "an", "if", "it",
    "not", "no", "when", "than", "then", "as", "by", "any", "all", "both",
    "shall", "should", "will", "can", "was", "were", "has", "have", "had",
    "into", "per", "up", "down", "each", "only", "also", "but", "its",
}

NUM_RE = re.compile(r"\d")
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[./%-][A-Za-z0-9]+)*")


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text or "")]


def keywords(text: str) -> list[str]:
    """Substantive tokens: any token containing a digit, or a word of 4+ chars
    that is not a stopword. Short function words are dropped; numbers never are."""
    out = []
    for tok in tokenize(text):
        if tok in STOPWORDS:
            continue
        if NUM_RE.search(tok) or len(tok) >= 4:
            if tok not in out:
                out.append(tok)
    return out


def gather(node: dict, fields) -> str:
    parts = []
    for key in fields:
        val = node.get(key)
        if isinstance(val, str):
            parts.append(val)
        elif isinstance(val, list):
            parts.extend(str(v) for v in val if isinstance(v, (str, int, float)))
        elif isinstance(val, dict):
            parts.extend(str(v) for v in val.values()
                         if isinstance(v, (str, int, float)))
        elif isinstance(val, (int, float)):
            parts.append(str(val))
    return " ".join(parts)


def item_id(node: dict, path: str) -> str:
    for key in ID_KEYS:
        val = node.get(key)
        if isinstance(val, (str, int)) and str(val).strip():
            return str(val)
    return "(no id) at %s" % (path or "<root>")


def looks_like_item(node: dict) -> bool:
    if node.get("_meta") or node.get("_comment"):
        return False
    return "src" in node or any(k in node for k in ANSWER_FIELDS)


def find_items(node, path="", out=None):
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


def check_item(node: dict, path: str, threshold: float) -> dict | None:
    """Return a finding dict when the item is not grounded, else None."""
    if str(node.get("src", "")).strip().lower() != "manual":
        return None

    answer = gather(node, ANSWER_FIELDS)
    evidence = gather(node, EVIDENCE_FIELDS)
    kws = keywords(answer)

    if not answer.strip():
        return {"id": item_id(node, path), "at": path, "reason": "no answer field",
                "missing": [], "missing_numeric": [], "coverage": 0.0,
                "keywords": 0}
    if not evidence.strip():
        return {"id": item_id(node, path), "at": path,
                "reason": "src is 'manual' but the item quotes no evidence "
                          "(verbatim/quote/ref/detail all empty)",
                "missing": kws, "missing_numeric": [k for k in kws
                                                    if NUM_RE.search(k)],
                "coverage": 0.0, "keywords": len(kws)}
    if not kws:
        return None

    hay = " ".join(tokenize(evidence))
    hay_padded = " %s " % hay
    missing = [k for k in kws if (" %s " % k) not in hay_padded and k not in hay]
    coverage = 1.0 - (len(missing) / len(kws))
    missing_numeric = [k for k in missing if NUM_RE.search(k)]

    # A missing number is disqualifying on its own: an unsupported figure is the
    # exact failure this tool exists to catch.
    if missing_numeric or coverage < threshold:
        reason = ("answer contains %d numeric term(s) absent from its own cited "
                  "text" % len(missing_numeric)) if missing_numeric else (
                  "only %.0f%% of answer keywords appear in its own cited text"
                  % (coverage * 100))
        return {"id": item_id(node, path), "at": path, "reason": reason,
                "missing": missing, "missing_numeric": missing_numeric,
                "coverage": round(coverage, 3), "keywords": len(kws)}
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Check manual-sourced answers against their own cited text.")
    ap.add_argument("files", nargs="+", help="data bank JSON file(s)")
    ap.add_argument("--threshold", type=float, default=0.6,
                    help="minimum fraction of answer keywords that must appear "
                         "in the evidence (default 0.6)")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--report-only", action="store_true",
                    help="always exit 0; use while triaging a large bank")
    args = ap.parse_args(argv)

    if not 0.0 <= args.threshold <= 1.0:
        ap.error("--threshold must be between 0 and 1")

    all_findings = []
    checked = 0
    manual_items = 0
    bad_input = False

    for path in args.files:
        try:
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            sys.stderr.write("error: cannot read %s (%s)\n" % (path, exc))
            bad_input = True
            continue
        for json_path, node in find_items(doc):
            checked += 1
            if str(node.get("src", "")).strip().lower() == "manual":
                manual_items += 1
            finding = check_item(node, json_path, args.threshold)
            if finding:
                finding["file"] = os.path.relpath(path)
                all_findings.append(finding)

    if args.as_json:
        json.dump({"checked_items": checked, "manual_items": manual_items,
                   "threshold": args.threshold,
                   "ungrounded": len(all_findings),
                   "findings": all_findings},
                  sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        if all_findings:
            print("UNGROUNDED ITEMS")
            print("")
            for f in all_findings:
                print("%s :: %s" % (f["file"], f["id"]))
                print("  at      : %s" % (f["at"] or "<root>"))
                print("  reason  : %s" % f["reason"])
                if f["missing_numeric"]:
                    print("  numbers not in cited text: %s"
                          % ", ".join(f["missing_numeric"]))
                other = [m for m in f["missing"] if m not in f["missing_numeric"]]
                if other:
                    print("  words not in cited text  : %s"
                          % ", ".join(other[:12])
                          + (" ..." if len(other) > 12 else ""))
                print("  coverage: %.0f%% of %d keyword(s)"
                      % (f["coverage"] * 100, f["keywords"]))
                print("")
        print("grounding check: %d item%s scanned, %d with src='manual', "
              "%d ungrounded (threshold %.2f)."
              % (checked, "" if checked == 1 else "s", manual_items,
                 len(all_findings), args.threshold))
        if not all_findings and manual_items:
            print("Every manual-sourced answer is supported by its own cited text.")

    if bad_input:
        return 2
    if args.report_only:
        return 0
    return 1 if all_findings else 0


if __name__ == "__main__":
    sys.exit(main())
