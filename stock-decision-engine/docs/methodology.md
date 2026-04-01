# Methodology

## Valuation engine
Uses a simplified owner-earnings DCF-like structure:
- Project owner earnings per share over 5 years for bear/base/bull growth assumptions.
- Apply terminal multiple.
- Discount back with user-selected discount rate.
- Publish range (`bear`, `base`, `bull`) instead of exact buy price.

## Quality engine
Scores business quality from:
- Revenue growth consistency proxy
- Margin quality (`gross_margin`, `fcf_margin`)
- Leverage and dilution penalties
- Optional ROIC proxy bonus

## Timing engine
Scores market timing from:
- Price vs 50-day and 200-day moving averages
- RSI regime (overbought/oversold)
- Drawdown from 52-week high

## Event risk engine
Penalizes near-term uncertainty from:
- Upcoming earnings proximity
- Historical earnings gap magnitude

## Decision engine
Weighted blend (default):
- Valuation 40%
- Quality 30%
- Timing 20%
- Event risk 10%

Maps score + valuation context into buy-zone classes and confidence level.

## Limitations
- Mock data providers in v1
- Simplified formulas
- Should be decision support only, not investment advice
