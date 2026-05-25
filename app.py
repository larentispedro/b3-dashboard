import streamlit as st
from datetime import date, datetime
from data import fetch_stocks, calc_performance, get_metrics, TICKERS
from charts import plot_performance, plot_prices, plot_volume

st.set_page_config(
    page_title="Ações B3 2026",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Análise de Ações B3 — 2026")
st.caption("Petrobrás (PETR4) · Itaú (ITUB4) · Vale (VALE3)")

# --- Sidebar ---
with st.sidebar:
    st.header("Configurações")

    start_date = st.date_input(
        "Data inicial",
        value=date(2026, 1, 2),
        min_value=date(2026, 1, 2),
        max_value=date.today(),
    )
    end_date = st.date_input(
        "Data final",
        value=date.today(),
        min_value=date(2026, 1, 2),
        max_value=date.today(),
    )

    st.divider()
    st.subheader("Ações exibidas")
    selected = {}
    for name in TICKERS:
        selected[name] = st.checkbox(name, value=True)

    st.divider()
    atualizar = st.button("🔄 Atualizar dados", use_container_width=True)

if start_date >= end_date:
    st.error("A data inicial deve ser anterior à data final.")
    st.stop()

active_tickers = {k: v for k, v in TICKERS.items() if selected.get(k)}

if not active_tickers:
    st.warning("Selecione ao menos uma ação na barra lateral.")
    st.stop()

if atualizar:
    st.cache_data.clear()

# --- Busca de dados ---
with st.spinner("Buscando cotações..."):
    close, volume = fetch_stocks(active_tickers, start_date, end_date)

if close.empty:
    st.error("Nenhum dado encontrado para o período selecionado.")
    st.stop()

# Filtra apenas colunas selecionadas presentes no DataFrame
cols = [c for c in active_tickers if c in close.columns]
close = close[cols]
volume = volume[[c for c in cols if c in volume.columns]]

# --- Métricas ---
metrics = get_metrics(close)
metric_cols = st.columns(len(metrics))
for col_ui, (name, m) in zip(metric_cols, metrics.items()):
    col_ui.metric(
        label=name,
        value=f"R$ {m['price']:.2f}",
        delta=f"{m['day_change']:+.2f}% no dia  |  {m['ytd_change']:+.2f}% no ano",
    )

st.divider()

# --- Gráfico de Performance ---
perf = calc_performance(close)
st.plotly_chart(plot_performance(perf), use_container_width=True)

# --- Gráfico de Preços ---
st.plotly_chart(plot_prices(close), use_container_width=True)

# --- Gráfico de Volume ---
if not volume.empty:
    st.plotly_chart(plot_volume(volume), use_container_width=True)

st.caption(f"Dados fornecidos por Yahoo Finance · Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
