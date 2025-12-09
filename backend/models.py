from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Airline(Base):
    __tablename__ = "airlines"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(200), nullable=False)

class Airport(Base):
    __tablename__ = "airports"
    code = Column(String(3), primary_key=True, index=True)  # IATA
    name = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, index=True)
    airline_id = Column(Integer, ForeignKey("airlines.id"), nullable=False)
    flight_number = Column(String(20), nullable=False)
    origin = Column(String(3), ForeignKey("airports.code"), nullable=False)
    destination = Column(String(3), ForeignKey("airports.code"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    base_price = Column(Integer, nullable=False)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)

    airline = relationship("Airline", lazy="joined")
    # fare_history relationship is defined on FareHistory via backref

class FareHistory(Base):
    __tablename__ = "fare_history"
    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    available_seats = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    flight = relationship("Flight", backref="fare_history_entries")
