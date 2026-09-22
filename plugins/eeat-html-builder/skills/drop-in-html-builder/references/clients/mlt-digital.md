# MLT Digital — client facts

MLT Digital (mltdigital.co.uk) — digital marketing agency for law firms; YMYL/EEAT content and HTML drop-in work. CEO is Stephen Moore.

- CMS: WordPress + Elementor. Yoast sitemaps at /sitemap_index.xml (pages in /page-sitemap.xml, blog posts in /post-sitemap.xml, no /service- or /person- sitemaps).
- Design tokens Chrome-verified 17 Jun 2026: headings Libre Franklin (hero h1 weight 800 white, section h2 weight 700 #333333, tight negative letter-spacing); body Inter #333333 / #212121, 16px, line-height ~1.5-1.7; brand accent pink #CC3366 (used for body links AND the header phone number); CTA buttons lime green #A3C126, pill border-radius 60px. Logo is "mlt." with a red/orange concentric-circle mark. Hero bands use a soft sky blue (~#EAF4FB).
- Site colour tokens: not yet captured. On the next build, run the token snippet in `cms-override-patterns.md` on the reference page and record here which `--e-global-color-*` (or other) names carry the verified brand values above, and which verified values have no maintained token. Cite tokens per build standard 9.
- Accessibility caveat: the live site puts WHITE text on the #A3C126 green button (~2:1, fails WCAG AA). For accessible builds use dark ink text on the green pill instead, and hard-code both the green and the ink as a pair (do not inherit the green from a site token while hard-coding the ink; a rebrand would break contrast silently). Record in the handover that the CTA pair needs a contrast re-check if the brand green changes.
- CTAs point to /contact-us/ (Elementor form, no verified fixed anchor — link to the full URL). Named enquiry contacts in supplied copy: Chris Davidson and Jamie Young.
- Team bios live at /our-team/<name>/ (e.g. /our-team/stephen-moore/, /chris-davidson/, /jamie-young/) — useful for EEAT authorship internal links.
- Good internal-link targets: /geo-for-law-firms-ai-search-visibility-by-mlt-digital/, /guides/seo-for-law-firms/, /guides/content-marketing-for-law-firms/, /law-firm-seo/, /ai-hub/, /insights/.
- First build 17 Jun 2026: YMYL / law-firm-SEO content drop-in, file mlt-digital--ymyl-law-firm-seo.html, scoped to #mlt-ymyl, BlogPosting JSON-LD, styled placeholder scoring table. Built per the universal build standards and CMS override patterns; content used verbatim per the no-content-changes rule.
