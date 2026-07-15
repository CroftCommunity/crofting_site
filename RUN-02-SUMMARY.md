# RUN-02 — arecipe and Skylite guide pages

Branch: `claude/run-02-guide-pages-mgdov1` (cut from `main`). Not merged; left for
review. Built on the RUN-01 site (index + plot/wall/valley/library + styles.css +
fonts).

## TDD: red-to-green

Per the standing convention, the checks harness was written first — with the NEW
assertions for the guide pages included — and run before the pages existed, to
prove the harness is honest (the new assertions fail; everything else passes).

### RED — `python3 checks/check_site.py` before Phase 2

```
checks run: 17

FAILURES (3):
  - arecipe/index.html exists
  - skylite/index.html exists
  - index.html growing section contains 'Skylite'

RESULT: FAIL
```

Only the three new-page assertions failed; the 14 whole-site assertions (no
scripts, CNAME, internal refs resolve, external allowlist, pillar tier order and
Signpost/Surface sync) all passed, confirming the harness was already exercising
the existing site correctly. (The nested content assertions inside the two new
pages did not run yet because their files were absent; they became active once the
files existed.)

### GREEN — `python3 checks/check_site.py` after Phases 2–3

```
checks run: 22

RESULT: PASS
```

## Files created

| Path | What it is |
| --- | --- |
| `checks/check_site.py` | Standing regression net, Python 3 stdlib only. Exits nonzero on any failure. |
| `arecipe/index.html` | Guide page for arecipe (directory style → `croft.ing/arecipe`). |
| `skylite/index.html` | Guide page for Skylite (directory style → `croft.ing/skylite`). |

## Files edited

| Path | Change |
| --- | --- |
| `index.html` | **Only** the "What's growing now" section: arecipe's name now links to `/arecipe/` and its arecipe.app link is presented as a "Use it:" link; a new **Skylite** entry was added between arecipe and The Plot (name links to `/skylite/`, "See it:" link to skylite.croft.ing). Nothing else on the page changed — hero, pillars, closing, and footer are untouched. |
| `styles.css` | Two additive rules only (below). No existing rule was modified. |
| `README.md` | Added the two guide pages and the checks harness to the Pages table; added a "Guide pages" section and a "Checks" section. |

## styles.css additions

Both additions are new and purely additive; no existing selector or value was
changed, so no existing page is restyled.

- `.colophon` — the guide-page footnote line (right-aligned, italic, small,
  `--granite`), used for arecipe's *"the a is for Amanda"* line.
- `.bedrock-links a { overflow-wrap: anywhere; }` — lets long bare-URL link text
  wrap inside the Bedrock lists so the arecipe/Skylite source URLs don't overflow
  the viewport at 360px. This selector is shared with the pillar pages, but their
  Bedrock links use short human-readable labels with no long unbreakable tokens,
  so there is zero visual change to any existing page.

## Guardrails honored

- Plain HTML + the single existing `styles.css`. No framework, no JS, no build
  step, no new dependencies. The checks harness is Python 3 stdlib only.
- **Zero loaded external requests** on the new pages: the only external
  references are clickable `<a href>` links (arecipe.app, arecipe.croft.ing,
  skylite.croft.ing, github.com/CroftCommunity). Stylesheet and favicon are
  local, referenced by absolute root paths (`/styles.css`, `/assets/favicon.svg`)
  because the pages live one level deep.
- Reused the existing header, footer, palette tokens, type, `.tier` / `.tier-label`
  styling, `.course` divider, `.button`, and `.bedrock-links`.
- Copy placed verbatim from the brief; no embellishment.
- Tier labels on the new pages are set in the copy's uppercase form
  (`THE SIGNPOST`, `THE SURFACE`, `THE BEDROCK`, etc.), styled by the existing
  small-caps `--granite` `.tier-label` rule.

## Verification

- `python3 checks/check_site.py` → 22 checks, **PASS**.
- Rendered both pages under a static server and screenshotted at **360px** and
  **desktop (1100px)**: single-column, readable, no horizontal overflow, button
  and Bedrock URLs wrap correctly.
- Confirmed via `git diff` that **no existing page's copy changed except the
  growing section** of `index.html`; the pillar/tier Signpost–Surface sync is
  untouched and still green.
