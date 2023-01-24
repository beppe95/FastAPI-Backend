from typing import List, Optional

from pydantic import BaseModel, Field, AnyHttpUrl


class Headers(BaseModel):
    key: str
    value: str


class Info(BaseModel):
    host: str
    port: int


class TrafficLogRequest(BaseModel):
    scheme: str
    http_version: str
    method: str
    server: Info
    client: Info
    url: AnyHttpUrl
    headers: List[Headers]
    body: Optional[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "scheme": "http",
                "http_version": "1.1",
                "method": "GET",
                "server": {
                    "host": "localhost",
                    "port": 8000
                },
                "client": {
                    "host": "127.0.0.1",
                    "port": 5500
                },
                "headers": [
                    {
                        "key": "",
                        "value": ""
                    },
                    {
                        "key": "",
                        "value": ""
                    },
                ],
                "body": "",
            }
        }


class TrafficLogOptional(TrafficLogRequest):
    __annotations__ = {k: Optional[v] for k, v in TrafficLogRequest.__annotations__.items()}


class TrafficLogResponse(BaseModel):
    status: int
    id: Optional[str]
    message: str
    traffic_log: Optional[TrafficLogOptional] = Field(None)


class TrafficLog(BaseModel):
    id: int
