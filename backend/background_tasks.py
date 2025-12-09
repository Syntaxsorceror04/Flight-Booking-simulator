import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict

from backend.database import SessionLocal
from backend.models import Flight, FareHistory
from backend.pricing import calculate_dynamic_price

# configuration (tune these for demo)
SIM_INTERVAL_SECONDS = 15      # how often the simulator ticks
SIM_FLIGHTS_PER_TICK = 6       # how many flights to perturb each tick
MAX_SEAT_CHANGE = 5            # seats to book/cancel per action

async def background_simulator(app):
    """
    Long-running background task that simulates demand changes.
    It runs until cancelled.
    """
    try:
        while True:
            await asyncio.sleep(SIM_INTERVAL_SECONDS)
            # perform one simulation tick
            try:
                _ = run_simulation_once()
            except Exception:
                # swallow to keep background loop alive; in prod log properly
                pass
    except asyncio.CancelledError:
        return

def run_simulation_once(db=None, num_changes: int = 6) -> List[Dict]:
    """
    Run a single simulation tick. If db not provided, create a session.
    Returns a list of fare update summaries.
    """
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    results = []
    try:
        flights = db.query(Flight).all()
        if not flights:
            return results

        sample = random.sample(flights, min(len(flights), num_changes))
        for f in sample:
            # randomly book or cancel between 1..MAX_SEAT_CHANGE seats
            change = random.randint(1, MAX_SEAT_CHANGE)
            if random.random() < 0.75:
                # book seats (decrease availability)
                new_avail = max(0, f.available_seats - change)
            else:
                # cancel seats (increase availability)
                new_avail = min(f.total_seats, f.available_seats + change)

            if new_avail != f.available_seats:
                f.available_seats = new_avail
                price, breakdown = calculate_dynamic_price(
                    base_price=f.base_price,
                    total_seats=f.total_seats,
                    available_seats=f.available_seats,
                    departure_dt=f.departure_time,
                    demand_factor=random.uniform(0.0, 0.5)
                )
                fh = FareHistory(
                    flight_id=f.id,
                    available_seats=f.available_seats,
                    price=price,
                    timestamp=datetime.utcnow()
                )
                db.add(fh)
                db.add(f)
                db.commit()
                results.append({
                    "flight_id": f.id,
                    "new_available_seats": f.available_seats,
                    "price": price,
                    "breakdown": breakdown
                })
    finally:
        if own_session:
            db.close()
    return results
