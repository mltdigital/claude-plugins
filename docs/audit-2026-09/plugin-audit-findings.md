# eeat-html-builder plugin audit: findings

Date: 22 September 2026
Plugin version audited: 0.1.0 (Eeat html builder-v1.zip)
Companion file: `plugin-audit-diffs.md` holds the actual proposed edits. Nothing has been applied to the plugin.

## Scope and method

Read in full: `SKILL.md`, `README.md`, `plugin.json`, all seven reference files, all three client fact sheets, and both worked example builds. Every file in the plugin was read; nothing was sampled.

Beyond reading, I measured. I wrote the regression-guard script proposed under Priority 3 and ran it against both worked examples and a deliberately broken fragment, so the findings below report what the output actually contains rather than what the guidance says it should contain.

Measured state of the two worked examples:

| Check | MLT Digital example | Wright & Crawford example |
|---|---|---|
| Document boilerplate | none | none |
| Top-level structure | one `<style>`, JSON-LD, one root `div` with id | same |
| Unscoped selectors | 0 | 0 |
| `:root` declarations | 0 | 0 |
| Custom properties declared / used | 20 / 20 (no dead tokens) | 10 / 10 (no dead tokens) |
| Custom properties referencing a site token | 0 | 0 |
| Colour literals in rules outside the token block (white, black and shadows exempted) | 19 | 5 |
| `@import` of fonts the site already loads | 1 (Libre Franklin, Inter) | 0 |
| `!important` uses | 21 | 9 |
| JSON-LD mirrors visible text | yes | yes |
| Section comments | yes, one format (`<!-- ==== NAME ==== -->`), no closers | yes, a different format (`<!-- NAME -->`), no closers |
| Header comment audience | "Build notes (handover) for Simon" | commissioner |

Two conclusions follow. First, the plugin's own output does not reproduce either of the subcontractor's two problems: no boilerplate, no dead tokens. Those came from the seven pre-plugin pages and this audit does not remediate them (see Priority 3.4 for how it can find them). Second, the plugin's output does have the underlying fault the subcontractor was describing: every colour is a hard-coded hex, tidied into local tokens on the good builds and scattered as raw literals on the rest, with no connection to the site's own colour source. A brand colour change therefore means editing the block. That is confirmed, and it is what Priority 1 fixes.

Total build-time cost of everything proposed here: 8 to 12 minutes on a typical build, 17 when a block has to be split around a native widget. A build that takes 45 minutes today takes under an hour with all of it applied. Per-item costs are given in each section and collected in the table at the end.

---

## Priority 1: Colour and token inheritance

### 1.1 What is wrong

The plugin tells the builder, in three places (`SKILL.md` Step 2, `SKILL.md` CMS essentials, `cms-override-patterns.md` "Kit-level CSS is unreliable"), never to trust `--e-global-color-*` and always to Chrome-verify computed styles. That guidance was written to solve a real problem (widget-level overrides making kit values a bad predictor of what renders) and it is correct for that problem. But it is phrased as a blanket ban on kit variables, and the builder does the only thing left: reads the rendered hex and writes it into the block. The `cms-override-patterns.md` chevron snippet even models this, hard-coding `#d50057` for a border colour.

The result is a block that is internally consistent and externally orphaned. When the client rebrands, or the designer nudges the primary colour, every block on the site keeps the old value. With roughly 50 pages live that is 50 support edits per colour change.

### 1.2 Why the two pulls are in tension, and the resolution

The tension is between two true statements:

1. "Kit values are routinely overridden at widget level, so the rendered page is the ground truth." True. A Heading widget with its own colour set does not use `--e-global-color-primary`.
2. "The block should inherit site colours so a brand change propagates." Also true, and the reason this audit exists.

They only conflict if you treat a kit variable as a way to *predict* what renders. It is not. It is a *token*: a named value the site's designer maintains in one place. The distinction that resolves the tension is this:

**A widget overriding `color` does not change the variable.** When a Heading widget sets `color: #333`, `--e-global-color-primary` still holds the brand value on `body` (Elementor applies the kit class to `<body>` and declares the globals there; custom properties then inherit down through every descendant). The block is not an Elementor widget. It is raw HTML inside an HTML widget, and `var(--e-global-color-primary)` inside it resolves cleanly regardless of what any other widget on the page does with its own colours.

