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
  and key contacts for Lewis Nedas, MLT Digital, Wright & Crawford and Complete
  Clarity (plus Complete Clarity's shared property-page stylesheet).
- **Two worked example builds** — a Wright & Crawford family-law block and an MLT
  Digital block, for reference (file discipline only; not a layout template — see
  `references/pattern-log.md`).

## How to use it

Start a job the way the skill expects: give Claude the client, the page URL, the
CMS, a reference page on the same site, and the content you want built. If you
leave fields out, Claude will ask for them before building.

Before building, Claude always checks `references/clients/` for the client's fact
sheet and tells you which of three paths it took:

1. **Sheet found**: it loads the sheet and follows any client-specific rules in it.
2. **Sheet with gaps**: it asks only the questions for missing person-supplied
   fields; gaps the live site can prove are filled by checking the site.
3. **No sheet**: it asks the eight questions in
   `references/fact-sheet-questions.md` (identity, CMS and CSS delivery, shared
   components, call tracking, enquiry route, schema ownership, authorship, after
   launch), creates the sheet, builds, then completes the sheet from what it
   verified on the live site.

If no client is named, it works the client out from the page URL's domain, or asks.

The plugin pairs with the **EEAT HTML Projects** working folder (the process docs
and finished client builds). Unzip that folder and select it in Cowork so you can
open and edit the actual HTML deliverables.

## Adding or updating a fact sheet

The plugin you install is a read-only synced copy. A sheet Claude writes inside it
is lost at the next sync, so new or updated sheets must go into this repository:

1. Save the sheet as
   `plugins/eeat-html-builder/skills/drop-in-html-builder/references/clients/<client-slug>.md`
   (start from `_template.md`).
2. List it under "Client facts" in `SKILL.md`, and add the client name to the
   trigger list in the `SKILL.md` front matter.
3. Bump the version in `plugins/eeat-html-builder/.claude-plugin/plugin.json` and
   in `.claude-plugin/marketplace.json`, update the version in the root README's
   plugin table, and add a changelog entry below.
4. Commit and push, then ask the team to update the plugin and confirm the new
   version number shows before their next build.

## Standing rules baked in

- Client-supplied copy is used exactly. Claude restructures and tightens only, it
  never rewrites the substance.
- Plain, confident British English. No em dashes, no emojis.
- Every block is scoped so its styles cannot leak into the rest of the page.
- WCAG 2.1 AA contrast is met, with coloured CTA and callout blocks checked
  explicitly.

## Changelog

**0.5.0**
- Fact-sheet check is now mandatory and happens before the build. Claude matches the client by name and domain, states which of three paths it took (sheet found, sheet with gaps, no sheet), and for a missing sheet asks the questions in the new `references/fact-sheet-questions.md` and creates the sheet up front instead of offering one at the end.
- Unattended runs create the sheet with human-supplied fields marked "not yet captured" rather than stalling.
- SKILL.md and this README now say where a sheet must be saved: the installed plugin is a read-only synced copy, so sheets go into this repository and ship with a version bump.
- Added the Complete Clarity Solicitors fact sheet and its shared property-page stylesheet (`references/clients/complete-clarity-shared.css`). Complete Clarity is the first client with a shared root id and shared classes across pages; the sheet records it as a client-specific exception.
- Pattern log: added the two Complete Clarity builds.
- SKILL.md notes that MSHB Legal and Balfour & Manson are trigger names without sheets.
- The client is identified from the firm name or, failing that, the page URL's domain; if neither is given Claude asks. "Complete for this job" is defined, fact-sheet and brief questions go in one message, and unattended runs default to stylesheet delivery and list their assumptions instead of stalling.
- `_template.md` gains a "Client-specific rules" section and fields for CSS delivery and shared components, required or banned wording, schema ownership and after-launch support; each question names the field it fills.
- `cms-override-patterns.md` allows a shared root id where a fact sheet sets one.
- **Guest-page bug fix.** The header template in `block-anatomy.md` put tag syntax ("<html>/<head>/<body>", "<form>") inside the handover comment. LiteSpeed Cache's HTML optimisation reads a `<style>` or `<script>` written inside a comment as a real tag, so a block built from it vanished for logged-out visitors (Complete Clarity, 24 Sep 2026: block and sidebar deleted for guests, fine when logged in). The template and both worked examples now name tags in words; `check-block.py` fails on tag syntax inside any comment; the QA checklist adds a logged-out check; `cms-override-patterns.md` documents the diagnosis (`?LSCWP_CTRL=before_optm` versus a logged-out fetch).
- Fixed `check-block.py` crashing (TypeError) on any fragment with the numbered section markers `block-anatomy.md` requires.

**0.4.0**
- CSS delivery is now a brief field. **Stylesheet** (the default when a developer handles insertion) ships two files: the fragment with no `<style>` and a companion `.css` for the child theme stylesheet or the CMS custom-CSS area, so styles are maintained in one place. **Inline** is the previous single-file form. Same scoped CSS, same header in both files, each naming the other.
- `check-block.py` takes the pair (`<file>.html <file>.css`, or finds a same-stem `.css` itself) and fails a fragment with no CSS in either place or CSS in both.

**0.3.0**
- Fact-sheet detection: when a named client has no sheet in `references/clients/`, Claude says so up front, builds from the brief and live page, and offers to write a sheet at the end from `references/clients/_template.md`. Existing sheets are updated in-session when a build verifies something they lack.
- Content width is now measured per page template on the target page's insertion container, with sidebar presence recorded, instead of on the reference page or from a single site-wide figure.

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
