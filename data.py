import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

TICKERS = {
    "Petrobrás": "PETR4.SA",
    "Itaú": "ITUB4.SA",
    "Vale": "VALE3.SA",
}

COLORS = {
    "Petrobrás": "#009B3A",
    "Itaú": "#003087",
    "Vale": "#0060A9",
}


@st.cache_data(ttl=3600)
def fetch_stocks(tickers: dict, start: date, end: date) -> pd.DataFrame:
    symbols = list(tickers.values())
    raw = yf.download(symbols, start=start, end=end, auto_adjust=True, progress=False)

    close = raw["Close"].copy()
    volume = raw["Volume"].copy()

    # Renomeia colunas de símbolo para nome legível
    reverse = {v: k for k, v in tickers.items()}
    close.columns = [reverse.get(c, c) for c in close.columns]
    volume.columns = [reverse.get(c, c) for c in volume.columns]

    return close.dropna(how="all"), volume.dropna(how="all")


def calc_performance(close: pd.DataFrame) -> pd.DataFrame:
    first = close.iloc[0]
    return ((close - first) / first * 100).round(4)


def get_metrics(close: pd.DataFrame) -> dict:
    metrics = {}
    for col in close.columns:
        series = close[col].dropna()
        if len(series) < 2:
            continue
        current = series.iloc[-1]
        prev = series.iloc[-2]
        start = series.iloc[0]
        metrics[col] = {
            "price": current,
            "day_change": (current - prev) / prev * 100,
            "ytd_change": (current - start) / start * 100,
        }
    return metrics
