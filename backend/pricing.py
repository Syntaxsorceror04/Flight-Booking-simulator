# ------------------------------
# File: backend/pricing.py
# ------------------------------
from datetime import datetime
from math import exp
from typing import Tuple

def hours_to_departure(departure_dt) -> float:
    now = datetime.utcnow()
    diff = departure_dt - now
    hours = diff.total_seconds() / 3600.0
    return max(hours, 0.0)

def calculate_dynamic_price(
    base_price: float,
    total_seats: int,
    available_seats: int,
    departure_dt,
    demand_factor: float = 0.0
) -> Tuple[int, dict]:
    """
    Compute dynamic price and return (price_int, breakdown).
    demand_factor: external simulated demand (0.0 neutral, >0 increases price)
    """
    if total_seats <= 0:
        total_seats = 1
    remaining_pct = max(0.0, min(1.0, available_seats / float(total_seats)))

    hours = hours_to_departure(departure_dt)

    # Time multiplier: smooth increase when departure is nearer
    if hours > 168:
        time_multiplier = 1.0
    else:
        time_multiplier = 1.0 + 1.5 * (1.0 - exp(-max(0.0, (168 - hours)) / 72.0))
        time_multiplier = max(1.0, min(time_multiplier, 4.0))

    seat_pressure_coef = 1.5
    seat_multiplier = 1.0 + seat_pressure_coef * (1.0 - remaining_pct)  # 1.0 -> 2.5

    demand_multiplier = 1.0 + float(demand_factor)

    raw = float(base_price) * time_multiplier * seat_multiplier * demand_multiplier

    min_price = max(1, int(round(base_price * 0.5)))
    max_price = max(min_price + 1, int(round(base_price * 4.0)))
    price = int(round(max(min_price, min(max_price, raw))))

    breakdown = {
        "base_price": base_price,
        "remaining_pct": round(remaining_pct, 3),
        "hours_to_departure": round(hours, 2),
        "time_multiplier": round(time_multiplier, 3),
        "seat_multiplier": round(seat_multiplier, 3),
        "demand_multiplier": round(demand_multiplier, 3),
        "raw_price": round(raw, 2),
        "clamped_min": min_price,
        "clamped_max": max_price,
    }
    return price, breakdown

