from app.engines.valuation_engine import run_valuation_engine
from app.models.schemas import EstimateSnapshot, FundamentalSnapshot


def test_valuation_range_ordering():
    fundamentals = FundamentalSnapshot(
        ticker="ABC",
        revenue_growth_3y=0.1,
        gross_margin=0.4,
        fcf_margin=0.2,
        debt_to_ebitda=1.0,
        share_dilution_3y=0.0,
        owner_earnings_per_share=5.0,
    )
    estimates = EstimateSnapshot(ticker="ABC", growth_bear=0.01, growth_base=0.05, growth_bull=0.10, discount_rate=0.1)
    result = run_valuation_engine(fundamentals, estimates)
    assert result.fair_value_bear < result.fair_value_base < result.fair_value_bull


def test_valuation_negative_owner_earnings_edge_case():
    fundamentals = FundamentalSnapshot(
        ticker="BAD",
        revenue_growth_3y=0.0,
        gross_margin=0.2,
        fcf_margin=-0.01,
        debt_to_ebitda=3.5,
        share_dilution_3y=0.05,
        owner_earnings_per_share=-1.0,
    )
    estimates = EstimateSnapshot(ticker="BAD", growth_bear=0.0, growth_base=0.03, growth_bull=0.07, discount_rate=0.11)
    result = run_valuation_engine(fundamentals, estimates)
    assert result.fair_value_base == 0
    assert result.valuation_score <= 20
