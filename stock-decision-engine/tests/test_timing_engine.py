from app.engines.timing_engine import run_timing_engine
from app.models.schemas import MarketSnapshot


def test_timing_accumulate_now_signal():
    snap = MarketSnapshot(ticker="UP", current_price=110, high_52w=120, sma_50=105, sma_200=95, rsi_14=58)
    result = run_timing_engine(snap)
    assert result.timing_state == "Accumulate now"


def test_timing_downtrend_signal():
    snap = MarketSnapshot(ticker="DN", current_price=80, high_52w=140, sma_50=92, sma_200=100, rsi_14=44)
    result = run_timing_engine(snap)
    assert result.timing_state == "Avoid until trend improves"
