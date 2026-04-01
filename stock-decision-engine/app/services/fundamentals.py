from __future__ import annotations

from app.models.schemas import FundamentalSnapshot


MOCK_FUNDAMENTALS = {
    "AAPL": {
        "revenue_growth_3y": 0.07,
        "gross_margin": 0.44,
        "fcf_margin": 0.26,
        "debt_to_ebitda": 1.2,
        "share_dilution_3y": -0.01,
        "roic_proxy": 0.29,
        "owner_earnings_per_share": 6.8,
    },
    "TSLA": {
        "revenue_growth_3y": 0.24,
        "gross_margin": 0.19,
        "fcf_margin": 0.08,
        "debt_to_ebitda": 1.7,
        "share_dilution_3y": 0.03,
        "roic_proxy": 0.12,
        "owner_earnings_per_share": 1.8,
    },
}


def get_fundamental_snapshot(ticker: str) -> FundamentalSnapshot:
    t = ticker.upper()
    payload = MOCK_FUNDAMENTALS.get(
        t,
        {
            "revenue_growth_3y": 0.06,
            "gross_margin": 0.35,
            "fcf_margin": 0.12,
            "debt_to_ebitda": 2.2,
            "share_dilution_3y": 0.01,
            "roic_proxy": 0.10,
            "owner_earnings_per_share": 3.0,
        },
    )
    return FundamentalSnapshot(ticker=t, **payload)
