// In-page WYSIWYG editor, injected by scripts/edit_server.py (local preview only).
(function () {
    'use strict';
    if (window.__vlEditor) return;
    window.__vlEditor = true;

    var EDITABLE = 'h1, h2, h3, h4, p, li, figcaption, blockquote, a.btn, .more, .chip, .brand b, .brand small, .what';
    var LOCKED = '.news-item, .t-news, #vl-editor';   // news text lives in news.json — edit it there

    // ---------------------------------------------------------------- toolbar
    var css = document.createElement('style');
    css.id = 'vl-editor-style';
    css.textContent = [
        '#vl-editor{position:fixed;right:16px;bottom:16px;z-index:9999;display:flex;gap:8px;align-items:center;',
        ' background:#0B1315;color:#fff;padding:10px 12px;border-radius:999px;box-shadow:0 12px 30px rgba(0,0,0,.35);',
        ' font:600 13px/1 Inter,system-ui,sans-serif}',
        '#vl-editor button{font:inherit;border:0;border-radius:999px;padding:8px 14px;cursor:pointer;background:#243135;color:#fff}',
        '#vl-editor button:disabled{opacity:.4;cursor:default}',
        '#vl-editor #vl-toggle{background:#FDBB30;color:#0B1315}',
        '#vl-editor #vl-status{font-weight:500;font-size:12px;color:#9fb0b5;max-width:220px}',
        'html.vl-editing [contenteditable="true"]:hover{outline:1.5px dashed rgba(253,187,48,.85);outline-offset:2px}',
        'html.vl-editing [contenteditable="true"]:focus{outline:2px solid #FDBB30;outline-offset:2px}',
        'html.vl-editing .news-item, html.vl-editing .t-news .list{opacity:.55}',
    ].join('');
    document.head.appendChild(css);

    var bar = document.createElement('div');
    bar.id = 'vl-editor';
    bar.innerHTML =
        '<button id="vl-toggle" type="button">&#9998; Edit page</button>' +
        '<button id="vl-save" type="button" disabled>Save</button>' +
        '<button id="vl-discard" type="button" disabled>Discard</button>' +
        '<span id="vl-status"></span>';
    document.body.appendChild(bar);

    var btnToggle = bar.querySelector('#vl-toggle');
    var btnSave = bar.querySelector('#vl-save');
    var btnDiscard = bar.querySelector('#vl-discard');
    var status = bar.querySelector('#vl-status');
    var editing = false, dirty = false;

    function editableEls() {
        return Array.prototype.filter.call(document.querySelectorAll(EDITABLE), function (el) {
            return !el.closest(LOCKED);
        });
    }

    function setEditing(on) {
        editing = on;
        document.documentElement.classList.toggle('vl-editing', on);
        editableEls().forEach(function (el) {
            if (on) { el.setAttribute('contenteditable', 'true'); el.setAttribute('spellcheck', 'true'); }
            else { el.removeAttribute('contenteditable'); el.removeAttribute('spellcheck'); }
        });
        btnToggle.innerHTML = on ? 'Done' : '&#9998; Edit page';
        btnSave.disabled = !on;
        btnDiscard.disabled = !on;
        status.textContent = on
            ? 'Click any text and type. Links are paused while editing \u2014 hit Done to browse again.'
            : (dirty ? 'Unsaved changes \u2014 re-enter Edit and Save, or Discard.' : '');
    }

    // Don't navigate away when clicking links mid-edit.
    document.addEventListener('click', function (e) {
        if (!editing) return;
        var a = e.target.closest('a');
        if (a && !a.closest('#vl-editor')) e.preventDefault();
    }, true);

    // Paste as plain text so no outside styling sneaks into the files.
    document.addEventListener('paste', function (e) {
        if (!editing) return;
        var t = e.target.closest && e.target.closest('[contenteditable="true"]');
        if (!t) return;
        e.preventDefault();
        document.execCommand('insertText', false, e.clipboardData.getData('text/plain'));
    });

    document.addEventListener('input', function (e) {
        if (!editing || !e.target.closest || e.target.closest('#vl-editor')) return;
        dirty = true;
        status.textContent = 'Unsaved changes';
    });

    window.addEventListener('beforeunload', function (e) {
        if (dirty) { e.preventDefault(); e.returnValue = ''; }
    });

    document.addEventListener('keydown', function (e) {
        if (editing && (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 's') {
            e.preventDefault();
            save();
        }
    });

    // Elements that existed when the page loaded. Anything that shows up later
    // (browser-extension containers, injected styles) is stripped before saving.
    var known = new WeakSet();
    Array.prototype.forEach.call(document.querySelectorAll('*'), function (el) { known.add(el); });

    function serialize() {
        var aliens = Array.prototype.filter.call(document.querySelectorAll('*'), function (el) {
            return !known.has(el);
        });
        aliens.forEach(function (el) { el.setAttribute('data-vl-alien', '1'); });
        var doc = document.documentElement.cloneNode(true);
        aliens.forEach(function (el) { el.removeAttribute('data-vl-alien'); });

        doc.classList.remove('vl-editing');
        if (!doc.className) doc.removeAttribute('class');
        doc.querySelectorAll('[data-vl-alien], #vl-editor, #vl-editor-style, script[data-vl-editor]')
            .forEach(function (n) { n.remove(); });
        doc.querySelectorAll('[contenteditable]').forEach(function (n) {
            n.removeAttribute('contenteditable');
            n.removeAttribute('spellcheck');
        });
        doc.querySelectorAll('details[open]').forEach(function (n) { n.removeAttribute('open'); });
        // Attributes stamped onto existing elements by browser extensions
        // (Grammarly, LanguageTool, ...) must not end up in the files.
        Array.prototype.forEach.call(doc.querySelectorAll('*'), function (n) {
            Array.prototype.slice.call(n.attributes).forEach(function (a) {
                if (/^data-(gr-|new-gr-|gramm|lt-|wxt)/.test(a.name)) n.removeAttribute(a.name);
            });
        });
        if (doc.querySelector('body')) {
            ['data-new-gr-c-s-check-loaded', 'data-gr-ext-installed'].forEach(function (a) {
                doc.querySelector('body').removeAttribute(a);
            });
        }

        var html = '<!DOCTYPE html>\n' + doc.outerHTML + '\n';
        // Cosmetic fixes for whitespace the DOM round trip cannot represent.
        html = html.replace(/^(<!DOCTYPE html>\n<html[^>]*>)<head>/, '$1\n<head>');
        html = html.replace(/\s*<\/body><\/html>\s*$/, '\n</body>\n</html>\n');
        return html;
    }

    function save() {
        if (!editing) return;
        status.textContent = 'Saving…';
        fetch('/_save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: location.pathname, html: serialize() }),
        }).then(function (r) { return r.json(); }).then(function (res) {
            if (res.ok) {
                dirty = false;
                setEditing(false);
                status.textContent = 'Saved \u2713 (' + res.file + ') \u2014 links work again.';
            } else {
                status.textContent = 'Save failed: ' + (res.error || 'unknown');
            }
        }).catch(function (err) {
            status.textContent = 'Save failed: ' + err;
        });
    }

    btnToggle.addEventListener('click', function () { setEditing(!editing); });
    btnSave.addEventListener('click', save);
    btnDiscard.addEventListener('click', function () {
        if (!dirty || confirm('Throw away unsaved edits on this page?')) { dirty = false; location.reload(); }
    });
})();
