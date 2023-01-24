from pydantic import BaseSettings


class AuthEndpoints(BaseSettings):
    TOKEN_ENDPOINT: str
    AUTHORIZE_ENDPOINT: str
    JWKS_ENDPOINT: str

    class Config:
        env_file = "./.env"


class AuthSettings(BaseSettings):
    GRANT_TYPE: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    AUDIENCE: str
    ISSUER: str
    ALGORITHM: str

    class Config:
        env_file = "./.env"


auth_settings = AuthSettings()
auth_endpoints = AuthEndpoints()
