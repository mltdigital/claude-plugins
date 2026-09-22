# eeat-html-builder plugin audit: proposed edits

Companion to `plugin-audit-findings.md`. Nothing here has been applied. Each edit is given as a BEFORE block quoting the current file verbatim (em dashes and all) and an AFTER block with the proposed text. Where a file gains a new section, only the AFTER block is shown and the insertion point is stated.

Files touched, in the order they appear below:

1. `references/build-standards.md`
2. `references/cms-override-patterns.md`
3. `SKILL.md`
4. `references/qa-checklist.md`
5. `references/job-brief-template.md`
6. `references/clients/*.md` (one line each)
7. `README.md`
8. New: `references/block-anatomy.md`
9. New: `scripts/check-block.py`

Statement of intent changes to the eight build standards, as required by the brief: Rule 3 is retitled and its scope narrowed to rendered values (its body already said this); Rule 8 gains "2.1"; a ninth standard is added. No other standard changes.

---

## 1. `references/build-standards.md`

### 1a. Rule 3: retitle, narrow to values, add the token distinction

**Change of intent, stated:** the title moves from the method (screenshot) to the goal (verified computed values). The body already described computed-style extraction and treated screenshots as one route. The new final paragraph adds the values/tokens distinction that Rule 9 depends on. Nothing the rule protected against is weakened.

BEFORE

```
**Rule 3 — Always Chrome-screenshot the live site before building.**
Use the Claude in Chrome tools to screenshot the live page. Extract actual rendered values — font-weight, text-align, heading colour, link colour, list style — not just the kit/theme CSS variables, which are routinely overridden at component level.

**Why:** Kit-level CSS (e.g. Elementor global colours, font-weight: 300 on headings) is frequently overridden by widget-level CSS. The rendered page is always the ground truth.
```

AFTER

```
**Rule 3: Verify computed styles on the rendered reference page before building.**
Use the Chrome JavaScript tool to read computed styles from the live reference page: font-weight, font-size, line-height, text-align, heading colour, link colour, list style. Read values, not screenshots; a screenshot is the fallback when the Chrome tools are unavailable (see `screenshot-style-extraction.md`). Do not take a kit or theme CSS variable's value as a prediction of what renders; widget-level CSS overrides it routinely.

Then probe the target container: inject a bare `<p>` and `<h2>` into the content column and read what they get with nothing applied (snippet in `cms-override-patterns.md`, "Probe the target container"). The block's CSS is the difference between that and the reference page. Where they match, declare nothing.

**Why:** Kit-level CSS (Elementor global colours, font-weight: 300 on headings) is frequently overridden by widget-level CSS, so its value is not what the page shows. The rendered page is the ground truth for what a block should look like. That is a statement about values. Which source the block cites for a value once it is known is Rule 9.
```

### 1b. Rule 8: WCAG version

**Change of intent:** none. Clarification to match `SKILL.md`, `README.md` and the QA checklist.

BEFORE

```
- WCAG AA contrast minimum on all text and interactive elements
```

AFTER

```
- WCAG 2.1 AA contrast minimum on all text and interactive elements (4.5:1 normal text, 3:1 large text and UI components)
```

### 1c. New Rule 9, inserted after Rule 8 and before "How to apply"

**Change of intent:** this is an addition. It is the fix for the reported fault.

AFTER (new)

```
**Rule 9: Inherit before you hard-code. No dead tokens, no orphan literals.**
Every colour in the block is declared once, on the block root, as a custom property with the block's prefix and a role name. Every rule that needs a colour cites the custom property. Outside the token block and outside `var()` fallbacks, no rule contains a colour literal (pure white, pure black and shadow values are exempt).

For each token, cite the site's own token where the site maintains one:

    #ln-road-traffic {
      --ln-brand: var(--e-global-color-primary, #060026);
      --ln-ink:   #1f2430;   /* hard-coded: site body text #4D4D4D fails AA on the tint panels */
    }

The fallback is the Chrome-verified rendered value. A site token may be cited only when (a) it resolves on `body` (`getComputedStyle(document.body).getPropertyValue('--e-global-color-primary')`) and (b) its resolved value equals the colour verified rendering on the reference page. If either fails, hard-code the verified value and say why in the comment and the handover.

Always hard-code, with a reason: typography metrics (size, weight, line-height, letter-spacing), spacing, radii, accessibility corrections, phone numbers, and anything the client asked to differ from the site.

AA pairs: a text colour and the background it sits on come from the same source, both inherited or both hard-coded, never mixed. A rebrand that changes an inherited background must not leave a hard-coded ink behind it.

Fonts: never `@import` or `@font-face` in a block. If a font renders on the reference page, the site loads it; declare nothing and inherit. A font the site does not load is a handover dependency, not something the block fetches.

Every declared custom property must be used. Every custom property used must be declared on the root or be a site token with a fallback. `scripts/check-block.py` enforces all of this.

**Why:** Blocks built as hard-coded hex are orphaned from the site. A brand colour change then means one support edit per block across the estate. Referencing the site's token with the verified value as fallback renders identically today and follows the site tomorrow, at no render cost. The AA pair rule exists because inheriting a background while hard-coding its text is the one way inheritance can silently break contrast.
```

### 1d. "How to apply"

BEFORE

```
**How to apply:** Check all eight rules before delivering. Note any gaps or deliberate exceptions in a handover comment at the top of the file.
```

AFTER

