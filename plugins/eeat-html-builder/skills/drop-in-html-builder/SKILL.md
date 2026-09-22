---
name: drop-in-html-builder
description: >
  Builds styled, self-contained HTML content blocks that drop into law firm
  websites as YMYL/EEAT quick-win updates. Use when the user wants to convert
  legal copy (a Word doc, PDF, or notes) into a drop-in HTML block, style content
  to match an existing live page, build a content block for Elementor or WordPress,
  run the pre-handover QA checklist, or work on a known client (Lewis Nedas,
  MLT Digital, Wright & Crawford, MSHB Legal, Balfour & Manson). Triggers include
  "build an HTML content block", "drop-in HTML", "YMYL content", "EEAT content",
  "style this to match the site", "law firm landing page content".
---

# Drop-in HTML Builder

Convert legal content into styled, self-contained HTML content blocks that drop
into client law firm websites as YMYL and EEAT quick-win updates. Every output is
bespoke — built to match each client's live site styling, not from a fixed
template. This skill encodes the process and the standards that get you there.

Follow the four-step process in order. Load the reference file named at each step.

## The four-step process

### Step 1 — Take the job brief

Every job starts from a completed brief. Read `references/job-brief-template.md`.
If the user has not supplied the brief fields (client, page URL, CMS and page
builder, sitemap URL, a reference page on the same site, scope, content source,
content the client will edit themselves, who supports the page after launch,
constraints, and style information) ask for the missing ones before doing
anything else. Do not start a build on a partial brief; that is what causes the
back-and-forth.

If the named client already has a fact sheet in `references/clients/`, load it now
(see "Client facts" below). It supplies the CMS, design tokens, verified URLs, and
call-tracking setup so you do not re-derive them.

### Step 2 — Extract the live style reference

You cannot guess styling. Get the ground truth from the rendered page.

- If the Chrome tools are available, read computed styles from the reference page
  with the JavaScript tool: font-weight, text-align, heading colour, link colour,
  list style. Do not take a kit variable's value as a prediction of what renders;
  widget-level CSS overrides it. Then run the two snippets in
  `references/cms-override-patterns.md`: find the site's colour tokens and confirm
  which ones carry the rendered brand values, and probe the target container to
  see what a bare element gets. The block's CSS is the difference between the
  probe and the reference page; its colours cite site tokens with verified
  fallbacks (standard 9).
- If the user provides a screenshot instead, use `references/screenshot-style-extraction.md`
  to extract a complete style reference from it.
- If only brand colours are available, note them in the brief and proceed, flagging
  that styling is approximate.

Complete this before writing any CSS.

### Step 3 — Structure the content

When the user provides a Word doc, PDF, or notes, restructure it using
`references/content-structuring-prompt.md` into the required sections: headline,
lead paragraph, key points, process steps, FAQ, trust signals, and CTA text.

Work strictly from the source. Never invent, pad, or rewrite the substance of
client content. See "Standing rules" below — this one is absolute.

### Step 4 — Build, then QA

Build the block applying every universal standard (below), the CMS override
patterns in `references/cms-override-patterns.md`, and the file shape, section
order and comment format in `references/block-anatomy.md`. Reference both the
style extraction and the structured content as you build.

Before calling any file finished, run `python3 scripts/check-block.py <file>` and
clear every FAIL, then run every item in `references/qa-checklist.md`. The header
comment at the top of the file is the handover (template in `block-anatomy.md`);
it is written for the support developer who will see the block cold, and the
delivery message copies it.

## The 9 universal build standards

These apply to every block, every client. Full detail and the reasoning behind
each is in `references/build-standards.md` — read it before your first build.

1. **Never include HTML document boilerplate.** Output only a `<style>` block, any
   `<script>` blocks (e.g. JSON-LD), and the content `<div>`. No `<!DOCTYPE>`,
   `<html>`, `<head>`, `<meta>`, `<title>`, or `<body>`. The file is a fragment,
   not a document.
2. **Identify the CMS and get a reference page before starting.** Ask for the page
   builder and a URL on the same site to verify against.
3. **Verify computed styles on the rendered reference page.** Read real computed
   values with the JavaScript tool; a kit variable's value is not a prediction of
   what renders. Probe the target container so the block declares only what differs.
4. **Fetch the sitemap for internal linking.** Pull `/sitemap_index.xml` →
   `/page-sitemap.xml` (or equivalent), link relevant service and team pages in the
   body copy.
5. **Verify every link before including it. Never guess.** Confirm page URLs return
   200 (`curl -s -o /dev/null -w "%{http_code}" <URL>`). Inspect the DOM for real
   anchor IDs before writing any `href="#..."`. If an anchor cannot be confirmed,
   link the full page URL and document why.
