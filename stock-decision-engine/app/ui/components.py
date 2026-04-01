from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render_summary_cards(metrics: dict[str, str]) -> None:
    cols = st.columns(len(metrics))
    for idx, (label, value) in enumerate(metrics.items()):
        cols[idx].metric(label=label, value=value)


def fair_value_chart(bear: float, base: float, bull: float, current_price: float):
    df = pd.DataFrame(
        {
            "Scenario": ["Bear", "Base", "Bull", "Current"],
            "Value": [bear, base, bull, current_price],
            "Type": ["Fair Value", "Fair Value", "Fair Value", "Market"],
        }
    )
    fig = px.bar(df, x="Scenario", y="Value", color="Type", title="Fair Value Range vs Market")
    fig.update_layout(height=360)
    return fig
