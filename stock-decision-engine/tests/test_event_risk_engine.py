from datetime import date, timedelta

from app.engines.event_risk_engine import run_event_risk_engine
from app.models.schemas import EventSnapshot


def test_event_risk_near_earnings_flag():
    snapshot = EventSnapshot(ticker="EVT", next_earnings_date=date.today() + timedelta(days=5), recent_earnings_gap_pct=2.0)
    result = run_event_risk_engine(snapshot)
    assert "Earnings within 10 days" in result.event_flags


def test_event_risk_missing_estimates_safe():
    snapshot = EventSnapshot(ticker="NONE", next_earnings_date=None, recent_earnings_gap_pct=None)
    result = run_event_risk_engine(snapshot)
    assert result.event_risk_score >= 80
