import random
from backend.utils.pnr import generate_pnr
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import models, schemas

router = APIRouter()
@router.post("/reserve", response_model=schemas.BookingResponse)
def reserve_seat(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db)
):
    # 1️⃣ Fetch flight
    flight = db.query(models.Flight).filter(
        models.Flight.id == booking.flight_id
    ).first()

    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    # 2️⃣ Check seat availability
    if flight.available_seats < booking.seats_booked:
        raise HTTPException(
            status_code=400,
            detail="Not enough seats available"
        )

    # 3️⃣ Reduce seats (LOCKED IN TRANSACTION)
    flight.available_seats -= booking.seats_booked

    # 4️⃣ Create booking (PENDING)
    new_booking = models.Booking(
        flight_id=booking.flight_id,
        passenger_name=booking.passenger_name,
        passenger_email=booking.passenger_email,
        seats_booked=booking.seats_booked,
        price_paid=flight.price * booking.seats_booked,
        status="PENDING"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking
@router.post("/{booking_id}/passenger", response_model=schemas.BookingResponse)
def add_passenger_info(
    booking_id: int,
    passenger: schemas.PassengerUpdate,
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Cannot update passenger for this booking"
        )

    booking.passenger_name = passenger.passenger_name
    booking.passenger_email = passenger.passenger_email

    db.commit()
    db.refresh(booking)

    return booking
@router.post("/{booking_id}/payment", response_model=schemas.PaymentResponse)
def process_payment(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Payment already processed"
        )

    flight = db.query(models.Flight).filter(
        models.Flight.id == booking.flight_id
    ).first()

    payment_success = random.choice([True, False])

    if payment_success:
        booking.status = "CONFIRMED"
        booking.pnr = generate_pnr()

        db.commit()
        db.refresh(booking)

        return {
            "booking_id": booking.id,
            "status": booking.status,
            "pnr": booking.pnr,
            "message": "Payment successful"
        }

    # PAYMENT FAILED → rollback seats
    booking.status = "CANCELLED"
    flight.available_seats += booking.seats_booked

    db.commit()

    return {
        "booking_id": booking.id,
        "status": booking.status,
        "pnr": None,
        "message": "Payment failed, booking cancelled"
    }
@router.post("/{booking_id}/cancel", response_model=schemas.BookingResponse)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status == "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Booking already cancelled"
        )

    flight = db.query(models.Flight).filter(
        models.Flight.id == booking.flight_id
    ).first()

    booking.status = "CANCELLED"
    booking.pnr = None

    flight.available_seats += booking.seats_booked

    db.commit()
    db.refresh(booking)

    return booking
@router.get("/history", response_model=list[schemas.BookingResponse])
def booking_history(
    email: str,
    db: Session = Depends(get_db)
):
    bookings = db.query(models.Booking).filter(
        models.Booking.passenger_email == email
    ).all()

    return bookings
