/* Antibody Database — self-contained helpers (ported subset of spinymice utils.js)
   plus the page logic. No BLAST tool, no gene-detail links (not present on this site). */
(function () {
  'use strict';

  // ---- helpers ----------------------------------------------------------
  var _cache = {};
  async function loadJSON(path) {
    if (_cache[path]) return _cache[path];
    var res = await fetch(path);
    if (!res.ok) throw new Error('Failed to load ' + path + ' (' + res.status + ')');
    var data = await res.json();
    _cache[path] = data;
    return data;
  }

  function fillSelect(id, defaultLabel, values) {
    var sel = document.getElementById(id);
    var current = sel.value;
    sel.innerHTML = '<option value="">' + defaultLabel + '</option>' +
      values.map(function (v) {
        return '<option value="' + v + '"' + (v === current ? ' selected' : '') + '>' + v + '</option>';
      }).join('');
  }

  // Resolve an antibody to an external registry link (RRID → SciCrunch, else catalog → Antibody Registry)
  function antibodyLookupUrl(a) {
    if (a.rrid) {
      var clean = a.rrid.replace(/^RRID:/i, '');
      return 'https://scicrunch.org/resolver/RRID:' + clean;
    }
    if (a.catalog_number) {
      return 'https://www.antibodyregistry.org/search?q=' + encodeURIComponent(a.catalog_number);
    }
    return '';
  }

  // Make a table sortable by clicking headers
  function makeSortable(table) {
    if (!table) return;
    var headers = table.querySelectorAll('thead th');
    headers.forEach(function (th, idx) {
      th.style.cursor = 'pointer';
      th.title = 'Click to sort';
      var asc = true;
      th.addEventListener('click', function () {
        var tbody = table.querySelector('tbody');
        var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
        rows.sort(function (r1, r2) {
          var a = (r1.children[idx].innerText || '').trim().toLowerCase();
          var b = (r2.children[idx].innerText || '').trim().toLowerCase();
          var na = parseFloat(a), nb = parseFloat(b);
          if (!isNaN(na) && !isNaN(nb)) return asc ? na - nb : nb - na;
          return asc ? a.localeCompare(b) : b.localeCompare(a);
        });
        asc = !asc;
        rows.forEach(function (r) { tbody.appendChild(r); });
      });
    });
  }

  function downloadTSV(rows, filename) {
    if (!rows.length) return;
    var cols = Object.keys(rows[0]);
    var lines = [cols.join('\t')];
    rows.forEach(function (r) {
      lines.push(cols.map(function (c) {
        return ('' + (r[c] == null ? '' : r[c])).replace(/[\t\n\r]/g, ' ');
      }).join('\t'));
    });
    var blob = new Blob([lines.join('\n')], { type: 'text/tab-separated-values' });
    var url = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = url; link.download = filename;
    document.body.appendChild(link); link.click(); document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  function esc(s) {
    return ('' + (s == null ? '' : s)).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // ---- state ------------------------------------------------------------
  var abData = null, abSources = null, abFiltered = [];

  async function ensureAbs() {
    if (abData) return;
    var d = await loadJSON('data/antibodies.json');
    abData = d.antibodies;
    abSources = d.sources || [];
    document.getElementById('ab-count-total').textContent = abData.length;
    populateFiltersFromData();
    filterAbs();
    if (abSources.length) renderSources();
  }

  function populateFiltersFromData() {
    var cats = new Set(), apps = new Set(), tissues = new Set();
    abData.forEach(function (a) {
      if (a.category) cats.add(a.category);
      if (a.application) a.application.split(/[,\/]/).map(function (s) { return s.trim(); }).filter(Boolean).forEach(function (v) { apps.add(v); });
      if (a.tissue_tested) a.tissue_tested.split(/[,;]/).map(function (s) { return s.trim(); }).filter(Boolean).forEach(function (v) { tissues.add(v); });
    });
    fillSelect('ab-cat', 'All categories', Array.from(cats).sort());
    fillSelect('ab-app', 'All applications', Array.from(apps).sort());
    fillSelect('ab-tissue', 'All tissues', Array.from(tissues).sort());
  }

  function filterAbs() {
    if (!abData) { ensureAbs(); return; }
    var q = document.getElementById('ab-search').value.trim().toUpperCase();
    var cat = document.getElementById('ab-cat').value;
    var wks = document.getElementById('ab-works').value;
    var app = document.getElementById('ab-app').value;
    var tis = document.getElementById('ab-tissue').value;

    abFiltered = abData.filter(function (a) {
      if (cat && a.category !== cat) return false;
      if (wks && a.result !== wks) return false;
      if (app && (a.application || '').indexOf(app) === -1) return false;
      if (tis && (a.tissue_tested || '').indexOf(tis) === -1) return false;
      if (q) {
        var blob = [a.target, a.clonality, a.catalog_number, a.vendor, a.rrid, a.notes, a.source_publication, a.host_species].join(' ').toUpperCase();
        if (blob.indexOf(q) === -1) return false;
      }
      return true;
    });
    renderAbTable(abFiltered);
  }

  function fmtRef(a) {
    var pub = a.source_publication || '—';
    if (a.doi) return '<a class="ab-link" href="https://doi.org/' + esc(a.doi) + '" target="_blank" rel="noopener">' + esc(pub) + '</a>';
    return esc(pub);
  }

  function fmtCloneCat(a) {
    var parts = [];
    if (a.host_species) parts.push('<span class="ab-muted">' + esc(a.host_species) + '</span>');
    if (a.clonality) parts.push(esc(a.clonality));
    if (a.catalog_number) {
      var url = antibodyLookupUrl(a);
      if (url) {
        var title = a.rrid ? ('Resolve RRID:' + a.rrid.replace(/^RRID:/i, '') + ' via SciCrunch')
                           : ('Look up ' + a.catalog_number + ' on the Antibody Registry');
        parts.push('<a class="ab-link" href="' + url + '" target="_blank" rel="noopener" title="' + esc(title) + '">' + esc(a.catalog_number) + '</a>');
      } else {
        parts.push(esc(a.catalog_number));
      }
    }
    if (a.rrid) {
      var clean = a.rrid.replace(/^RRID:/i, '');
      parts.push('<a class="ab-link ab-rrid" href="https://scicrunch.org/resolver/RRID:' + clean + '" target="_blank" rel="noopener">RRID:' + esc(clean) + '</a>');
    }
    return parts.length ? parts.join('<br>') : '—';
  }

  function renderAbTable(abs) {
    var el = document.getElementById('ab-results');
    if (!abs.length) {
      el.innerHTML = '<div class="ab-empty">🧪<p>No antibodies match your filters.</p></div>';
      return;
    }
    el.innerHTML =
      '<div class="ab-result-count"><strong>' + abs.length + '</strong> antibod' + (abs.length !== 1 ? 'ies' : 'y') + ' found' +
      '<button class="btn btn-outline btn-sm" onclick="AntibodyDB.downloadFiltered()">Download TSV</button></div>' +
      '<div class="ab-table-wrap"><table id="ab-table"><thead><tr>' +
      '<th>Target</th><th>Category</th><th>Host / Clone / Cat #</th><th>Company</th>' +
      '<th>App</th><th>Dilution</th><th>Tissue</th><th>Works?</th><th>Notes</th><th>Reference</th>' +
      '</tr></thead><tbody>' +
      abs.map(function (a) {
        var wc = a.result === 'works' ? 'works-yes' : a.result === 'fails' ? 'works-no' : 'works-part';
        var wi = a.result === 'works' ? '✓ Works' : a.result === 'fails' ? '✗ Fails' : '~ Partial';
        return '<tr>' +
          '<td><strong>' + (a.target ? esc(a.target) : '—') + '</strong></td>' +
          '<td><span class="ab-cat-badge">' + esc(a.category || '—') + '</span></td>' +
          '<td class="ab-mono">' + fmtCloneCat(a) + '</td>' +
          '<td>' + esc(a.vendor || '—') + '</td>' +
          '<td>' + esc(a.application || '—') + '</td>' +
          '<td class="ab-mono">' + esc(a.dilution || '—') + '</td>' +
          '<td>' + esc(a.tissue_tested || '—') + '</td>' +
          '<td><span class="' + wc + '">' + wi + '</span></td>' +
          '<td class="ab-notes">' + esc(a.notes || '—') + '</td>' +
          '<td class="ab-ref">' + fmtRef(a) + '</td>' +
          '</tr>';
      }).join('') +
      '</tbody></table></div>';
    makeSortable(document.getElementById('ab-table'));
  }

  function renderSources() {
    var wrap = document.getElementById('ab-sources');
    var list = document.getElementById('ab-sources-list');
    wrap.style.display = '';
    document.getElementById('ab-sources-count').textContent = abSources.length;
    list.innerHTML = '<div class="ab-table-wrap"><table><thead><tr><th>Citation</th><th>Tissue Focus</th><th>Ab Count</th><th>DOI</th></tr></thead><tbody>' +
      abSources.map(function (s) {
        return '<tr><td><strong>' + esc(s.short_citation) + '</strong></td>' +
          '<td>' + esc(s.tissue_focus || '—') + '</td>' +
          '<td>' + esc(s.antibody_count || '—') + '</td>' +
          '<td>' + (s.doi ? '<a class="ab-link" href="https://doi.org/' + esc(s.doi) + '" target="_blank" rel="noopener">' + esc(s.doi) + '</a>' : '—') + '</td></tr>';
      }).join('') + '</tbody></table></div>';
  }

  function tsvRows(list) {
    return list.map(function (a) {
      return {
        target: a.target, category: a.category, host_species: a.host_species,
        clonality: a.clonality, catalog_number: a.catalog_number, rrid: a.rrid,
        vendor: a.vendor, application: a.application, dilution: a.dilution,
        tissue_tested: a.tissue_tested, result: a.result, notes: a.notes,
        source_publication: a.source_publication, doi: a.doi, contributor: a.contributor
      };
    });
  }

  async function downloadFull() {
    await ensureAbs();
    downloadTSV(tsvRows(abData), 'acomys_all_antibodies.tsv');
  }
  function downloadFiltered() {
    downloadTSV(tsvRows(abFiltered), 'acomys_antibodies.tsv');
  }

  // ---- expose + init ----------------------------------------------------
  window.AntibodyDB = { filterAbs: filterAbs, downloadFull: downloadFull, downloadFiltered: downloadFiltered };

  document.addEventListener('DOMContentLoaded', async function () {
    ['ab-search'].forEach(function (id) {
      document.getElementById(id).addEventListener('input', filterAbs);
    });
    ['ab-cat', 'ab-works', 'ab-app', 'ab-tissue'].forEach(function (id) {
      document.getElementById(id).addEventListener('change', filterAbs);
    });
    await ensureAbs();
    var urlQ = new URLSearchParams(window.location.search).get('q');
    if (urlQ) { document.getElementById('ab-search').value = urlQ; filterAbs(); }
  });
})();
