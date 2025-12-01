from pydantic import BaseModel, constr
from datetime import datetime

class AirportOut(BaseModel):
    code: str
    name: str
    city: str
    country: str
    class Config:
        orm_mode = True

class AirlineOut(BaseModel):
    id: int
    code: str
    name: str
    class Config:
        orm_mode = True

class FlightOut(BaseModel):
    id: int
    flight_number: str
    airline_id: int
    origin: constr(min_length=3, max_length=3)
    destination: constr(min_length=3, max_length=3)
    departure_time: datetime
    arrival_time: datetime
    base_price: int
    total_seats: int
    available_seats: int
    class Config:
        orm_mode = True
