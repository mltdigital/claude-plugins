# Universal build standards

These rules apply to every HTML content block built in this project, for any client. They are CMS-agnostic unless a rule specifies otherwise.

**Rule 1 — Never include HTML document boilerplate.**
Drop-in blocks must contain only: any `<script>` blocks (e.g. JSON-LD), the content `<div>`, and, for inline CSS delivery, one `<style>` block. For stylesheet delivery the same CSS ships as a separate `.css` file and the fragment has no `<style>` at all. Never include `<!DOCTYPE>`, `<html>`, `<head>`, `<meta>`, `<title>`, or `<body>`. These conflict with the existing CMS page structure.

**Why:** Learned the hard way — a full HTML document wrapper in an Elementor page caused active conflicts and style bleed. The file must be a fragment, not a document.

**Rule 2 — Always identify the CMS and get a reference page before starting.**
Ask for: (a) the CMS and page builder (e.g. WordPress + Elementor, Webflow, Gutenberg), and (b) a URL to an existing page on the same site that can be used as a style reference. Without both, the build is guessing.

**Why:** Every CMS injects its own styles with varying specificity. A reference page lets you Chrome-verify the actual rendered output before writing a single line of CSS.

**Rule 3: Verify computed styles on the rendered reference page before building.**
Use the Chrome JavaScript tool to read computed styles from the live reference page: font-weight, font-size, line-height, text-align, heading colour, link colour, list style. Read values, not screenshots; a screenshot is the fallback when the Chrome tools are unavailable (see `screenshot-style-extraction.md`). Do not take a kit or theme CSS variable's value as a prediction of what renders; widget-level CSS overrides it routinely.

Then probe the target container: inject a bare `<p>` and `<h2>` into the content column and read what they get with nothing applied (snippet in `cms-override-patterns.md`, "Probe the target container"). The block's CSS is the difference between that and the reference page. Where they match, declare nothing.

**Why:** Kit-level CSS (Elementor global colours, font-weight: 300 on headings) is frequently overridden by widget-level CSS, so its value is not what the page shows. The rendered page is the ground truth for what a block should look like. That is a statement about values. Which source the block cites for a value once it is known is Rule 9.

**Rule 4 — Always fetch the sitemap for internal linking.**
Before building, fetch /sitemap_index.xml → /page-sitemap.xml (or equivalent). Find relevant service/practice pages and link appropriate terms in the body copy. If the client hasn't provided a sitemap URL, ask for it before starting.

**Why:** Internal linking is a core EEAT and SEO signal. Every drop-in block should connect to the wider site architecture.

**Rule 5 — Always verify every link before including it. Never guess.**
- Use `curl -s -o /dev/null -w "%{http_code}" <URL>` to confirm page URLs return 200
- Use the Claude in Chrome JavaScript tool to inspect the DOM for actual anchor IDs before writing `href="#..."` links
- If an anchor cannot be confirmed, fall back to the full page URL and document why

**Why:** The `#contact-form` mistake — an anchor that didn't exist — cost multiple revision rounds. Guessing anchor IDs sends users to the top of the page silently.

**Rule 6 — Always include relevant JSON-LD structured data.**
- Before adding any schema, inspect the page for a Yoast (or other SEO-plugin) schema graph already in the page source, and add only what it doesn't already own. Two FAQPage or HowTo nodes on one page is duplication, not reinforcement.
- FAQPage schema for any page with a FAQ section, if the site's own schema graph doesn't already carry one
- HowTo for step-by-step guides where appropriate, same check
- LegalService or other service schema where the client type warrants it
- JSON-LD must exactly match the visible on-page content — no invented entries

**Why:** FAQPage and HowTo remain useful vocabulary for describing the page to a crawler, but FAQPage no longer earns a rich result: Google restricted it to authoritative government and health sites in August 2023, then discontinued FAQ rich results outright, updating its documentation on 7 May 2026 and removing Search Console support by August 2026. Treat this schema as a semantic/EEAT signal, not a SERP-appearance play, and never duplicate a graph the SEO plugin already emits.

**Rule 7 — Align every build with EEAT and YMYL best practice.**
- Step-by-step process section, where the source content supports one (demonstrates expertise and depth); skip it rather than invent a process the source doesn't describe
- FAQ section, where the source content supports one (captures long-tail queries); skip it rather than manufacture questions
- Specific, verifiable claims only — no vague marketing language
- No invented facts, credentials, or statistics
- Headings come from the client's copy or the practice area. "Step-by-Step Guide to [X]", "Why Choose [Firm]?" and "Frequently Asked Questions About [X]" are banned as default headings — they are how three unrelated clients' builds ended up recognisable as one developer's work (`references/pattern-log.md`).

**Rule 8 — Align every build with CRO and UX best practices.**
- Place a CTA within the first screen — not only at the bottom
- Repeat CTAs at natural decision points (after process guide, after FAQ)
- Use numbered steps and accordions to reduce cognitive load
- WCAG 2.1 AA contrast minimum on all text and interactive elements (4.5:1 normal text, 3:1 large text and UI components)

**Rule 9: Inherit before you hard-code. No dead tokens, no orphan literals.**
Every colour in the block is declared once, on the block root, as a custom property with the block's prefix and a role name. Every rule that needs a colour cites the custom property. Outside the token block and outside `var()` fallbacks, no rule contains a colour literal (pure white, pure black and shadow values are exempt).

For each token, cite the site's own token where the site maintains one:

    #ln-road-traffic {
      --ln-brand: var(--e-global-color-primary, #060026);
      --ln-ink:   #1f2430;   /* hard-coded: site body text #4D4D4D fails AA on the tint panels */
    }

The fallback is the Chrome-verified rendered value. A site token may be cited only when (a) it resolves on `body` (`getComputedStyle(document.body).getPropertyValue('--e-global-color-primary')`) and (b) its resolved value equals the colour verified rendering on the reference page, and (c) the reference page's own CSS actually cites that token — grep the page's Elementor/theme CSS for `var(--e-global-color-...)` on the property in question, not just a matching computed value, since two different tokens can resolve to the same colour by coincidence. If any of the three fails, hard-code the verified value and say why in the comment and the handover.

A `var()` fallback value is not a contrast safeguard. It only ever renders if the token is undefined; once the token resolves, the fallback is invisible to the browser. Any contrast check must be run against the token's live resolved value, not the fallback.

Always hard-code, with a reason: typography metrics (size, weight, line-height, letter-spacing), spacing, radii, accessibility corrections, phone numbers, and anything the client asked to differ from the site.

AA pairs: a text colour and the background it sits on come from the same source, both inherited or both hard-coded, never mixed. A rebrand that changes an inherited background must not leave a hard-coded ink behind it.

Fonts: never `@import` or `@font-face` in a block. If a font renders on the reference page, the site loads it; declare nothing and inherit. A font the site does not load is a handover dependency, not something the block fetches.

Every declared custom property must be used. Every custom property used must be declared on the root or be a site token with a fallback. `scripts/check-block.py` enforces all of this.

**Why:** Blocks built as hard-coded hex are orphaned from the site. A brand colour change then means one support edit per block across the estate. Referencing the site's token with the verified value as fallback renders identically today and follows the site tomorrow, at no render cost. The AA pair rule exists because inheriting a background while hard-coding its text is the one way inheritance can silently break contrast.

**How to apply:** Check all nine rules before delivering. Run `python3 scripts/check-block.py <file>`; the file is not finished while it reports BLOCKED. Record every gap and deliberate exception in the handover header at the top of the file (template in `block-anatomy.md`). The header is the handover; the delivery message copies it.
