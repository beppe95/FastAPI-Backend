import sys
import uuid

import loguru
from bson.objectid import ObjectId
from fastapi import FastAPI, status, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo import ReturnDocument

from api.traffic_logs.schemas import TrafficLogRequest, TrafficLogOptional, TrafficLogResponse
from database import client

DATABASE = "ermes"
TRAFFIC_LOGS_COLLECTION = "traffic_logs"

app = FastAPI()

logger = loguru.logger
logger.remove()
logger.add(
    sys.stdout,
    format="{time} - {level} - ({extra[request_id]}) {message} ",
    level="INFO"
)


@app.get(
    "/traffic_log/echo",
    status_code=status.HTTP_200_OK
)
async def echo():
    logger.info("Logging from echo method")
    return {"message": "Echo method"}


@app.get(
    "/traffic_log/{traffic_log_id}",
    status_code=status.HTTP_200_OK,
    response_model=TrafficLogResponse
)
def fetch_traffic_log(
        *,
        traffic_log_id: str = Path(title="The ID of the traffic log to retrieve")
):
    """
    Fetch a single TrafficLog by ID
    """
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):
        logger.info(f"Fetching traffic log ID {traffic_log_id}")

        traffic_log_collection = client[DATABASE][TRAFFIC_LOGS_COLLECTION]

        result = traffic_log_collection.find_one(
            {"_id": ObjectId(traffic_log_id)}
        )

        if not result:
            response = TrafficLogResponse(
                status=status.HTTP_404_NOT_FOUND,
                message=f"Traffic log ID {traffic_log_id} not found",
                traffic_log=None
            )

            return JSONResponse(
                content=jsonable_encoder(response, exclude_none=True),
                status_code=status.HTTP_404_NOT_FOUND,
                media_type="application/json"
            )

        logger.info(f"Successfully retrieved traffic log ID {traffic_log_id}")

        traffic_log = TrafficLogOptional(
            scheme=result['scheme'],
            http_version=result['http_version'],
            method=result['method'],
            server=result['server'],
            client=result['client'],
            headers=result['headers'],
            body=result['body']
        )

        response = TrafficLogResponse(
            status=status.HTTP_200_OK,
            message=f"Traffic log ID {traffic_log_id} found",
            traffic_log=traffic_log
        )

        return JSONResponse(
            content=jsonable_encoder(response, exclude_none=True),
            media_type="application/json",
        )


@app.delete(
    "/traffic_log/{traffic_log_id}",
    status_code=status.HTTP_200_OK,
    response_model=TrafficLogResponse
)
def delete_traffic_log(
        *,
        traffic_log_id: str = Path(title="The ID of the traffic log to delete")
):
    """
    Delete a single TrafficLog by ID
    """
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):
        logger.info(f"Fetching traffic log ID {traffic_log_id}")

        traffic_log_collection = client[DATABASE][TRAFFIC_LOGS_COLLECTION]

        result = traffic_log_collection.find_one_and_delete(
            {"_id": ObjectId(traffic_log_id)}
        )

        if not result:
            response = TrafficLogResponse(
                status=status.HTTP_404_NOT_FOUND,
                message=f"Traffic log ID {traffic_log_id} not found",
                traffic_log=None
            )

            return JSONResponse(
                content=jsonable_encoder(response, exclude_none=True),
                status_code=status.HTTP_404_NOT_FOUND,
                media_type="application/json"
            )

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


@app.patch(
    "/traffic_log/{traffic_log_id}",
    status_code=status.HTTP_200_OK,
    response_model=TrafficLogResponse
)
async def patch_traffic_log(
        *,
        traffic_log_id: str = Path(title="The ID of the traffic log to retrieve"),
        traffic_log_update: TrafficLogOptional
):
    """
    Patch a single TrafficLog by ID
    """
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):

        logger.info(f"Fetching traffic log ID {traffic_log_id}")

        traffic_log_collection = client[DATABASE][TRAFFIC_LOGS_COLLECTION]

        new_traffic_log = {k: v for k, v in traffic_log_update.dict().items() if v is not None}
        new_traffic_log = jsonable_encoder(new_traffic_log)

        if len(new_traffic_log) == 0:
            logger.warning("New traffic log was empty, no update will be done")

            response = TrafficLogResponse(
                status=status.HTTP_200_OK,
                message=f"New traffic log was empty, no update will be done",
                traffic_log=None
            )

            return JSONResponse(
                content=jsonable_encoder(response, exclude_none=True),
                status_code=status.HTTP_404_NOT_FOUND,
                media_type="application/json"
            )

        result = await traffic_log_collection.find_one_and_update(
            {"_id": ObjectId(traffic_log_id)},
            {"$set": {new_traffic_log}},
            return_document=ReturnDocument.AFTER
        )

        if not result:
            response = TrafficLogResponse(
                status=status.HTTP_404_NOT_FOUND,
                message=f"Traffic log ID {traffic_log_id} not found",
                traffic_log=None
            )

            return JSONResponse(
                content=jsonable_encoder(response, exclude_none=True),
                status_code=status.HTTP_404_NOT_FOUND,
                media_type="application/json"
            )

        logger.info(f"Successfully updated traffic log ID {traffic_log_id}")

        traffic_log = TrafficLogOptional(
            scheme=result['scheme'],
            http_version=result['http_version'],
            method=result['method'],
            server=result['server'],
            client=result['client'],
            headers=result['headers'],
            body=result['body']
        )

        response = TrafficLogResponse(
            status=status.HTTP_200_OK,
            message=f"Traffic log ID {traffic_log_id} updated",
            traffic_log=traffic_log
        )

        return JSONResponse(
            content=jsonable_encoder(response, exclude_none=True),
            media_type="application/json"
        )


@app.post(
    "/traffic_log",
    status_code=status.HTTP_201_CREATED,
    response_model=TrafficLogResponse,
    response_model_exclude_none=True
)
def create_traffic_log(request: TrafficLogRequest):
    """
    Insert a new HTTP traffic log
    """
    request_id = str(uuid.uuid4())

    with logger.contextualize(request_id=request_id):
        request = jsonable_encoder(request)

        logger.info(f"Received request {request}")

        traffic_log_collection = client[DATABASE][TRAFFIC_LOGS_COLLECTION]
        result = traffic_log_collection.insert_one(request)
        logger.info(f"Successfully created TrafficLog with ID {result.inserted_id}")

        logger.info(type(result.inserted_id))

        response = TrafficLogResponse(
            status=status.HTTP_201_CREATED,
            id=str(result.inserted_id),
            message=f"Traffic log ID {result.inserted_id} created",
            traffic_log=None
        )

        return JSONResponse(
            content=jsonable_encoder(response, exclude_none=True),
            media_type="application/json"
        )
