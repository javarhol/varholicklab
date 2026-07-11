#!/usr/bin/env python3
"""
find_antibody_candidates.py

Mine the Acomys Library's parsed full text for papers that describe antibodies
and are NOT yet represented in the antibody database, then emit a per-paper
report of antibody-relevant text snippets for a curated extraction pass.

Inputs (relative to repo root):
  - acomys_library/search_index.json        full-text chunks of every library PDF
  - acomys_library/acomys_library_cleaned.json  paper metadata incl. DOIs
  - antibody_db/data/antibodies.json        current database (for already-mined DOIs)

Output:
  - antibody_db/antibody_candidates.json    ranked candidate papers + snippets

Papers are excluded if their DOI already appears in antibodies.json `sources`.
DOI matching is used deliberately (not author-name matching): library `authors`
strings begin with a full first name ("Jennifer Simkin, ...") while the database
sources read "Simkin et al.", so name matching is unreliable.

Run from the repo root:  python3 antibody_db/find_antibody_candidates.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEARCH_INDEX = os.path.join(ROOT, "acomys_library", "search_index.json")
LIBRARY = os.path.join(ROOT, "acomys_library", "acomys_library_cleaned.json")
ANTIBODIES = os.path.join(HERE, "data", "antibodies.json")
OUT = os.path.join(HERE, "antibody_candidates.json")

# --- signal regexes -------------------------------------------------------
APP_SIG = re.compile(
    r"antibod|immunohisto|immunofluoresc|immunostain|western\s*blot|"
    r"\bIHC\b|\bICC\b|\bIF\b|flow\s*cytom|\bRRID\b",
    re.I,
)
VENDOR_SIG = re.compile(
    r"abcam|santa\s*cruz|cell\s*signaling|invitrogen|thermo\s*(?:fisher|scientific)?|"
    r"sigma|aldrich|millipore|merck|\bBD\b|becton|pharmingen|dako|agilent|"
    r"\bR&D\b|biolegend|novus|proteintech|jackson\s*immuno|vector\s*lab|"
    r"genetex|origene|biorbyt|wako|cusabio|bio-rad|biorad|ebioscience|"
    r"synaptic\s*systems|aviva|rockland|leica|roche|beckman",
    re.I,
)
# Catalog numbers / RRIDs — used for ranking and snippet targeting
DETAIL_SIG = re.compile(
    r"RRID:?\s*AB_?\d+|\bab\d{4,}\b|\bsc[-\s]?\d{3,}\b|"
    r"cat(?:alog|\.)?\s*(?:no\.?|#|number)?\s*:?\s*[A-Za-z0-9\-]{3,}|"
    r"clone\s+[A-Za-z0-9\-\.]+|\d+\s*:\s*\d+(?:,?\d{3})?",  # dilutions like 1:500
    re.I,
)
CATRRID_COUNT = re.compile(r"RRID|\bab\d{4,}\b|\bsc[-\s]?\d{3,}\b|cat\.?\s*(?:no|#)", re.I)


def norm_doi(s):
    if not s:
        return ""
    s = str(s).strip().lower()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s)
    s = re.sub(r"^doi:\s*", "", s)
    return s.strip().rstrip(".")


def extract_doi_from_links(links_field):
    """cleaned.json `links` is a Python-repr string like
    "{'doi': 'https://doi.org/10.x', 'pdf': ''}" (or already a dict)."""
    if isinstance(links_field, dict):
        return norm_doi(links_field.get("doi", ""))
    if not links_field:
        return ""
    m = re.search(r"'doi'\s*:\s*'([^']*)'", str(links_field))
    return norm_doi(m.group(1)) if m else ""


def surname_of_first_author(authors):
    if not authors:
        return ""
    first = authors.split(",")[0].strip()
    parts = [p for p in re.split(r"\s+", first) if p]
    return parts[-1] if parts else ""


def make_snippets(text, max_snips=60, window=260):
    """Return de-duplicated context windows around antibody-detail signals."""
    spans = []
    for m in DETAIL_SIG.finditer(text):
        s = max(0, m.start() - window)
        e = min(len(text), m.end() + window)
        spans.append([s, e])
    if not spans:
        # fall back to windows around the application signals
        for m in APP_SIG.finditer(text):
            s = max(0, m.start() - window)
            e = min(len(text), m.end() + window)
            spans.append([s, e])
    spans.sort()
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1] + 40:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    snips = []
    for s, e in merged[:max_snips]:
        chunk = re.sub(r"\s+", " ", text[s:e]).strip()
        snips.append(chunk)
    return snips


def main():
    print("Loading data...")
    idx = json.load(open(SEARCH_INDEX))
    library = json.load(open(LIBRARY))
    abdb = json.load(open(ANTIBODIES))

    mined = {norm_doi(s.get("doi")) for s in abdb.get("sources", []) if s.get("doi")}
    print(f"  already-mined source DOIs: {len(mined)}")

    doi_by_id, meta_by_id = {}, {}
    for p in library:
        pid = p.get("id")
        if not pid:
            continue
        doi_by_id[pid] = extract_doi_from_links(p.get("links"))
        meta_by_id[pid] = p

    # group full-text chunks by paper
    papers = {}
    for c in idx:
        pid = c.get("id")
        if not pid:
            continue
        p = papers.setdefault(
            pid,
            {"title": c.get("title", ""), "authors": c.get("authors", ""),
             "year": str(c.get("year", "")), "text": []},
        )
        p["text"].append(c.get("text", "") or "")

    candidates = []
    for pid, p in papers.items():
        full = " ".join(p["text"])
        if not (APP_SIG.search(full) and VENDOR_SIG.search(full)):
            continue
        doi = doi_by_id.get(pid, "")
        if doi and doi in mined:
            continue
        score = len(CATRRID_COUNT.findall(full))
        surname = surname_of_first_author(p["authors"])
        year = p["year"]
        short = f"{surname} et al. {year}" if surname else (meta_by_id.get(pid, {}).get("title", "")[:40])
        candidates.append({
            "id": pid,
            "doi": doi,
            "short_citation": short,
            "authors": p["authors"],
            "year": year,
            "title": re.sub(r"<[^>]+>", "", p["title"]),
            "score": score,
            "snippets": make_snippets(full),
        })

    candidates.sort(key=lambda c: c["score"], reverse=True)

    out = {
        "generated_from": "acomys_library/search_index.json",
        "n_candidates": len(candidates),
        "note": "Papers with antibody+vendor signals whose DOI is not yet an antibody-DB source. "
                "For curated extraction — not auto-imported.",
        "candidates": candidates,
    }
    json.dump(out, open(OUT, "w"), indent=1, ensure_ascii=False)

    n_with_doi = sum(1 for c in candidates if c["doi"])
    print(f"Papers with full text: {len(papers)}")
    print(f"Candidate papers (antibody+vendor, not yet a source): {len(candidates)}")
    print(f"  ...with a resolved DOI: {n_with_doi}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
