from typing import Optional, List

from pydantic import BaseModel, AnyHttpUrl

from .traffic_log_headers import Headers
from .traffic_log_info import Info


class TrafficLogUpdate(BaseModel):
    """Body of TrafficLog for PATCH requests"""
    scheme: Optional[str]
    http_version: Optional[str]
    method: Optional[str]
    server: Optional[Info]
    client: Optional[Info]
    url: Optional[AnyHttpUrl]
    headers: Optional[List[Headers]]
    body: Optional[str]
