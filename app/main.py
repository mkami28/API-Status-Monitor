import asyncio
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.models import StatusResult
from app.monitor import check_all, load_config, load_endpoints
from app.templates import render_dashboard


status_store: Dict[str, StatusResult] = {}
monitor_task: asyncio.Task | None = None


async def monitoring_loop() -> None:
    global status_store

    while True:
        config = load_config()
        endpoints = load_endpoints(config)
        timeout_seconds = config.get("request_timeout_seconds", 5)
        interval_seconds = config.get("check_interval_seconds", 60)

        status_store = await check_all(endpoints, timeout_seconds)
        await asyncio.sleep(interval_seconds)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global monitor_task, status_store

    config = load_config()
    endpoints = load_endpoints(config)
    timeout_seconds = config.get("request_timeout_seconds", 5)
    status_store = await check_all(endpoints, timeout_seconds)

    monitor_task = asyncio.create_task(monitoring_loop())
    yield

    if monitor_task:
        monitor_task.cancel()


app = FastAPI(
    title="API Status Monitor",
    description="A lightweight API uptime monitor with a dashboard and JSON API.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", response_class=HTMLResponse)
async def dashboard() -> str:
    return render_dashboard(status_store)


@app.get("/api/status")
async def get_status() -> Dict[str, StatusResult]:
    return status_store


@app.post("/api/check-now")
async def check_now() -> Dict[str, StatusResult]:
    global status_store

    config = load_config()
    endpoints = load_endpoints(config)
    timeout_seconds = config.get("request_timeout_seconds", 5)
    status_store = await check_all(endpoints, timeout_seconds)
    return status_store


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
