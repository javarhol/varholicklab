#!/usr/bin/env python3
"""Merge curated mined antibodies (_mined_entries.py) into the antibody database.

Re-runnable: always starts from the pristine seed (antibodies.seed.json), applies
the mined entries, and writes antibodies.json. Convention (matching the seed): one
row per antibody PRODUCT (catalog #); additional papers using the same product are
folded into that row's `notes` rather than duplicated. A mined source publication
is only added if it contributed at least one genuinely new product.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _mined_entries as M  # noqa: E402

SEED = os.path.join(HERE, "data", "antibodies.seed.json")
OUT = os.path.join(HERE, "data", "antibodies.json")


def ncat(x):
    return re.sub(r"[^a-z0-9]", "", (x or "").lower())


def nrrid(x):
    return re.sub(r"[^a-z0-9]", "", (x or "").lower()).replace("rrid", "")


def key_no_cat(a):
    return (ncat(a.get("target")), ncat(a.get("vendor")), ncat(a.get("application")))


def main():
    db = json.load(open(SEED))
    abs_ = db["antibodies"]

    by_cat, by_rrid, by_soft = {}, {}, {}
    for a in abs_:
        if a.get("catalog_number"):
            by_cat[ncat(a["catalog_number"])] = a
        if a.get("rrid"):
            by_rrid[nrrid(a["rrid"])] = a
        by_soft[key_no_cat(a)] = a

    added, merged = 0, 0
    sources_with_new = set()

    for e in M.ENTRIES:
        e = dict(e)
        e["contributor"] = M.CONTRIB
        e["date_added"] = M.DATE
        src = e["source_publication"]

        existing = None
        if e.get("catalog_number") and ncat(e["catalog_number"]) in by_cat:
            existing = by_cat[ncat(e["catalog_number"])]
        elif e.get("rrid") and nrrid(e["rrid"]) in by_rrid:
            existing = by_rrid[nrrid(e["rrid"])]
        elif not e.get("catalog_number") and key_no_cat(e) in by_soft:
            existing = by_soft[key_no_cat(e)]

        if existing is not None:
            merged += 1
            # enrich missing fields
            for f in ("rrid", "dilution", "host_species", "clonality"):
                if not existing.get(f) and e.get(f):
                    existing[f] = e[f]
            # fold the new paper into notes (idempotent)
            tag = f"Also {src}"
            if existing.get("source_publication") != src and tag not in (existing.get("notes") or ""):
                extra = tag + (f" {e['tissue_tested']}" if e.get("tissue_tested") else "")
                existing["notes"] = ((existing.get("notes") or "").strip()
                                     + ("; " if existing.get("notes") else "") + extra)
            continue

        # genuinely new product
        abs_.append(e)
        if e.get("catalog_number"):
            by_cat[ncat(e["catalog_number"])] = e
        if e.get("rrid"):
            by_rrid[nrrid(e["rrid"])] = e
        by_soft[key_no_cat(e)] = e
        added += 1
        sources_with_new.add(src)

    # add sources only for papers that produced >=1 new product
    existing_source_dois = {re.sub(r"^https?://doi.org/", "", (s.get("doi") or "").lower())
                            for s in db["sources"]}
    src_added = 0
    for s in M.SOURCES:
        if s["short_citation"] not in sources_with_new:
            continue
        if (s.get("doi") or "").lower() in existing_source_dois:
            continue
        db["sources"].append(s)
        src_added += 1

    db["n"] = len(abs_)
    db["version"] = "v6"
    json.dump(db, open(OUT, "w"), indent=1, ensure_ascii=False)

    print(f"Seed antibodies: {json.load(open(SEED))['n']}")
    print(f"Mined entries processed: {len(M.ENTRIES)}  (new products: {added}, merged into existing: {merged})")
    print(f"New source publications added: {src_added}")
    print(f"Total antibodies now: {db['n']}  |  total sources: {len(db['sources'])}  |  version {db['version']}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
