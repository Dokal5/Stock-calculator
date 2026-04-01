from __future__ import annotations

from app.models.schemas import DecisionResult, EventRiskResult, QualityResult, TimingResult, ValuationResult
from app.utils.math_utils import clamp


DEFAULT_WEIGHTS = {"valuation": 40, "quality": 30, "timing": 20, "event_risk": 10}


def _buy_zone(current_price: float, fair_bear: float, fair_base: float) -> str:
    if current_price <= fair_bear:
        return "Strong buy"
    if current_price <= fair_base * 0.95:
        return "Normal buy"
    if current_price <= fair_base * 1.08:
        return "Watchlist"
    return "Avoid chasing"


def run_decision_engine(
    current_price: float,
    valuation: ValuationResult,
    quality: QualityResult,
    timing: TimingResult,
    event_risk: EventRiskResult,
    weights: dict[str, float] | None = None,
) -> DecisionResult:
    w = weights or DEFAULT_WEIGHTS
    total = sum(w.values())
    normalized = {k: v / total for k, v in w.items()}

    final_score = (
        valuation.valuation_score * normalized["valuation"]
        + quality.quality_score * normalized["quality"]
        + timing.timing_score * normalized["timing"]
        + event_risk.event_risk_score * normalized["event_risk"]
    )
    final_score = round(clamp(final_score, 0, 100), 1)

    if final_score >= 80:
        label = "High conviction"
    elif final_score >= 65:
        label = "Balanced opportunity"
    elif final_score >= 50:
        label = "Speculative"
    else:
        label = "Low conviction"

    buy_zone = _buy_zone(current_price, valuation.fair_value_bear, valuation.fair_value_base)

    reasons = [
        valuation.valuation_explanation,
        quality.quality_explanation,
        timing.timing_explanation,
        event_risk.event_explanation,
    ]
    warnings = quality.quality_flags + event_risk.event_flags

    confidence = "High" if len(warnings) <= 1 and final_score >= 70 else "Medium" if final_score >= 55 else "Low"

    return DecisionResult(
        final_score=final_score,
        final_label=label,
        buy_zone=buy_zone,
        reasons=reasons,
        warnings=warnings,
        confidence_level=confidence,
    )
