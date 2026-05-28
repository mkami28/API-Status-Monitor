import asyncio
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import httpx
import yaml

from app.models import EndpointConfig, StatusResult


CONFIG_PATH = Path("config.yaml")


def load_config(path: Path = CONFIG_PATH) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    data.setdefault("check_interval_seconds", 60)
    data.setdefault("request_timeout_seconds", 5)
    data.setdefault("endpoints", [])
    return data


def load_endpoints(config: dict) -> List[EndpointConfig]:
    return [EndpointConfig(**endpoint) for endpoint in config.get("endpoints", [])]


async def check_endpoint(endpoint: EndpointConfig, timeout_seconds: int = 5) -> StatusResult:
    started = time.perf_counter()

    try:
        async with httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=True) as client:
            response = await client.get(str(endpoint.url))

        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        is_up = 200 <= response.status_code < 400

        return StatusResult(
            name=endpoint.name,
            url=str(endpoint.url),
            is_up=is_up,
            status_code=response.status_code,
            response_time_ms=elapsed_ms,
            checked_at=datetime.now(timezone.utc),
            error=None,
        )

    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return StatusResult(
            name=endpoint.name,
            url=str(endpoint.url),
            is_up=False,
            status_code=None,
            response_time_ms=elapsed_ms,
            checked_at=datetime.now(timezone.utc),
            error=str(exc),
        )


async def check_all(endpoints: List[EndpointConfig], timeout_seconds: int = 5) -> Dict[str, StatusResult]:
    checks = [check_endpoint(endpoint, timeout_seconds) for endpoint in endpoints]
    results = await asyncio.gather(*checks)
    return {result.name: result for result in results}
