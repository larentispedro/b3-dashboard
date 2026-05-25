# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```
streamlit run app.py
```

Install dependencies first:

```
pip install -r requirements.txt
```

To force a data refresh at runtime, click the "🔄 Atualizar dados" button in the sidebar (calls `st.cache_data.clear()`).

## Architecture

Three-module Streamlit dashboard for B3 (Brazilian stock market) analysis:

- **`data.py`** — data layer: defines `TICKERS` (name → Yahoo Finance symbol) and `COLORS` (name → hex). `fetch_stocks` downloads Close + Volume via `yfinance` and is cached for 1 hour with `@st.cache_data(ttl=3600)`. `calc_performance` and `get_metrics` are pure transforms on the resulting DataFrames.
- **`charts.py`** — presentation layer: three Plotly figure builders (`plot_performance`, `plot_prices`, `plot_volume`) that consume DataFrames produced by `data.py`. Reads `COLORS` from `data.py`.
- **`app.py`** — UI layer: wires sidebar controls (date range, ticker checkboxes, refresh button) to data fetches and chart renders. All user-facing text is in Portuguese.

Data flow: `app.py` calls `fetch_stocks` → passes result to `calc_performance` / `get_metrics` → passes to chart functions → renders with `st.plotly_chart`.

## Adding a new ticker

1. Add an entry to `TICKERS` and `COLORS` in `data.py`.
2. No changes needed in `charts.py` or `app.py` — both iterate over DataFrame columns dynamically.

## GitHub repository

Repository: `https://github.com/larentispedro/b3-dashboard`

**Auto-sync**: Every time Claude edits a file (Edit or Write tool), a PostToolUse hook in `.claude/settings.json` automatically commits and pushes to GitHub with a message like `auto: sync changes YYYY-MM-DD HH:MM:SS`.

**Manual sync**: If you edit files outside Claude, run:
```
git add -A
git commit -m "sua mensagem"
git push origin master
```

**GitHub CLI**: Installed at `C:\Program Files\GitHub CLI\gh.exe`. Authenticated as `larentispedro`.
