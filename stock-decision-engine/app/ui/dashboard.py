from __future__ import annotations

import streamlit as st
import yaml

from app.engines.decision_engine import run_decision_engine
from app.engines.event_risk_engine import run_event_risk_engine
from app.engines.quality_engine import run_quality_engine
from app.engines.timing_engine import run_timing_engine
from app.engines.valuation_engine import run_valuation_engine
from app.services.estimates import get_estimate_snapshot
from app.services.events import get_event_snapshot
from app.services.fundamentals import get_fundamental_snapshot
from app.services.market_data import get_market_snapshot
from app.ui.components import fair_value_chart, render_summary_cards


def _load_weights(path: str = "config/scoring_weights.yaml") -> dict[str, float]:
    with open(path, "r", encoding="utf-8") as f:
        payload = yaml.safe_load(f)
    return payload["weights"]


def render_dashboard() -> None:
    st.title("Stock Decision Engine")
    st.caption("Transparent single-ticker decision support. Outputs ranges, signals, and explicit assumptions.")

    ticker = st.text_input("Ticker", value="AAPL").strip().upper()

    st.sidebar.header("Assumptions")
    discount_rate = st.sidebar.slider("Discount rate", min_value=0.06, max_value=0.16, value=0.10, step=0.005)
    growth_bear = st.sidebar.slider("Bear growth", min_value=-0.03, max_value=0.08, value=0.02, step=0.005)
    growth_base = st.sidebar.slider("Base growth", min_value=0.00, max_value=0.15, value=0.06, step=0.005)
    growth_bull = st.sidebar.slider("Bull growth", min_value=0.02, max_value=0.22, value=0.10, step=0.005)

    market = get_market_snapshot(ticker)
    fundamentals = get_fundamental_snapshot(ticker)
    estimates = get_estimate_snapshot(
        ticker,
        {
            "discount_rate": discount_rate,
            "growth_bear": growth_bear,
            "growth_base": growth_base,
            "growth_bull": growth_bull,
        },
    )
    events = get_event_snapshot(ticker)

    valuation = run_valuation_engine(fundamentals, estimates)
    quality = run_quality_engine(fundamentals)
    timing = run_timing_engine(market)
    event_risk = run_event_risk_engine(events)
    decision = run_decision_engine(
        market.current_price,
        valuation,
        quality,
        timing,
        event_risk,
        weights=_load_weights(),
    )

    premium_discount = (market.current_price / max(valuation.fair_value_base, 1e-6) - 1) * 100

    render_summary_cards(
        {
            "Current Price": f"${market.current_price:,.2f}",
            "Fair Value (Base)": f"${valuation.fair_value_base:,.2f}",
            "Premium/Discount": f"{premium_discount:+.1f}%",
            "Score": f"{decision.final_score:.1f}/100",
            "Buy Zone": decision.buy_zone,
            "Timing": timing.timing_state,
        }
    )

    st.plotly_chart(
        fair_value_chart(
            valuation.fair_value_bear,
            valuation.fair_value_base,
            valuation.fair_value_bull,
            market.current_price,
        ),
        use_container_width=True,
    )

    st.subheader("Score Breakdown")
    st.write(
        {
            "Valuation": valuation.valuation_score,
            "Quality": quality.quality_score,
            "Timing": timing.timing_score,
            "Event Risk": event_risk.event_risk_score,
            "Final": decision.final_score,
        }
    )

    st.subheader("Explanation")
    for reason in decision.reasons:
        st.write(f"- {reason}")

    if decision.warnings:
        st.subheader("Key Risk Flags")
        for warning in decision.warnings:
            st.warning(warning)

    st.info(f"Confidence: {decision.confidence_level}. This tool provides ranges and signals, not exact buy prices.")
