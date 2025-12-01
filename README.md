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
http://127.0.0.1:8000/redoc