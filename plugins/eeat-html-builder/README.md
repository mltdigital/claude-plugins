# EEAT HTML Builder

A Cowork plugin for building styled, self-contained HTML content blocks that drop
into law firm websites as YMYL and EEAT quick-win updates. Once installed, Claude
follows a consistent four-step build process, applies a fixed set of build
standards, knows the CMS quirks to work around, runs a pre-handover QA pass, and
already holds the design facts for several existing clients.

## What you get

Installing this plugin gives Claude one skill, **Drop-in HTML Builder**, which
triggers whenever you ask it to build or style a drop-in HTML content block, work
from a Word doc or PDF, or work on a named client. The skill carries:

- **The four-step process** — job brief, live-style extraction, content
  structuring, then build and QA.
- **Nine universal build standards**: no document boilerplate, verify computed
  styles on the live page, sitemap-driven internal linking, verified links only,
  JSON-LD structured data, EEAT/CRO/accessibility discipline, and colour
  inheritance from the site's own tokens with no dead tokens.
- **CMS override patterns** — how to write CSS that survives WordPress and
  Elementor theme injection (ID scoping, native `details`/`summary` accordions,
  avoiding themed `li` markers, surgical `!important`).
- **Four reusable templates** — the job-brief intake form, a screenshot
  style-extraction prompt, a content-structuring prompt, and the QA checklist.
- **A regression check**: `scripts/check-block.py` runs on the output file before
  handover and blocks boilerplate, unscoped selectors, dead or orphaned colour
  tokens, font imports and JSON-LD that has drifted from the visible text.
- **Block anatomy**: a fixed file order, section comment format and a handover
  header written for the support developer who sees the block cold.
- **Client fact sheets** — design tokens, verified URLs, call-tracking behaviour
  and key contacts for Lewis Nedas, MLT Digital, and Wright & Crawford.
- **Two worked example builds** — a Wright & Crawford family-law block and an MLT
  Digital block, for reference (file discipline only; not a layout template — see
  `references/pattern-log.md`).

## How to use it

Start a job the way the skill expects: give Claude the client, the page URL, the
CMS, a reference page on the same site, and the content you want built. If you
leave fields out, Claude will ask for them before building. Name a known client and
Claude loads that client's facts automatically.

The plugin pairs with the **EEAT HTML Projects** working folder (the process docs
and finished client builds). Unzip that folder and select it in Cowork so you can
open and edit the actual HTML deliverables.

## Standing rules baked in

- Client-supplied copy is used exactly. Claude restructures and tightens only, it
  never rewrites the substance.
- Plain, confident British English. No em dashes, no emojis.
- Every block is scoped so its styles cannot leak into the rest of the page.
- WCAG 2.1 AA contrast is met, with coloured CTA and callout blocks checked
  explicitly.

## Changelog

**0.2.0**
- Added a ninth build standard: inherit colour from the site's own tokens before hard-coding, with no dead tokens or orphan literals.
- Added `scripts/check-block.py`, a stdlib regression check for structure, scoping, tokens and JSON-LD drift, and `references/block-anatomy.md` defining the fixed file shape and handover header.
- Added an anti-fingerprint step: a component inventory before styling, disclosure treatments presented as a choice rather than a default, banned canned section headings, and `references/pattern-log.md` tracking devices used on recent builds so consecutive clients don't end up visibly identical.
- Folded in review fixes: schema graph check before adding JSON-LD (FAQPage no longer earns a rich result), corrected the large-text contrast threshold, added 320px reflow / 200% resize / text-spacing checks, and removed an unmeasured "750-900px content width" claim in favour of measuring it on the reference page.

## A note on the client facts

The client fact sheets and example builds contain real client details (firm names,
phone numbers, SRA numbers, internal contacts, design tokens). Treat them as
confidential and only share this plugin with people who should have that
information. Design tokens are point-in-time — if a build looks off, re-verify
against the live site, because sites change.
