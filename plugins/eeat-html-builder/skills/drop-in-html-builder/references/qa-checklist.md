# Pre-Handover QA Checklist

Run through this before sending the final HTML file to the client or developer. Each item is a real issue that has come up on previous jobs. Do not skip sections on the assumption the build is clean.

---

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
- [ ] Not a repeat of the pattern log: section headings, disclosure treatment and component shapes checked against the last two entries in `references/pattern-log.md`; anything repeated is justified because the client's own site already uses that device

---

## 1. Contrast and accessibility (WCAG 2.1 AA)

The minimum contrast ratios are 4.5:1 for normal text and 3:1 for large text (24px+ regular or 19px+ bold; WCAG defines large as 18pt regular or 14pt bold, and 18px bold sits just under the bold threshold) and UI components such as button borders and focus indicators. Check the resolved colours, not the token names: where a token inherits from the site, read the rendered value on the live page after insertion.

Check every combination in use:

- [ ] Body text on main background
- [ ] Heading text on main background
- [ ] Light text on coloured/dark backgrounds (CTA blocks, callout boxes, coloured card headers)
- [ ] Button label text on button fill colour
- [ ] Ghost/outline button text on page background
- [ ] Muted or secondary text (e.g. step numbers, label text, captions) -- these often fail
- [ ] Hover states -- check both text and background changes on hover
- [ ] Link text within body copy on white background
- [ ] AA pairs: every text colour and the background it sits on come from the same source (both inherited or both hard-coded). List any inherited background in the handover as needing a contrast re-check on rebrand. A `var()` fallback is not a contrast safeguard -- it never renders once the token resolves, so check the token's live value.
- [ ] Reflow at 320px CSS width: no horizontal scrolling and no loss of content or function (WCAG 1.4.10)
- [ ] Text resized to 200% in the browser: no clipped or overlapping text, no loss of content or function (WCAG 1.4.4)
- [ ] Page still usable with the browser's own text-spacing overrides applied (line-height 1.5x, paragraph spacing 2x, letter-spacing 0.12x, word-spacing 0.16x) -- no clipped or overlapping text (WCAG 1.4.12)

Use https://webaim.org/resources/contrastchecker/ if you are not sure. If anything fails, fix the colour before handing over -- do not flag it as a known issue and leave it.

---

## 2. FAQ accordion

- [ ] Built with `<details>/<summary>`; no `<button>` and no JavaScript (the check script warns on `<button>`)
- [ ] Each item opens and closes correctly
- [ ] If the brief asks for one item open at a time, every `<details>` carries the same `name` attribute (Chrome 120+, Safari 17.2+, Firefox 130+; older browsers show independent items, which is acceptable). Otherwise items are independent.
- [ ] `summary` has a visible focus style that passes 3:1 against its background
- [ ] Disclosure treatment (chevron/plus-minus/marker/none) matches one already in the site's own component inventory, not applied by default
- [ ] Icon (if any) drawn in `currentColor`; it changes state on open
- [ ] Text does not get clipped or overflow at 375px

---

## 3. External dependencies

- [ ] If using an icon CDN (Tabler, Font Awesome, etc.) -- confirm whether it is already loaded on the client site. If unknown, switch to inline SVG for all icons.
- [ ] No `@import` and no `@font-face` in the block. Fonts that render on the reference page are already loaded; the block inherits them by declaring no font-family. A font the site does not load is listed in the handover as a dependency for the developer to add site-wide, not fetched by the block.
- [ ] No dependencies on JavaScript libraries that are not confirmed as available (e.g. do not use jQuery unless you know it is present)

---

## 4. CMS and theme compatibility

**Elementor (most common)**
- [ ] Every selector starts with the block's unique id (`#client-page-block`), including inside `@media`. ID specificity beats theme selectors without blanket `!important` (see `cms-override-patterns.md`). The check script enforces this.
- [ ] No `<form>` inside the block. A form belongs in a native widget; split the block around it (see `block-anatomy.md`).
- [ ] `!important` used only on properties the theme is actually overriding; the script warns above 15 uses
- [ ] Tested at the content area's actual max-width, not at full viewport; measured on the reference page, not assumed (Wright & Crawford's own sheet records 1080px)
- [ ] Anything dynamic (ACF field, dynamic tag, shortcode) sits in a native widget outside the fragment; the HTML widget outputs raw content and does not process them

**WordPress (general)**
- [ ] Styles stay in the fragment's `<style>` block by default. If the developer moves them into the theme, every selector keeps its `#id` prefix; the check script still passes on the CSS alone.
- [ ] The root id is unique on the page and prefixed for the client and page (`#wc-divorce-separation`), so it cannot collide with WordPress or Elementor ids
- [ ] Images, if any, use URLs that resolve on the client's server; no localhost or Claude output paths

**Webflow**
- [ ] Note in the handover that custom code blocks have a character limit; if the file is large, it may need splitting
- [ ] Global colour variables, if the designer has set any, are found by the token snippet in `cms-override-patterns.md` and cited the same way

(Boilerplate has moved to section 0 and applies to every CMS.)

---

## 5. Mobile and responsive layout

- [ ] Test at 375px (iPhone SE) and 390px (iPhone 14) as minimum widths
- [ ] Multi-column layouts collapse to single column correctly
- [ ] Process/steps section stacks vertically with connectors hidden or adapted
- [ ] CTA block text does not overflow its container
- [ ] No horizontal scroll introduced by fixed widths or negative margins

---

## 6. Content and copy

- [ ] CTA links are clearly marked as placeholders (e.g. `href="#"` with a comment `<!-- replace with contact form URL -->`) -- never leave a dead link without flagging it
- [ ] Phone numbers are wrapped in `<a href="tel:...">` so they are tappable on mobile
- [ ] No Lorem Ipsum or placeholder copy has been left in accidentally
- [ ] Solicitor names and credential details match exactly what was provided -- do not abbreviate or paraphrase
- [ ] SRA number, if included, matches the document exactly

---

## 7. Handover

The handover is the header comment at the top of the file (template in `block-anatomy.md`). It is written for a support developer who has never seen the block and has a ticket to action. The delivery message to the client or commissioner copies the header; it adds nothing the file does not carry, because the message does not survive to the ticket.

HTML comments ship to production and are visible to anyone who views source. Never put a backup file path, a server path, a staging URL with credentials, or any other access detail in the header or anywhere else in the file -- if a developer needs that, send it separately, not in the block.

- [ ] Header present and in the template order: Block, Token map, Deliberate deviations, Edit index, Mirror warning, Do not, Sections, Check result
- [ ] Token map has one line per custom property: block token, site token cited or "none", fallback value, reason if hard-coded
- [ ] Every AA correction and every client-requested difference from the site is under Deliberate deviations, so nobody reverts it to brand
- [ ] Edit index lists every `EDIT:` marker in the file: phone numbers, CTA destinations, placeholder links, solicitor names, SRA number, dates
- [ ] Mirror warning states that the JSON-LD duplicates the FAQ and step text and both must change together
- [ ] Header contains no backup path, server path, staging credential or other access detail
- [ ] Dependencies the site must provide (a font not loaded, an icon set) are listed; the block fetches none of them
- [ ] If the block is split around a native widget, each fragment's header names the other and what sits between them
- [ ] Last line of the `check-block.py` output pasted under Check result
