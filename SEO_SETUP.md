# SEO & Discoverability — Setup and Maintenance

This site is tuned so researchers can find the **Acomys Library** and **Antibody
Database** through Google, Bing, and **Google Dataset Search**. Most of it is
automatic; this file covers the one-time account steps only you can do, plus how
the pieces fit together.

## What's already in place (code)

- **`robots.txt`** — allows all crawlers, points to the sitemap.
- **`sitemap.xml`** — every page + one landing page per antibody target
  (`antibody_db/targets/*.html`). Regenerated automatically (see below).
- **Canonical URLs, Open Graph & Twitter cards** on every page; social-preview
  images now use absolute URLs so they render on LinkedIn/X/Slack.
- **Structured data (JSON-LD):**
  - Home page → `ResearchOrganization` + `WebSite` (site search box).
  - Acomys Library & Antibody Database → a `Dataset` each → **eligible for Google
    Dataset Search.**
  - Team → lab members; Publications → article list.
- **Crawlable database content** — both databases render entries via JavaScript,
  which crawlers often skip. `generate_seo.py` injects a static, no-JS list of
  every antibody/paper into each page so search engines can index them. Human
  visitors still get the interactive UI (the page's JS replaces the static list
  on load).
- **Per-target antibody pages** (e.g. `/antibody_db/targets/collagen-i.html`) so
  long-tail searches like *"spiny mouse collagen antibody"* land directly.

## Regenerating SEO assets

```bash
python scripts/generate_seo.py
```

Run from the repo root. It rewrites the sitemap, the crawlable listings, the
per-target pages, and the Dataset/publication JSON-LD from the data files. It is
**idempotent** (safe to run repeatedly) and has **no dependencies** beyond the
Python standard library.

The weekly GitHub Actions workflow (`.github/workflows/update_library.yml`) runs
it automatically after each library update and commits the results, so the
sitemap and crawlable content stay current as new papers/antibodies are added.

---

## One-time account steps (do these once, manually)

### 1. Google Search Console  *(highest priority)*

1. Go to <https://search.google.com/search-console> and sign in.
2. **Add property → URL prefix →** `https://varholicklab.org/`.
3. Choose the **HTML tag** verification method. Google shows a tag like
   `<meta name="google-site-verification" content="ABC123...">`.
4. Copy the token and paste it into **`index.html`**, replacing
   `REPLACE_WITH_GSC_TOKEN` in this line:
   ```html
   <meta name="google-site-verification" content="REPLACE_WITH_GSC_TOKEN">
   ```
5. Commit + push, wait for GitHub Pages to publish, then click **Verify**.
6. In Search Console → **Sitemaps**, submit: `sitemap.xml`
7. (Optional) Use **URL Inspection** on the Library and Antibody DB URLs and
   click **Request indexing** to speed up first crawl.

### 2. Bing Webmaster Tools

1. Go to <https://www.bing.com/webmasters> and sign in.
2. Use **Import from Google Search Console** (fastest) — this copies the verified
   site and sitemap. Otherwise add `https://varholicklab.org/` and submit
   `https://varholicklab.org/sitemap.xml` manually.

### 3. Confirm Google Dataset Search eligibility

1. Open Google's **Rich Results Test**: <https://search.google.com/test/rich-results>
2. Test these URLs and confirm a **Dataset** item is detected with no errors:
   - `https://varholicklab.org/acomys_library/`
   - `https://varholicklab.org/antibody_db/`
3. Once indexed, the databases become findable at
   <https://datasetsearch.research.google.com/>. (Indexing can take days to weeks.)

### 4. (Optional) Google Scholar

Scholar indexes the **`publications.html`** page and the linked PDFs. No action is
usually required, but you can confirm coverage in your
[Scholar profile](https://scholar.google.com/citations?user=JustinVarholick) and,
if pages are missed, review Scholar's inclusion guidelines:
<https://scholar.google.com/intl/en/scholar/inclusion.html>

---

## Verifying changes locally

```bash
# 1. Regenerate and confirm the sitemap is well-formed
python scripts/generate_seo.py
python -c "import xml.dom.minidom; xml.dom.minidom.parse('sitemap.xml'); print('OK')"

# 2. Confirm the databases expose content without JavaScript
#    (open the files with JS disabled, or grep the raw HTML)
grep -c "<tr>" antibody_db/index.html        # ~366 (365 antibodies + header)
grep -c "<li>" acomys_library/index.html     # ~955 papers (+ nav items)
```

Then paste each page's URL into the Rich Results Test (step 3 above) to validate
the structured data after deploying.
