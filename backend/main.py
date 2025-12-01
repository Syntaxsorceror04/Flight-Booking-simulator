from fastapi import FastAPI
from backend.database import Base, engine
from backend.routers import flights as flights_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Booking Simulator - Milestone 1")
app.include_router(flights_router.router)

@app.get("/")
def root():
    return {"service": "Flight Booking Simulator - Milestone 1", "status": "ok"}
