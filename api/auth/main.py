import sys
import uuid

import aiohttp
import loguru
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from api.auth.exceptions import UnauthorizedException
from api.auth.utils import VerifyToken
from config.auth_setting import auth_settings, auth_endpoints

token_verifier = VerifyToken()

app = FastAPI(
    title="Auth Controller"
)

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
def echo():
    """
    Echo for auth module
    """
    return {"message": "Echo method"}


@app.post(
    "/auth/token",
    status_code=status.HTTP_200_OK,
    description="Retrieve access token from Auth0 provider "
                "(https://auth0.com/docs/secure/tokens/access-tokens/get-access-tokens)",
)
async def get_access_token():
    """
    Get access token from Auth0
    """
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):
        async with aiohttp.ClientSession() as session:

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

            async with session.post(
                    url=auth_endpoints.TOKEN_ENDPOINT,
                    data=access_token_body,
                    headers=headers
            ) as access_token_response:

                if access_token_response \
                        and access_token_response.status == 200 \
                        and 'content-type' in access_token_response.headers \
                        and 'application/json' in access_token_response.headers['content-type']:

                    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(await access_token_response.json()),
                        media_type="application/json",
                    )

                else:
                    logger.error(f"Error while retrieving access token - "
                                 f"Status {access_token_response.status}, "
                                 f"Error {access_token_response.json()}")


@app.post(
    "/auth/authorize",
    description="Validate a given access token",
)
async def authorize(access_token: str):
    try:
        token_verifier.verify(access_token)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=None,
            media_type="application/json",
        )
    except UnauthorizedException as uex:

        error_message = f"Error validating access token, message={uex.message}"

        logger.error(error_message)

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder({"message": error_message}, exclude_none=True),
            media_type="application/json",
        )
