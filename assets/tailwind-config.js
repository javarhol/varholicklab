// Shared Tailwind CDN theme extension — Kennesaw State University palette.
// Loaded on every page immediately after the Tailwind CDN <script>.
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'ksu-black': '#0B1315',   // primary text / dark sections
                'ksu-gold': '#FDBB30',    // single accent: links, rules, key CTAs
                'ksu-grey': '#C5C6C8',    // hairlines, muted UI
                'ksu-cream': '#FAF9F6',   // off-white section background
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                display: ['"Space Grotesk"', 'Inter', 'system-ui', 'sans-serif'],
            },
            maxWidth: {
                prose: '65ch',
            },
        },
    },
};
