from __future__ import annotations

from app.models.schemas import EventRiskResult, EventSnapshot
from app.utils.date_utils import days_until
from app.utils.math_utils import clamp


def run_event_risk_engine(events: EventSnapshot) -> EventRiskResult:
    flags: list[str] = []
    score = 85.0

    days = days_until(events.next_earnings_date)
    if days is not None and 0 <= days <= 10:
        score -= 35
        flags.append("Earnings within 10 days")
    elif days is not None and 0 <= days <= 21:
        score -= 15
        flags.append("Earnings within 3 weeks")

    gap = events.recent_earnings_gap_pct
    if gap is not None and abs(gap) >= 8:
        score -= 20
        flags.append("Large recent earnings gap")

    score = clamp(score, 0, 100)
    caution = "Caution" if score < 55 else "Manageable"
    explanation = f"{caution} event risk based on earnings proximity and historical earnings-gap volatility."
    return EventRiskResult(event_risk_score=round(score, 1), event_flags=flags, event_explanation=explanation)
