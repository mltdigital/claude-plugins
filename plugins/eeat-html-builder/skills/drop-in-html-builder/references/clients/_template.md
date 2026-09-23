# [Client name] — client facts

[One line: full firm name (domain), jurisdiction and practice focus, office locations. Drop-in HTML content work started DD Mon YYYY.]

- CMS: [platform + theme + page builder, kit name if Elementor, sitemap location (e.g. Yoast /sitemap_index.xml → /page-sitemap.xml)]. [Note whether an existing client's CMS override patterns apply directly.]
- Design tokens (Chrome-verified DD Mon YYYY): [heading family/size/weight per level, body family/size/weight, heading colour, body colour, primary brand colour and where it is used, accent colours, section backgrounds, button shape/radius].
- Site colour tokens: [which `--e-global-color-*` (or theme.json / designer variable) names carry the verified brand values above, and which verified values have no maintained token. Cite tokens per build standard 9. If not yet captured, say so and record on the next build.]
- Content width by page template (measured on the target page's insertion container, DD Mon YYYY): [e.g. "Service page, no sidebar: 1080px. Blog single, right sidebar: 720px."]. One figure per template; never a single site-wide number.
- Accessibility: [any site colours that fail WCAG AA and the correction applied in builds; link underline policy; small-text colours that must be darkened].
- Phone: [call-tracking provider (CallRail, Infinity, none) and its swap behaviour; the number to hardcode in content and why].
- Contact form / CTA destination: [page URL; whether a stable anchor ID exists or CTAs must link the full page URL].
- Verified URLs (HTTP 200, DD Mon YYYY): [comma-separated paths for service, team, contact and any authorship pages].
- Authorship / EEAT targets: [named solicitors, accreditations, profile URLs to cite].
- Builds: [one line per build: date, topic, filename, block ID, starting heading level, schema types used].
- Notes: [tool quirks, fetch behaviour (e.g. site returns 403 to plain curl), anything the next builder would otherwise rediscover].
