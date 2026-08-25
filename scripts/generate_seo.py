#!/usr/bin/env python3
"""
generate_seo.py — regenerate the site's SEO / discoverability assets from data.

What it (re)writes, idempotently:
  1. Static, crawler-readable listings injected into the two database pages
     (antibody_db/index.html and acomys_library/index.html) between
     <!-- SEO_PRERENDER_START --> ... <!-- SEO_PRERENDER_END -->.
     The pages' JavaScript replaces these containers on load, so human visitors
     still get the interactive UI; search engines that don't run JS get the data.
  2. schema.org Dataset JSON-LD for each database page, between
     <!-- SEO_DATASET_JSONLD_START --> ... <!-- SEO_DATASET_JSONLD_END -->.
     This is what qualifies each resource for Google Dataset Search.
  3. Per-target antibody landing pages under antibody_db/targets/, so long-tail
     queries ("spiny mouse collagen antibody") land directly on relevant content.
  4. ScholarlyArticle JSON-LD for publications.html (parsed from the page itself),
     between <!-- SEO_PUBLICATIONS_JSONLD_START --> ... <!-- ..._END -->.
  5. sitemap.xml at the repo root, covering every static page plus target pages.

Run from the repo root:  python generate_seo.py
No third-party dependencies (standard library only).
"""

import os
import re
import json
import html
import datetime

SITE = "https://varholicklab.org"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()

AB_JSON = os.path.join(ROOT, "antibody_db", "data", "antibodies.json")
LIB_JSON = os.path.join(ROOT, "acomys_library", "acomys_library.json")
AB_PAGE = os.path.join(ROOT, "antibody_db", "index.html")
LIB_PAGE = os.path.join(ROOT, "acomys_library", "index.html")
PUB_PAGE = os.path.join(ROOT, "publications.html")
TARGETS_DIR = os.path.join(ROOT, "antibody_db", "targets")
SITEMAP = os.path.join(ROOT, "sitemap.xml")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def replace_between(text, start_marker, end_marker, inner):
    """Replace the content between two marker comments (markers preserved)."""
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL
    )
    replacement = start_marker + "\n" + inner + "\n    " + end_marker
    # Use a function replacement so backslashes/group-refs in data aren't interpreted.
    new_text, n = pattern.subn(lambda _m: replacement, text)
    if n == 0:
        raise RuntimeError(
            "Markers %s / %s not found — cannot inject." % (start_marker, end_marker)
        )
    return new_text


def slugify(s):
    s = re.sub(r"\(.*?\)", " ", s or "")           # drop parentheticals
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s or "other"


def target_base(target):
    """Collapse "Collagen I (WB)" and "Collagen I" to one landing page."""
    base = re.sub(r"\s*\(.*?\)\s*", " ", target or "").strip()
    return base or (target or "Other").strip()


def jsonld(obj):
    body = json.dumps(obj, indent=2, ensure_ascii=False)
    body = "\n".join("    " + line for line in body.splitlines())
    return '    <script type="application/ld+json">\n' + body + "\n    </script>"


# --------------------------------------------------------------------------- #
# 1 + 3. Antibody database: prerender listing, Dataset JSON-LD, target pages
# --------------------------------------------------------------------------- #
def antibody_row(a):
    doi = a.get("doi")
    pub = a.get("source_publication") or "—"
    ref = (
        '<a href="https://doi.org/%s" rel="noopener">%s</a>' % (esc(doi), esc(pub))
        if doi
        else esc(pub)
    )
    result = a.get("result") or ""
    result_label = {"works": "Works", "fails": "Does not work"}.get(result, "Partial")
    return (
        "<tr>"
        "<td><strong>%s</strong></td>"
        "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"
        "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"
        "</tr>"
        % (
            esc(a.get("target") or "—"),
            esc(a.get("host_species") or "—"),
            esc(a.get("clonality") or "—"),
            esc(a.get("vendor") or "—"),
            esc(a.get("catalog_number") or "—"),
            esc(a.get("application") or "—"),
            esc(a.get("tissue_tested") or "—"),
            esc(result_label),
            ref,
        )
    )


