# Ing.Dylan — GitHub banner system

Final PNG exports live in this folder. Standalone Canva-importable SVG files live in `canva/`; working SVG sources and their background plates live in `source/`.

| Canva page name | Final export | Size |
| --- | --- | --- |
| 01 — GitHub Header | `01-github-header.png` | 1280 × 320 |
| 02 — DylanOS | `02-dylanos.png` | 900 × 300 |
| 03 — DylanOS Website | `03-dylanos-website.png` | 900 × 300 |
| 04 — Projects & Experiments | `04-projects-experiments.png` | 900 × 300 |
| 05 — Robotics | `05-robotics.png` | 900 × 300 |
| 06 — GitHub Footer | `06-github-footer.png` | 1280 × 180 |
| 07 — GitHub Stats | `07-github-stats.png` | 900 × 300 |
| 08 — Top Languages | `08-top-languages.png` | 900 × 300 |
| 09 — Contribution Graph | `09-contribution-graph.png` | 900 × 300 |
| 10 — Social & Contact | `10-social-contact.png` | 900 × 300 |

## Design system

- Palette: `#080808`, `#111111`, `#E50914`, `#8F0008`, `#FFFFFF`, `#B8B8B8`
- Display type: DejaVu Sans Bold
- Technical type: Noto Sans Mono
- Shared language: thin technical grid, one-pixel frames, restrained red signals, dark UI modules, generous negative space

Import the ten self-contained SVG files from `canva/` into one Canva project and keep the page names above. The SVGs preserve vector text, frames, dividers, and accents, with each technical plate embedded inside its file so no external image link is required.

The activity banners `07`–`09` are fully vector-based and use a public-data snapshot from GitHub. Run `source/generate-github-activity.py` to refresh repositories, followers, stars, forks, language bytes, and the last-year contribution calendar before re-exporting the PNGs.