```
**How to apply:** Check all nine rules before delivering. Run `python3 scripts/check-block.py <file>`; the file is not finished while it reports BLOCKED. Record every gap and deliberate exception in the handover header at the top of the file (template in `block-anatomy.md`). The header is the handover; the delivery message copies it.
```

---

## 2. `references/cms-override-patterns.md`

### 2a. Chevron snippet: stop modelling a hard-coded brand colour

BEFORE

```css
#block summary::after {
  content: '';
  width: 20px; height: 20px;
  border-right: 2px solid #d50057;
  border-bottom: 2px solid #d50057;
  transform: rotate(45deg);
}
#block details[open] summary::after { transform: rotate(-135deg); }
```

AFTER

```css
#block summary::after {
  content: '';
  width: 20px; height: 20px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(45deg);
}
#block details[open] summary::after { transform: rotate(-135deg); }
```

Add one sentence after the snippet:

```
`currentColor` makes the chevron follow the summary's text colour, which is itself a block token, so there is one colour to change rather than three.
```

### 2b. Replace "Kit-level CSS is unreliable" with the values/tokens rule

BEFORE

```
**Kit-level CSS is unreliable.**
Elementor global kit CSS (set in Theme Style) is routinely overridden at widget level. Never trust `--e-global-color-*` variables or kit-level `font-weight` declarations as the build source. Always Chrome-verify computed styles on a live rendered page.

**Specific known overrides on Hello Elementor:**
- `font-weight: 300` on headings in the kit is typically overridden to 600 at widget level
- `color: #4D4D4D` for body text may actually render as the darker secondary colour
- `text-align: justify` is common on law firm sites — add `hyphens: none` to prevent mid-word line breaks on links
```

AFTER

```
**Kit values are unreliable. Kit tokens are the colour source.**
Elementor global kit CSS (set in Theme Style) is routinely overridden at widget level, so never read a kit variable's value to predict what the reference page looks like. Always verify computed styles on the rendered page (Rule 3).

