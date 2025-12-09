This backend project is built using FastAPI, SQLite, and SQLAlchemy.
It simulates a flight booking system with dynamic pricing, airline data, airport data, and a seeded database of sample flights.

🚀 Features Implemented (Milestone 1)
✔ Core Functionalities

FastAPI backend with clean modular structure

SQLite database with SQLAlchemy ORM

Models for:

Airlines

Airports

Flights

Dynamic flight pricing (changes based on demand)

Flight search based on:

Origin

Destination

Date

Sorting options (price, duration, departure time)

Sample seed data generation

Automatic sample flight generation API

✔ API Endpoints
Method	Endpoint	Description
GET	/	Health check
GET	/flights	Get all flights
GET	/flights/search	Search flights
GET	/airlines	Get all airlines
GET	/airports	Get all airports
POST	/utils/generate	Generate random flights
<br>
📁 Project Structure
flight-booking-backend/
│── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   ├── seed_data.py
│   ├── routers/
│   │   └── flights.py
│   └── utils/
│       └── external_feed.py
│
├── requirements.txt
├── README.md
└── venv/  (ignored)

🛠️ How to Run Locally
1. Clone the Repository
git clone https://github.com/<your-username>/flight-booking-backend.git
cd flight-booking-backend

2. Create & Activate Virtual Environment

Windows:

python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install Dependencies
pip install -r requirements.txt

4. Seed the Database
python -m backend.seed_data

5. Start the Server
.\venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000

📌 API Documentation

Once the server is running, open:

👉 Swagger UI:
http://127.0.0.1:8000/docs

👉 ReDoc:

http://127.0.0.1:8000/redoc# Flight Booking Simulator – Backend  
### Infosys Springboard Wingspire Internship — Milestone 2  

This backend project is built using **FastAPI**, **SQLite**, and **SQLAlchemy**.  
It simulates a flight booking system with **dynamic pricing**, **airline data**, **airport data**, **fare history tracking**, and **automatic demand simulation**.

## 🚀 Features Implemented (Milestone 2)

### ✔ Core Functionalities (from Milestone 1)
- FastAPI backend with modular routing
- SQLite database with SQLAlchemy ORM  
- Models for:
  - Airlines  
  - Airports  
  - Flights  
- Flight search based on:
  - Origin  
  - Destination  
  - Date  
  - Sort by price or duration  
- Database seeding with sample data  
- Automatic sample flight generation API  

---

## 🔥 **New Features Added in Milestone 2**
### ✔ **Dynamic Pricing Engine**
- Real-time price calculation based on:
  - Remaining seats  
  - Hours left to departure  
  - Demand factor  

### ✔ **Fare History Tracking**
- Every time the simulator updates seat availability,
  the system:
  - recalculates price  
  - inserts a new **FareHistory** record  

`GET /flights/{id}/fare-history`  
returns time series price history.

### ✔ **Background Demand Simulator**
Runs automatically every few seconds and:
- randomly books/cancels seats  
- recalculates prices  
- stores fare history  

Works continuously in the background after server startup.

### ✔ **Manual Demand Simulation**
`POST /utils/simulate-demand?count=5`  
Runs one simulation tick instantly (useful for demos).

### ✔ **Current Price in All Flight Responses**
Every `GET /flights` and `GET /flights/search` response now includes:
- `current_price`  
- `price_breakdown` (multipliers: time, demand, seat pressure)

---

## ⚙️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/flights` | Get all flights with dynamic pricing |
| GET | `/flights/search` | Search flights by origin, destination, date |
| GET | `/airlines` | Get all airlines |
| GET | `/airports` | Get all airports |
| GET | `/flights/{id}/fare-history` | View historical price changes |
| POST | `/utils/generate` | Generate random flights |
| POST | `/utils/simulate-demand` | Run one demand simulation tick |

