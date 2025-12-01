# File: backend/utils/external_feed.py
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.models import Flight

ORIGINS = ["DEL", "BLR", "BOM", "MAA", "HYD"]
DESTS = ["GOI", "CCU", "PNQ", "IXC", "TRV"]

def generate_random_flight(db: Session, airline_id: int = 1):
    origin = random.choice(ORIGINS)
    dest = random.choice([d for d in DESTS if d != origin])

    dep = datetime.now() + timedelta(days=random.randint(1, 10), hours=random.randint(0, 23))
    arr = dep + timedelta(hours=random.randint(1, 4), minutes=random.choice([0, 15, 30, 45]))

    flight = Flight(
        airline_id=airline_id,
        flight_number=f"AI{random.randint(100,999)}",
        origin=origin,
        destination=dest,
        departure_time=dep,
        arrival_time=arr,
        base_price=random.randint(3000, 9000),
        total_seats=150,
        available_seats=150
    )

    db.add(flight)
    db.commit()
    db.refresh(flight)
    return flight

def bulk_generate(db: Session, n: int = 5):
    created = []
    for _ in range(n):
        created.append(generate_random_flight(db))
    return created
