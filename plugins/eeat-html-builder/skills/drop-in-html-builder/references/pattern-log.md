# Pattern log

One line per build: the distinctive structural and component devices it used, so the next build can check it isn't repeating the last two. This is what stops three unrelated clients' pages reading as one developer's work even though each one correctly matches its own site's colours.

Rule: before structuring a new build, read the last two entries below. Do not repeat a device either of them used unless the client's own site already uses that device (then it's the site's pattern, not a habit — note why).

Log a new line here after every build, before handover.

| Date | Client / page | Section skeleton | Disclosure treatment | Distinctive components |
|---|---|---|---|---|
| 2026 | mshblegal.com — divorce page | Intro > step-by-step guide (7-8 steps) > "Why Choose [Firm]?" card grid > FAQ (7-9 items) > contact | Chevron accordion (rotating `::after`, ~18px summary padding) | Numbered circle step markers, left-accent-border panels, uppercase eyebrow labels, card grid with box-shadow |
| 2026 | richardsilver.co.uk — totting-up page | Intro > step-by-step guide (7-8 steps) > "Why Choose [Firm]?" card grid > FAQ (7-9 items) > contact | Chevron accordion (rotating `::after`, ~18px summary padding) | Numbered circle step markers, left-accent-border panels, uppercase eyebrow labels, card grid with box-shadow |
| 2026 | Balfour & Manson — buying/selling page | Intro > step-by-step guide (7-8 steps) > "Why Choose [Firm]?" card grid > FAQ (7-9 items) > contact | Chevron accordion (rotating `::after`, ~18px summary padding) | Numbered circle step markers, left-accent-border panels, uppercase eyebrow labels, card grid with box-shadow |

The three rows above are the fault this file exists to fix: same skeleton, same disclosure widget, same component shapes, three different clients, only the site's own colours changed. The next build must not repeat the disclosure treatment or the component shapes above unless the client's own site already uses that specific device — check the component inventory (`screenshot-style-extraction.md`) first.
