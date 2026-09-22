# Screenshot Style Extraction -- Standing Prompt

Use this prompt whenever you have a screenshot of the client's existing page (taken via the Chrome extension). Paste this prompt and attach the screenshot. The output becomes your style reference for the build -- do not start writing HTML until this has been completed.

---

## Prompt to paste (with screenshot attached)

Please analyse this screenshot of the client's existing webpage and extract a complete style reference. I need this to ensure the HTML block I am building matches the existing site visually. Cover every section below.

### 1. Colours

- Primary / brand colour (buttons, links, accents):
- Background colour (main content area):
- Secondary background (cards, callout boxes, alternating sections):
- Heading text colour:
- Body text colour:
- Border / divider colour:
- Any additional colours in use:

Give hex values where you can infer them confidently, or describe the tone clearly if not.

### 2. Typography

- Heading font (H1, H2): name if identifiable, otherwise describe the style (serif, sans-serif, weight, letter spacing)
- Body copy font: same
- Approximate heading sizes relative to body (e.g. H2 is roughly 1.5x body)
- Line height / paragraph spacing: tight, normal, or generous
- Any notable typographic treatments (uppercase headings, tracked-out labels, etc.)

### 3. Spacing and layout

- Content area max width (approximate):
- Paragraph spacing (tight/normal/generous):
- Section padding (how much vertical breathing room between sections):
- Is the layout single column, or does it use a sidebar?

### 4. Component inventory

List what the site actually has. This inventory is what the block is allowed to reuse — it does not import a component shape the site doesn't already use, even if that shape is a common pattern elsewhere.

- Accordion / expandable items: present or not; if present, how is it styled (icon, rotation, padding)? If the site has no accordion anywhere, the FAQ is built as plain headings and paragraphs, not a `<details>` accordion borrowed from habit.
- List markers: bullets, numbers, custom icons, or none
- Cards or panels: border style, shadow, radius, background, accent border (and on which side, if any)
- Buttons: shape (pill/rounded/square), fill style (solid/ghost/underlined), hover state if visible
- Heading devices: uppercase eyebrows, numbered/circle markers, underlines, rules under headings
- Horizontal rules or dividers: visible, or purely whitespace separation
- Icons: library in use if identifiable, or style (outline/filled/illustrated)

Keep this to what's actually on the page. This is a five-minute pass, not a redesign brief: check `references/pattern-log.md` afterwards so the block doesn't also repeat the last two builds' component shapes where the site doesn't call for them.

### 5. Trust and credential signals

- How are accreditations or logos displayed (inline, footer strip, sidebar)
- Are solicitor names or credentials shown, and in what format
- Are testimonials or reviews present, and how are they laid out

### 6. Overall impression

- One sentence describing the design direction (e.g. "clean corporate serif with generous whitespace and muted navy/grey palette")
- Anything unusual or distinctive about the styling that I should preserve or be aware of

---

## After you get the output

Save the style reference as a note or paste it into your build message. Reference it explicitly when prompting the build -- e.g. "using the style reference above, build the content block."

If anything is ambiguous from the screenshot (e.g. a colour is unclear, a font is unidentifiable), flag it before starting the build rather than guessing.
