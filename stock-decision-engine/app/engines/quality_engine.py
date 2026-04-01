from __future__ import annotations

from app.models.schemas import FundamentalSnapshot, QualityResult
from app.utils.math_utils import clamp


def run_quality_engine(fundamentals: FundamentalSnapshot) -> QualityResult:
    flags: list[str] = []

    growth_score = clamp(50 + fundamentals.revenue_growth_3y * 120, 0, 100)
    margin_score = clamp(40 + fundamentals.gross_margin * 80 + fundamentals.fcf_margin * 120, 0, 100)
    leverage_penalty = clamp((fundamentals.debt_to_ebitda - 1.5) * 12, 0, 35)
    dilution_penalty = clamp(fundamentals.share_dilution_3y * 250, 0, 20)
    roic_bonus = clamp((fundamentals.roic_proxy or 0) * 40, 0, 8)

    if fundamentals.debt_to_ebitda > 3.0:
        flags.append("High leverage")
    if fundamentals.share_dilution_3y > 0.04:
        flags.append("Meaningful dilution")
    if fundamentals.fcf_margin < 0.05:
        flags.append("Weak cash conversion")

    score = 0.38 * growth_score + 0.42 * margin_score - leverage_penalty - dilution_penalty + roic_bonus
    score = clamp(score, 0, 100)

    explanation = (
        "Quality score combines growth consistency, margin/cash profile, leverage, dilution, "
        "and optional return-on-capital proxy."
    )
    return QualityResult(quality_score=round(score, 1), quality_flags=flags, quality_explanation=explanation)
