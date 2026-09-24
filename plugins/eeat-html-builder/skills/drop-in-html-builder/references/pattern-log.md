# Pattern log

One line per build: the distinctive structural and component devices it used, so the next build can check it isn't repeating the last two. This is what stops three unrelated clients' pages reading as one developer's work even though each one correctly matches its own site's colours.

Rule: before structuring a new build, read the last two entries below. Do not repeat a device either of them used unless the client's own site already uses that device (then it's the site's pattern, not a habit — note why).

Log a new line here after every build, before handover.

| Date | Client / page | Section skeleton | Disclosure treatment | Distinctive components |
|---|---|---|---|---|
| 2026 | mshblegal.com — divorce page | Intro > step-by-step guide (7-8 steps) > "Why Choose [Firm]?" card grid > FAQ (7-9 items) > contact | Chevron accordion (rotating `::after`, ~18px summary padding) | Numbered circle step markers, left-accent-border panels, uppercase eyebrow labels, card grid with box-shadow |
| 2026 | richardsilver.co.uk — totting-up page | Intro > step-by-step guide (7-8 steps) > "Why Choose [Firm]?" card grid > FAQ (7-9 items) > contact | Chevron accordion (rotating `::after`, ~18px summary padding) | Numbered circle step markers, left-accent-border panels, uppercase eyebrow labels, card grid with box-shadow |
| 2026 | Balfour & Manson — buying/selling page | Intro > step-by-step guide (7-8 steps) > "Why Choose [Firm]?" card grid > FAQ (7-9 items) > contact | Chevron accordion (rotating `::after`, ~18px summary padding) | Numbered circle step markers, left-accent-border panels, uppercase eyebrow labels, card grid with box-shadow |
| 24 Sep 2026 | completeclaritysolicitors.com — /property/ conveyancing | Lead panel with CTAs and jump links > service card grid > explanatory H2 sections > costs with CTA > profile > buying steps (9) > selling steps (9) > FAQ (7) > navy CTA panel | Chevron accordion (rotating `::after`) | Numbered circle step markers with connector line, left-accent lead panel, top-border card grid, check-mark list, profile card. Built on plugin v0.1.0; repeats the flagged devices. Now the client's shared component set (see sheet) |
| 24 Sep 2026 | completeclaritysolicitors.com — transfer of title | Same shared skeleton as /property/: lead panel > H2 sections > check-mark lists > steps (7) > costs with CTA > profile > FAQ (6) > navy CTA panel | Chevron accordion (shared stylesheet) | Same shared `ccsp-` components; consistent within the client by design. Next build for a different client must not repeat any of them |

The first three rows (MSHB, Richard Silver, Balfour & Manson) are the fault this file exists to fix: same skeleton, same disclosure widget, same component shapes, three different clients, only the site's own colours changed. The next build must not repeat the disclosure treatment or the component shapes above unless the client's own site already uses that specific device — check the component inventory (`screenshot-style-extraction.md`) first.
