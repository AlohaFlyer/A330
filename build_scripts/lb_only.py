#!/usr/bin/env python3
"""Portal-wide weights in whole thousands of pounds (Ryan 2026-09-22): no kg anywhere a pilot reads, every weight
at or above 1 000 lb written "<N>k lb" (rounded to the nearest thousand, half up), values under 1 000 lb exact.

Rewrites the answer, question, title and note fields of the data banks, the corpus and the generator sources.
Verbatim manual quotes (drill `src`, limitations `verbatim`, phase-flow `q`/`fcom` quotes, oe `quote`) are left
as printed so verify_phase_flows.py / verify_flows_trainer.py still prove them literal; they surface only behind
the Source button and carry the FCOM's own kg (lb) pair. Idempotent: run as often as you like.

Usage: python3 build_scripts/lb_only.py [--check]   (--check only reports, exit 1 when anything is left)
"""
import json, os, re, sys
WORK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KG_PER_LB = 0.45359237

def k(lb, orig=None):
    if lb < 1000:
        # under a thousand pounds the figure stays exact (5.5 lb dry ice, 300 lb tolerance); a kg-only value is rounded
        return (orig.strip() + ' lb') if orig else f'{int(round(lb))} lb'
    return f'{int(lb / 1000 + 0.5)}k lb'

def num(s):
    return float(s.replace(' ', '').replace(',', '').replace(' ', '').replace(' ', ''))

N = r'\d{1,3}(?:[ ,  ]\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?'
# "168 000 kg (370 376 lb)"  -> "370k lb"      (the FCOM's own pound figure wins)
PAIR = re.compile(rf'({N})\s?(?:kg|kilograms?|kilos?)\s?\(\s?({N})\s?(?:lb|lbs|pounds?)\s?\)')
# "116 000 kg" alone          -> converted
BARE = re.compile(rf'({N})\s?(?:kg|kilograms?|kilos?)\b')
# "401 241 lb" / "11,461 lb" / "5.5 pounds" alone -> thousands
LB = re.compile(rf'(?<![\d.])({N})\s?(lb|lbs|pounds?)\b(?!\s?\))(?!/)')
# "526.7 klbs" / "401.2 Klbs" (Rev 13 style) -> "527k lb"
KLB = re.compile(rf'({N})\s?[kK]lbs?\b')
# already converted "401k lb" is left alone (the LB regex cannot match it: 'k' sits between the number and lb)

# rates: "820 kg/h (1 800 lb/h)" -> "1 800 lb/h", "1 000 kg/min" -> "2 205 lb/min"; a rate keeps its exact figure
RATE_PAIR = re.compile(rf'({N})\s?(?:kg|kilograms?)/(h|hr|min)\s?\(\s?({N})\s?(?:lb|lbs|pounds?)/(?:h|hr|min)\s?\)')
RATE_BARE = re.compile(rf'({N})\s?(?:kg|kilograms?)/(h|hr|min)\b')
def grp(v): return f'{int(round(v)):,}'.replace(',', ' ')

def conv(s):
    if not isinstance(s, str) or ('kg' not in s and 'lb' not in s and 'pound' not in s and 'kilo' not in s): return s
    s = RATE_PAIR.sub(lambda m: f'{m.group(3).strip()} lb/{m.group(2)}', s)
    s = RATE_BARE.sub(lambda m: f'{grp(num(m.group(1)) / KG_PER_LB)} lb/{m.group(2)}', s)
    s = PAIR.sub(lambda m: k(num(m.group(2)), m.group(2)), s)
    s = BARE.sub(lambda m: k(num(m.group(1)) / KG_PER_LB), s)
    s = KLB.sub(lambda m: k(num(m.group(1)) * 1000), s)
    def lbrep(m):
        v = num(m.group(1))
        return k(v) if v >= 1000 else m.group(0)
    s = LB.sub(lbrep, s)
    return s

SKIP = {'src', 'verbatim', 'quote', 'fcom', 'ref', 'ident', 'id'}
def walk(o, skip_q=False):
    if isinstance(o, dict):
        return {kk: (v if isinstance(v, str) and (kk in SKIP or (skip_q and kk == 'q')) else walk(v, skip_q)) for kk, v in o.items()}
    if isinstance(o, list): return [walk(v, skip_q) for v in o]
    return conv(o)

FILES = ['data/limitations.json', 'data/limitations_drill.json', 'data/oe.json', 'data/fom_all.json', 'data/fom_questions.json',
         'data/oral_scope.json', 'data/jeopardy_pool.json', 'data/limit_or_bust_num.json', 'data/limit_or_bust_bool.json',
         'data/hot_seat_scenarios.json', 'data/memory_items_drill.json', 'data/flows_trainer.json', 'data/phase_flows.json',
         'corpus/limitations.json', 'corpus/fom.json', 'corpus/ioe.json', 'corpus/memory.json', 'corpus/flows.json',
         'fom_q/ch14.json']
SOURCES = ['build_scripts/gen/gen_phase_flows.py', 'build_scripts/gen/ans_part3.py', 'build_scripts/gen/spine_cockpit_prep.py']

def main():
    check = '--check' in sys.argv
    changed = 0
    for rel in FILES:
        p = os.path.join(WORK, rel)
        if not os.path.exists(p): continue
        raw = open(p, encoding='utf-8').read()
        d = json.loads(raw)
        new = walk(d, skip_q=(rel == 'data/phase_flows.json'))
        if json.dumps(new, ensure_ascii=False) != json.dumps(d, ensure_ascii=False):
            changed += 1
            if not check:
                # keep the file's own layout: re-dump with the same indent it had
                indent = None
                m = re.match(r'[\[{]\n( *)', raw)
                if m: indent = len(m.group(1))
                open(p, 'w', encoding='utf-8').write(json.dumps(new, ensure_ascii=False, indent=indent) + ('\n' if raw.endswith('\n') else ''))
            print(('would change' if check else 'rewrote'), rel)
    for rel in SOURCES:
        p = os.path.join(WORK, rel)
        if not os.path.exists(p): continue
        raw = open(p, encoding='utf-8').read()
        # only string literals carry values; quotes passed to box()/L() as verbatim FCOM text are the 5th arg and stay.
        # Simplest safe rule: convert every line that is not a verbatim quote line (those contain "........" dot leaders).
        # generator sources: only the Rev 13 style "526.7 klbs" literals are rewritten; answers come from the data
        # banks (already converted) and verbatim FCOM quotes must stay as printed.
        new = KLB.sub(lambda m: k(num(m.group(1)) * 1000), raw)
        if new != raw:
            changed += 1
            if not check: open(p, 'w', encoding='utf-8').write(new)
            print(('would change' if check else 'rewrote'), rel)
    print('files changed:', changed)
    if check and changed: sys.exit(1)

if __name__ == '__main__':
    main()
