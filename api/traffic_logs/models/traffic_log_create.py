from typing import List

from pydantic import AnyHttpUrl

from .traffic_log_headers import Headers
from .traffic_log_info import Info
from .traffic_log_update import TrafficLogUpdate


class TrafficLogCreate(TrafficLogUpdate):
    """Body of TrafficLog POST requests"""
    scheme: str
    http_version: str
    method: str
    server: Info
    client: Info
    url: AnyHttpUrl
    headers: List[Headers]
