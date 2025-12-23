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
# =======================
# Booking Schemas (Milestone 3)
# =======================

# Step 1: Seat reservation request
class BookingCreate(BaseModel):
    flight_id: int
    seats: int


# Step 2: Passenger details update
class PassengerInfo(BaseModel):
    passenger_name: str
    passenger_email: str


# Response after booking creation
class BookingResponse(BaseModel):
    booking_id: int
    flight_id: int
    seats_booked: int
    price_paid: int
    status: str
    pnr: str | None

    class Config:
        from_attributes = True


# Payment response
class PaymentResponse(BaseModel):
    success: bool
    message: str
    pnr: str | None = None
from pydantic import BaseModel, EmailStr


class PassengerUpdate(BaseModel):
    passenger_name: str
    passenger_email: EmailStr
class PaymentResponse(BaseModel):
    booking_id: int
    status: str
    pnr: str | None = None
    message: str


