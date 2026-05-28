from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class EndpointConfig(BaseModel):
    name: str
    url: HttpUrl


class StatusResult(BaseModel):
    name: str
    url: str
    is_up: bool
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    checked_at: datetime
    error: Optional[str] = None
