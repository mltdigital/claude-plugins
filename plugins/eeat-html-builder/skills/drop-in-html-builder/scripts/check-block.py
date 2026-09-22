#!/usr/bin/env python3
"""check-block.py: pre-handover regression guard for drop-in HTML fragments.

Usage: python3 check-block.py <fragment.html> [--strict]
Exit 1 on any FAIL. --strict also turns WARN into FAIL.
Stdlib only. Run it on the output file before every handover.

The CSS walker is a simple brace-depth parser: it does not understand CSS
nesting (a selector inside another selector's body) or :is()/:where(), and
both would otherwise be silently mis-parsed (nesting read as declarations,
:is()/:where() commas read as selector-list separators). Both are FAILs.
Flatten nested rules and write out :is()/:where() as an explicit selector
list before running this script.
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
        # Unsupported syntax this checker cannot walk safely: fail loudly
        # instead of silently mis-parsing (nested rules read as declarations,
        # :is()/:where() commas read as selector-list separators).
        if re.search(r"[{}]", rbody):
            F("CSS nesting is not supported by this checker: '%s' contains a "
              "nested rule%s. Flatten it to a top-level selector."
              % (sel.strip(), " in " + " ".join(ctx) if ctx else ""))
            continue
        if re.search(r":(?:is|where)\(", sel, re.I):
            F("':is()'/':where()' is not supported by this checker: '%s'%s. "
              "Write out the selector list explicitly instead."
              % (sel.strip(), " in " + " ".join(ctx) if ctx else ""))
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
