import sys
import uuid

import loguru
import uvicorn
from fastapi import FastAPI, status, Path
from fastapi.encoders import jsonable_encoder

from api.traffic_logs.schemas import TrafficLogResponse
from .exceptions import *
from .models.traffic_log_create import TrafficLogCreate
from .models.traffic_log_update import TrafficLogUpdate
from .repositories import TrafficLogRepository

app = FastAPI(
    title="FastAPI Backend"
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
async def echo():
    logger.info("Logging from echo method")
    return {"message": "Echo method"}


@app.get(
    "/agent/traffic_logs/{traffic_log_id}",
    description="Fetch a single TrafficLog by its ID",
    response_model=TrafficLogResponse
)
def fetch_traffic_log(
        *,
        traffic_log_id: str = Path(title="The ID of the traffic log to retrieve")
):
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):
        logger.info(f"Fetching traffic log ID {traffic_log_id}")

        try:
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
        *,
        traffic_log_id: str = Path(title="The ID of the traffic log to retrieve"),
        traffic_log_update: TrafficLogUpdate
):
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):

        logger.info(f"Fetching traffic log ID {traffic_log_id}")

        try:

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
        *,
        traffic_log_id: str = Path(title="The ID of the traffic log to delete")
):
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):
        logger.info(f"Fetching traffic log ID {traffic_log_id}")

        try:

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
def create_traffic_log(
        request: TrafficLogCreate
):
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):
        traffic_log_request = jsonable_encoder(request)

        logger.info(f"Received request {request}")

        result = TrafficLogRepository.create(traffic_log_request)

        logger.info(f"Successfully created TrafficLog {result}")

        response = TrafficLogResponse(
            status=status.HTTP_201_CREATED,
            message="Traffic log created",
            traffic_log=result
        )

        return JSONResponse(
            status_code=response.status,
            content=jsonable_encoder(response, exclude_none=True),
            media_type="application/json"
        )


def run():
    uvicorn.run(
        app,
        host="localhost",
        port=8000
    )
