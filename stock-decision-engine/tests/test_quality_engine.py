from app.engines.quality_engine import run_quality_engine
from app.models.schemas import FundamentalSnapshot


def test_quality_high_debt_flagged():
    fundamentals = FundamentalSnapshot(
        ticker="LEV",
        revenue_growth_3y=0.08,
        gross_margin=0.33,
        fcf_margin=0.06,
        debt_to_ebitda=4.1,
        share_dilution_3y=0.02,
        owner_earnings_per_share=2.0,
    )
    result = run_quality_engine(fundamentals)
    assert "High leverage" in result.quality_flags


def test_quality_missing_roic_is_safe():
    fundamentals = FundamentalSnapshot(
        ticker="NOROIC",
        revenue_growth_3y=0.05,
        gross_margin=0.30,
        fcf_margin=0.10,
        debt_to_ebitda=1.5,
        share_dilution_3y=0.0,
        roic_proxy=None,
        owner_earnings_per_share=2.2,
    )
    result = run_quality_engine(fundamentals)
    assert 0 <= result.quality_score <= 100
