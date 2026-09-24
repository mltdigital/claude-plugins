# [Client name] — client facts

<!-- Identity line below answers Q1 of fact-sheet-questions.md. -->

[One line: full firm name (domain), jurisdiction and practice focus, office locations. Drop-in HTML content work started DD Mon YYYY.]

Field status words: "to verify this build" (the site will prove it; filled before handover), "not yet captured" (unknown after the build or unanswered), otherwise the verified or supplied value with its date.

## Client-specific rules (override the general defaults in SKILL.md)
- [Only rules that differ from the skill's defaults, e.g. a shared stylesheet and shared root id across pages, a required disclaimer, banned wording. Write "None" if there are none.]

## Facts

- CMS: [platform + theme + page builder, kit name if Elementor, sitemap location (e.g. Yoast /sitemap_index.xml → /page-sitemap.xml)]. [Note whether an existing client's CMS override patterns apply directly.]
- Design tokens (Chrome-verified DD Mon YYYY): [heading family/size/weight per level, body family/size/weight, heading colour, body colour, primary brand colour and where it is used, accent colours, section backgrounds, button shape/radius].
- Site colour tokens: [which `--e-global-color-*` (or theme.json / designer variable) names carry the verified brand values above, and which verified values have no maintained token. Cite tokens per build standard 9. If not yet captured, say so and record on the next build.]
- Content width by page template (measured on the target page's insertion container, DD Mon YYYY): [e.g. "Service page, no sidebar: 1080px. Blog single, right sidebar: 720px."]. One figure per template; never a single site-wide number.
- Accessibility: [any site colours that fail WCAG AA and the correction applied in builds; link underline policy; small-text colours that must be darkened].
- CSS delivery and shared components (Q2, Q3): [who inserts blocks; stylesheet or inline; where shared CSS lives; shared root id and class prefix if any; path to any shared stylesheet kept in this folder].
- Phone (Q4): [call-tracking provider (CallRail, Infinity, none) and its swap behaviour; the number to hardcode in content and why].
- Contact form / CTA destination (Q5): [page URL; whether a stable anchor ID exists or CTAs must link the full page URL].
- Required or banned wording (Q5): [e.g. "free consultation" not allowed; must state "we do not provide Legal Aid"].
- Schema ownership (Q6, then verified): [SEO plugin, hand-written JSON-LD widget, templates that output FAQPage or HowTo; what blocks may add].
- Verified URLs (HTTP 200, DD Mon YYYY): [comma-separated paths for service, team, contact and any authorship pages].
- Authorship / EEAT targets (Q7): [named solicitors, accreditations, profile URLs to cite].
- After launch (Q8): [content the client edits themselves; who supports the pages].
- Builds: [one line per build: date, topic, filename, block ID, starting heading level, schema types used].
- Notes: [tool quirks, fetch behaviour (e.g. site returns 403 to plain curl), anything the next builder would otherwise rediscover].
