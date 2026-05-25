import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from data import COLORS


def plot_performance(df_perf: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for col in df_perf.columns:
        fig.add_trace(go.Scatter(
            x=df_perf.index,
            y=df_perf[col],
            name=col,
            line=dict(color=COLORS.get(col), width=2.5),
            hovertemplate=f"<b>{col}</b><br>Data: %{{x|%d/%m/%Y}}<br>Retorno: %{{y:.2f}}%<extra></extra>",
        ))
    fig.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.5)
    fig.update_layout(
        title="Performance Acumulada em 2026 (%)",
        xaxis_title="Data",
        yaxis_title="Retorno % acumulado",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="white",
        yaxis=dict(gridcolor="#eeeeee", zeroline=False),
        xaxis=dict(gridcolor="#eeeeee"),
    )
    return fig


def plot_prices(df_close: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for col in df_close.columns:
        fig.add_trace(go.Scatter(
            x=df_close.index,
            y=df_close[col],
            name=col,
            line=dict(color=COLORS.get(col), width=2),
            hovertemplate=f"<b>{col}</b><br>Data: %{{x|%d/%m/%Y}}<br>Preço: R$ %{{y:.2f}}<extra></extra>",
        ))
    fig.update_layout(
        title="Preço de Fechamento (R$)",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="white",
        yaxis=dict(gridcolor="#eeeeee"),
        xaxis=dict(gridcolor="#eeeeee"),
    )
    return fig


def plot_volume(df_vol: pd.DataFrame) -> go.Figure:
    n = len(df_vol.columns)
    fig = make_subplots(rows=n, cols=1, shared_xaxes=True,
                        subplot_titles=list(df_vol.columns),
                        vertical_spacing=0.08)
    for i, col in enumerate(df_vol.columns, start=1):
        fig.add_trace(
            go.Bar(
                x=df_vol.index,
                y=df_vol[col],
                name=col,
                marker_color=COLORS.get(col),
                hovertemplate=f"<b>{col}</b><br>Data: %{{x|%d/%m/%Y}}<br>Volume: %{{y:,.0f}}<extra></extra>",
            ),
            row=i, col=1,
        )
        fig.update_yaxes(title_text="Volume", row=i, col=1, gridcolor="#eeeeee")
    fig.update_layout(
        title="Volume Diário de Negociação",
        showlegend=False,
        plot_bgcolor="white",
        height=200 * n,
        xaxis=dict(gridcolor="#eeeeee"),
    )
    return fig
