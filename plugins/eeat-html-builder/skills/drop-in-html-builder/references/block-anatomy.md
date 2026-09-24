# Block anatomy

The shape every drop-in block takes, so that a support developer who has never seen it can find any section, any colour and any editable value in under two minutes. `scripts/check-block.py` enforces the parts of this that can be checked mechanically.

## File order (fixed)

1. Header comment: the handover (template below).
2. The CSS, in this internal order, each part introduced by a `/* [n] NAME */` comment. Inline delivery: one `<style>` block here. Stylesheet delivery: the same CSS in a companion `<slug>.css`, and no `<style>` in the fragment (see "CSS delivery" below):
   - Tokens: the bare `#root { --prefix-role: ...; }` rule and nothing else in it
   - Base: root typography and layout that differ from the container probe
   - Components: buttons, cards, steps, details/summary, bands
   - Sections: rules specific to one section, in page order, numbered to match the HTML markers
   - Responsive: `@media` blocks last, every selector still starting with the root id
3. JSON-LD `<script type="application/ld+json">` blocks.
4. One root `<div id="prefix-page">` and nothing else at the top level.

## Root id and prefix

Root id: client prefix, then page slug, for example `#wc-divorce-separation`, `#ln-road-traffic`. Unique on the page. Every selector starts with it. Every custom property and every class starts with the same prefix (`--wc-`, `.wc-`).

## CSS delivery

The brief chooses one of two shapes. The CSS itself is identical in both.

- **Stylesheet** (default when a developer handles insertion): `<slug>.html` holds the header, JSON-LD and the root `<div>`, with no `<style>`. `<slug>.css` holds the header as a `/* */` comment followed by the CSS in the order above. The developer adds the `.css` to the child theme stylesheet or the CMS custom-CSS area and pastes the fragment into the HTML widget. One stylesheet edit then reaches every page that uses the block's prefix.
- **Inline** (nobody has stylesheet access, or the client pastes the block themselves): one `<slug>.html` with the `<style>` block in position 2.

Both headers carry a `CSS` line: the fragment's names the stylesheet file and where it goes; the stylesheet's names the fragment. `check-block.py` takes the pair (`check-block.py <slug>.html <slug>.css`, or finds a same-stem `.css` itself) and fails a fragment that has neither a `<style>` nor a companion file, or both.

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

No colour literal appears anywhere else in the CSS except as a `var()` fallback, pure white, pure black or a shadow. A `var()` fallback is not a contrast safeguard: it only ever renders while the token is undefined, so any AA check must be run against the token's live resolved value, not the fallback.

## Section comment format

Opener and closer, both mandatory. Number, name in capitals, the CSS hook a developer greps for, one optional note.

    <!-- [3] STEP-BY-STEP GUIDE | .wc-steps | HowTo schema mirrors these step names -->
      ...
    <!-- /[3] STEP-BY-STEP GUIDE -->

The `<style>` block uses `/* [3] STEP-BY-STEP GUIDE */` for the matching rules.

Section headings themselves (the visible `<h2>`/`<h3>` text, not this comment marker) come from the client's copy or the practice area, never from a stock template. "Step-by-Step Guide to [X]", "Why Choose [Firm]?" and "Frequently Asked Questions About [X]" are banned as defaults — see `references/pattern-log.md` for why.

## Editable hotspots

Mark every value a client is likely to ask for by ticket with an `EDIT:` comment on the line above it, and list every marker in the header's Edit index.

    <!-- EDIT: phone number. CallRail swaps it on render; keep it static here. -->
    <a href="tel:02078702736">020 7870 2736</a>

    <!-- EDIT: enquiry CTA destination. Full URL, not an anchor (no stable form id on /contact/). -->
    <a class="ln-btn" href="https://www.example.co.uk/contact/">Speak to a solicitor</a>

Mark: phone numbers, CTA hrefs, placeholder links, solicitor names and roles, SRA number, any date or figure.

HTML comments ship to production and are visible to anyone who views source. Never put a backup file path, a server path, a staging URL with credentials, or any other access detail in the header or anywhere else in the file.

## Default content order

The output order of the content-structuring prompt, with the first CTA after the lead paragraph (standard 8):

1. Intro (H2 if the page title supplies the H1; H1 only for a full-page replacement)
2. First CTA
3. Key points
4. Process or steps, where the source supports one
5. Topic sections, in the order the source document gives them
6. FAQ, where the source supports one
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

Never write tag syntax (anything in angle brackets) inside the header or any other comment. Server-side minifiers such as LiteSpeed Cache read a `<style>` or `<script>` written inside a comment as a real tag and delete everything up to the next real closing tag for logged-out visitors. Name tags in words instead: "a style block", "html, head or body tags". `check-block.py` fails on it.

    <!--
      BLOCK        Wright & Crawford: divorce and separation (drop-in content block)
      Root id      #wc-divorce-separation   Prefix --wc- / .wc-
      File         wright-crawford--divorce-and-separation.html
      CSS          wright-crawford--divorce-and-separation.css, stylesheet delivery: add to the child theme style.css
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
        wrap this in html, head or body tags; it is a fragment
        move the CSS into the theme without keeping the #wc-divorce-separation prefix on every selector
        add @import or @font-face; the site loads the fonts
        add a form or button element inside the block; use a native widget and split the block
        put a backup path, server path or staging credential in this header

      SECTIONS     [1] INTRO  [2] KEY POINTS  [3] STEP-BY-STEP GUIDE  [4] FINANCIAL SETTLEMENTS
                   [5] SEPARATION AGREEMENTS  [6] CHILD ARRANGEMENTS  [7] ALTERNATIVES TO COURT
                   [8] FAQ  [9] CONTACT BAND
                   Deviation from default order: trust signals folded into [2]; closing CTA is [9].

      CHECK        PASS: 0 fail, 0 warn (wright-crawford--divorce-and-separation.html)
    -->

The example values above are illustrative of the format only; every build fills the header from its own verified data.