def build_antibody_prerender(abs_):
    rows = "\n".join(antibody_row(a) for a in abs_)
    # This block is visible only to no-JS crawlers; antibody.js overwrites it.
    return (
        '            <noscript><p class="ab-muted">This page is interactive; '
        "enable JavaScript to search and filter.</p></noscript>\n"
        '            <h2 class="sr-only">All %d validated antibodies</h2>\n'
        '            <div class="ab-table-wrap"><table><thead><tr>'
        "<th>Target</th><th>Host</th><th>Clonality</th><th>Company</th>"
        "<th>Catalog #</th><th>Application</th><th>Tissue tested</th>"
        "<th>Result</th><th>Source</th>"
        "</tr></thead><tbody>\n%s\n</tbody></table></div>"
        % (len(abs_), rows)
    )


def build_antibody_dataset(abs_):
    dates = [a.get("date_added") for a in abs_ if a.get("date_added")]
    modified = max(dates) if dates else TODAY
    obj = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "Acomys Antibody & Reagent Database",
        "description": (
            "A community-curated database of %d antibodies and reagents validated "
            "to cross-react with spiny mouse (Acomys) proteins, with target, vendor, "
            "catalog number, application, tissue, validation result, and source "
            "publication for each entry." % len(abs_)
        ),
        "url": SITE + "/antibody_db/",
        "sameAs": SITE + "/antibody_db/",
        "keywords": [
            "Acomys", "spiny mouse", "antibody validation", "immunohistochemistry",
            "western blot", "cross-reactivity", "regeneration", "reagents",
        ],
        "creator": {
            "@type": "ResearchOrganization",
            "name": "Varholick Lab",
            "url": SITE + "/",
        },
        "isAccessibleForFree": True,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "datePublished": "2026-03-08",
        "dateModified": modified,
        "distribution": [
            {
                "@type": "DataDownload",
                "encodingFormat": "application/json",
                "contentUrl": SITE + "/antibody_db/data/antibodies.json",
            }
        ],
    }
    return jsonld(obj)


