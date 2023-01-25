from pydantic import BaseModel


class Headers(BaseModel):
    key: str
    value: str
