from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Flight, Airport, Airline
from backend.schemas import FlightOut, AirportOut, AirlineOut
from typing import List
from datetime import datetime
from backend.utils.external_feed import bulk_generate

router = APIRouter(prefix="", tags=["Flights"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/airports", response_model=List[AirportOut])
def list_airports(db: Session = Depends(get_db)):
    return db.query(Airport).all()

@router.get("/airlines", response_model=List[AirlineOut])
def list_airlines(db: Session = Depends(get_db)):
    return db.query(Airline).all()

@router.get("/flights", response_model=List[FlightOut])
def get_all_flights(db: Session = Depends(get_db)):
    return db.query(Flight).all()

@router.get("/flights/search", response_model=List[FlightOut])
def search_flights(
    origin: str,
    destination: str,
    date: str,
    sort_by: str = Query("price", regex="^(price|duration)$"),
    db: Session = Depends(get_db)
):
    origin = origin.upper()
    destination = destination.upper()

    if origin == destination:
        raise HTTPException(400, "origin and destination cannot be same")

    if not db.query(Airport).filter(Airport.code == origin).first():
        raise HTTPException(400, "Invalid origin airport")

    if not db.query(Airport).filter(Airport.code == destination).first():
        raise HTTPException(400, "Invalid destination airport")

    try:
        date_parsed = datetime.strptime(date, "%Y-%m-%d").date()
    except:
        raise HTTPException(400, "Date must be YYYY-MM-DD")

    flights = db.query(Flight).filter(
        Flight.origin == origin,
        Flight.destination == destination
    ).all()

    flights = [f for f in flights if f.departure_time.date() == date_parsed]

    if sort_by == "price":
        flights.sort(key=lambda f: f.base_price)
    else:
        flights.sort(key=lambda f: (f.arrival_time - f.departure_time))

    return flights

@router.post("/utils/generate", response_model=List[FlightOut])
def generate_flights(count: int = Query(5, ge=1, le=100), db: Session = Depends(get_db)):
    return bulk_generate(db, n=count)
