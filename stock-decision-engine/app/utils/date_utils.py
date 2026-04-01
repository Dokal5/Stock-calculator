from __future__ import annotations

from datetime import date


def days_until(target: date | None, today: date | None = None) -> int | None:
    if target is None:
        return None
    ref = today or date.today()
    return (target - ref).days
