import sys
import uuid

import loguru
import requests
from fastapi import FastAPI, status

from config.auth_setting import auth_settings, auth_endpoints

app = FastAPI()

logger = loguru.logger
logger.remove()
logger.add(
    sys.stdout,
    format="{time} - {level} - ({extra[request_id]}) {message} ",
    level="INFO"
)


@app.get(
    "/auth/echo",
    status_code=status.HTTP_200_OK
)
async def echo():
    """
    Echo for auth module
    """
    logger.info("Logging from echo method")
    return {"message": "Echo method"}


@app.post(
    "/auth/token",
    status_code=status.HTTP_200_OK
)
def get_access_token():
    """
    Get access token from Auth0
    """
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):
        with requests.Session() as session:

            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            access_token_body = {
                "grant_type": auth_settings.GRANT_TYPE,
                "client_id": auth_settings.CLIENT_ID,
                "client_secret": auth_settings.CLIENT_SECRET,
                "audience": auth_settings.AUDIENCE
            }

            access_token_response = session.post(
                url=auth_endpoints.AUTH_ENDPOINT,
                data=access_token_body,
                headers=headers
            )

            if access_token_response \
                    and access_token_response.status_code == 200 \
                    and 'content-type' in access_token_response.headers \
                    and 'application/json' in access_token_response.headers['content-type']:
                return access_token_response.json()
            else:
                logger.error(f"Error while retrieving access token - "
                             f"Status {access_token_response.status_code}, "
                             f"Error {access_token_response.json()}")


@app.post(
    "/auth/authorize",
    status_code=status.HTTP_200_OK
)
async def authorize():

    return {"message": "Server up and running!"}