6. **Include relevant JSON-LD structured data.** Check the page's own schema graph
   (e.g. Yoast) first and add only what it doesn't already own. FAQPage for any FAQ
   section, HowTo for step-by-step guides, LegalService or similar where warranted —
   these remain useful vocabulary even though FAQPage no longer earns a rich result.
   JSON-LD must match the visible content exactly — no invented entries.
7. **Align with EEAT and YMYL best practice.** Step-by-step process section and FAQ
   section where the source content supports them, specific verifiable claims only,
   no invented facts or credentials. Section headings come from the client's copy
   or the practice area, never from a stock template — "Step-by-Step Guide to X",
   "Why Choose [Firm]?" and "Frequently Asked Questions About X" are banned as
   defaults (see `references/pattern-log.md`).
8. **Align with CRO and UX best practice.** A CTA within the first screen, repeated
   CTAs at natural decision points, numbered steps and accordions to reduce load,
   WCAG 2.1 AA contrast minimum on all text and interactive elements.
9. **Inherit before you hard-code. No dead tokens, no orphan literals.** Every colour
   is a prefixed, role-named custom property on the block root, citing the site's
   token where the site maintains one: `var(--e-global-color-primary, #verified)`.
   No colour literals outside the token block. Text and its background come from the
   same source (both inherited or both hard-coded). Hard-code typography metrics,
   spacing, accessibility corrections and phone numbers, with a reason. Never
   `@import` a font.

Check all nine before delivering. Note any deliberate exception in the handover header.

## CMS override patterns

When building for WordPress + Elementor (Hello theme and similar), follow the
technical patterns in `references/cms-override-patterns.md`. The essentials:

- **Scope every rule to a unique ID** (`#client-page-block`), not a class — ID
  specificity beats theme selectors without blanket `!important`.
- **Build FAQs with `<details>/<summary>`, not `<button>` + JS.** Native disclosure
  sidesteps Elementor's high-specificity button style injection. Draw the chevron
  with a CSS border trick in `currentColor`, not a background-image SVG — and
  choose the disclosure treatment from the site's own component inventory, not by
  default (`references/cms-override-patterns.md`).
- **Avoid `<ul>/<li>` for decorative link lists** — themes inject their own
  `li::before` markers. Use a grid of plain `<a>` tags with the arrow as plain text.
- **Kit values are unreliable; kit tokens are the colour source.** Never read
  `--e-global-color-*` or kit font-weight to predict what renders. Do cite a kit
  colour token, with the verified value as fallback, once you have confirmed it
  carries the rendered brand colour.
- **Use `!important` surgically**, only on properties actually being overridden.
- **Build and preview at the real content width.** Measure it on the reference
  page; don't assume 750–900px (Wright & Crawford's own sheet records 1080px).

## Standing rules for every job

- **Use the client's supplied content exactly.** Reorganise and tighten only. Do
  not change meaning, facts, names, or credentials. Content is client-approved
  copy — altering it breaks the approval chain and creates liability. This rule is
  absolute and overrides any instinct to "improve" the copy.
- **Write in plain, confident British English.** No em dashes, no emojis, no jargon,
  no filler.
- **Scope every CSS rule to one unique parent ID** (`#client-page-block`) so styles
  cannot leak into the page. Custom properties are declared on that ID, never on
  `:root`.
- **Wrap phone numbers in `<a href="tel:...">`** so they are tappable on mobile.
- **Mark CTA links clearly** and never leave a dead link unflagged.
- **Meet WCAG 2.1 AA contrast** (4.5:1 normal text, 3:1 large text and UI). Check
  coloured CTA and callout blocks explicitly. Fix failures — do not flag and leave.

## Client facts

When the job names a client with a fact sheet in `references/clients/`, load it
before building. Each sheet holds the CMS, Chrome-verified design tokens (colours,
fonts, weights, radii), accessibility caveats, call-tracking behaviour, verified
URLs, and key internal-link and authorship targets. Available sheets:

- `references/clients/lewis-nedas.md` — Lewis Nedas Law (London criminal defence)
- `references/clients/mlt-digital.md` — MLT Digital (law-firm marketing agency)
- `references/clients/wright-crawford.md` — Wright & Crawford (Scottish solicitors)

Treat tokens as point-in-time and re-verify against the live page if a build looks
off — sites change. Call-tracking numbers (CallRail, Infinity) are swapped on
render; keep whatever number is in the supplied content unless the sheet says
otherwise.

## Worked examples

`examples/` holds two finished builds for reference — a Wright & Crawford family-law
block (FAQPage + HowTo + LegalService schema, serif Scottish styling) and an MLT
Digital block (BlogPosting schema, pink/green brand). They demonstrate file
discipline — header, token block, section markers, scoping — not layout. Do not
reuse their section order, component shapes (step markers, card grids, chevron
accordion) or styling on a different client; each build matches its own site and
its own component inventory (`references/screenshot-style-extraction.md`).
Check `references/pattern-log.md` before structuring a new build so it doesn't
repeat the last two.
