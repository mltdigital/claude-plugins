---
name: drop-in-html-builder
description: >
  Builds styled, self-contained HTML content blocks that drop into law firm
  websites as YMYL/EEAT quick-win updates. Use when the user wants to convert
  legal copy (a Word doc, PDF, or notes) into a drop-in HTML block, style content
  to match an existing live page, build a content block for Elementor or WordPress,
  run the pre-handover QA checklist, or work on a known client (Lewis Nedas,
  MLT Digital, Wright & Crawford, Complete Clarity, MSHB Legal, Balfour & Manson). Triggers include
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

**Fact sheet check (mandatory, always first).** Identify the client from the
request: the firm name if one is given, otherwise the domain of the page URL. If
there is neither, ask which client this is before anything else. The check is
never skipped.

List the files in `references/clients/` (ignore `_template.md`) and match the
client by firm name and by the domain on each sheet's first line. Then take
exactly one of these three paths and say in one line which one you took:

1. **Sheet found and complete for this job.** Complete means the sheet records
   CSS delivery, call tracking and the enquiry route (questions 2, 4 and 5 in
   `references/fact-sheet-questions.md`), and no field this build depends on is
   marked "not yet captured". Load it now (see "Client facts" below). It supplies
   the CMS, design tokens, CSS delivery, verified URLs and call-tracking setup, so
   you do not re-derive them. Anything in its "Client-specific rules" section
   overrides the general defaults in this skill and its references.
2. **Sheet found with gaps.** Load it. For gaps in fields a person must supply,
   ask only the matching questions from `references/fact-sheet-questions.md`. Gaps
   in fields the live site can prove (tokens, widths, URLs, anchors, schema) are
   filled by verification in Steps 2 and 4, never by asking. Update the sheet with
   the answers before building.
3. **No sheet.** Say so ("No fact sheet for [client] yet, so I'll ask a few
   questions and create one before building"). Ask the questions in
   `references/fact-sheet-questions.md`. Create `<client-slug>.md` (lowercase
   firm name, words joined by hyphens, "&" written as "and", for example
   `smith-and-co.md`) from `references/clients/_template.md` with the answers,
   saved where "Where the sheet is saved" (under "Client facts") says, then build.

Put the fact-sheet questions and any missing brief fields in the same single
message, so the user answers once.

**Then the brief.** Every job starts from a completed brief. Read
`references/job-brief-template.md`. If the user has not supplied the brief fields
(client, page URL, CMS and page builder, sitemap URL, a reference page on the same
site, scope, content source, content the client will edit themselves, who
supports the page after launch, constraints, style information, and CSS delivery:
stylesheet or inline), ask for the missing ones in that same message. Do not
start a build on a partial brief; that is what causes the back-and-forth. A
field the fact sheet already answers is not missing.

**Unattended runs** (scheduled, or nobody is there to answer): do not stall. Use
the sheet where one exists; otherwise create it with every person-supplied field
marked "not yet captured". Default CSS delivery to stylesheet unless the sheet says
otherwise, take every other field from the live page, and list all assumptions
and "not yet captured" fields at the top of the handover header.

Never silently proceed without a sheet. Everything you verify during the build
(tokens, widths, URLs, call tracking, form anchors, existing schema) is
fact-sheet material: record it in the sheet as you go, and complete the sheet
before handover (see "Client facts").

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

Deliver the CSS the way the brief asks (`CSS delivery`). **Stylesheet** is the
default when a developer handles the CMS insertion: two files, `<slug>.html`
with no `<style>` and `<slug>.css` holding the whole scoped stylesheet for the
child theme or the CMS custom-CSS area. **Inline** is one file with the `<style>`
inside the fragment, for when nobody has stylesheet access or the client pastes
the block themselves. Nothing else changes between the two: same root id on
every selector, same token rule on the block root, same header in both files
(as a `/* */` comment in the `.css`), each naming the other. If the brief does
not say, ask; do not pick silently
(unattended runs: see Step 1).

Before calling any file finished, run `python3 scripts/check-block.py <file>` (for
stylesheet delivery pass both files; a same-stem `.css` is found automatically) and
clear every FAIL, then run every item in `references/qa-checklist.md`. The header
comment at the top of the file is the handover (template in `block-anatomy.md`);
it is written for the support developer who will see the block cold, and the
delivery message copies it.

## The 9 universal build standards

These apply to every block, every client. Full detail and the reasoning behind
each is in `references/build-standards.md` — read it before your first build.

1. **Never include HTML document boilerplate.** The fragment holds only any
   `<script>` blocks (e.g. JSON-LD), the content `<div>`, and, for inline CSS
   delivery, one `<style>` block. For stylesheet delivery the CSS ships as a
   separate `.css` file and the fragment has no `<style>`. No `<!DOCTYPE>`,
   `<html>`, `<head>`, `<meta>`, `<title>`, `<link>` or `<body>`. The file is a
   fragment, not a document.
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
- **Stylesheet delivery changes where the CSS lives, not how it is written.** The
  `.css` goes in the child theme stylesheet (first choice), the Customizer's
  Additional CSS, or Elementor's Custom CSS; never inside the HTML widget. Every
  selector keeps the root id and the tokens stay on the block root, so the same
  file passes the same check.
- **Build and preview at the target page's own content width.** Never assume a
  figure and never carry one over from another page or a fact sheet without
  checking: width is a property of the page template, not the site. A service page
  with no sidebar and a blog single with a sidebar on the same site can differ by
  several hundred pixels. Measure the insertion container on the actual target
  page (the element the block will sit in, not `main` or `body`, which may include
  the sidebar), note whether a sidebar is present, and record both in the handover
  header and the fact sheet as a per-template value. If the reference page uses a
  different template from the target, the target's measurement wins for layout
  and the reference is used for styling only.

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
- `references/clients/complete-clarity.md` — Complete Clarity Solicitors (Scottish
  property pages; shared Customiser stylesheet `complete-clarity-shared.css`,
  HTML-only builds, one shared root id across pages)

No sheet exists yet for MSHB Legal or Balfour & Manson, although both are in the
trigger list; a build for either takes path 3 of the fact sheet check.

Treat tokens as point-in-time and re-verify against the live page if a build looks
off — sites change. Call-tracking numbers (CallRail, Infinity) are swapped on
render; keep whatever number is in the supplied content unless the sheet says
otherwise.

**Creating a sheet for a new client.** The sheet is created at Step 1, from the
answers to `references/fact-sheet-questions.md`, not offered at the end. Before
handover, fill every field the build verified, add the build to the Builds line,
and mark anything still unknown "not yet captured" rather than guessing. Add the
client to the list above and to the trigger list in this file's front matter, in
the same copy of the plugin the sheet is saved to (see below).

**Where the sheet is saved.** The installed plugin is a read-only synced copy:
a sheet written only there is lost at the next sync and never reaches colleagues.
If you are working in a clone of the plugins repository, write the sheet into it.
Otherwise save it to the user's working folder and tell them in one line that it
only reaches the team once it is committed to
`plugins/eeat-html-builder/skills/drop-in-html-builder/references/clients/` and the
plugin version is bumped. Do not report a sheet as "added to the plugin" until one
of those has happened.

**Updating an existing sheet.** When a build verifies something the sheet lacks or
contradicts (a new page template's width, a token name, a URL that now 404s),
append or correct the sheet in the same session and note the date.

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
