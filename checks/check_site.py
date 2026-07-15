#!/usr/bin/env python3
"""croft.ing site checks — standing regression net.

Python 3 standard library only. No third-party dependencies, matching the
site's own no-dependency stance. Run from anywhere:

    python3 checks/check_site.py

Exits nonzero if any check fails, printing every failure. This is the
regression net RUN-01 lacked: it covers the whole site (index, pillar pages,
library, and the RUN-02 guide pages) and is meant to stay honest — the NEW
assertions are written before the pages exist, so they fail first (RED) and
pass once the pages are built (GREEN).
"""

import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FAILURES = []
CHECKS_RUN = 0


def fail(msg):
    FAILURES.append(msg)


def check(msg, condition):
    """Record one assertion. Truthy condition passes; falsy fails with msg."""
    global CHECKS_RUN
    CHECKS_RUN += 1
    if not condition:
        fail(msg)
    return bool(condition)


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def html_files():
    found = []
    for dirpath, _dirs, files in os.walk(ROOT):
        if os.path.join(ROOT, ".git") in dirpath:
            continue
        for name in files:
            if name.endswith(".html"):
                found.append(os.path.join(dirpath, name))
    return sorted(found)


def relpath(path):
    return os.path.relpath(path, ROOT)


# ---- Small HTML helpers -----------------------------------------------------

class TierLabelParser(HTMLParser):
    """Collect the text of every <span class="tier-label">…</span> in order."""

    def __init__(self):
        super().__init__()
        self.labels = []
        self._capture = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            cls = dict(attrs).get("class", "")
            if "tier-label" in cls.split():
                self._capture = True
                self._buf = []

    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "span" and self._capture:
            self._capture = False
            self.labels.append("".join(self._buf).strip())


def tier_labels(html):
    parser = TierLabelParser()
    parser.feed(html)
    return parser.labels


def strip_tags(html):
    return re.sub(r"<[^>]+>", "", html)


def is_subsequence(needles, haystack):
    """True if needles appear in haystack in order (not necessarily adjacent)."""
    it = iter(haystack)
    return all(any(n == h for h in it) for n in needles)


# ---- Checks -----------------------------------------------------------------

def check_no_scripts(files):
    for path in files:
        if re.search(r"<script\b", read(path), re.IGNORECASE):
            fail("script tag found in %s" % relpath(path))
    check("no <script> tags in any HTML file", not any(
        re.search(r"<script\b", read(p), re.IGNORECASE) for p in files))


def check_cname():
    path = os.path.join(ROOT, "CNAME")
    check("CNAME exists", os.path.exists(path))
    if os.path.exists(path):
        check("CNAME is exactly 'croft.ing'", read(path).strip() == "croft.ing")


def resolve_ref(ref, from_file):
    """Resolve an internal href/src to a filesystem path, or None to skip."""
    ref = ref.split("#", 1)[0].split("?", 1)[0]
    if not ref:
        return None
    if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
        return None
    if ref.startswith("/"):
        target = os.path.normpath(os.path.join(ROOT, ref.lstrip("/")))
    else:
        target = os.path.normpath(os.path.join(os.path.dirname(from_file), ref))
    if ref.endswith("/") or os.path.isdir(target):
        target = os.path.join(target, "index.html")
    return target


