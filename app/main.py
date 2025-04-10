import logging
from fastapi import FastAPI
from app.routers import table_router, reservation_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ReserveApp")

app.include_router(table_router.router)
app.include_router(reservation_router.router)