But a widget overriding `color` does not change the variable. Elementor declares `--e-global-color-*` on `<body>` through the kit class, custom properties inherit, and the block is not a widget: `var(--e-global-color-primary)` inside an HTML widget resolves to the kit value regardless of what any Heading widget on the page does. So once you know the rendered colour, cite the site token that carries it, with the verified value as fallback (Rule 9):

    --wc-brand: var(--e-global-color-primary, #3D093D);

**Decision table (per property):**

| Property group | Default | Hard-code when |
|---|---|---|
| Body and heading font family | Inherit: declare nothing | Probe (below) shows the container gives a different family from the reference page |
| Font size, weight, line-height, letter-spacing, text-align | Hard-code the verified value where it differs from the probe | Always permitted: these are the widget-overridden properties |
| Brand, secondary, accent; link colour; button fill and border; band and card backgrounds; borders | `var(--site-token, #verified)` | No token; token value differs from what renders; AA failure |
| Body text colour | Inherit if it passes AA on every block background | Fails AA |
| White, black, shadows | Literal allowed | n/a |
| Spacing, radii, widths | Hard-code | Always |
| Phone numbers | Hard-code, `EDIT:` marker | Always (call tracking swaps on render) |

**Find the site's tokens.** Run on the reference page. Elementor 3.x declares `--e-global-color-primary`, `-secondary`, `-text`, `-accent` and hashed custom names; Elementor 4 and its Variables Manager may add designer-named ones; block themes declare `--wp--preset--color--{slug}`. Discover by inspection, never by assumption.

    [...document.styleSheets].flatMap(s => { try { return [...s.cssRules] } catch (e) { return [] } })
      .filter(r => r.selectorText && /^(:root|body|html|\.elementor-kit-\d+)/.test(r.selectorText))
      .flatMap(r => [...r.style].filter(p => p.startsWith('--'))
        .map(p => `${p}: ${r.style.getPropertyValue(p).trim()}`))

Confirm the value that reaches the block, then compare with the rendered colour on buttons, links and headings:

    getComputedStyle(document.body).getPropertyValue('--e-global-color-primary').trim()

Equal: cite the token. Not equal: the site's designer is not maintaining it; hard-code and note it in the handover.

**Probe the target container.** The reference page's headings are Heading widgets with widget styles. An `<h2>` inside an HTML widget gets the kit's `h2` rule instead. The block's CSS is the difference. Run on the reference page:

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

Where the probe matches the reference page, declare nothing. Where it differs, declare only the differing property.

**Specific known overrides on Hello Elementor:**
- `font-weight: 300` on headings in the kit is typically overridden to 600 at widget level; the probe will show 300 and the reference page 600, so the block declares `font-weight: 600`
- `color: #4D4D4D` for body text may actually render as the darker secondary colour
- `text-align: justify` is common on law firm sites; add `hyphens: none` to prevent mid-word line breaks on links

**Fonts.**
Never `@import` or `@font-face` in a block. If the font renders on the reference page the site loads it, and the block inherits by declaring nothing. An `@import` is a duplicate request and pins the block to a family the site may change. A font that is genuinely absent is a dependency for the handover, not something the block fetches.
```

---

## 3. `SKILL.md`

### 3a. Step 1: brief fields

BEFORE

```
If the user has not supplied the brief fields — client, page URL, CMS and page
builder, sitemap URL, a reference page on the same site, scope, content source,
constraints, and style information — ask for the missing ones before doing
anything else.
```

AFTER

```
If the user has not supplied the brief fields (client, page URL, CMS and page
builder, sitemap URL, a reference page on the same site, scope, content source,
content the client will edit themselves, who supports the page after launch,
constraints, and style information) ask for the missing ones before doing
anything else.
```

### 3b. Step 2: first bullet

BEFORE

```
- If the Claude in Chrome tools are available, screenshot the live page and inspect
  computed styles. Extract actual rendered values — font-weight, text-align,
  heading colour, link colour, list style — not kit/theme CSS variables, which are
  routinely overridden at component level.
```

AFTER

```
- If the Chrome tools are available, read computed styles from the reference page
  with the JavaScript tool: font-weight, text-align, heading colour, link colour,
  list style. Do not take a kit variable's value as a prediction of what renders;
  widget-level CSS overrides it. Then run the two snippets in
  `references/cms-override-patterns.md`: find the site's colour tokens and confirm
  which ones carry the rendered brand values, and probe the target container to
  see what a bare element gets. The block's CSS is the difference between the
  probe and the reference page; its colours cite site tokens with verified
  fallbacks (standard 9).
```

### 3c. Step 4

BEFORE

```
Build the block applying every universal standard (below) and the CMS override
patterns in `references/cms-override-patterns.md`. Reference both the style
extraction and the structured content as you build.

Before calling any file finished, run every item in `references/qa-checklist.md`.
Deliver with a short handover note (template at the bottom of the QA checklist).
```

AFTER

```
Build the block applying every universal standard (below), the CMS override
patterns in `references/cms-override-patterns.md`, and the file shape, section
order and comment format in `references/block-anatomy.md`. Reference both the
style extraction and the structured content as you build.

Before calling any file finished, run `python3 scripts/check-block.py <file>` and
clear every FAIL, then run every item in `references/qa-checklist.md`. The header
comment at the top of the file is the handover (template in `block-anatomy.md`);
it is written for the support developer who will see the block cold, and the
delivery message copies it.
```

### 3d. Standards list: heading, item 3, item 8, new item 9, closing line

BEFORE

```
## The 8 universal build standards
```
```
3. **Verify live styling on the rendered page.** Extract real computed values, not
   kit-level CSS variables.
```
```
Check all eight before delivering. Note any deliberate exception in the handover.
```

AFTER

```
## The 9 universal build standards
```
```
3. **Verify computed styles on the rendered reference page.** Read real computed
   values with the JavaScript tool; a kit variable's value is not a prediction of
   what renders. Probe the target container so the block declares only what differs.
```
Insert after item 8:
```
9. **Inherit before you hard-code. No dead tokens, no orphan literals.** Every colour
   is a prefixed, role-named custom property on the block root, citing the site's
   token where the site maintains one: `var(--e-global-color-primary, #verified)`.
   No colour literals outside the token block. Text and its background come from the
   same source (both inherited or both hard-coded). Hard-code typography metrics,
   spacing, accessibility corrections and phone numbers, with a reason. Never
   `@import` a font.
```
```
Check all nine before delivering. Note any deliberate exception in the handover header.
```

### 3e. CMS essentials: two bullets

BEFORE

```
- **Build FAQs with `<details>/<summary>`, not `<button>` + JS** — native disclosure
  sidesteps Elementor's high-specificity button style injection. Draw the chevron
  with a CSS border trick, not a background-image SVG.
```
```
- **Never trust kit-level CSS** (`--e-global-color-*`, kit font-weight). Verify
  computed styles on the live page.
```

AFTER

```
- **Build FAQs with `<details>/<summary>`, not `<button>` + JS.** Native disclosure
  sidesteps Elementor's high-specificity button style injection. Draw the chevron
  with a CSS border trick in `currentColor`, not a background-image SVG.
```
```
- **Kit values are unreliable; kit tokens are the colour source.** Never read
  `--e-global-color-*` or kit font-weight to predict what renders. Do cite a kit
  colour token, with the verified value as fallback, once you have confirmed it
  carries the rendered brand colour.
```

### 3f. Standing rules: scoping

BEFORE

```
- **Scope every CSS rule to one unique parent** so styles cannot leak into the page.
```

AFTER

```
- **Scope every CSS rule to one unique parent ID** (`#client-page-block`) so styles
  cannot leak into the page. Custom properties are declared on that ID, never on
  `:root`.
```

---

## 4. `references/qa-checklist.md`

### 4a. New section 0, inserted before section 1

AFTER (new)

```
## 0. Structure and tokens (automated)

Run the check first. It exits BLOCKED on any failure and the file is not finished until it passes:

    python3 scripts/check-block.py <file>

It enforces: no document boilerplate; one root element with an id; every selector scoped to that id, including inside `@media`; no `:root`; no dead custom properties; no site token without a fallback; no colour literals outside the token block; no `@import` or `@font-face`; no `<form>`; JSON-LD questions, answers and step names present verbatim on the page; header comment, `[n]` section markers with closers, TOKEN MAP and EDIT INDEX present.

No tooling fallback. If the script cannot be run, these greps cover boilerplate, dead tokens, `:root` and `@import`. They do not cover unscoped selectors or JSON-LD drift, which then have to be read by eye:

    grep -ciE '<(!doctype|html|head|body|meta|title)[ >]' block.html   # must be 0
    grep -oE -- '--[a-z0-9-]+:' block.html | sort -u                     # declared tokens
    grep -oE 'var\(--[a-z0-9-]+' block.html | sort -u                    # used tokens; sets must match
    grep -c ':root' block.html                                            # must be 0
    grep -c '@import' block.html                                          # must be 0

- [ ] `check-block.py` reports PASS (or the greps above are all clean and selectors and JSON-LD have been read by eye)
- [ ] Every WARN has been either fixed or listed in the handover header with a reason
```

### 4b. Section 1: large-text threshold

BEFORE

```
The minimum contrast ratios are 4.5:1 for normal text and 3:1 for large text (18px+ bold or 24px+ regular) and UI components such as button borders and focus indicators.
```

AFTER

```
The minimum contrast ratios are 4.5:1 for normal text and 3:1 for large text (24px+ regular or 19px+ bold; WCAG defines large as 18pt regular or 14pt bold, and 18px bold sits just under the bold threshold) and UI components such as button borders and focus indicators. Check the resolved colours, not the token names: where a token inherits from the site, read the rendered value on the live page after insertion.
```

Add one item to section 1:

```
- [ ] AA pairs: every text colour and the background it sits on come from the same source (both inherited or both hard-coded). List any inherited background in the handover as needing a contrast re-check on rebrand.
```

### 4c. Section 2: FAQ accordion

BEFORE

```
- [ ] Each item opens and closes correctly
- [ ] Only one item open at a time (if that is the intended behaviour -- confirm with brief)
- [ ] Keyboard accessible: Tab moves focus to each question, Enter/Space opens it
- [ ] No Elementor or theme button styles leaking in (check for unexpected background colours or borders on the trigger element)
- [ ] Open/close icon changes state visually (e.g. + becomes x, chevron rotates)
- [ ] Text does not get clipped or overflow on small screens
```

AFTER

```
- [ ] Built with `<details>/<summary>`; no `<button>` and no JavaScript (the check script warns on `<button>`)
- [ ] Each item opens and closes correctly
- [ ] If the brief asks for one item open at a time, every `<details>` carries the same `name` attribute (Chrome 120+, Safari 17.2+, Firefox 130+; older browsers show independent items, which is acceptable). Otherwise items are independent.
- [ ] `summary` has a visible focus style that passes 3:1 against its background
- [ ] Chevron drawn with the border trick in `currentColor`; it rotates on open
- [ ] Text does not get clipped or overflow at 375px
```

### 4d. Section 3: external dependencies

BEFORE

```
- [ ] If using Google Fonts -- confirm whether the font is already loaded. If unknown, add the @import but note in the handover that a duplicate load may occur and the developer should check.
```

AFTER

```
- [ ] No `@import` and no `@font-face` in the block. Fonts that render on the reference page are already loaded; the block inherits them by declaring no font-family. A font the site does not load is listed in the handover as a dependency for the developer to add site-wide, not fetched by the block.
```

### 4e. Section 4: CMS and theme compatibility

BEFORE

```
**Elementor (most common)**
- [ ] `.faq-q` or equivalent accordion trigger has `background: transparent !important`, `border: none !important`, `box-shadow: none !important` to prevent Elementor injecting button styles
- [ ] No `<form>` tags inside the block -- Elementor can conflict with these
- [ ] All styles are scoped to a unique parent class (e.g. `.mw-block`, `.client-content-block`) to prevent bleed into other page elements
- [ ] Tested at the content area's actual max-width, not at full viewport -- law firm pages are commonly 750px to 900px content width

**WordPress (general)**
- [ ] No inline `<style>` tags if the developer prefers styles in a separate file -- flag this in the handover note
- [ ] No IDs used for styling -- use classes only to avoid conflicts with WP's own ID assignments
- [ ] Images, if any, use relative or absolute URLs that will resolve on the client's server -- no localhost or Claude output paths

**Webflow**
- [ ] Note in the handover that custom code blocks have a character limit -- if the file is large, it may need splitting
- [ ] No `<html>`, `<head>`, or `<body>` tags in the output -- Webflow embeds require the inner content only
```

AFTER

```
**Elementor (most common)**
- [ ] Every selector starts with the block's unique id (`#client-page-block`), including inside `@media`. ID specificity beats theme selectors without blanket `!important` (see `cms-override-patterns.md`). The check script enforces this.
- [ ] No `<form>` inside the block. A form belongs in a native widget; split the block around it (see `block-anatomy.md`).
- [ ] `!important` used only on properties the theme is actually overriding; the script warns above 15 uses
- [ ] Tested at the content area's actual max-width, not at full viewport; law firm pages are commonly 750px to 900px content width
- [ ] Anything dynamic (ACF field, dynamic tag, shortcode) sits in a native widget outside the fragment; the HTML widget outputs raw content and does not process them

**WordPress (general)**
- [ ] Styles stay in the fragment's `<style>` block by default. If the developer moves them into the theme, every selector keeps its `#id` prefix; the check script still passes on the CSS alone.
- [ ] The root id is unique on the page and prefixed for the client and page (`#wc-divorce-separation`), so it cannot collide with WordPress or Elementor ids
- [ ] Images, if any, use URLs that resolve on the client's server; no localhost or Claude output paths

**Webflow**
- [ ] Note in the handover that custom code blocks have a character limit; if the file is large, it may need splitting
- [ ] Global colour variables, if the designer has set any, are found by the token snippet in `cms-override-patterns.md` and cited the same way
```

(Boilerplate has moved to section 0 and applies to every CMS.)

### 4f. Section 7: handover note, replaced

BEFORE

```
## 7. Handover note

Include a short note with every file delivery covering:

- What the file contains and where it should be inserted
- Any external dependencies (fonts, icon libraries) and whether they need to be loaded separately
- Any known conflicts or CMS-specific instructions (e.g. the Elementor button override)
- Which links are placeholders and need replacing before going live
- Confirmation that the file has been QA'd against this checklist
```

AFTER

```
## 7. Handover

The handover is the header comment at the top of the file (template in `block-anatomy.md`). It is written for a support developer who has never seen the block and has a ticket to action. The delivery message to the client or commissioner copies the header; it adds nothing the file does not carry, because the message does not survive to the ticket.

- [ ] Header present and in the template order: Block, Token map, Deliberate deviations, Edit index, Mirror warning, Do not, Sections, Check result
- [ ] Token map has one line per custom property: block token, site token cited or "none", fallback value, reason if hard-coded
- [ ] Every AA correction and every client-requested difference from the site is under Deliberate deviations, so nobody reverts it to brand
- [ ] Edit index lists every `EDIT:` marker in the file: phone numbers, CTA destinations, placeholder links, solicitor names, SRA number, dates
- [ ] Mirror warning states that the JSON-LD duplicates the FAQ and step text and both must change together
- [ ] Dependencies the site must provide (a font not loaded, an icon set) are listed; the block fetches none of them
- [ ] If the block is split around a native widget, each fragment's header names the other and what sits between them
- [ ] Last line of the `check-block.py` output pasted under Check result
```

---

## 5. `references/job-brief-template.md`

### 5a. Page URL note

BEFORE

```
**URL of the page being updated:** *(paste the live URL — Claude will Chrome-screenshot it before building)*
```

AFTER

```
**URL of the page being updated:** *(paste the live URL; Claude will read its computed styles and find its colour tokens before building)*
```

### 5b. Reference page note

BEFORE

```
*(Claude will use this to verify rendered typography, heading weights, link colours, and component styles. Without this, the first build is guessing.)*
```

AFTER

```
*(Claude will read rendered typography, heading weights, link colours and component styles from it, probe what a bare element gets in its content column, and find the site's global colour tokens. Without this, the first build is guessing.)*
```

### 5c. New fields under "What we are building", after "Contact form / CTA destination"

AFTER (new)

```
**Content the client will change themselves after launch:**
*(fees, opening hours, dated statistics, rotating testimonials, anything updated without a designer. This goes in a native widget, not the block, and the block is split around it. Leave blank if none.)*

**Who supports this page after launch?**
*(name or team; the handover header is written for them)*
```

### 5d. New field under "Style matching", after "Brand colours"

AFTER (new)

```
**Does the site maintain global colour tokens?** *(Elementor global colours, theme.json presets, or designer variables. Leave blank if unknown; Claude will check and record what it finds in the handover.)*
```

---

## 6. `references/clients/*.md`

Add one line to each of `lewis-nedas.md`, `mlt-digital.md` and `wright-crawford.md`, after the design tokens bullet. Values are deliberately not filled in; the brief forbids inventing client specifics and the sheets are point in time.

AFTER (new, identical in each file)

```
- Site colour tokens: not yet captured. On the next build, run the token snippet in `cms-override-patterns.md` on the reference page and record here which `--e-global-color-*` (or other) names carry the verified brand values above, and which verified values have no maintained token. Cite tokens per build standard 9.
```

And in `mlt-digital.md`, extend the existing accessibility caveat so the pair rule is explicit:

BEFORE

```
- Accessibility caveat: the live site puts WHITE text on the #A3C126 green button (~2:1, fails WCAG AA). For accessible builds use dark ink text on the green pill instead.
```

AFTER

```
- Accessibility caveat: the live site puts WHITE text on the #A3C126 green button (~2:1, fails WCAG AA). For accessible builds use dark ink text on the green pill instead, and hard-code both the green and the ink as a pair (do not inherit the green from a site token while hard-coding the ink; a rebrand would break contrast silently). Record in the handover that the CTA pair needs a contrast re-check if the brand green changes.
```

---

## 7. `README.md`

BEFORE

```
- **Eight universal build standards** — no document boilerplate, verify styling on
  the live page, sitemap-driven internal linking, verified links only, JSON-LD
  structured data, and EEAT/CRO/accessibility discipline.
```

AFTER

```
- **Nine universal build standards**: no document boilerplate, verify computed
  styles on the live page, sitemap-driven internal linking, verified links only,
  JSON-LD structured data, EEAT/CRO/accessibility discipline, and colour
  inheritance from the site's own tokens with no dead tokens.
```

Add after the "Four reusable templates" bullet:

```
- **A regression check**: `scripts/check-block.py` runs on the output file before
  handover and blocks boilerplate, unscoped selectors, dead or orphaned colour
  tokens, font imports and JSON-LD that has drifted from the visible text.
- **Block anatomy**: a fixed file order, section comment format and a handover
  header written for the support developer who sees the block cold.
```

---

## 8. New file: `references/block-anatomy.md`

```
# Block anatomy

The shape every drop-in block takes, so that a support developer who has never seen it can find any section, any colour and any editable value in under two minutes. `scripts/check-block.py` enforces the parts of this that can be checked mechanically.

## File order (fixed)

1. Header comment: the handover (template below).
2. One `<style>` block, in this internal order, each part introduced by a `/* [n] NAME */` comment:
   - Tokens: the bare `#root { --prefix-role: ...; }` rule and nothing else in it
   - Base: root typography and layout that differ from the container probe
   - Components: buttons, cards, steps, details/summary, bands
   - Sections: rules specific to one section, in page order, numbered to match the HTML markers
   - Responsive: `@media` blocks last, every selector still starting with the root id
3. JSON-LD `<script type="application/ld+json">` blocks.
4. One root `<div id="prefix-page">` and nothing else at the top level.

## Root id and prefix

Root id: client prefix, then page slug, for example `#wc-divorce-separation`, `#ln-road-traffic`. Unique on the page. Every selector starts with it. Every custom property and every class starts with the same prefix (`--wc-`, `.wc-`).

## Token block

Role names, not colour names. One line per token. Site token cited where the site maintains one, verified value as fallback, reason comment where hard-coded.

    #wc-divorce-separation {
      --wc-brand:      var(--e-global-color-primary, #3D093D);
      --wc-accent:     var(--e-global-color-accent, #BAB364);
      --wc-panel:      var(--e-global-color-6f2a1b3, #F4F4F4);
      --wc-ink:        #4d4d4d;   /* hard-coded: site body #8A8A8A fails AA */
      --wc-eyebrow:    #6b6428;   /* hard-coded: site olive small text fails AA */
      --wc-border:     #e4e4ea;   /* hard-coded: no maintained site token */
    }

No colour literal appears anywhere else in the CSS except as a `var()` fallback, pure white, pure black or a shadow.

## Section comment format

Opener and closer, both mandatory. Number, name in capitals, the CSS hook a developer greps for, one optional note.

    <!-- [3] STEP-BY-STEP GUIDE | .wc-steps | HowTo schema mirrors these step names -->
      ...
    <!-- /[3] STEP-BY-STEP GUIDE -->

The `<style>` block uses `/* [3] STEP-BY-STEP GUIDE */` for the matching rules.

## Editable hotspots

Mark every value a client is likely to ask for by ticket with an `EDIT:` comment on the line above it, and list every marker in the header's Edit index.

    <!-- EDIT: phone number. CallRail swaps it on render; keep it static here. -->
    <a href="tel:02078702736">020 7870 2736</a>

    <!-- EDIT: enquiry CTA destination. Full URL, not an anchor (no stable form id on /contact/). -->
    <a class="ln-btn" href="https://www.example.co.uk/contact/">Speak to a solicitor</a>

Mark: phone numbers, CTA hrefs, placeholder links, solicitor names and roles, SRA number, any date or figure.

## Default content order

The output order of the content-structuring prompt, with the first CTA after the lead paragraph (standard 8):

1. Intro (H2 if the page title supplies the H1; H1 only for a full-page replacement)
2. First CTA
3. Key points
4. Process or steps
5. Topic sections, in the order the source document gives them
6. FAQ
7. Trust and credential signals
8. Closing CTA band

Deviate for CRO or content reasons, and list every deviation under the header's Sections line.

## What does not go in the block

Apply three tests. Content that fails any of them goes in a native widget or a site-wide source, and the block is split around it.

1. It changes on a schedule or by a non-developer (fees, hours, dated statistics, rotating testimonials).
2. It already exists elsewhere on the site (address, SRA number, accreditation strip, credentials the profile page carries). Link to it; do not restate it.
3. It needs to be dynamic (ACF field, dynamic tag, shortcode). The Elementor HTML widget outputs raw content and does not process these.

Phone numbers stay in the block, marked `EDIT:`; the call-tracking swap makes duplication safe. Solicitor name and role stay; credentials beyond that are linked to the profile page.

Splitting: deliver `part-1` and `part-2` with root ids `#prefix-page-1` and `#prefix-page-2`, the same token block in each, and each header naming the other fragment and what sits between them.

## Header template

    <!--
      BLOCK        Wright & Crawford: divorce and separation (drop-in content block)
      Root id      #wc-divorce-separation   Prefix --wc- / .wc-
      File         wright-crawford--divorce-and-separation.html
      Page         https://www.example.co.uk/family-law/divorce-and-separation-agreements/
      Pasted into  Elementor HTML widget, main content column, below the page-title hero
      Built        17 Jun 2026   Styles verified on live reference page 17 Jun 2026

      TOKEN MAP    block token     site token cited              fallback   note
                   --wc-brand      --e-global-color-primary      #3D093D
                   --wc-accent     --e-global-color-accent       #BAB364
                   --wc-panel      --e-global-color-6f2a1b3      #F4F4F4
                   --wc-ink        none (hard-coded)             #4d4d4d    site body #8A8A8A fails AA
                   --wc-eyebrow    none (hard-coded)             #6b6428    site olive small text fails AA
                   --wc-border     none (hard-coded)             #e4e4ea    no maintained token on site

      DELIBERATE DEVIATIONS FROM THE SITE
        Body text darkened to #4d4d4d (site #8A8A8A fails WCAG 2.1 AA). Do not revert.
        Inline links underlined (site does not; needed for AA without colour alone).

      EDIT INDEX   search the file for "EDIT:"
        phone number (static; Infinity call tracking swaps it)
        enquiry CTA destination x2 (full /contact-us/ URL; CF7 has no stable anchor)
        solicitor name and role: Denise Hooper, Family Law Department lead
        dates in the JSON-LD (datePublished, dateModified)

      MIRROR WARNING
        The JSON-LD at the top duplicates every FAQ question and answer and every
        step name. If you change one, change both. check-block.py reports drift.

      DO NOT
        wrap this in <html>/<head>/<body>; it is a fragment
        move the CSS into the theme without keeping the #wc-divorce-separation prefix on every selector
        add @import or @font-face; the site loads the fonts
        add <form> or <button> inside the block; use a native widget and split the block

      SECTIONS     [1] INTRO  [2] KEY POINTS  [3] STEP-BY-STEP GUIDE  [4] FINANCIAL SETTLEMENTS
                   [5] SEPARATION AGREEMENTS  [6] CHILD ARRANGEMENTS  [7] ALTERNATIVES TO COURT
                   [8] FAQ  [9] CONTACT BAND
                   Deviation from default order: trust signals folded into [2]; closing CTA is [9].

      CHECK        PASS: 0 fail, 0 warn (wright-crawford--divorce-and-separation.html)
    -->

The example values above are illustrative of the format only; every build fills the header from its own verified data.
```

---

## 9. New file: `scripts/check-block.py`

Place at `skills/drop-in-html-builder/scripts/check-block.py`. Stdlib only; tested against both worked examples and a synthetic broken fragment (results in the findings file, Priority 3.1). Usage: `python3 scripts/check-block.py <fragment.html> [--strict]`.

```python
#!/usr/bin/env python3
"""check-block.py: pre-handover regression guard for drop-in HTML fragments.

Usage: python3 check-block.py <fragment.html> [--strict]
Exit 1 on any FAIL. --strict also turns WARN into FAIL.
Stdlib only. Run it on the output file before every handover.
"""
import html
import json
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
SITE_TOKEN = re.compile(r"^--(e-global-|wp--preset--|_colors|_fonts)")
COLOUR_LIT = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgb|hsl)a?\(")
SHADOW = {"box-shadow", "text-shadow"}
UK_PHONE = re.compile(r"\b0\d{2,4}[ \d]{6,9}\b")


class Walker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.top = []
        self.ids = []
        self.text = []
        self.tags = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.depth == 0:
            self.top.append((tag, a.get("id")))
        if a.get("id"):
            self.ids.append(a["id"])
        self.tags.append((tag, a, self.depth))
        if tag in ("style", "script"):
            self.skip += 1
        if tag not in VOID:
            self.depth += 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.depth -= 1

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.skip = max(0, self.skip - 1)
        if tag not in VOID:
            self.depth = max(0, self.depth - 1)

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


def norm(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip().lower()


def css_rules(css):
    """Yield (selector, body, context) for every rule, descending into @media."""
    out = []

    def walk(block, ctx):
        i = 0
        while True:
            o = block.find("{", i)
            if o < 0:
                break
            sel = block[i:o].strip().rstrip(";").split(";")[-1].strip()
            depth, j = 1, o + 1
            while depth and j < len(block):
                depth += {"{": 1, "}": -1}.get(block[j], 0)
                j += 1
            body = block[o + 1:j - 1]
            if sel.startswith("@media") or sel.startswith("@supports"):
                walk(body, ctx + [sel])
            elif sel.startswith("@keyframes") or sel.startswith("@-webkit-keyframes"):
                out.append((sel, body, ctx))
            else:
                out.append((sel, body, ctx))
            i = j
    walk(css, [])
    return out


def main(path, strict=False):
    src = open(path, encoding="utf-8").read()
    fails, warns = [], []
    F, W = fails.append, warns.append

    comments = re.findall(r"<!--(.*?)-->", src, re.S)
    body = re.sub(r"<!--.*?-->", "", src, flags=re.S)

    # Header comment and section markers
    if not src.lstrip().startswith("<!--"):
        F("no handover header comment at the top of the file")
    opens = {re.sub(r"\s+", " ", m).strip() for c in comments
             for m in re.findall(r"^\s*\[(\d+)\]\s*([^|\n]+)", c, re.M)}
    closes = set()
    for c in comments:
        for m in re.finditer(r"^\s*/\[(\d+)\]\s*([^|\n]+)", c, re.M):
            closes.add(re.sub(r"\s+", " ", m.group(0)).strip().lstrip("/"))
    if len(opens) < 3:
        W("fewer than 3 standard section markers '<!-- [n] NAME | ... -->' found")
    elif opens != closes:
        W("section open/close markers do not match: %s" % sorted(opens ^ closes))
    if not any("EDIT INDEX" in c.upper() for c in comments):
        W("header has no 'EDIT INDEX' block (support developer quick-edit list)")
    if not any("TOKEN MAP" in c.upper() for c in comments):
        W("header has no 'TOKEN MAP' block (site token -> block token -> fallback)")

    # Boilerplate
    for tag in ("!doctype", "html", "head", "body", "meta", "title", "link"):
        if re.search(r"<%s[\s>]" % tag, body, re.I):
            F("document boilerplate present: <%s>" % tag)
    if re.search(r"<form[\s>]", body, re.I):
        F("<form> inside the block (banned: Elementor conflicts)")
    if re.search(r"<button[\s>]", body, re.I):
        W("<button> present: Elementor injects button styles, prefer details/summary or <a>")

    # Structure
    w = Walker()
    w.feed(body)
    non_meta_top = [(t, i) for t, i in w.top if t not in ("style", "script")]
    root_id = None
    if len(non_meta_top) != 1:
        F("expected exactly one top-level content element besides <style>/<script>, found %d: %s"
          % (len(non_meta_top), [t for t, _ in non_meta_top]))
    elif not non_meta_top[0][1]:
        F("top-level content element has no id (needed for CSS scoping)")
    else:
        root_id = non_meta_top[0][1]
    dupes = {i for i in w.ids if w.ids.count(i) > 1}
    if dupes:
        F("duplicate ids in fragment: %s" % sorted(dupes))
    page_text = norm(" ".join(w.text))

    # CSS
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", body, re.S | re.I))
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    if "@import" in css:
        F("@import in CSS (fonts that render on the reference page are already loaded)")
    if "@font-face" in css:
        F("@font-face in CSS (fonts belong to the site, not the block)")
    if re.search(r"(^|[,\s]):root\b", css):
        F(":root selector in CSS (custom properties must be declared on the block root)")
    rules = css_rules(css)
    declared, used, fallbacks = set(), set(), set()
    literals = []
    token_rule_seen = False
    for sel, rbody, ctx in rules:
        if sel.startswith("@"):
            continue
        if root_id:
            for s in sel.split(","):
                s = s.strip()
                if not re.match(r"#%s(?![\w-])" % re.escape(root_id), s):
                    F("unscoped selector '%s'%s" % (s, " in " + " ".join(ctx) if ctx else ""))
        is_token_rule = root_id and sel.strip() == "#" + root_id and not ctx
        if is_token_rule:
            token_rule_seen = True
        for decl in rbody.split(";"):
            if ":" not in decl:
                continue
            prop, val = decl.split(":", 1)
            prop, val = prop.strip(), val.strip()
            if prop.startswith("--"):
                declared.add(prop)
            for m in re.finditer(r"var\(\s*(--[\w-]+)\s*(,)?", val):
                used.add(m.group(1))
                if m.group(2):
                    fallbacks.add(m.group(1))
            stripped_val = re.sub(r"var\([^()]*(?:\([^()]*\)[^()]*)*\)", "", val)
            stripped_val = re.sub(r"#(?:fff(?:fff)?|000(?:000)?)\b", "", stripped_val, flags=re.I)
            if (not is_token_rule and not prop.startswith("--") and prop not in SHADOW
                    and COLOUR_LIT.search(stripped_val)):
                literals.append("%s { %s: %s }" % (sel.strip(), prop, val))
    for m in re.finditer(r"var\(\s*(--[\w-]+)\s*(,)?", css):
        used.add(m.group(1))
    dead = sorted(declared - used)
    if dead:
        F("dead custom properties (declared, never used): %s" % dead)
    for u in sorted(used - declared):
        if SITE_TOKEN.match(u):
            if u not in fallbacks:
                F("site token %s referenced without a verified fallback value" % u)
        else:
            F("custom property %s used but never declared on the block root" % u)
    if literals:
        F("%d colour literal(s) outside the token block (use var(--token) instead):\n    "
          % len(literals) + "\n    ".join(literals[:12]) + ("\n    ..." if len(literals) > 12 else ""))
    if declared and root_id and not token_rule_seen:
        W("custom properties are not declared on the bare root selector '#%s'" % root_id)
    prefixes = {d.split("-")[2] for d in declared if d.count("-") >= 3}
    if len(prefixes) > 1:
        W("custom properties use mixed prefixes %s; use one block prefix" % sorted(prefixes))
    elif declared and not prefixes:
        W("custom properties have no block prefix (e.g. --wc-brand)")
    n_imp = css.count("!important")
    if n_imp > 15:
        W("%d uses of !important; the pattern is surgical, not blanket" % n_imp)

    # JSON-LD must mirror visible content
    for attrs, code in re.findall(r"<script([^>]*)>(.*?)</script>", body, re.S | re.I):
        if "ld+json" not in attrs:
            continue
        try:
            data = json.loads(code)
        except ValueError as e:
            F("JSON-LD does not parse: %s" % e)
            continue
        nodes = data if isinstance(data, list) else [data]
        stack = list(nodes)
        while stack:
            n = stack.pop()
            if not isinstance(n, dict):
                continue
            t = n.get("@type", "")
            if "FAQPage" in t:
                for q in n.get("mainEntity", []):
                    for label, txt in (("question", q.get("name", "")),
                                       ("answer", (q.get("acceptedAnswer") or {}).get("text", ""))):
                        if txt and norm(txt) not in page_text:
                            F("FAQ %s in JSON-LD not found verbatim on the page: %r" % (label, txt[:70]))
            if "HowTo" in t:
                for s in n.get("step", []):
                    nm = s.get("name", "")
                    if nm and norm(nm) not in page_text:
                        F("HowTo step in JSON-LD not found on the page: %r" % nm[:70])
            for v in n.values():
                if isinstance(v, (dict, list)):
                    stack.extend(v if isinstance(v, list) else [v])

    # Links and phones
    for href in re.findall(r'href="([^"]*)"', body):
        if href == "#":
            W("placeholder href=\"#\": must appear in the header EDIT INDEX")
        elif href.startswith("#"):
            W("anchor link %s: confirm the id was DOM-verified on the live page" % href)
        elif href.startswith("http://"):
            W("insecure link %s" % href)
    tel_texts = " ".join(re.findall(r'<a[^>]+href="tel:[^"]*"[^>]*>(.*?)</a>', body, re.S | re.I))
    tel_norm = norm(tel_texts)
    for m in UK_PHONE.finditer(page_text):
        if m.group(0) not in tel_norm:
            W("phone number %r is not wrapped in <a href=\"tel:...\">" % m.group(0))

    for f in fails:
        print("FAIL  " + f)
    for w_ in warns:
        print("WARN  " + w_)
    bad = len(fails) + (len(warns) if strict else 0)
    print("\n%s: %d fail, %d warn (%s)" % ("PASS" if not bad else "BLOCKED", len(fails), len(warns), path))
    return 1 if bad else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(args[0], strict="--strict" in sys.argv))
```
