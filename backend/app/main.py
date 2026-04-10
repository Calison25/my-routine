import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="My Routine API")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


from app.presentation.routers import categories, muscle_groups, workouts

app.include_router(categories.router)
app.include_router(muscle_groups.router)
app.include_router(workouts.router)


@app.get("/health")
async def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})
