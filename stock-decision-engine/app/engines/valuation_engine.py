from __future__ import annotations

from app.models.schemas import EstimateSnapshot, FundamentalSnapshot, ValuationResult
from app.utils.math_utils import clamp


def _scenario_value(owner_eps: float, growth: float, discount_rate: float, terminal_multiple: float) -> float:
    horizon = 5
    future_eps = owner_eps * ((1 + growth) ** horizon)
    terminal_value = future_eps * terminal_multiple
    discounted = terminal_value / ((1 + discount_rate) ** horizon)
    return max(0.0, discounted)


def run_valuation_engine(
    fundamentals: FundamentalSnapshot,
    estimates: EstimateSnapshot,
    peer_multiple_adjustment: float = 0.0,
    analyst_target_adjustment: float = 0.0,
) -> ValuationResult:
    owner_eps = fundamentals.owner_earnings_per_share or 0.0
    if owner_eps <= 0:
        return ValuationResult(
            fair_value_bear=0,
            fair_value_base=0,
            fair_value_bull=0,
            valuation_score=20,
            valuation_explanation="Owner earnings are non-positive, so valuation confidence is low.",
        )

    adjustments = 1 + peer_multiple_adjustment + analyst_target_adjustment
    bear = _scenario_value(owner_eps, estimates.growth_bear, estimates.discount_rate, estimates.terminal_multiple) * adjustments
    base = _scenario_value(owner_eps, estimates.growth_base, estimates.discount_rate, estimates.terminal_multiple) * adjustments
    bull = _scenario_value(owner_eps, estimates.growth_bull, estimates.discount_rate, estimates.terminal_multiple) * adjustments

    spread = (bull - bear) / max(base, 1)
    score = clamp(85 - (spread * 15), 30, 95)
    explanation = (
        f"Fair value uses a 5-year owner-earnings projection with discount rate {estimates.discount_rate:.1%} "
        f"and terminal multiple {estimates.terminal_multiple:.1f}."
    )

    return ValuationResult(
        fair_value_bear=round(bear, 2),
        fair_value_base=round(base, 2),
        fair_value_bull=round(bull, 2),
        valuation_score=round(score, 1),
        valuation_explanation=explanation,
    )
