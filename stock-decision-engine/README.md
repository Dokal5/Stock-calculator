# stock-decision-engine

Transparent single-stock decision support app built with Python + Streamlit.

## What it does
For one ticker at a time, the app returns:
1. Current price
2. Fair value range (bear/base/bull)
3. Premium/discount vs fair value
4. Buy zone classification
5. Decision score out of 100
6. Timing state
7. Key risk flags
8. Plain-language explanation

## Tech stack
- Python
- Streamlit
- Pandas
- Plotly
- Pydantic
- PyYAML
- pytest

## Project structure
See `app/` for engines, providers, and UI, `config/` for YAML assumptions, `tests/` for unit tests, and `docs/` for methodology + spec.

## Setup
```bash
cd stock-decision-engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

## User flow
1. Enter ticker.
2. Adjust assumptions in sidebar.
3. Review fair value range, buy zone, timing state, and risk flags.
4. Inspect score breakdown and explanation text.

## Notes
- v1 uses mock data providers with clean interfaces for future API adapters.
- App intentionally outputs ranges and confidence, not a single exact buy price.
