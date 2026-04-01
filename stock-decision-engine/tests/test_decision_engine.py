from datetime import date, timedelta

from app.engines.decision_engine import run_decision_engine
from app.engines.event_risk_engine import run_event_risk_engine
from app.engines.quality_engine import run_quality_engine
from app.engines.timing_engine import run_timing_engine
from app.engines.valuation_engine import run_valuation_engine
from app.models.schemas import EstimateSnapshot, EventSnapshot, FundamentalSnapshot, MarketSnapshot


def test_decision_golden_case_aapl_like():
    market = MarketSnapshot(ticker="AAPL", current_price=190, high_52w=205, sma_50=185, sma_200=172, rsi_14=57)
    fundamentals = FundamentalSnapshot(
        ticker="AAPL",
        revenue_growth_3y=0.07,
        gross_margin=0.44,
        fcf_margin=0.26,
        debt_to_ebitda=1.2,
        share_dilution_3y=-0.01,
        roic_proxy=0.29,
        owner_earnings_per_share=6.8,
    )
    estimates = EstimateSnapshot(ticker="AAPL", growth_bear=0.02, growth_base=0.06, growth_bull=0.10, discount_rate=0.1)
    events = EventSnapshot(ticker="AAPL", next_earnings_date=date.today() + timedelta(days=18), recent_earnings_gap_pct=3.5)

    valuation = run_valuation_engine(fundamentals, estimates)
    quality = run_quality_engine(fundamentals)
    timing = run_timing_engine(market)
    event_risk = run_event_risk_engine(events)

    decision = run_decision_engine(market.current_price, valuation, quality, timing, event_risk)

    assert 0 <= decision.final_score <= 100
    assert decision.buy_zone in {"Strong buy", "Normal buy", "Watchlist", "Avoid chasing"}
    assert decision.confidence_level in {"High", "Medium", "Low"}
