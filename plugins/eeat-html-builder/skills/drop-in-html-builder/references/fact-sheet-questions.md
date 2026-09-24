# Fact sheet questions

Use this when Step 1 finds no fact sheet for the named client, or finds a sheet
with gaps that matter to this build. These are the facts only a person can
supply. Everything the live site can prove (fonts, colours, widths, URLs, form
anchors, existing schema) is verified during the build instead, and is never
asked.

## How to ask

- Ask in one message, numbered, before any build work starts. Do not spread the
  questions across the conversation.
- For an existing sheet, ask only the questions whose field is missing or marked
  "not yet captured" (person-supplied fields only). Do not re-ask what the sheet already records.
- Every question accepts "don't know". Record that answer as "not yet captured"
  and move on; do not guess and do not block the build on it.
- Where a question can be answered by checking a system you have access to (for
  example a call-tracking connector), check it and state the answer instead of
  asking.
- If nobody is there to answer (a scheduled or unattended run), create the sheet
  with every human-supplied field marked "not yet captured", say so at the top of
  the handover, and carry on.

## The questions

Each question names the `_template.md` field it fills. Gaps in fields the live
site can prove (tokens, widths, URLs, anchors, schema actually present) are
filled by verification in Steps 2 and 4, never by asking.

1. **Client identity.** Full firm name, website domain, jurisdiction (England and
   Wales, Scotland, Northern Ireland), main practice areas, and office locations. *(Fills: first line.)*

2. **CMS access and CSS delivery.** Which CMS and page builder the site runs on, who
   inserts blocks (MLT, the client, a third-party developer), and where shared CSS
   should live: child theme stylesheet, Customiser Additional CSS, Elementor Custom
   CSS, or inline in each block. *(Fills: CMS; CSS delivery and shared components.)*

3. **Shared components.** Should this client's pages share one stylesheet and one
   set of class names across pages, or should each block be self-contained? If
   shared, is there an existing stylesheet or class prefix to reuse? *(Fills: CSS delivery and shared components; Client-specific rules.)*

4. **Call tracking.** Which provider (CallRail, Infinity, none), which numbers are
   swap targets, and which number should be hardcoded in content. *(Fills: Phone.)*

5. **Enquiry route.** Where CTAs should send people: a contact page, a form on the
   page itself, or a booking tool. Any wording the client insists on or bans
   (for example "free consultation" or "we do not provide Legal Aid"). *(Fills: Contact form / CTA destination; Required or banned wording.)*

6. **Schema ownership.** Does an SEO plugin (Yoast, Rank Math), a hand-written
   JSON-LD widget, or a template (such as an ACF FAQ block) already output schema
   on service pages? "Don't know" is fine; the build checks the live page anyway. *(Fills: Schema ownership.)*

7. **Authorship and trust.** Named solicitors to cite, their exact job titles,
   accreditations, regulator numbers (SRA or Law Society of Scotland), awards and
   review platforms the client is happy to reference. Use only what the client
   supplies or has published. *(Fills: Authorship / EEAT targets.)*

8. **After launch.** Content the client edits themselves (fees, hours, statistics)
   and who supports the pages after launch, so the handover header is written for
   them. *(Fills: After launch.)*

## After the answers

1. Copy `references/clients/_template.md` to `<client-slug>.md` (saved as step 5
   says) and fill it from the answers. Fields the site will prove stay "to verify this
   build" until Step 2 and Step 4 have measured them.
2. Build.
3. Before handover, fill every "to verify this build" field from what was
   measured, add the build to the Builds line, and change anything still unknown
   to "not yet captured".
4. Add the client to the "Client facts" list in `SKILL.md` and to the trigger
   list in its front matter, in the same copy you save the sheet to.
5. Save the sheet. The installed plugin is a read-only synced copy, so a sheet
   written only inside it is lost. If you are working in a clone of the plugins
   repository, write it at
   `plugins/eeat-html-builder/skills/drop-in-html-builder/references/clients/<client-slug>.md`.
   Otherwise save it to the user's working folder and tell them in one line that
   it only reaches the team once it is committed to that path and the plugin
   version is bumped.

