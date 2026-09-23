# CMS override patterns

Hard-won technical patterns for building drop-in blocks that hold their styling when inserted into WordPress + Elementor (Hello theme or similar). Many apply to other CMS/page-builder combinations too.

**Scoping: use ID selectors, not class selectors.**
Scope all CSS to a unique ID (`#block-name`) rather than a class (`.block-name`). ID specificity beats almost any theme selector without needing `!important` everywhere. Pick a unique ID per client/page — no collisions.

**Why:** Class-scoped blocks still lose to Elementor widget selectors in some contexts. ID scoping solved the problem cleanly on the MSHB settlement agreements page.

**FAQs: use `<details>/<summary>`, not `<button>` + JS.**
Native `<details>/<summary>` elements need no JavaScript, no button elements, and are immune to Elementor's button style injection.

Disclosure treatments are a set, not a default — pick one from the reference site's own component inventory (`screenshot-style-extraction.md`), not automatically the chevron below. If the site already uses a chevron accordion somewhere, match it. If it doesn't, prefer plus/minus, a restyled native `::marker`, no icon at all, or (where the site has no accordion anywhere) plain heading-and-paragraph FAQ with no disclosure widget.

Chevron, drawn with a CSS border trick (not a background-image SVG, which Elementor can also override):

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

`currentColor` makes the chevron follow the summary's text colour, which is itself a block token, so there is one colour to change rather than three.

Plus/minus, as an alternative that reads less like a template default:

```css
#block summary::after { content: '+'; font-weight: 700; }
#block details[open] summary::after { content: '\2212'; }
```

Restyled native marker, where the site's own disclosure pattern (if any) is closer to a plain triangle:

```css
#block summary { list-style: none; }
#block summary::marker { content: none; }
#block summary::before { content: '\25B8'; display: inline-block; transition: transform .15s; }
#block details[open] summary::before { transform: rotate(90deg); }
```

**Why:** Elementor injects high-specificity styles onto `<button>` elements (background, border, color, font). `<details>/<summary>` sidesteps this entirely. Treating the icon as a menu rather than a fixed snippet is what stops every build defaulting to the same chevron regardless of client (see `references/pattern-log.md`).

**Decorative link lists: avoid `<ul>/<li>`.**
WordPress/Elementor themes inject their own `li::before` pseudo-elements (dots, dashes, custom icons). These cannot be reliably overridden without `!important` on every property. Instead, use a CSS grid of plain `<a>` tags inside a `<div>`. Put decorative arrows (→) as plain text inside the `<a>` — not as `::before` content.

```html
<div class="links-grid">
  <a href="...">→ Link text</a>
  <a href="...">→ Link text</a>
</div>
```

**Why:** Three separate attempts to fix `li::before` dots with CSS failed. Removing `<li>` entirely solved it in one change.

**Kit values are unreliable. Kit tokens are the colour source.**
Elementor global kit CSS (set in Theme Style) is routinely overridden at widget level, so never read a kit variable's value to predict what the reference page looks like. Always verify computed styles on the rendered page (Rule 3).

But a widget overriding `color` does not change the variable. Elementor declares `--e-global-color-*` on `<body>` through the kit class, custom properties inherit, and the block is not a widget: `var(--e-global-color-primary)` inside an HTML widget resolves to the kit value regardless of what any Heading widget on the page does. So once you know the rendered colour, cite the site token that carries it, with the verified value as fallback (Rule 9) — provided the reference page's own CSS actually references that token (see the confirmation step below), not merely a variable that happens to resolve to the same value:

    --wc-brand: var(--e-global-color-primary, #3D093D);

**Decision table (per property):**

| Property group | Default | Hard-code when |
|---|---|---|
| Body and heading font family | Inherit: declare nothing | Probe (below) shows the container gives a different family from the reference page |
| Font size, weight, line-height, letter-spacing, text-align | Hard-code the verified value where it differs from the probe | Always permitted: these are the widget-overridden properties |
| Brand, secondary, accent; link colour; button fill and border; band and card backgrounds; borders | `var(--site-token, #verified)` | No token; token value differs from what renders; the reference page's CSS doesn't actually cite the token; AA failure |
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

Then confirm the token is actually the source, not a coincidence — two unrelated tokens can resolve to the same hex. Fetch the page's own CSS (e.g. `curl -L <reference page URL>` and its linked Elementor/theme stylesheets, following redirects and noting the final URL) and grep it for the property in question citing that token:

    grep -o "color:[^;]*var(--e-global-color-[a-z0-9-]*" elementor-kit.css

Token cited on the property, and value equal: cite the token. Either fails: the site's designer is not maintaining it, or something else supplies the colour; hard-code and note it in the handover.

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

**Anchor IDs: inspect the DOM, never assume.**
Contact Form 7 wrapper IDs are auto-generated as `wpcf7-f{form_id}-p{post_id}-o{instance}` and change per page. Elementor section IDs may not exist at all unless explicitly set. Always use the Claude in Chrome JavaScript tool to query the DOM before writing any `href="#anchor"` link.

```javascript
document.querySelectorAll('[id]') // lists all elements with an ID on the page
```

If the anchor doesn't exist, link to the full page URL and add a comment explaining why.

**`!important` strategy: targeted, not blanket.**
Use `!important` only on properties that are actually being overridden — typically `color`, `background-color`, `text-decoration`, `display` on interactive elements. Blanket `!important` on every property creates its own specificity debt and makes future overrides harder.

**Content area width.**
Content width is a property of the page template, not the site, so never assume a figure and never reuse one from another page. A service page with no sidebar and a blog single with a sidebar on the same site can differ by several hundred pixels. Measure it on the actual target page, on the element the block will be inserted into, not on `main` or `body`, which may span the sidebar too. In the JavaScript tool, select the insertion container (for Elementor, usually the `.elementor-widget-container` or column the HTML widget sits in; for Gutenberg, `.entry-content`) and read `getBoundingClientRect().width`. Also note whether a sidebar is present. Build and preview at that width, record it with the template name and sidebar status in the handover header, and add it to the client fact sheet as a per-template entry. If the reference page uses a different template from the target, use the target's width for layout and the reference for styling only. Components that look correct at full width often break at content-area width.

**Fetching reference pages.**
Use `curl -L` (follow redirects) when fetching a reference page or its stylesheets, and report the final URL you landed on — law firm sites redirect www/non-www, http/https and trailing slashes often enough that the URL you were given and the URL you fetched can differ.

**Test CSS at component level, not just block level.**
When a style isn't applying, check whether the theme has a more specific selector on the same element. Use Chrome DevTools (or the JS tool) to inspect computed styles and identify which rule is winning.
