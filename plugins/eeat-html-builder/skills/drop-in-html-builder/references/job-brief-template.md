# Job Brief -- YMYL/EEAT HTML Content Block

Paste this at the start of every new job in this project. Fill in every field before sending. The more accurate this is upfront, the less back-and-forth during the build.

If the client has no fact sheet in `references/clients/` yet, Claude will also ask the questions in `references/fact-sheet-questions.md` before building. Answering them once creates the sheet, so later jobs for that client skip them.

---

## Client and page context

**Client name:**
**Practice area / page topic:**
**URL of the page being updated:** *(paste the live URL; Claude will read its computed styles and find its colour tokens before building)*
**CMS / page builder:** *(e.g. WordPress + Elementor, Webflow, WordPress + Gutenberg, custom)*
**Sitemap URL:** *(usually /sitemap_index.xml — needed for internal linking)*

---

## Reference page

**URL of an existing page on the same site that looks correct:**
*(Claude will read rendered typography, heading weights, link colours and component styles from it, probe what a bare element gets in its content column, and find the site's global colour tokens. Without this, the first build is guessing.)*

---

## What we are building

**Scope:**
- [ ] Full page replacement — the entire content area is being replaced
- [ ] Content block drop-in — sits inside an existing page layout, within the content area only
- [ ] New standalone page — no existing page to match, but must fit the site's global styles

**Where does the block sit in the page?**
*(e.g. below the hero, replacing the main body copy, above the footer CTA)*

**Contact form / CTA destination:**
*(phone number, contact page URL, or anchor ID — Claude will verify the anchor exists in the DOM before using it)*

**Content the client will change themselves after launch:**
*(fees, opening hours, dated statistics, rotating testimonials, anything updated without a designer. This goes in a native widget, not the block, and the block is split around it. Leave blank if none.)*

**Who supports this page after launch?**
*(name or team; the handover header is written for them)*

---

## Content source

**Format of the content I am providing:**
- [ ] Word document (.docx)
- [ ] PDF
- [ ] Plain text / notes in this message
- [ ] Existing page copy (pull from the live URL)

**Content attached:** *(confirm yes/no — attach the file to this message)*

---

## Known constraints

**Any CSS conflicts or theme issues to be aware of?**
*(e.g. Elementor overrides button styles, theme injects bullets onto li elements, page builder wraps content in a fixed-width container)*

**Any sections that must or must not be included?**
*(e.g. client has asked for a process section, no pricing tables, must include Law Society number)*

**Are there any trust/credential signals to include?**
*(e.g. Law Society accreditations, years established, named solicitor credentials, client testimonials)*

**CSS delivery:**
- [ ] Stylesheet — two files: the HTML fragment with no `<style>`, plus a `.css` file the developer adds to the child theme stylesheet or the CMS custom-CSS area. Default when a developer handles insertion; one place to maintain.
- [ ] Inline — one file with the `<style>` inside the fragment. Use when nobody has stylesheet access or the client pastes the block themselves.

---

## Style matching

**Brand colours (if known):**
- Primary:
- Secondary / dark:
- Accent (if any):

**Does the site maintain global colour tokens?** *(Elementor global colours, theme.json presets, or designer variables. Leave blank if unknown; Claude will check and record what it finds in the handover. Note: a `var()` fallback value is not a contrast safeguard — it only renders while the token is undefined, so any AA check must be against the token's live resolved value.)*

**Any explicit fonts in use?** *(if known — leave blank if to be extracted from the live site)*

**Are icon libraries already loaded on the site?** *(e.g. Font Awesome — if unknown, Claude will use inline SVG or plain-text icons only)*

---

## Notes

*(Anything else relevant — e.g. priority page for a Google update recovery, client has approved specific copy, a developer will handle CMS insertion, page has an unusual layout)*
