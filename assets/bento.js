// Minimal shared behavior: close open <details> menus on outside click / Escape,
// and land cleanly on hash targets after images load.
(function () {
    'use strict';
    var menus = document.querySelectorAll('details.dd, details.mnav');
    function closeAll(except) {
        menus.forEach(function (d) { if (d !== except) d.removeAttribute('open'); });
    }
    document.addEventListener('click', function (e) {
        var inside = e.target.closest('details.dd, details.mnav');
        closeAll(inside);
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(null); });

    if (window.location.hash.length > 1) {
        if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
        window.addEventListener('load', function () {
            var t;
            try { t = document.querySelector(window.location.hash); } catch (err) { return; }
            if (t) requestAnimationFrame(function () { t.scrollIntoView({ behavior: 'instant', block: 'start' }); });
        });
    }
})();
