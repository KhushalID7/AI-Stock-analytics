from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path

from apps.api.routes_health import router as health_router
from apps.api.routes_agent import router as agent_router

# Load environment variables from .env once at startup
load_dotenv()

app = FastAPI(title="AI Stock Analytics API")


app.include_router(health_router)
app.include_router(agent_router)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")