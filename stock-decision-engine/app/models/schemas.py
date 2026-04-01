from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class MarketSnapshot(BaseModel):
    ticker: str
    current_price: float = Field(..., gt=0)
    high_52w: float = Field(..., gt=0)
    sma_50: float = Field(..., gt=0)
    sma_200: float = Field(..., gt=0)
    rsi_14: float = Field(..., ge=0, le=100)


class FundamentalSnapshot(BaseModel):
    ticker: str
    revenue_growth_3y: float
    gross_margin: float
    fcf_margin: float
    debt_to_ebitda: float
    share_dilution_3y: float
    roic_proxy: Optional[float] = None
    owner_earnings_per_share: Optional[float] = None


class EstimateSnapshot(BaseModel):
    ticker: str
    growth_bear: float
    growth_base: float
    growth_bull: float
    discount_rate: float
    terminal_multiple: float = 14.0


class EventSnapshot(BaseModel):
    ticker: str
    next_earnings_date: Optional[date] = None
    recent_earnings_gap_pct: Optional[float] = None


class ValuationResult(BaseModel):
    fair_value_bear: float
    fair_value_base: float
    fair_value_bull: float
    valuation_score: float
    valuation_explanation: str


class QualityResult(BaseModel):
    quality_score: float
    quality_flags: List[str]
    quality_explanation: str


class TimingResult(BaseModel):
    timing_score: float
    timing_state: str
    timing_explanation: str


class EventRiskResult(BaseModel):
    event_risk_score: float
    event_flags: List[str]
    event_explanation: str


class DecisionResult(BaseModel):
    final_score: float
    final_label: str
    buy_zone: str
    reasons: List[str]
    warnings: List[str]
    confidence_level: str
