"""
Main

FastAPI application entry point. Initializes the database and registers
the routers.

@author adrianpmdev
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import clicks, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Click Reports",
    description="Internal service that summarizes product clicks into simple statistics.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(clicks.router)
app.include_router(stats.router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
