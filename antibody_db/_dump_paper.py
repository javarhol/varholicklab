#!/usr/bin/env python3
"""Dev helper for the curated extraction pass: print tight antibody-declaration
sentences for a candidate paper (by index into antibody_candidates.json, or by
DOI/id substring). Not part of the site; used only while mining.

Usage:
  python3 antibody_db/_dump_paper.py <index>
  python3 antibody_db/_dump_paper.py doi:10.1016/j.devcel.2021.12.008
  python3 antibody_db/_dump_paper.py id:W2009749644
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
idx = json.load(open(os.path.join(ROOT, "acomys_library", "search_index.json")))
cand = json.load(open(os.path.join(HERE, "antibody_candidates.json")))["candidates"]

# full text by paper id
text_by_id = {}
for c in idx:
    text_by_id.setdefault(c["id"], []).append(c.get("text", "") or "")

DECL = re.compile(
    r"RRID:?\s*AB_?\d+|\bab\d{3,}\b|\bsc[-\s]?\d{2,}\b|cat(?:alog|\.)?\s*(?:no|#|number)|"
    r"anti[-\s]|antibod|\bIgG\b|\d+\s*:\s*\d{2,}", re.I)
VEND = re.compile(
    r"abcam|santa\s*cruz|cell\s*signaling|invitrogen|thermo|sigma|aldrich|millipore|merck|"
    r"becton|pharmingen|\bBD\b|dako|agilent|R&D|biolegend|novus|proteintech|jackson|vector|"
    r"genetex|origene|biorbyt|wako|cusabio|bio-?rad|ebioscience|synaptic|aviva|rockland|"
    r"leica|roche|beckman", re.I)


def dump(c):
    print("=" * 90)
    print(f"{c['short_citation']}  |  {c['year']}  |  score={c['score']}")
    print(f"DOI: {c['doi'] or '(none)'}   id={c['id']}")
    print(f"TITLE: {c['title']}")
    print(f"AUTHORS: {c['authors'][:120]}")
    print("-" * 90)
    full = " ".join(text_by_id.get(c["id"], []))
    full = re.sub(r"\s+", " ", full)
    # sentence-ish split
    sents = re.split(r"(?<=[.;])\s+", full)
    seen = set()
    n = 0
    for s in sents:
        if len(s) < 12 or len(s) > 600:
            continue
        if DECL.search(s) and (VEND.search(s) or re.search(r"anti[-\s]|antibod", s, re.I)):
            key = s[:80].lower()
            if key in seen:
                continue
            seen.add(key)
            n += 1
            print(f"[{n}] {s.strip()}")
    if n == 0:
        print("(no antibody-declaration sentences matched)")


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "0"
    if arg.startswith("doi:"):
        key = arg[4:].lower()
        hits = [c for c in cand if key in (c["doi"] or "").lower()]
    elif arg.startswith("id:"):
        key = arg[3:]
        hits = [c for c in cand if key == c["id"]]
    elif "-" in arg and all(p.isdigit() for p in arg.split("-")):
        a, b = map(int, arg.split("-"))
        hits = cand[a:b + 1]
    else:
        hits = [cand[int(arg)]]
    for c in hits:
        dump(c)


if __name__ == "__main__":
    main()
