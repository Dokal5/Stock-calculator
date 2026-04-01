# Data Dictionary

## MarketSnapshot
- `current_price`: latest traded price (mock seeded)
- `high_52w`: rolling 52-week high
- `sma_50`, `sma_200`: simple moving averages
- `rsi_14`: RSI regime indicator

## FundamentalSnapshot
- `revenue_growth_3y`: annualized growth proxy
- `gross_margin`, `fcf_margin`: profitability + cash conversion
- `debt_to_ebitda`: leverage stress indicator
- `share_dilution_3y`: issuance pressure proxy
- `owner_earnings_per_share`: valuation anchor

## EventSnapshot
- `next_earnings_date`: event proximity signal
- `recent_earnings_gap_pct`: prior earnings volatility proxy
