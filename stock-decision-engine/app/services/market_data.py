from __future__ import annotations

from app.models.schemas import MarketSnapshot


MOCK_MARKET_DATA = {
    "AAPL": {"current_price": 190.0, "high_52w": 205.0, "sma_50": 185.0, "sma_200": 172.0, "rsi_14": 57.0},
    "MSFT": {"current_price": 415.0, "high_52w": 430.0, "sma_50": 402.0, "sma_200": 375.0, "rsi_14": 61.0},
    "TSLA": {"current_price": 175.0, "high_52w": 265.0, "sma_50": 182.0, "sma_200": 205.0, "rsi_14": 41.0},
}


def get_market_snapshot(ticker: str) -> MarketSnapshot:
    t = ticker.upper()
    payload = MOCK_MARKET_DATA.get(t, {"current_price": 100.0, "high_52w": 120.0, "sma_50": 98.0, "sma_200": 95.0, "rsi_14": 50.0})
    return MarketSnapshot(ticker=t, **payload)