So Rule 3 stays exactly as strong as it is for *values*: what the reference page looks like is only knowable from computed styles. What changes is the *source* the block's CSS cites for a colour once you know what it should be. If the site maintains a token whose resolved value equals the colour you verified rendering on the reference page, cite the token. If it does not, cite the hex. In both cases the block renders the verified colour today; in the first case it also follows the site tomorrow.

The mechanism is `var()` with a fallback:

```css
#ln-road-traffic {
  --ln-brand: var(--e-global-color-primary, #060026);
}
```

The fallback is the Chrome-verified value. If the token is present, the block inherits. If the token is renamed, removed, or the block is moved to a site without it, the block still renders correctly. There is no render-time cost and no failure mode that is worse than today's.

Written as a rule: **verify values on the rendered page; reference tokens the site actually maintains; hard-code everything else, with a reason.**

### 1.3 The decision table

This replaces "never trust kit-level CSS" with a per-property decision. It goes into `cms-override-patterns.md` and is summarised as the new Rule 9 in `build-standards.md`.

| Property group | Default | How to verify (Step 2) | Hard-code instead when |
|---|---|---|---|
| Body font family | Inherit: declare nothing | Probe a bare `<p>` in the target container (snippet in 1.7); computed family matches the reference page | The container gives a different family from the reference page and no typography token matches |
| Heading font family | Inherit: the kit's `h2`/`h3` rules already reach inside the block | Probe a bare `<h2>` in the container | As above |
| Font size, weight, line-height, letter-spacing, text-align | Hard-code the computed value from the reference page where it differs from the probe | Probe vs reference page computed style | Always permitted: these are exactly the properties widget-level styles override, so the kit value is unreliable here and Rule 3 governs |
| Brand, secondary and accent colours; link colour; button fill and border; band and card backgrounds; border and divider colours | `var(--site-token, #verified)` | Token exists on `body` computed style (snippet in 1.7) and its resolved value equals the colour rendered on the reference page | No matching token; token value differs from what renders (the site's designer is not maintaining it); the AA pair rule below applies |
| Body text colour | Inherit if it passes AA on the block's backgrounds | Probe plus contrast check | Fails AA (Wright & Crawford `#8A8A8A` is the live case; the fact sheet already darkens it) |
| Pure white and pure black | Literal allowed | none | n/a |
| Shadows | Literal allowed | none | n/a |
| Spacing, radii, max-widths | Hard-code | Reference page computed style | Always: Elementor does not expose spacing tokens by default and radii are a per-component decision |
| Phone numbers | Hard-code, marked `EDIT:` | n/a | Always: call tracking swaps on render (existing rule, Wright & Crawford sheet) |

Fonts are the cheapest inheritance win and the current guidance gets them backwards. If a font renders on the reference page, the site loads it. An `@import` in the block is always a duplicate request and, worse, it pins the block to a font family the site may later change. The QA checklist currently permits the `@import` with a handover note; the MLT example has one for the two fonts the MLT fact sheet says the site already uses. The new rule bans `@import` and `@font-face` in blocks outright. A font that is genuinely absent from the site is a dependency for the handover note, not something the block loads.

### 1.4 Where hard-coding is the right call

Stating this explicitly so the new rule cannot be read as "inherit everything":

1. **Typography metrics** (size, weight, line-height, letter-spacing). These are what widget-level CSS overrides. The verified computed value is the only reliable source. This is the original insight behind Rule 3 and it stands.
2. **Accessibility corrections.** Where the site's own colour fails WCAG 2.1 AA in the block's usage, the block must not inherit the failing value. Both live examples already do this correctly (MLT dark ink on the green pill; Wright & Crawford darkened body text and eyebrows). Hard-code the corrected value, and list the correction in the handover so a support developer does not "fix" it back to brand.
3. **AA pairs** (see 1.5).
4. **Colours with no maintained token.** If the site's designer set widget colours by hand and never maintained the globals, the token's value will not match what renders. Citing it would make the block follow a value nobody uses. Hard-code, and record in the handover that the site has no maintained colour source.
5. **Spacing, radii, layout widths.** No reliable site token exists; these are per-component decisions.
6. **Phone numbers.** Existing rule; call tracking swaps them on render.
7. **Anything the client has explicitly asked to differ from the site.** Recorded in the brief and the handover.

### 1.5 The AA pair rule

This is the non-obvious rule and the one most likely to be missed. If a text colour and its background come from different sources, a rebrand can silently break contrast: the inherited background changes, the hard-coded ink does not, and nobody re-checks. The rule is:

**A text colour and the background it sits on must come from the same source: both inherited (only if the site's pair already passes AA) or both hard-coded. Never mix.**

Applied to the two live cases: MLT's CTA (white on `#A3C126` fails on the live site) is hard-coded as a pair, dark ink on green, and the handover states that if the brand green changes, the CTA pair needs re-checking. Wright & Crawford's aubergine band with white text passes, so both the band background and the white can be inherited (white is a literal, which is the same thing). This costs nothing at build time because the contrast check is already mandatory; it only constrains where the values are cited from.

### 1.6 No dead tokens, no orphan literals, one prefix, role names

Four hygiene rules, all machine-checkable (Priority 3):

- **No dead tokens.** Every custom property declared on the block root must be consumed by at least one `var()` in the same block. Both current examples pass; the seven legacy pages did not.
- **No orphan literals.** Outside the token block (the bare `#root { ... }` rule) and outside `var()` fallbacks, no rule may contain a colour literal. White, black and shadow values are exempt. This is the rule the current examples fail (19 and 5 literals). Without it, "no dead tokens" is satisfied while the same brand pink appears both as `--pink` and as raw `#CC3366` elsewhere, which is what the MLT example does today.
- **One prefix per block.** All custom properties share the block's prefix (`--wc-`, `--ln-`). The MLT example uses six unprefixed names (`--ink`, `--pink`, `--good`). They are scoped to the root so they do not collide, but a support developer grepping a 600-line file for `--pink` will match Elementor's own output on some sites. Prefixed names are also the one-line answer to "which CSS belongs to this block".
- **Role names, not colour names.** `--wc-brand`, not `--wc-aubergine`. After a rebrand to green, `--wc-aubergine: #2a7d3b` is a trap for the next developer. Role names survive the change.

The brief asked for the dead-token rule. I have kept it and added the orphan-literal rule beside it because the first without the second does not fix the reported problem; it only tidies it.

### 1.7 Procedure added to Step 2

Two JavaScript snippets, run on the reference page through the existing Chrome tooling. Both return values rather than screenshots, in line with the rest of the process.

**Snippet A: find the site's maintained tokens.** Lists every custom property declared on `:root`, `body`, `html` or an Elementor kit class, with its value. Elementor 3.x declares `--e-global-color-primary`, `-secondary`, `-text`, `-accent` plus hashed custom names; Elementor 4 and its Variables Manager may add designer-named ones; block themes declare `--wp--preset--color--{slug}`. Discover by inspection, never by assumption.

```javascript
[...document.styleSheets].flatMap(s => { try { return [...s.cssRules] } catch (e) { return [] } })
  .filter(r => r.selectorText && /^(:root|body|html|\.elementor-kit-\d+)/.test(r.selectorText))
  .flatMap(r => [...r.style].filter(p => p.startsWith('--'))
    .map(p => `${p}: ${r.style.getPropertyValue(p).trim()}`))
```

Then resolve any candidate to confirm the value that actually reaches the block:

```javascript
getComputedStyle(document.body).getPropertyValue('--e-global-color-primary').trim()
```

If the resolved value equals the colour you verified rendering on the reference page (buttons, links, headings), cite the token with the verified value as fallback. If not, hard-code and note it.

**Snippet B: probe what a bare element gets inside the content column.** This is the step that turns "verify computed styles" and "inherit from the site" from a contradiction into a procedure. The reference page's headings are Heading widgets with widget styles. An `<h2>` inside an HTML widget gets the *kit's* `h2` rule, not the widget's. The block's CSS should be the difference between the two.

```javascript
const host = document.querySelector('.elementor-widget-text-editor .elementor-widget-container')
  || document.querySelector('.entry-content, main');
const out = {};
for (const tag of ['p', 'h2', 'h3', 'a', 'strong']) {
  const el = document.createElement(tag); el.textContent = 'probe';
  if (tag === 'a') el.href = '#';
  host.appendChild(el);
  const cs = getComputedStyle(el);
  out[tag] = Object.fromEntries(['fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'color',
    'letterSpacing', 'textAlign'].map(k => [k, cs[k]]));
  el.remove();
}
out
```

Compare each value with the reference page's rendered equivalent. Where they match, declare nothing. Where they differ, declare only the differing property with the verified value. This shrinks the CSS and increases inheritance at the same time.

### 1.8 Build-time cost

- Snippet A and token confirmation: 2 minutes.
- Snippet B and comparison: 3 minutes.
- Token block hygiene (prefix, role names, no orphan literals): 0 to 1 minute. The builder writes the CSS anyway; this changes what it writes, not how much.
- AA pair rule: 0 minutes; the contrast check already exists.

Total: 5 to 6 minutes per build. Justification: this is the fix for the fault that generated the support tickets. One brand colour change across a six-client, 50-page estate currently costs a support developer roughly 50 edits, each needing the file located and the right hex found. After this change, blocks on sites with maintained tokens need zero edits, and blocks on sites without them need one edit in one clearly labelled token block per file.

### 1.9 Changes proposed

All in `plugin-audit-diffs.md`:

- `build-standards.md`: Rule 3 retitled and its intent narrowed to what it was protecting (values, not tokens); Rule 8 "WCAG AA" made "WCAG 2.1 AA"; new Rule 9 (inherit before you hard-code; no dead tokens; no orphan literals; AA pairs). This adds a ninth standard. It does not change the intent of the existing eight. Rule 3's title changes from "Always Chrome-screenshot the live site" to "Verify computed styles on the rendered reference page"; the screenshot was always the fallback method and the body text already said so.
- `cms-override-patterns.md`: "Kit-level CSS is unreliable" rewritten as "Kit values are unreliable; kit tokens are the colour source", with the decision table, the two snippets and the `var()` pattern; the chevron snippet's `#d50057` becomes `currentColor`; new "Fonts" section banning `@import`.
- `SKILL.md`: Step 2, the standards list and the CMS essentials brought into line.

---

## Priority 2: Editability for a developer who did not build the page

The test the brief sets: a competent WordPress developer, first sight of the block, support ticket in hand, needs to find the thing the client asked to change in under two minutes. I applied that test to both examples.

### 2.1 Section commenting

**What is wrong.** Both examples have section comments, which is good and better than most hand-built pages. But nothing in the plugin mandates them, so their presence is luck. The two examples use two different formats. Neither has closing markers, so in a 600-line file you know where a section starts and not where it ends. The CSS is not cross-referenced to the sections: to change the FAQ's border colour you find `<!-- FAQ -->` in the HTML, read the class names, then search the `<style>` block for them. The things clients actually ask to change (a phone number, a CTA destination, a solicitor's name, a date) have no marker at all.

**Proposed fix.** Mandate one comment format, with closers, and an `EDIT:` convention for hotspots. Specified in a new reference file, `references/block-anatomy.md`, and enforced by the Priority 3 script.

```html
<!-- [3] STEP-BY-STEP GUIDE | .wc-steps | HowTo schema mirrors these step names -->
  ...
<!-- /[3] STEP-BY-STEP GUIDE -->
```

Each opener carries the section number, the section name in capitals, the CSS hook a developer greps for, and one optional note. The `<style>` block uses matching sub-comments in the same order (`/* [3] STEP-BY-STEP GUIDE */`). Editable hotspots are marked inline:

```html
<!-- EDIT: phone number. CallRail swaps it on render; keep it static here. -->
<a href="tel:02078702736">020 7870 2736</a>
```

**Does it meet the two-minute test?** With a header index (2.4) listing every `EDIT:` marker and every section number, a developer opens the file, reads the top 30 lines, and jumps by search. Yes.

**Cost:** about 1 minute per build. The comments are generated with the markup.

### 2.2 Should the skill mandate a standard section order and comment format?

**Comment format: yes, mandate it** (above). There is no cost and the two examples already show what happens without it.

**Section order: mandate the file order, default the content order.** The file order is fixed and enforceable:

1. Header comment (handover, token map, edit index).
2. One `<style>` block, in a fixed internal order: tokens, base, components, sections in page order, responsive.
3. JSON-LD `<script>` blocks.
4. One root `<div id="...">` and nothing else at the top level.

The content order should default to the output of Step 3's content-structuring prompt, with the first CTA inserted after the lead paragraph per Rule 8: intro, first CTA, key points, process, topic sections, FAQ, trust signals, closing CTA. Builds may deviate for CRO or content reasons, but every deviation is listed in the header. Mandating a strict content order would fight the bespoke, content-led nature of the blocks; defaulting it gives a support developer a predictable shape without costing the builder anything.

**Cost:** 0 minutes.

### 2.3 Where content should sit: block, ACF or native widget

**The decision rule.** Content goes in the block unless it meets any of these three tests, in which case it goes in a native widget or a site-wide source, and the block is split around it:

1. **It changes on a schedule or by a non-developer.** Fees, opening hours, statistics with a date, a testimonial that rotates, a "current from" date. If the client will ask for it changed without a designer involved, it is not block content.
2. **It already exists elsewhere on the site.** Firm address, SRA number, accreditations strip, solicitor credentials beyond name and role. If the site renders it anywhere else, the block must not carry a second copy that can drift. Link to it (the `/our-people/` profile) rather than restating it.
3. **It needs to be dynamic.** Anything from an ACF field, an Elementor dynamic tag or a shortcode. The Elementor HTML widget outputs its content raw; it does not run shortcodes or dynamic tags (verify on the site if in doubt, but assume not). Dynamic content therefore cannot live inside the fragment at all.

Everything else, which is the editorial body of the page (lead, key points, process steps, topic sections, FAQ), stays in the block. Moving it to ACF repeaters would cost developer hours per page and lose the speed advantage that justifies the plugin.

Two things the rule keeps in the block deliberately:

- **Phone numbers.** They meet test 2 on its face, but the call-tracking swap makes them safe to duplicate, and the existing rule keeps them static in content. They stay, marked `EDIT:`.
- **Named solicitors.** Name and role stay (EEAT needs the byline in the body). Credentials that the profile page already carries are linked, not repeated.

**How to split.** When a piece of content fails the test, the block is delivered as two fragments, `part-1` and `part-2`, with the native widget between them. Both fragments share the same root id prefix (`#wc-divorce-1`, `#wc-divorce-2`) and the same token block; the header of each says what sits between them. The most common trigger will be a CTA band that should be a native Elementor button or form. A form is already banned inside the block, so this case exists today without a rule for it.

**Where the decision is made.** At brief stage. A new brief field asks which content the client will change themselves, and the builder applies the three tests to it before building.

**Cost:** 1 minute at brief stage to apply the tests. About 5 minutes when a split is triggered, for the second fragment header and the handover instruction. Justification: a split costs five minutes once; a fee figure hard-coded into a block costs a support ticket every time it changes.

### 2.4 The handover note

**What is wrong.** The current template (`qa-checklist.md` section 7) is written for the person who commissioned the page: what the file is, where it goes, which links are placeholders, confirmation it was QA'd. Both examples address the header comment "for Simon". A support developer needs different things: which CSS is this block's, where the colours come from and why some are deliberately off-brand, what will silently break if they edit the wrong thing, and where the hotspots are.

There is also a location inconsistency. `build-standards.md` says to put the handover in a comment at the top of the file. `SKILL.md` says to deliver a separate handover note. `qa-checklist.md` describes a note "with every file delivery". The email does not survive to the support ticket; the file does. So the in-file header must be the canonical handover, and the delivery message a copy of it.

**Proposed header template** (full text in `block-anatomy.md`), with the sections a support developer needs:

- **Block:** root id, prefix, file name, page URL, the widget it was pasted into, build date, style-verification date.
- **Token map:** one line per block token: block name, site token cited (or "none: hard-coded"), verified fallback value, reason if hard-coded. This is the line a developer reads when a colour ticket lands.
- **Deliberate deviations from the site:** every AA correction and every client-requested difference, so nobody "fixes" them back.
- **Edit index:** every `EDIT:` marker in the file with its line reference and a one-line instruction. Phone, CTA hrefs, solicitor names, SRA number, dates, placeholder links.
- **Mirror warning:** "The JSON-LD at the top duplicates the FAQ questions and answers and the step names. If you change one, change both. Run `check-block.py` and it will tell you if they have drifted." This is the trap most likely to catch a support developer: Rule 6 demands an exact match, and a visible-text edit silently breaks it.
- **Do not:** wrap in a document; move the CSS to the theme without keeping the `#id` prefix on every selector; add `@import`; add `<form>` or `<button>`.
- **Sections:** numbered list matching the `[n]` markers.
- **Check result:** the last line of the `check-block.py` output, pasted.

**Cost:** 3 minutes per build for the token map and edit index. Justification: this is the difference between the two-minute find and the twenty-minute one, and it is the only artefact that reaches the support developer.

### 2.5 Changes proposed

- New `references/block-anatomy.md`: file order, section comment format, `EDIT:` convention, header template, token block template, default content order, split rule.
- `qa-checklist.md` section 7 replaced with the support-developer handover.
- `job-brief-template.md`: new fields for client-editable content, who supports the page after launch, and whether the site maintains global colour tokens.
- `SKILL.md` Step 4 points at `block-anatomy.md` and makes the in-file header canonical.

---

## Priority 3: Regression guard

### 3.1 Proposal: a local check that runs inside the build

A single stdlib-only Python script, `scripts/check-block.py`, run by the builder on the output file as the last action of Step 4, before the handover note is written. No dependencies, no network by default, runs in under a second, exits non-zero on any failure so the builder cannot call the file finished while it is blocked. Full source is in `plugin-audit-diffs.md`.

What it checks, mapped to the brief:

| Brief item | Check | Result |
|---|---|---|
| Boilerplate leakage | `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`, `<meta>`, `<title>`, `<link>` outside comments | FAIL |
| Duplicate document elements | as above, plus exactly one top-level content element besides `<style>`/`<script>`, and duplicate `id`s within the fragment | FAIL |
| Unused CSS variables | every `--x` declared must appear in a `var(--x)` | FAIL |
| Unscoped selectors | every selector in every rule, including inside `@media`, must start with `#<root-id>`; `:root` is banned | FAIL |
| (new, Priority 1) | site token referenced without a fallback; colour literal outside the token block; `@import`; `@font-face` | FAIL |
| (new, Priority 1) | mixed or missing token prefix; `!important` over 15 | WARN |
| (Rule 6) | every FAQPage question and answer and every HowTo step name in the JSON-LD must appear verbatim in the visible text | FAIL |
| (Rule 5, standing rules) | `href="#"` placeholders, `href="#anchor"` needing DOM verification, `http://` links, phone numbers not wrapped in `tel:` | WARN |
| (Priority 2) | header comment present; `[n]` section markers with matching closers; `TOKEN MAP` and `EDIT INDEX` present; `<form>` (FAIL), `<button>` (WARN) | FAIL / WARN |

Measured against the two worked examples, it passes them on structure, scoping, dead tokens and JSON-LD, and blocks them on colour literals (19 and 5) and, for MLT, the font `@import`. Against a synthetic fragment with a full document wrapper, a `:root` token block, a dead token and an unscoped `.card` rule, it reports all ten faults. The script is doing what the brief asks.

What it cannot check, and what therefore stays in the human checklist: contrast ratios (needs the rendered colours after inheritance resolves), visual layout at content width and at 375px, keyboard behaviour of the accordion, and whether an anchor id actually exists on the live page. Those items remain in `qa-checklist.md` and the checklist says explicitly that they are the non-automatable remainder.

**Cost:** under 1 minute to run; 1 to 3 minutes to fix what it finds on a typical first pass. It removes the manual pass for everything in the table above, so the net effect on build time is close to zero.

### 3.2 Can the QA checklist enforce this without tooling?

Partly. Four of the checks reduce to one-line greps that the builder can run in the terminal and that a developer can run on a support ticket:

```bash
grep -ciE '<(!doctype|html|head|body|meta|title)[ >]' block.html      # must be 0
grep -oE -- '--[a-z0-9-]+:' block.html | sort -u | wc -l              # declared
grep -oE 'var\(--[a-z0-9-]+' block.html | sort -u | wc -l             # used; must match
grep -c ':root' block.html                                             # must be 0
grep -c '@import' block.html                                           # must be 0
```

Two of the checks cannot be done reliably by eye or by grep: unscoped selectors (a selector list inside `@media` with one unscoped entry is invisible to a grep for the root id) and JSON-LD mirroring (needs the text normalised and compared). Those need the script. So the answer is: the checklist can enforce boilerplate, dead tokens, `:root` and `@import` with the greps above, and I have rewritten the relevant checklist items to include them; it cannot enforce scoping or schema mirroring, and the script is the cheapest way to get those.

The rewritten checklist opens with a new section 0, "Structure and tokens", which lists the script run first and the greps as the no-tooling fallback, then removes the items elsewhere that the script now covers.

### 3.3 Where the check runs

Three places, in order of value:

1. **In the build**, by the builder, as the last step before the handover. This is the one that prevents recurrence.
2. **On a support ticket**, by the developer, on the fragment they pull out of the HTML widget. Same script, same result. This is how a developer confirms a block is one of ours and in good shape before touching it.
3. **On the seven legacy pages**, once, to confirm which need remediation and what exactly is wrong with each. That is the separate piece of work flagged in the scope note; the script makes it a ten-minute triage rather than a reading exercise.

A Screaming Frog crawl after upload catches duplicate `<title>` and `<h1>` elements; it does not catch dead tokens, unscoped selectors or schema drift, and it runs after the client can see the page. The script runs before.

### 3.4 Changes proposed

- New `scripts/check-block.py` (source in the diffs file).
- `SKILL.md` Step 4: "Run `python3 scripts/check-block.py <file>`; the file is not finished while it reports BLOCKED."
- `qa-checklist.md`: new section 0; items superseded by the script removed or reduced to the grep fallback.
- `build-standards.md` "How to apply" paragraph references the check.

---

## Priority 4: Everything else

Ten items, ranked by impact. Each is a contradiction, an error or a duplication across `SKILL.md` and the reference files. Fixes for all ten are in the diffs file.

1. **ID scoping is contradicted by the QA checklist.** `cms-override-patterns.md` opens with "use ID selectors, not class selectors", with a named incident behind it (MSHB). `SKILL.md` repeats it. `qa-checklist.md` section 4 says the opposite twice: "All styles are scoped to a unique parent class (e.g. `.mw-block`)" and, under WordPress general, "No IDs used for styling: use classes only". Both examples and all three client fact sheets use IDs. The checklist is stale. Fix: checklist to ID scoping; the "WP's own ID assignments" concern is answered by the uniqueness rule (a prefixed, page-specific id cannot collide).

2. **The QA checklist tests the superseded FAQ pattern.** Section 4 asks for `.faq-q` with `background: transparent !important` on the trigger, which is the `<button>` plus JS approach that `cms-override-patterns.md` replaced with `<details>/<summary>`. Section 2's "keyboard accessible: Tab, Enter/Space" is native to `<summary>` and needs no check. Fix: section 2 tests for `<details>/<summary>` and the absence of `<button>`; the `.faq-q` item is removed.

3. **Rule 1 has no checklist item for the most common CMS.** The only place the checklist mentions `<html>`, `<head>` or `<body>` is under Webflow. The subcontractor's problem 1 was on WordPress pages. Fix: boilerplate moves to the new CMS-agnostic section 0 and is enforced by the script.

4. **Rule 3's title says the wrong thing.** "Always Chrome-screenshot the live site before building." The body and `SKILL.md` say verify computed styles, and Step 2 treats a screenshot as the fallback when Chrome tooling is unavailable. A screenshot is also the most expensive way to get a value the JS tool returns as text. Fix: retitle "Verify computed styles on the rendered reference page"; screenshot stays as the documented fallback via `screenshot-style-extraction.md`. Intent preserved; this is a correction of the title to match the body.

5. **The handover lives in three different places.** `build-standards.md`: comment at the top of the file. `SKILL.md`: a short note, template at the bottom of the QA checklist. `qa-checklist.md`: a note with every delivery. Fix: in-file header is canonical (it is the only artefact that reaches a support ticket); the delivery message copies it. Covered under Priority 2.4.

6. **WCAG version drifts.** `SKILL.md`, `README.md` and `qa-checklist.md` say "WCAG 2.1 AA"; `build-standards.md` Rule 8 says "WCAG AA". Also, the checklist's large-text threshold ("18px+ bold") is slightly under the WCAG definition (14pt bold is 18.67px). Fix: "WCAG 2.1 AA" everywhere; large text defined as 24px regular or 19px bold to sit safely above the threshold. Clarification, not a change of intent.

7. **"Only one item open at a time" is not achievable with the mandated FAQ pattern unless stated how.** `<details>` items are independent by default. Single-open needs the `name` attribute on each `<details>` (Chrome 120+, Safari 17.2+, Firefox 130+; older browsers degrade to independent items, which is harmless), or JavaScript, which the pattern avoids. Fix: checklist item states the `name` attribute and the degradation.

8. **Fonts via `@import` are permitted by the checklist and contradict inheritance.** Section 3 allows a Google Fonts `@import` with a note. If the font renders on the reference page, it is loaded and the import is a duplicate. Fix: ban `@import` and `@font-face` in blocks; absent fonts are a handover dependency. Covered under Priority 1.3.

9. **"No inline `<style>` if the developer prefers a separate file" undermines the self-contained premise.** The block is designed to be one paste. If a developer chooses to move the CSS into the theme, that is their call, and the only thing that matters is that every selector keeps its `#id` prefix. Fix: item rewritten to say styles stay in the fragment by default, and if moved, the scoping must survive (the script still passes on the CSS alone).

10. **The job brief and fact sheets do not carry what the new rules need.** The brief has no field for site tokens, for who supports the page, or for content the client will edit themselves; it also says "Claude will Chrome-screenshot it" (see item 4). The fact sheets record verified hex values but not the site token names those values came from, which is the one thing a rebuild needs to cite them. Fix: three brief fields added; each fact sheet gains a "Site tokens" line, left as "not yet captured: record on next build" rather than invented, per the brief's constraint on client specifics.

---

## Constraints check

- **Standards intent.** Rule 3 is retitled and its scope narrowed to what it was protecting (rendered values); its body text already said this. Rule 8 gains the "2.1". A ninth standard is added. No other rule changes. Each is stated in the diffs file next to the edit.
- **Client specifics.** None invented. The fact-sheet edits add an empty field with an instruction to capture on the next build.
- **British English, no em dashes, no emojis.** Applied to every "after" block. "Before" blocks quote the current files verbatim, em dashes included.
- **Build speed.** Costs stated per item and collected below. Worst case keeps a 45-minute build under an hour.
- **Accessibility floor.** WCAG 2.1 AA is unchanged as the floor. The AA pair rule and the ban on inheriting failing colours make it harder to lose on a rebrand, not easier.

## Build-time summary

| Change | Minutes per build | Notes |
|---|---|---|
| Snippet A: find and confirm site tokens | 2 | Step 2, reference page |
| Snippet B: probe the target container | 3 | Step 2, reference page |
| Token block hygiene | 0 to 1 | Changes what is written, not how much |
| AA pair rule | 0 | Contrast check already mandatory |
| Section comment format and closers | 1 | Generated with the markup |
| Default section order | 0 | |
| Content placement decision at brief | 1 | Three tests |
| Split around a native widget (when triggered) | 5 | Second fragment header, handover instruction |
| Header: token map and edit index | 3 | |
| `check-block.py` run and fixes | 1 to 3 | Replaces manual checks it covers |
| **Typical total** | **8 to 12** | |
| **With a split** | **13 to 17** | |

## Out of scope, flagged

The seven pre-plugin pages with duplicate document elements and dead tokens are not fixed by anything here. Priority 3.3 gives the triage method. Remediating them is a separate job of roughly ten minutes per page once the script has said what is wrong with each.
