// Shared site behavior: mobile menu toggle + smooth in-page scrolling.
(function () {
    'use strict';

    // --- Mobile menu ---
    var menuButton = document.getElementById('mobile-menu-button');
    var menu = document.getElementById('mobile-menu');
    var closeButton = document.getElementById('close-mobile-menu');

    function openMenu() { if (menu) menu.classList.remove('hidden'); }
    function closeMenu() { if (menu) menu.classList.add('hidden'); }

    if (menuButton) menuButton.addEventListener('click', openMenu);
    if (closeButton) closeButton.addEventListener('click', closeMenu);
    if (menu) {
        menu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', closeMenu);
        });
    }

    // --- Smooth scroll for same-page anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var id = this.getAttribute('href');
            if (id === '#' || id.length < 2) return;
            var target = document.querySelector(id);
            if (!target) return;
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // --- Scroll-reveal (fade / slide-up as sections enter the viewport) ---
    var revealEls = document.querySelectorAll('.reveal');
    if (revealEls.length) {
        if ('IntersectionObserver' in window) {
            var io = new IntersectionObserver(function (entries, obs) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        obs.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
            revealEls.forEach(function (el) { io.observe(el); });
        } else {
            // No IO support: just show everything.
            revealEls.forEach(function (el) { el.classList.add('is-visible'); });
        }
    }

    // --- Transparent header over hero, solidify on scroll (homepage only) ---
    var header = document.querySelector('.site-header[data-transparent-header]');
    if (header) {
        var syncHeader = function () {
            if (window.scrollY > 80) {
                header.classList.add('is-solid');
                header.removeAttribute('data-transparent-header');
            } else {
                header.classList.remove('is-solid');
                header.setAttribute('data-transparent-header', '');
            }
        };
        window.addEventListener('scroll', syncHeader, { passive: true });
        syncHeader();
    }
})();
