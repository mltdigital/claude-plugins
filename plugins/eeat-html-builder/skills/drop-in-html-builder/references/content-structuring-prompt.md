# Content Structuring -- Standing Prompt

Use this prompt when you have a Word document, PDF, or set of written recommendations to convert into structured page content. Attach the file and paste this prompt. The output is clean, structured text ready to populate the HTML build -- it is not a formatted document, not a report, and not a Word file.

---

## Prompt to paste (with content file attached)

I am building a styled HTML content block for a law firm website page. The attached document contains the content and/or recommendations for this page. Please extract and restructure the content into the sections below.

Work strictly from what is in the document. Do not invent content, add generic filler, or expand on points beyond what is written. If a section has no relevant content in the document, mark it as "Not provided" rather than writing something generic.

Write in plain, confident British English. No jargon, no passive voice, no filler phrases. This is legal sector content on a YMYL page so accuracy and tone matter -- do not rewrite substantively, just reorganise and tighten.

---

### Output sections required

**1. Page headline (H1)**
One clear, specific headline for the page. Should reflect the practice area and be written for a user who has just arrived from a search. Not a slogan.

**2. Lead paragraph**
Two to three sentences maximum. What this page covers, who it is for, and what the firm offers in this area. No fluff.

**3. Key points / what clients need to know**
A set of three to six standalone points that answer the most common questions or concerns a user arriving on this page would have. Each point should have a short heading and two to three sentences of explanation. Do not pad. Title the section from the content, not the stock "Why Choose [Firm]?".

**4. Process or steps (if applicable)**
If the document describes a process, journey, or timeline (e.g. how a case works, what happens after first contact), extract it as a numbered sequence. Short label per step and one to two sentences of explanation. Skip this section if there is no process content. Title the section from what it actually covers, not the stock "Step-by-Step Guide to [X]".

**5. FAQ**
Extract any questions and answers present in the document, where the document supports them. Do not convert prose into invented questions and do not aim for a target count -- the number of questions is whatever the source document actually contains. Questions should be written as a user would actually ask them, not headings rewritten as questions. A plain "FAQ" or "Questions and answers" heading is fine; skip the stock "Frequently Asked Questions About [X]".

**6. Credentials and trust signals**
Any specific credentials, accreditations, years of experience, named solicitors, case outcomes, or other trust signals mentioned in the document. List them as-is -- do not embellish.

**7. CTA text**
Extract the CTA wording from the document if it specifies one. If it doesn't, mark this "Not provided" -- do not write CTA copy here. CTA wording is a client-facing decision, not something to draft during content structuring.

---

## After you get the output

Review each section before building. Check:
- Nothing has been invented or padded
- FAQ questions sound like real user queries, not headings rewritten as questions
- Trust signals are specific (a generic "experienced team" is not a trust signal)

Then use this structured output as the content input for the HTML build prompt.
