# Merge log — EEAT/YMYL plugin audit (v0.1.0 → v0.2.0)

Applying `plugin-audit-diffs.md` §1–§9, then Codex/Astra fold-ins, then the
anti-fingerprint step, then the check-block.py hardening. One line per change.

## Step 1 — plugin-audit-diffs.md §1–§9

- `references/build-standards.md` §1a: Rule 3 retitled/rewritten to "Verify computed styles on the rendered reference page before building", added container-probe step. Verified via grep before/after.
- `references/build-standards.md` §1b: Rule 8 bullet now "WCAG 2.1 AA ... (4.5:1 normal text, 3:1 large text and UI components)".
- `references/build-standards.md` §1c: new Rule 9 (inherit-before-hard-code / token discipline) inserted after Rule 8. Folded in Codex 2c (reference page's own CSS must reference the token, not just match value) and 2e (var() fallback is not a contrast safeguard) directly into Rule 9 rather than as a separate later edit.
- `references/build-standards.md` §1d: "How to apply" now references nine rules and `scripts/check-block.py`.

## Step 2 — Codex/Astra fold-ins

- 2a: Rule 6 rewritten — dropped "FAQPage schema generates rich results in Google search"; added "inspect the page for a Yoast (or other SEO-plugin) schema graph already in the page source, and add only what it doesn't already own"; FAQPage/HowTo kept as vocabulary. Verified the "May 2026 FAQ rich-result discontinuation" claim via WebSearch before citing it (see Verification section below) — confirmed, so cited both the August 2023 restriction (government/health only) and the May 2026 documentation update / August 2026 Search Console removal.
- 2b: `content-structuring-prompt.md` — FAQ section (§5): removed "convert prose into Q+A" instruction and the "four to eight questions" target; process/FAQ now explicitly "where the document supports them". CTA section (§7): removed suggested CTA copy example, now "Not provided" if the document doesn't specify one. "After you get the output": removed the lead-trimming bullet.
- 2b (cont.): `build-standards.md` Rule 7 reworded so process/FAQ sections are included "where the source content supports one", not mandatory — resolves the contradiction with content-structuring-prompt's "Not provided" instruction.
- 2c: folded into Rule 9 above (site-token condition now requires the reference page's own CSS to actually cite the token, verified by grepping the Elementor/theme CSS for `var(--e-global-color-...)`, not merely equal resolved values).
- `references/cms-override-patterns.md` §2a: chevron now `currentColor`; presented as one of several disclosure treatments (chevron / plus-minus / restyled native marker / no icon / non-accordion headings), chosen from the reference site's component inventory — this also satisfies STEP 3's anti-fingerprint requirement for this file.
- `references/cms-override-patterns.md` §2b: "Kit-level CSS is unreliable" replaced with "Kit values are unreliable. Kit tokens are the colour source." plus decision table, token-finding snippet, container probe snippet, and the confirmation step that the reference page's CSS actually cites the token (Codex 2c).
- `references/cms-override-patterns.md` 2h: replaced the "750–900px" content-width claim with "measure it; Wright & Crawford's own sheet records 1080px", and added a `curl -L` + report-final-URL note for fetching reference pages/stylesheets.
- `SKILL.md` §3a–3f applied verbatim/adapted: brief fields (content client edits + who supports page), Step 2 tokens/probe workflow, Step 4 check-block.py + block-anatomy.md, "8"→"9 universal build standards" with new item 9 and reworded items 3/6/7, CMS essentials bullets (currentColor chevron + disclosure choice, kit tokens, content-width), scoping bullet (ID + no `:root`).
- `SKILL.md` STEP 3 fold-in: "Worked examples" section now states the examples show file discipline, not layout, and tells the builder not to reuse their component shapes; points to `references/pattern-log.md`.
- `SKILL.md` + `references/build-standards.md` Rule 7: banned canned headings ("Step-by-Step Guide to…", "Why Choose [Firm]?", "Frequently Asked Questions About…") as defaults.
- `references/content-structuring-prompt.md`: added "title from the content, not the stock heading" notes to the key-points, process and FAQ sections.
- `references/qa-checklist.md` §4a: new section 0 (automated check-block.py + grep fallback) inserted; also added the STEP 3 "not a repeat of the pattern log" tick here per the brief.
- `references/qa-checklist.md` §4b: large-text threshold corrected, AA-pairs item added, plus Codex 2f: reflow at 320px (1.4.10), 200% text resize (1.4.4), text-spacing overrides (1.4.12).
- `references/qa-checklist.md` §4c–4e: FAQ accordion, external dependencies and CMS/theme sections rewritten per diff; Elementor content-width line now says "measure it" instead of restating 750–900px.
- `references/qa-checklist.md` §4f: Handover section replaced; added Codex 2g tick ("no backup path, server path, staging credential or other access detail" in the header) plus an explanatory line that HTML comments ship to production.
- `references/job-brief-template.md` §5a–5d applied: page-URL note, reference-page note, new "content client will edit" + "who supports this page" fields, new "does the site maintain global colour tokens" field with Codex 2e's var()-fallback-is-not-a-contrast-safeguard note folded in.
- `references/clients/lewis-nedas.md`, `mlt-digital.md`, `wright-crawford.md`: added the "Site colour tokens: not yet captured" line (§6, values deliberately left blank). `mlt-digital.md` accessibility caveat extended with the hard-code-as-a-pair instruction.
- `README.md` §7: "Eight" → "Nine" universal build standards bullet rewritten; added "regression check" and "block anatomy" bullets; worked-examples bullet now notes file-discipline-only / see pattern-log.
- `plugin/.claude-plugin/plugin.json`: version 0.1.0 → 0.2.0.
- `README.md`: added a short "0.2.0" changelog section (STEP 5).
- New file `references/block-anatomy.md` (§8): created verbatim from the diff, with the Codex/anti-fingerprint fold-ins added directly (var()-is-not-a-contrast-safeguard note in the token block section; banned-canned-headings note in the section-comment-format section; "where the source supports one" in default content order; HTML-comments-are-public note + a "no backup/server/staging credential" DO NOT line in the header template).
- New file `scripts/check-block.py` (§9): copied verbatim from `check-block.py` at the work-dir root (byte-identical, diffed to confirm) to `plugin/skills/drop-in-html-builder/scripts/check-block.py`.

## Step 4 — check-block.py hardening (CSS nesting / :is() / :where())

- Added an explicit check in the main per-rule loop: if a rule's body contains a stray `{`/`}` (i.e. a nested rule), the script now emits `FAIL "CSS nesting is not supported by this checker..."` and skips further (unreliable) parsing of that rule, instead of silently reading the nested selector's declarations as if they belonged to the outer rule.
- Added a second check: if a selector contains `:is(` or `:where(` (case-insensitive), the script now emits `FAIL "':is()'/':where()' is not supported by this checker..."` instead of silently splitting on the commas inside the parentheses and misreporting unscoped-selector fails.
- Updated the script's module docstring to document this limitation.
- Verified on the deliberately broken fixture (see Skipped/Findings section below for full output) and on both worked examples.

### check-block.py actual output — after hardening

**mlt-digital--ymyl-law-firm-seo.html** (after removing the inert `@import`, the "swap text to #fff" line, and adding tokens for the 19 previously-literal colours found by the checker):

```
WARN  fewer than 3 standard section markers '<!-- [n] NAME | ... -->' found
WARN  header has no 'EDIT INDEX' block (support developer quick-edit list)
WARN  header has no 'TOKEN MAP' block (site token -> block token -> fallback)
WARN  custom properties use mixed prefixes ['av', 'blue', 'dark', 'good', 'green', 'ink', 'lede', 'pink', 'warn']; use one block prefix
WARN  21 uses of !important; the pattern is surgical, not blanket

PASS: 0 fail, 5 warn (examples/mlt-digital--ymyl-law-firm-seo.html)
```
Exit code: 0

**wright-crawford--divorce-and-separation.html** (after tokenising 5 previously-literal colours: `strong` text, band paragraph text, and two olive/aubergine hover shades that already had sibling tokens or needed one):

```
WARN  fewer than 3 standard section markers '<!-- [n] NAME | ... -->' found
WARN  header has no 'EDIT INDEX' block (support developer quick-edit list)
WARN  header has no 'TOKEN MAP' block (site token -> block token -> fallback)

PASS: 0 fail, 3 warn (examples/wright-crawford--divorce-and-separation.html)
```
Exit code: 0

**Deliberately broken fixture** (`scratchpad/broken-fixture.html`: unscoped selector, one nested CSS rule, one `:is(...)`):

```
FAIL  CSS nesting is not supported by this checker: '#test-block' contains a nested rule. Flatten it to a top-level selector.
FAIL  unscoped selector '.unscoped-selector-outside-root'
FAIL  ':is()'/':where()' is not supported by this checker: '#test-block :is(h2, h3)'. Write out the selector list explicitly instead.
FAIL  custom property --tb-brand used but never declared on the block root
WARN  fewer than 3 standard section markers '<!-- [n] NAME | ... -->' found
WARN  header has no 'EDIT INDEX' block (support developer quick-edit list)
WARN  header has no 'TOKEN MAP' block (site token -> block token -> fallback)

BLOCKED: 4 fail, 3 warn (.../scratchpad/broken-fixture.html)
```
Exit code: 1

(The fourth FAIL on the fixture is a legitimate knock-on effect: because the whole `#test-block` rule is skipped once nesting is detected in it, the `--tb-brand` declaration inside that same rule is never registered as declared, so the `var(--tb-brand)` reference elsewhere correctly reads as undeclared. All four messages point at real problems in the fixture.)

## Step 3 — Anti-fingerprint (new)

- New file `references/pattern-log.md`: seeded with the three named builds (mshblegal.com divorce page, richardsilver.co.uk totting-up page, Balfour & Manson buying/selling page), each logged with the shared skeleton, chevron disclosure treatment and component shapes described in the brief. Rule stated: don't repeat the last two entries' devices unless the client's site already uses that device.
- `references/screenshot-style-extraction.md` §4: "Component styles" renamed/rewritten to "Component inventory" — accordion, list markers, card/panel treatment, button shapes, heading devices, dividers; states the block reuses only shapes the site already has (no accordion on the site -> FAQ as headings + paragraphs), and points to `pattern-log.md`.
- `references/cms-override-patterns.md` §2a (see Step 1/2 above): chevron snippet presented as one of several disclosure treatments (chevron / plus-minus / restyled marker / no icon / non-accordion headings), chosen from the inventory — this is also the anti-fingerprint fix for this file.
- Canned headings ("Step-by-Step Guide to…", "Why Choose [Firm]?", "Frequently Asked Questions About…") banned as defaults in `SKILL.md` (standard 7 and CMS bullet), `references/build-standards.md` (Rule 7), and `references/content-structuring-prompt.md` (process/key-points/FAQ section notes).
- `SKILL.md` "Worked examples" section rewritten: examples demonstrate file discipline, not layout; explicit instruction not to reuse their section order or component shapes; points to `pattern-log.md`.
- `references/qa-checklist.md` §0: added a "Not a repeat of the pattern log" tick.
- Kept short per the brief: each of the above additions is a few lines, not new workflow steps; the whole anti-fingerprint pass is a single inventory step plus a log lookup, estimated at the requested 5-8 minutes per build.

## Skipped / could not do

- Nothing in the brief was skipped outright. The one deviation from a literal reading of the brief: STEP 4 says "Both examples must pass" — achieving that required editing the two example HTML files beyond the specific line-level changes named in Codex item 2d (which only mentioned the MLT `@import` and the "swap to #fff" comment). To reach 0 FAIL under the new Rule 9 token-literal check, `wright-crawford--divorce-and-separation.html` needed 5 new tokens (a handful of hover/emphasis shades) and `mlt-digital--ymyl-law-firm-seo.html` needed ~17 new tokens (avatar colours, pink/green alpha variants, warning/success text shades). This is a real, mechanical widening of scope beyond "no new files/edits not listed" — flagged here rather than silently expanded. No content, layout or visible styling changed; only literal colour values were moved into named custom properties with identical values.
- The examples still carry 3 WARNs each (no `[n]` section markers, no EDIT INDEX, no TOKEN MAP block in the header) plus 2 more on the MLT file (mixed token prefixes, 21 `!important` uses). These are pre-existing from before this audit and are WARN, not FAIL, so `check-block.py` reports PASS regardless; retrofitting the full block-anatomy.md header format onto both example files was not requested and was not attempted, to avoid a further unrequested scope increase.
- Verified the "May 2026 FAQ rich-result discontinuation" claim via one WebSearch (see Step 2 above) rather than assuming it — confirmed accurate, so both the August 2023 and May/June/August 2026 dates are cited in `build-standards.md` Rule 6.

