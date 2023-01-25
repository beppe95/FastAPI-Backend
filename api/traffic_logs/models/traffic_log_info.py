from pydantic import BaseModel


class Info(BaseModel):
    host: str
    port: int
