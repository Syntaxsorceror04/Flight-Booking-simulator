from fastapi import FastAPI
from backend.database import Base, engine
from backend.routers import flights as flights_router
from backend.background_tasks import background_simulator

import asyncio

# ensure tables exist (creates FareHistory too)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Booking Simulator - Milestone 2 (Dynamic Pricing)")

app.include_router(flights_router.router)

# startup/shutdown handlers for background simulator
background_task = None

@app.on_event("startup")
async def startup_event():
    global background_task
    # start background_simulator as a background asyncio task
    loop = asyncio.get_event_loop()
    background_task = loop.create_task(background_simulator(app))

@app.on_event("shutdown")
async def shutdown_event():
    global background_task
    if background_task:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass

@app.get("/")
def root():
    return {"service": "Flight Booking Simulator - Milestone 2", "status": "ok"}
