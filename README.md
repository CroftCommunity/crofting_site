# crofting_site

The source for **croft.ing** — the landing page for Croft, a quiet, personal
space on the modern web. A plot of your own, built to last. No profit motive.

## No dependencies, by design

This site is plain HTML and one CSS file. There is:

- no framework, no `package.json`, no build step;
- no JavaScript on any page;
- no external requests — fonts are self-hosted, there are no CDN links, no
  analytics, no external images, and no tracking of any kind.

The only outbound `http(s)` references anywhere are intentional links the reader
can click (the discovery repo on GitHub, and arecipe.app). Nothing is loaded from
a third party. The pages render correctly both from `file://` and from a static
server.

## Preview

```
python3 -m http.server
```

then open <http://localhost:8000>. Or just open `index.html` directly in a
browser.

## The depth-tier convention

Croft's writing is layered into four tiers of increasing depth. The same idea is
told briefly at the top and more fully as you go down:

1. **Signpost** — the one-line version.
2. **Surface** — the two-to-three-sentence elevator pitch.
3. **Soil** — the one-page essay.
4. **Bedrock** — links into the [discovery repo](https://github.com/CroftCommunity/discovery)
   where the full thinking lives.

The pillar pages (`plot.html`, `wall.html`, `valley.html`) show all four tiers
explicitly, with visible tier labels, so the layers sit side by side. The
**Signpost** and **Surface** text on each pillar page is intentionally identical
to the corresponding text on the landing page: they are meant to be kept in sync,
not de-duplicated. If you edit one, edit the other to match.

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | The landing page. |
| `plot.html` | Pillar page: The Plot. |
| `wall.html` | Pillar page: The Wall. |
| `valley.html` | Pillar page: The Valley. |
| `library.html` | The Bedrock index — links out to the discovery repo. |
| `styles.css` | The single stylesheet. |
| `assets/fonts/` | Self-hosted Lora and Inter (woff2) plus their OFL licenses. |
| `assets/favicon.svg` | The drystone-cairn favicon. |
| `CNAME` | The custom domain (`croft.ing`) for GitHub Pages. |

## Palette and type — source of record

The tectonic palette and the Lora / Inter type choices are defined by the
discovery repo's visual-identity document,
`beta/socialization/visual-identity-and-the-progressive-depth-website.md`. The
working token values live in `styles.css` under `:root`. Treat the discovery doc
as the source of record; the CSS mirrors it.

- Headings: **Lora** (500, 600), self-hosted, SIL OFL 1.1.
- Body / UI: **Inter** (400, 600), self-hosted, SIL OFL 1.1.

## License

Site content and code: **AGPL-3.0** (see `LICENSE`). The bundled fonts are under
the SIL Open Font License 1.1 (see `assets/fonts/OFL-Lora.txt` and
`assets/fonts/OFL-Inter.txt`).
