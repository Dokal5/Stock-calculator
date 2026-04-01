from __future__ import annotations

from app.models.schemas import MarketSnapshot, TimingResult
from app.utils.math_utils import clamp


def run_timing_engine(market: MarketSnapshot) -> TimingResult:
    above_50 = market.current_price / market.sma_50 - 1
    above_200 = market.current_price / market.sma_200 - 1
    drawdown = market.current_price / market.high_52w - 1

    trend_score = 50 + (above_50 * 120) + (above_200 * 140)
    rsi_penalty = 12 if market.rsi_14 > 70 else 0
    rsi_bonus = 8 if market.rsi_14 < 35 else 0
    drawdown_bonus = 8 if drawdown < -0.20 else 0

    score = clamp(trend_score - rsi_penalty + rsi_bonus + drawdown_bonus, 0, 100)

    if market.current_price > market.sma_50 > market.sma_200 and market.rsi_14 < 68:
        state = "Accumulate now"
    elif market.current_price > market.sma_200:
        state = "Wait for pullback"
    else:
        state = "Avoid until trend improves"

    explanation = (
        "Timing checks trend versus 50/200-day moving averages, RSI regime, and drawdown from 52-week high."
    )

    return TimingResult(timing_score=round(score, 1), timing_state=state, timing_explanation=explanation)
