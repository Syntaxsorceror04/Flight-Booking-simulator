from backend.database import Base, engine, SessionLocal
from backend.models import Airport, Airline, Flight
from datetime import datetime, timedelta
import random

def create_tables():
    Base.metadata.create_all(bind=engine)

def seed_airports(db):
    airports = [
        {"code":"DEL","name":"Indira Gandhi Intl","city":"New Delhi","country":"India"},
        {"code":"BLR","name":"Kempegowda Intl","city":"Bengaluru","country":"India"},
        {"code":"BOM","name":"Chhatrapati Shivaji Intl","city":"Mumbai","country":"India"},
        {"code":"MAA","name":"Chennai Intl","city":"Chennai","country":"India"},
        {"code":"HYD","name":"Rajiv Gandhi Intl","city":"Hyderabad","country":"India"},
        {"code":"GOI","name":"Dabolim Airport","city":"Goa","country":"India"},
        {"code":"CCU","name":"Netaji Subhash Chandra Bose","city":"Kolkata","country":"India"},
        {"code":"PNQ","name":"Pune Airport","city":"Pune","country":"India"},
    ]
    for a in airports:
        if not db.query(Airport).filter(Airport.code == a["code"]).first():
            db.add(Airport(**a))
    db.commit()

def seed_airlines(db):
    airlines = [
        {"code":"AI","name":"Air India"},
        {"code":"6E","name":"IndiGo"},
        {"code":"UK","name":"Vistara"},
    ]
    for a in airlines:
        if not db.query(Airline).filter(Airline.code == a["code"]).first():
            db.add(Airline(**a))
    db.commit()

def seed_flights(db):
    airlines = db.query(Airline).all()
    airport_codes = [a.code for a in db.query(Airport).all()]
    for airline in airlines:
        for day in range(1, 8):
            for _ in range(2):
                origin, dest = random.sample(airport_codes, 2)
                dep = datetime.now() + timedelta(days=day, hours=random.randint(0, 23))
                arr = dep + timedelta(hours=random.randint(1, 4))
                price = random.randint(2500, 10000)
                flight = Flight(
                    airline_id=airline.id,
                    flight_number=f"{airline.code}{random.randint(100,999)}",
                    origin=origin,
                    destination=dest,
                    departure_time=dep,
                    arrival_time=arr,
                    base_price=price,
                    total_seats=150,
                    available_seats=150
                )
                db.add(flight)
    db.commit()

def run_seed():
    create_tables()
    db = SessionLocal()
    try:
        seed_airports(db)
        seed_airlines(db)
        seed_flights(db)
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
    print("Seed complete")
