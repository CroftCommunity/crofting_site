# RUN-01 — Initial croft.ing landing page

Branch: `claude/run-01-landing-page-2cp060` (cut from `main`). Not merged; left for
review. The repo held only `LICENSE` and `README.md` at the start of the run, so the
guardrail snapshot check passed and work proceeded.

## Files created

| Path | What it is |
| --- | --- |
| `index.html` | The landing page (hero, three pillars, "What's growing now", closing). |
| `plot.html` | Pillar page: The Plot — four depth tiers. |
| `wall.html` | Pillar page: The Wall — four depth tiers. |
| `valley.html` | Pillar page: The Valley — four depth tiers. |
| `library.html` | The Bedrock index — plain link list into the discovery repo. |
| `styles.css` | The single stylesheet (palette, type, layout, drystone-course divider). |
| `CNAME` | Contains exactly `croft.ing`. |
| `assets/favicon.svg` | Drystone-cairn favicon (three stacked rectangles, `--schist`, 293 bytes). |
| `assets/fonts/lora-latin-500-normal.woff2` | Lora 500, latin subset. |
| `assets/fonts/lora-latin-600-normal.woff2` | Lora 600, latin subset. |
| `assets/fonts/inter-latin-400-normal.woff2` | Inter 400, latin subset. |
| `assets/fonts/inter-latin-600-normal.woff2` | Inter 600, latin subset. |
| `assets/fonts/OFL-Lora.txt` | SIL OFL 1.1 for Lora. |
| `assets/fonts/OFL-Inter.txt` | SIL OFL 1.1 for Inter. |
| `README.md` | Replaced — repo description, no-dependency stance, preview, tier convention, token source of record. |
| `RUN-01-SUMMARY.md` | This file. |

## Font sourcing outcome

Fonts were fetched successfully and self-hosted; no fallback was needed.

- **Lora** (headings, weights 500 & 600) — pre-subset latin woff2 from fontsource via
  the jsDelivr npm CDN, package `@fontsource/lora@5.0.19`
  (`.../files/lora-latin-{500,600}-normal.woff2`).
- **Inter** (body/UI, weights 400 & 600) — pre-subset latin woff2 from fontsource via
  the jsDelivr npm CDN, package `@fontsource/inter@5.0.18`
  (`.../files/inter-latin-{400,600}-normal.woff2`).
- **License texts** — `OFL-Lora.txt` from `google/fonts` (`ofl/lora/OFL.txt`) and
  `OFL-Inter.txt` from `rsms/inter` (`LICENSE.txt`); both are SIL Open Font License 1.1.

All four files verified as valid WOFF2 (TrueType flavour). `@font-face` uses
`font-display: swap`. The fallback stacks are wired in regardless
(headings `Lora, Georgia, 'Times New Roman', serif`;
body `Inter, system-ui, -apple-system, 'Segoe UI', sans-serif`).

## Phase 6 link verification / substitutions

All discovery-repo paths were verified to exist on `main` before linking. **No
substitutions were required.** Verified paths:

- `https://github.com/CroftCommunity/discovery` (root) — exists.
- `.../tree/main/beta/drystone-spec` — exists.
- `.../tree/main/beta/philosophy` — exists.
- `.../tree/main/beta/croft` — exists.
- `.../blob/main/beta/croft/croft-ing-the-website-and-the-plot.md` — exists (Plot Bedrock).
- `.../tree/main/beta/socialization` — exists (Valley Bedrock).
- `.../tree/main/beta/governance` — exists (Valley Bedrock).

(The GitHub REST API was proxy-blocked with HTTP 403; verification was done against the
public github.com tree/blob pages instead.)

## Copy smoothing in DRAFT sections

**None.** The three Soil essays (`plot.html`, `wall.html`, `valley.html`) and every
other copy block were placed verbatim from the run instruction. No editorial smoothing
was applied, so there is no before/after to record. The Signpost and Surface text on
each pillar page is byte-for-byte identical to the corresponding landing-page text (this
is intended, and verified).

## Acceptance checks (all passed)

- **Zero loaded external requests.** Every `http(s)` occurrence in HTML/CSS is either the
  SVG XML namespace inside the inline drystone-course data URI (not a network fetch) or an
  intentional, clickable outbound link (`github.com`, `arecipe.app`). No fonts, images,
  scripts, or styles are loaded from any third party.
- **No `<script>` tags** anywhere.
- **All four tier labels** (THE SIGNPOST / THE SURFACE / THE SOIL / THE BEDROCK) appear in
  order on each pillar page; tiers 1 and 2 match the landing-page text exactly.
- **Responsive / readable at 360px and desktop.** Verified with a true 360px-viewport
  render (Playwright device emulation): `scrollWidth == clientWidth == 360` on index,
  plot, and library — no horizontal overflow. Desktop render shows the 3-column pillar
  grid and centered prose column as intended.
- **`CNAME`** contains exactly `croft.ing`.
- **favicon** is 293 bytes (well under 1 KB).

## Manual follow-ups for the maintainer

These were deliberately **not** done by this run (repo settings and DNS are out of scope):

1. **Enable GitHub Pages** — in the repo settings, set Pages to *Deploy from a branch*,
   selecting this branch (or `main` after merge) and the **root** (`/`) folder. The
   `CNAME` file is already committed, so Pages will pick up the custom domain
   automatically.
2. **Point `croft.ing` DNS at GitHub Pages** — at the domain registrar, add the apex
   `A` records (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153) and
   the matching `AAAA` records (2606:50c0:8000::153, 2606:50c0:8001::153,
   2606:50c0:8002::153, 2606:50c0:8003::153) for the apex `croft.ing`. The committed
   `CNAME` file handles the Pages side; confirm "Enforce HTTPS" once the certificate is
   issued. (Verify the current GitHub Pages IPs against GitHub's docs before applying.)
