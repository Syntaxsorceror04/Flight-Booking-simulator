Flight Booking Simulator – Backend

**Infosys Springboard Wingspire Internship**
**Python Backend | FastAPI | SQLite | SQLAlchemy**

This project implements a **flight booking backend system** with **dynamic pricing, demand simulation, and a complete booking workflow**.
It is built incrementally across internship milestones, following real-world backend engineering practices.

---

## 🧱 Tech Stack

* **FastAPI** – REST API framework
* **SQLite** – Lightweight relational database
* **SQLAlchemy ORM** – Database modeling & transactions
* **Pydantic** – Request/response validation
* **Uvicorn** – ASGI server

---

## 🚀 Features by Milestone

---

## ✅ Milestone 1 – Core Flight Management

### Implemented Features

* Modular FastAPI backend structure
* SQLite database with SQLAlchemy ORM
* Database models for:

  * Airlines
  * Airports
  * Flights
* Flight search with filters:

  * Origin
  * Destination
  * Date
* Sorting options:

  * Price
  * Duration
  * Departure time
* Database seeding with sample airlines, airports, and flights
* Automatic random flight generation API

### Core APIs

| Method | Endpoint          | Description             |
| ------ | ----------------- | ----------------------- |
| GET    | `/`               | Health check            |
| GET    | `/flights`        | Get all flights         |
| GET    | `/flights/search` | Search flights          |
| GET    | `/airlines`       | Get all airlines        |
| GET    | `/airports`       | Get all airports        |
| POST   | `/utils/generate` | Generate random flights |

---

## 🔥 Milestone 2 – Dynamic Pricing & Demand Simulation

### New Features Added

#### Dynamic Pricing Engine

Flight prices update dynamically based on:

* Remaining seats
* Time left to departure
* Demand pressure

#### Fare History Tracking

* Each price update is recorded in `FareHistory`
* Historical prices can be queried per flight

#### Background Demand Simulator

* Runs automatically after server startup
* Simulates:

  * Random seat bookings & cancellations
  * Price recalculations
  * Fare history insertion

#### Manual Demand Simulation

* Trigger one simulation tick manually for demo/testing

### Additional APIs

| Method | Endpoint                         | Description                   |
| ------ | -------------------------------- | ----------------------------- |
| GET    | `/flights/{id}/fare-history`     | View historical price changes |
| POST   | `/utils/simulate-demand?count=5` | Run demand simulation         |

All flight responses now include:

* `current_price`
* `price_breakdown` (time, demand, seat pressure multipliers)

---

## 🧾 Milestone 3 – Booking Workflow & Transaction Management

### Booking Lifecycle Implemented

* Seat reservation with **transaction safety**
* Passenger information capture
* Simulated payment processing (success/failure)
* Automatic **PNR generation** for confirmed bookings
* Booking cancellation with seat restoration
* Booking history retrieval by passenger email

### Key Backend Concepts Used

* Database transactions to prevent overbooking
* Multi-step booking workflow
* Concurrency-safe seat updates
* Persistent booking storage

---

## 📁 Project Structure

```
flight-booking-backend/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed_data.py
│   ├── routers/
│   │   ├── flights.py
│   │   └── bookings.py
│   └── utils/
│       ├── external_feed.py
│       └── pnr.py
│
├── requirements.txt
├── README.md
└── venv/   (ignored)
```

---

## 🛠️ How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/flight-booking-backend.git
cd flight-booking-backend
```

### 2️⃣ Create & Activate Virtual Environment (Windows)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Seed Database

```bash
python -m backend.seed_data
```

### 5️⃣ Start Server

```bash
uvicorn backend.main:app --reload --port 8000
```

---

## 📌 API Documentation

Once running, access:

* **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc** → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

