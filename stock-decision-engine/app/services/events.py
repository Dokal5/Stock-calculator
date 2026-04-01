from __future__ import annotations

from datetime import date, timedelta

from app.models.schemas import EventSnapshot


MOCK_EVENTS = {
    "AAPL": {"next_earnings_date": date.today() + timedelta(days=18), "recent_earnings_gap_pct": 3.5},
    "TSLA": {"next_earnings_date": date.today() + timedelta(days=7), "recent_earnings_gap_pct": 9.2},
}


def get_event_snapshot(ticker: str) -> EventSnapshot:
    payload = MOCK_EVENTS.get(ticker.upper(), {"next_earnings_date": None, "recent_earnings_gap_pct": None})
    return EventSnapshot(ticker=ticker.upper(), **payload)
