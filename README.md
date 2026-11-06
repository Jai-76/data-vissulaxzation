# World in Motion — animated Gapminder-style world dashboard, 1960–2026

`world-dashboard.html` is a single self-contained file (≈0.67 MB, no libraries, no network calls) that
plots 217 economies as bubbles and animates them from 1960 to 2026.

- **X / Y / size / colour** are each switchable between nine World Bank indicators
  (GDP per capita PPP, GDP per capita constant 2015 US$, life expectancy, CO₂ per capita,
  population, fertility, under-5 mortality, urban share, energy use per capita).
- **Play / scrub** the timeline with speed control, or step year by year with the arrow keys.
- **Hover** for values, **click** to pin a country — pinned countries keep a label, a 22-year trail
  and a full-history sparkline in the side panel.
- Region and income-group legend chips filter the view; the header numbers are population-weighted
  live for the current year.

## Data

World Bank **World Development Indicators**, retrieved from `api.worldbank.org` on 6 November 2026.

| series | latest observation |
|---|---|
| GDP per capita (PPP), GDP per capita (const. 2015 US$), population, urban share | **2025** |
| life expectancy, CO₂ per capita, fertility, under-5 mortality, energy use | **2024** |
| anything | **no 2026 observations exist** — the API was last refreshed 8 Oct 2026 |

To reach 2026 the dashboard extrapolates each country's own recent trend (average annual change over
its last ten observations, clamped to a plausible range). Those years are never presented as data:
the canvas shows an amber **PROJECTED** badge and year watermark, headline stats and tooltips prefix
affected values with **≈**, and the **“to 2026”** switch turns the extension off, ending the timeline
at the last observed year for whatever indicators are selected.

Aggregates are excluded. Indicator codes are listed in the “Data & methods” panel inside the dashboard.

## Rebuilding

```
python3 build/fetch_wb.py    # -> data/wb_raw.json     (World Bank API, cached in data/cache/)
python3 build/build_data.py  # -> build/payload.json   (compact, year-encoded series)
python3 build/build.py       # -> world-dashboard.html (inlines CSS + JS + data)
```

Build sources live in `build/`: `template.html`, `style.css`, `app.js`, and the two data scripts.
The chart is drawn on a single `<canvas>`; axes are fixed across all years for the selected
indicators, and internal data gaps of up to 8 years are interpolated so the animation stays smooth.
