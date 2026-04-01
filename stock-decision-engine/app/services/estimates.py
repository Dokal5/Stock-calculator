from __future__ import annotations

from app.models.schemas import EstimateSnapshot


DEFAULT_ESTIMATES = {
    "growth_bear": 0.02,
    "growth_base": 0.06,
    "growth_bull": 0.10,
    "discount_rate": 0.10,
    "terminal_multiple": 15.0,
}


def get_estimate_snapshot(ticker: str, overrides: dict | None = None) -> EstimateSnapshot:
    payload = dict(DEFAULT_ESTIMATES)
    if overrides:
        payload.update(overrides)
    return EstimateSnapshot(ticker=ticker.upper(), **payload)
