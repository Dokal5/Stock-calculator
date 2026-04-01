from __future__ import annotations


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def score_to_band(score: float) -> str:
    if score >= 80:
        return "Strong"
    if score >= 65:
        return "Moderate"
    if score >= 45:
        return "Cautious"
    return "Weak"