TARGET_PAGE_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{site}/images/mus_uninjuredpad.png">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:site_name" content="Varholick Lab">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="canonical" href="{url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="../../assets/tailwind-config.js?v=r7"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../assets/styles.css?v=r7">
    <style>
      table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
      th, td {{ text-align: left; padding: 0.5rem 0.7rem; border-bottom: 1px solid rgba(197,198,200,0.5); vertical-align: top; }}
      th {{ background: var(--ksu-cream); font-family: 'Space Grotesk', sans-serif; }}
      a {{ color: #a67c00; text-decoration: underline; }}
    </style>
    <script type="application/ld+json">
{jsonld}
    </script>
</head>
<body class="bg-ksu-cream">
    <header class="bg-white border-b border-ksu-grey/60 py-4 px-6 md:px-12">
        <nav class="container mx-auto flex items-center gap-3">
            <a href="../../index.html" class="flex items-center gap-3">
                <img src="../../images/repairlablogo.png" alt="Varholick Lab logo" class="h-10 w-auto object-contain">
                <span class="text-lg font-extrabold text-ksu-black uppercase tracking-wide">Varholick Lab</span>
            </a>
        </nav>
    </header>
    <main class="container mx-auto px-6 md:px-12 py-10 max-w-4xl">
        <p class="text-sm text-gray-500 mb-4">
            <a href="../../index.html">Home</a> ›
            <a href="../index.html">Antibody Database</a> › {target}
        </p>
        <h1 class="text-3xl md:text-4xl font-extrabold text-ksu-black mb-3">{target} antibodies for spiny mouse (<em class="italic">Acomys</em>)</h1>
        <p class="text-gray-600 mb-6">{desc}</p>
        <div style="overflow-x:auto;"><table>
            <thead><tr><th>Target</th><th>Host</th><th>Clonality</th><th>Company</th><th>Catalog #</th><th>Application</th><th>Tissue tested</th><th>Result</th><th>Source</th></tr></thead>
            <tbody>
{rows}
            </tbody>
        </table></div>
        <p class="mt-8"><a href="../index.html">← Search the full Acomys Antibody Database</a></p>
    </main>
    <footer class="bg-ksu-black text-gray-400 py-8 px-6 md:px-12 mt-8 text-sm">
        <div class="container mx-auto">&copy; 2026 Varholick Lab · Kennesaw State University</div>
    </footer>
</body>
</html>
"""


def build_target_pages(abs_):
    # Group case-insensitively so "SOX9"/"Sox9" share one page; keep a display name.
    groups = {}          # lower-key -> list of antibodies
    display = {}         # lower-key -> display label (first seen)
    for a in abs_:
        base = target_base(a.get("target"))
        key = base.lower()
        groups.setdefault(key, []).append(a)
        display.setdefault(key, base)
    groups = {display[k]: v for k, v in groups.items()}

    if os.path.isdir(TARGETS_DIR):
        for old in os.listdir(TARGETS_DIR):
            if old.endswith(".html"):
                os.remove(os.path.join(TARGETS_DIR, old))
    os.makedirs(TARGETS_DIR, exist_ok=True)

    slugs = []
    for base, entries in sorted(groups.items()):
        slug = slugify(base)
        url = "%s/antibody_db/targets/%s.html" % (SITE, slug)
        vendors = sorted({e.get("vendor") for e in entries if e.get("vendor")})
        desc = (
            "%d validated %s antibod%s confirmed to cross-react with spiny mouse "
            "(Acomys) proteins%s. Includes vendor, catalog number, application, "
            "tissue, and source publication."
            % (
                len(entries),
                base,
                "y" if len(entries) == 1 else "ies",
                (" from " + ", ".join(vendors[:4])) if vendors else "",
            )
        )
        rows = "\n".join("            " + antibody_row(e) for e in entries)
        ds = {
            "@context": "https://schema.org",
            "@type": "Dataset",
            "name": "%s antibodies validated in Acomys" % base,
            "description": desc,
            "url": url,
            "keywords": ["Acomys", "spiny mouse", base, "antibody validation"],
            "isPartOf": {"@type": "Dataset", "name": "Acomys Antibody & Reagent Database",
                         "url": SITE + "/antibody_db/"},
            "creator": {"@type": "ResearchOrganization", "name": "Varholick Lab",
                        "url": SITE + "/"},
            "isAccessibleForFree": True,
            "dateModified": TODAY,
        }
        ds_str = "\n".join(
            "    " + line for line in json.dumps(ds, indent=2, ensure_ascii=False).splitlines()
        )
        page = TARGET_PAGE_TMPL.format(
            title=esc("%s antibodies for spiny mouse (Acomys) — Varholick Lab" % base),
            desc=esc(desc),
            site=SITE,
            url=esc(url),
            target=esc(base),
            rows=rows,
            jsonld=ds_str,
        )
        write(os.path.join(TARGETS_DIR, slug + ".html"), page)
        slugs.append(slug)
    return slugs


# --------------------------------------------------------------------------- #
# 1 + 2. Acomys library: prerender listing + Dataset JSON-LD
# --------------------------------------------------------------------------- #
def library_item(p):
    title = strip_tags(p.get("title"))
    doi = (p.get("links") or {}).get("doi") or ""
    if doi and not doi.startswith("http"):
        doi = "https://doi.org/" + doi
    year = p.get("year") or ""
    journal = strip_tags(p.get("journal"))
    authors = strip_tags(p.get("authors"))
    meta = " · ".join([x for x in [authors, journal, str(year) if year else ""] if x])
    link = ' <a href="%s" rel="noopener">DOI</a>' % esc(doi) if doi else ""
    return (
        '<li><span class="font-semibold">%s</span><br>'
        '<span class="text-sm text-gray-600">%s</span>%s</li>'
        % (esc(title), esc(meta), link)
    )


def build_library_prerender(papers):
    ordered = sorted(papers, key=lambda p: (p.get("year") or 0), reverse=True)
    items = "\n".join(library_item(p) for p in ordered)
    return (
        '            <noscript><p class="text-gray-600">This page is interactive; '
        "enable JavaScript to search and filter.</p></noscript>\n"
        '            <h2 class="sr-only">All %d publications on spiny mice (Acomys)</h2>\n'
        '            <ul class="space-y-4 list-none">\n%s\n</ul>' % (len(ordered), items)
    )


def build_library_dataset(papers):
    years = [p.get("year") for p in papers if p.get("year")]
    span = ""
    if years:
        span = " spanning %d–%d" % (min(years), max(years))
    obj = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "Acomys Library — spiny mouse literature database",
        "description": (
            "A comprehensive, continuously updated bibliography of %d peer-reviewed "
            "articles, preprints, and conference abstracts on spiny mice (Acomys)%s, "
            "with titles, authors, journals, abstracts, topics, and DOI links."
            % (len(papers), span)
        ),
        "url": SITE + "/acomys_library/",
        "sameAs": SITE + "/acomys_library/",
        "keywords": [
            "Acomys", "spiny mouse", "regeneration", "wound healing", "blastema",
            "bibliography", "literature database", "preprints",
        ],
        "creator": {
            "@type": "ResearchOrganization",
            "name": "Varholick Lab",
            "url": SITE + "/",
        },
        "isAccessibleForFree": True,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "datePublished": "2025-01-01",
        "dateModified": TODAY,
        "distribution": [
            {
                "@type": "DataDownload",
                "encodingFormat": "application/json",
                "contentUrl": SITE + "/acomys_library/acomys_library.json",
            }
        ],
    }
    return jsonld(obj)


# --------------------------------------------------------------------------- #
# 4. Publications ScholarlyArticle JSON-LD (parsed from publications.html)
# --------------------------------------------------------------------------- #
def build_publications_jsonld(pub_html):
    articles = []
    for m in re.finditer(r"<article\b.*?</article>", pub_html, re.DOTALL):
        block = m.group(0)
        h = re.search(r"<h4[^>]*>(.*?)</h4>", block, re.DOTALL)
        if not h:
            continue
        title = strip_tags(h.group(1))
        cite = re.search(r"<p[^>]*>(.*?)</p>", block, re.DOTALL)
        cite_txt = strip_tags(cite.group(1)) if cite else ""
        year_m = re.search(r"\((\d{4})\)", cite_txt)
        doi_m = re.search(r'href="(https://doi\.org/[^"]+)"', block)
        art = {"@type": "ScholarlyArticle", "headline": title, "name": title}
        if year_m:
            art["datePublished"] = year_m.group(1)
        if doi_m:
            art["sameAs"] = doi_m.group(1)
        articles.append(art)

    obj = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Publications — Varholick Lab",
        "url": SITE + "/publications.html",
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(articles),
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "item": a}
                for i, a in enumerate(articles)
            ],
        },
    }
    return jsonld(obj), len(articles)


# --------------------------------------------------------------------------- #
# 5. sitemap.xml
# --------------------------------------------------------------------------- #
def build_sitemap(target_slugs):
    urls = [
        (SITE + "/", "1.0"),
        (SITE + "/research.html", "0.8"),
        (SITE + "/publications.html", "0.8"),
        (SITE + "/team.html", "0.6"),
        (SITE + "/news.html", "0.6"),
    ]
    for slug in target_slugs:
        urls.append((SITE + "/antibody_db/targets/%s.html" % slug, "0.5"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pri in urls:
        lines.append("  <url>")
        lines.append("    <loc>%s</loc>" % esc(loc))
        lines.append("    <lastmod>%s</lastmod>" % TODAY)
        lines.append("    <priority>%s</priority>" % pri)
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    ab_data = json.loads(read(AB_JSON))
    abs_ = ab_data.get("antibodies", [])
    papers = json.loads(read(LIB_JSON))

    # Antibody page
    ab_html = read(AB_PAGE)
    ab_html = replace_between(
        ab_html, "<!-- SEO_PRERENDER_START -->", "<!-- SEO_PRERENDER_END -->",
        build_antibody_prerender(abs_),
    )
    ab_html = replace_between(
        ab_html, "<!-- SEO_DATASET_JSONLD_START -->", "<!-- SEO_DATASET_JSONLD_END -->",
        build_antibody_dataset(abs_),
    )
    write(AB_PAGE, ab_html)

    # Library page
    lib_html = read(LIB_PAGE)
    lib_html = replace_between(
        lib_html, "<!-- SEO_PRERENDER_START -->", "<!-- SEO_PRERENDER_END -->",
        build_library_prerender(papers),
    )
    lib_html = replace_between(
        lib_html, "<!-- SEO_DATASET_JSONLD_START -->", "<!-- SEO_DATASET_JSONLD_END -->",
        build_library_dataset(papers),
    )
    write(LIB_PAGE, lib_html)

    # Publications JSON-LD
    pub_html = read(PUB_PAGE)
    pub_jsonld, n_pubs = build_publications_jsonld(pub_html)
    pub_html = replace_between(
        pub_html,
        "<!-- SEO_PUBLICATIONS_JSONLD_START -->",
        "<!-- SEO_PUBLICATIONS_JSONLD_END -->",
        pub_jsonld,
    )
    write(PUB_PAGE, pub_html)

    # Target pages + sitemap
    slugs = build_target_pages(abs_)
    write(SITEMAP, build_sitemap(slugs))

    print("SEO assets regenerated:")
    print("  antibodies:        %d entries, %d target pages" % (len(abs_), len(slugs)))
    print("  library:           %d papers pre-rendered" % len(papers))
    print("  publications:      %d articles in JSON-LD" % n_pubs)
    print("  sitemap.xml:       %d URLs" % (7 + len(slugs)))


if __name__ == "__main__":
    main()