def check_internal_refs(files):
    ok = True
    # href/src in HTML.
    for path in files:
        html = read(path)
        for attr in ("href", "src"):
            for m in re.finditer(attr + r'="([^"]*)"', html):
                target = resolve_ref(m.group(1), path)
                if target is None:
                    continue
                if not os.path.exists(target):
                    ok = False
                    fail("broken internal reference %r in %s -> %s"
                         % (m.group(1), relpath(path), relpath(target)))
    # url(...) in CSS, skipping data: URIs.
    css_path = os.path.join(ROOT, "styles.css")
    if os.path.exists(css_path):
        css = read(css_path)
        for m in re.finditer(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', css):
            val = m.group(1).strip()
            if val.startswith("data:"):
                continue
            target = resolve_ref(val, css_path)
            if target and not os.path.exists(target):
                ok = False
                fail("broken CSS url() reference %r -> %s"
                     % (val, relpath(target)))
    check("every internal href/asset reference resolves to a file", ok)


ALLOWED_HOSTS = {
    "arecipe.app",
    "arecipe.croft.ing",
    "skylite.croft.ing",
    "recipe.exchange",
}


def external_url_allowed(url):
    rest = url.split("://", 1)[1]
    host = rest.split("/", 1)[0].lower()
    path = "/" + rest.split("/", 1)[1] if "/" in rest else "/"
    if host == "www.w3.org" and path.startswith("/2000/svg"):
        return True  # SVG namespace inside CSS data URIs
    if host == "github.com" and path.startswith("/CroftCommunity"):
        return True
    if host in ALLOWED_HOSTS:
        return True
    return False


def check_external_allowlist(files):
    ok = True
    scan = list(files)
    css_path = os.path.join(ROOT, "styles.css")
    if os.path.exists(css_path):
        scan.append(css_path)
    for path in scan:
        for m in re.finditer(r'https?://[^\s"\'<>)]+', read(path)):
            url = m.group(0)
            if not external_url_allowed(url):
                ok = False
                fail("external URL not on allowlist: %s (in %s)"
                     % (url, relpath(path)))
    check("external URLs limited to the allowlist", ok)


def check_pillar_tiers_and_sync():
    expected = ["The Signpost", "The Surface", "The Soil", "The Bedrock"]
    index = read(os.path.join(ROOT, "index.html"))

    # Extract each landing-page pillar: name, signpost (lede), surface (plain <p>).
    pillars = {}
    for block in re.findall(
            r'<article class="pillar">(.*?)</article>', index, re.DOTALL):
        name = re.search(r"<h2>(.*?)</h2>", block)
        lede = re.search(r'<p class="lede">(.*?)</p>', block, re.DOTALL)
        surface = re.search(r"<p>(.*?)</p>", block, re.DOTALL)
        if name and lede and surface:
            pillars[name.group(1).strip()] = (
                lede.group(1).strip(), surface.group(1).strip())

    for filename, name in (("plot.html", "The Plot"),
                           ("wall.html", "The Wall"),
                           ("valley.html", "The Valley")):
        html = read(os.path.join(ROOT, filename))
        check("%s shows the four tier labels in order" % filename,
              tier_labels(html) == expected)
        page_signpost = re.search(r'<p class="lede">(.*?)</p>', html, re.DOTALL)
        page_surface = re.search(r'<p class="surface">(.*?)</p>', html, re.DOTALL)
        idx = pillars.get(name)
        check("%s Signpost matches index.html" % filename,
              bool(page_signpost) and bool(idx)
              and page_signpost.group(1).strip() == idx[0])
        check("%s Surface matches index.html" % filename,
              bool(page_surface) and bool(idx)
              and page_surface.group(1).strip() == idx[1])


def check_new_pages():
    # arecipe/index.html
    arecipe_path = os.path.join(ROOT, "arecipe", "index.html")
    if check("arecipe/index.html exists", os.path.exists(arecipe_path)):
        html = read(arecipe_path)
        labels = tier_labels(html)
        check("arecipe page has THE SIGNPOST, THE SURFACE, THE BEDROCK in order",
              is_subsequence(["THE SIGNPOST", "THE SURFACE", "THE BEDROCK"], labels))
        text = strip_tags(html)
        check("arecipe page contains 'A shared community recipe box.'",
              "A shared community recipe box." in text)
        check("arecipe page contains the Amanda tagline",
              "arecipe: the a is for Amanda" in text)

    # skylite/index.html
    skylite_path = os.path.join(ROOT, "skylite", "index.html")
    if check("skylite/index.html exists", os.path.exists(skylite_path)):
        html = read(skylite_path)
        labels = tier_labels(html)
        check("skylite page has THE SIGNPOST, THE SURFACE, THE BEDROCK in order",
              is_subsequence(["THE SIGNPOST", "THE SURFACE", "THE BEDROCK"], labels))
        text = strip_tags(html)
        check("skylite page contains the butterfly-garden signpost",
              "A tended window into the butterfly garden of Bluesky." in text)

    # index.html growing section mentions Skylite
    index = read(os.path.join(ROOT, "index.html"))
    growing = re.search(r'id="growing".*?</section>', index, re.DOTALL)
    check("index.html growing section contains 'Skylite'",
          bool(growing) and "Skylite" in growing.group(0))


def main():
    files = html_files()
    check_no_scripts(files)
    check_cname()
    check_internal_refs(files)
    check_external_allowlist(files)
    check_pillar_tiers_and_sync()
    check_new_pages()

    print("checks run: %d" % CHECKS_RUN)
    if FAILURES:
        print("\nFAILURES (%d):" % len(FAILURES))
        for msg in FAILURES:
            print("  - %s" % msg)
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
