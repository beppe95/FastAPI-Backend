import sys
import uuid

import loguru
from fastapi import FastAPI, status, Path, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer

from api.traffic_logs.schemas import TrafficLogResponse
from .exceptions import *
from .models.traffic_log_create import TrafficLogCreate
from .models.traffic_log_update import TrafficLogUpdate
from .repositories import TrafficLogRepository
from ..auth import main as auth_app
from ..auth.exceptions import UnauthorizedException, ForbiddenException

# Scheme for the Authorization header
token_auth_scheme = HTTPBearer()

app = FastAPI(
    title="Traffic Logs Controller"
)

logger = loguru.logger
logger.remove()
logger.add(
    sys.stdout,
    format="{time} - {level} - ({extra[request_id]}) {message} ",
    level="INFO"
)


@app.get(
    "/agent/traffic_logs/echo",
    status_code=status.HTTP_200_OK
)
def echo():
    """
    Echo for traffic_logs module
    """
    return {"message": "Echo method"}


@app.get(
    "/agent/traffic_logs/{traffic_log_id}",
    description="Fetch a single TrafficLog by its ID",
    response_model=TrafficLogResponse
)
def fetch_traffic_log(
        traffic_log_id: str = Path(title="The ID of the traffic log to retrieve"),
        access_token: str = Depends(token_auth_scheme)
):
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):

        try:

            auth_app.authorize(access_token.credentials)

            logger.info(f"Fetching traffic log ID {traffic_log_id}")

            result = TrafficLogRepository.get(traffic_log_id)

            logger.info(f"Successfully retrieved traffic log {result}")

            response = TrafficLogResponse(
                status=status.HTTP_200_OK,
                message=f"Traffic log ID {traffic_log_id} found",
                traffic_log=result
            )

            return JSONResponse(
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )

        except UnauthorizedException:

            response = TrafficLogResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                message=f"Unauthorized to retrieve Traffic log ID {traffic_log_id}"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )

        except ForbiddenException:

            response = TrafficLogResponse(
                status=status.HTTP_403_FORBIDDEN,
                message=f"Traffic log ID {traffic_log_id} cannot be accessed"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )

        except TrafficLogNotFoundException:

            response = TrafficLogResponse(
                status=status.HTTP_404_NOT_FOUND,
                message=f"Traffic log ID {traffic_log_id} not found"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )


@app.patch(
    "/agent/traffic_logs/{traffic_log_id}",
    description="Patch a single TrafficLog by its ID",
    response_model=TrafficLogResponse
)
def patch_traffic_log(
        traffic_log_update: TrafficLogUpdate,
        traffic_log_id: str = Path(title="The ID of the traffic log to retrieve"),
        access_token: str = Depends(token_auth_scheme)

):
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):

        logger.info(f"Fetching traffic log ID {traffic_log_id}")

        try:

            auth_app.authorize(access_token.credentials)

            result = TrafficLogRepository.update(traffic_log_id, traffic_log_update)

            response = TrafficLogResponse(
                status=status.HTTP_200_OK,
                message=f"Traffic log ID {traffic_log_id} updated",
                traffic_log=result
            )

            return JSONResponse(
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json"
            )

        except UnauthorizedException:

            response = TrafficLogResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                message=f"Unauthorized to update Traffic log ID {traffic_log_id}"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )

        except ForbiddenException:

            response = TrafficLogResponse(
                status=status.HTTP_403_FORBIDDEN,
                message=f"Traffic log ID {traffic_log_id} cannot be updated"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )

        except TrafficLogNotFoundException:

            response = TrafficLogResponse(
                status=status.HTTP_404_NOT_FOUND,
                message=f"Traffic log ID {traffic_log_id} not found"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )


@app.delete(
    "/agent/traffic_logs/{traffic_log_id}",
    description="Delete a single TrafficLog by ID",
    status_code=status.HTTP_200_OK,
    response_model=TrafficLogResponse
)
def delete_traffic_log(
        traffic_log_id: str = Path(title="The ID of the traffic log to delete"),
        access_token: str = Depends(token_auth_scheme)
):
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):

        logger.info(f"Fetching traffic log ID {traffic_log_id}")

        try:

            auth_app.authorize(access_token.credentials)

            TrafficLogRepository.delete(traffic_log_id)

            logger.info(f"Successfully deleted traffic log ID {traffic_log_id}")

            response = TrafficLogResponse(
                status=status.HTTP_200_OK,
                message=f"Traffic log ID {traffic_log_id} deleted",
                traffic_log=None
            )

            return JSONResponse(
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json"
            )

        except UnauthorizedException:

            response = TrafficLogResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                message=f"Unauthorized to delete Traffic log ID {traffic_log_id}"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )

        except ForbiddenException:

            response = TrafficLogResponse(
                status=status.HTTP_403_FORBIDDEN,
                message=f"Traffic log ID {traffic_log_id} cannot be deleted"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )

        except TrafficLogNotFoundException:
            response = TrafficLogResponse(
                status=status.HTTP_404_NOT_FOUND,
                message=f"Traffic log ID {traffic_log_id} not found"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )


@app.post(
    "/agent/traffic_logs",
    description="Create a new traffic log",
    response_model=TrafficLogResponse
)
async def create_traffic_log(
        request: TrafficLogCreate,
        access_token: str = Depends(token_auth_scheme)
):
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):

        try:

            await auth_app.authorize(access_token.credentials)

            traffic_log_request = jsonable_encoder(request)

            logger.info(f"Received request {request}")

            resultId, result = TrafficLogRepository.create(traffic_log_request)

            logger.info(f"Successfully created TrafficLog {result}")

            response = TrafficLogResponse(
                status=status.HTTP_201_CREATED,
                message=f"Traffic log ID {resultId} created",
                traffic_log=result
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json"
            )

        except UnauthorizedException:

            response = TrafficLogResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized to create new Traffic log"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )

        except ForbiddenException:

            response = TrafficLogResponse(
                status=status.HTTP_403_FORBIDDEN,
                message="Resource forbidden, cannot create new Traffic log"
            )

            return JSONResponse(
                status_code=response.status,
                content=jsonable_encoder(response, exclude_none=True),
                media_type="application/json",
            )
