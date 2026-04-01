# Agent Guidelines for `stock-decision-engine`

## Core principles
1. Preserve modularity across providers, engines, UI, and models.
2. Keep calculations transparent: expose assumptions and intermediate values.
3. Never output a single "magic" buy price; always return ranges and confidence.
4. Favor deterministic, testable logic over hidden heuristics.
5. Add or update tests whenever engine logic changes.

## Coding rules
- Maintain clean interfaces between `services/` and `engines/`.
- Keep business logic in engine modules, not Streamlit UI files.
- Use Pydantic models for cross-module data contracts.
- Read configurable behavior from YAML files in `config/`.
- Handle missing data with safe defaults and explicit warnings.

## Testing expectations
- Run `pytest` before finalizing changes.
- Include edge cases for missing fields, negative earnings proxies, and leverage stress.

## Documentation expectations
- Update `docs/methodology.md` when formulas or scoring weights change.
- Keep README setup instructions synchronized with real commands.
