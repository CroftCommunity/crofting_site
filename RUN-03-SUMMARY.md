# RUN-03 — the terms pages: `/terms/` and `/terms/ens/`

Branch: `claude/run-03-terms-pages-63a0h4` (cut from `main`). Not merged; left
for review. Extends the RUN-02 harness (`checks/check_site.py`), whose presence
— along with `arecipe/index.html` — was verified before starting, per the
run-ordering requirement.

## TDD: red-to-green

Per the standing convention, the new assertions were added to
`checks/check_site.py` first (a `check_terms_pages()` section plus the
allowlist extension) and run before any page existed.

### RED — `python3 checks/check_site.py` before Phase 2

```
checks run: 25

FAILURES (3):
  - terms/index.html exists
  - terms/ens/index.html exists
  - library.html links to /terms/

RESULT: FAIL
```

Only the three new assertions failed; all 22 pre-existing checks still passed,
confirming the net was honest before construction. (The nested content
assertions inside the two new pages — tier-label order, the one-liner, the
"ENS is Not Service" string, the `/terms/ens/` entry link — did not run yet
because their files were absent; they became active once the files existed.)

### GREEN — `python3 checks/check_site.py` after Phases 2–3

```
checks run: 30

RESULT: PASS
```

## Files created

| Path | What it is |
| --- | --- |
| `terms/index.html` | The vocabulary index (directory style → `croft.ing/terms/`). Heading, intro copy, and a one-entry list (ENS) in the same markup shape as the landing page's growing section: bold linked term, description paragraph, no dashes. |
| `terms/ens/index.html` | The ENS term page. Kicker `A CROFT TERM` (small caps, `--granite`, via the existing `.tier-label` rule) above the `ENS` h1, then THE SIGNPOST / THE SURFACE / THE SOIL / THE BEDROCK tiers separated by `.course` dividers. |

## Files edited

| Path | Change |
| --- | --- |
| `checks/check_site.py` | New `check_terms_pages()`: both files exist; the ENS page shows THE SIGNPOST, THE SURFACE, THE SOIL, THE BEDROCK in order and contains "A polite acronym for how platforms rot." and "ENS is Not Service"; the terms index entry links to `/terms/ens/`; `library.html` links to `/terms/`. Plus the allowlist extension below. |
| `library.html` | **One line only**: the link list gains `The working vocabulary → /terms/` before the discovery-repo links. Nothing else on any existing page changed. |

## Allowlist addition

`ALLOWED_HOSTS` gains **`pluralistic.net`** (per the brief — the Bedrock cites
Doctorow's origin essay) and **`croft.ing`** itself. The second addition was
not in the brief but is forced by the verbatim Bedrock copy, whose final line
cites `https://croft.ing` as a bare absolute URL; the host is the site's own
canonical domain, so admitting it keeps the allowlist's real invariant (no
third-party surface beyond the named set) intact. All external URLs remain
plain `<a href>` links — nothing is loaded.

## Guardrails honored

- Plain HTML + the single existing `styles.css`, unchanged. No JS, no build
  step, no new dependencies. **No new CSS was needed**: the kicker reuses
  `.tier-label`, the index entry list reuses `.growing-list`/`.term`, the
  Bedrock list reuses `.bedrock-links` (whose `overflow-wrap: anywhere` keeps
  the long pluralistic.net URL from overflowing at 360px).
- Both pages carry the shared header, footer, favicon, and `.course` dividers;
  asset paths are absolute-root (`/styles.css`, `/assets/favicon.svg`) since
  the pages live one and two levels deep.
- Copy placed verbatim from the brief, including the "its treatise" link to
  `https://arecipe.croft.ing` inside the final Soil paragraph.
- **Zero loaded external requests**, verified at runtime (below), not just by
  inspection.

## Verification

- `python3 checks/check_site.py` → 30 checks, **PASS**.
- Rendered both pages under a local static server (Chromium via
  playwright-core, real viewports): horizontal overflow **0px at 360px and
  1100px** on both pages, and the network log recorded **zero requests to any
  non-local origin** on both pages.
- `git diff` confirms the only existing files touched are
  `checks/check_site.py` and the single added line in `library.html`.

## Out of scope, noted for the follow-up

The appendix's one-line amendment (linking the "ENS" parenthetical in the
treatise's Act I to `https://croft.ing/terms/ens/`) belongs to the
`arecipe_treatise` repo and is deliberately not part of this run.
