from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument

from database import traffic_log_collection
from .exceptions import TrafficLogNotFoundException
from .models.traffic_log_create import TrafficLogCreate
from .models.traffic_log_read import TrafficLogRead
from .models.traffic_log_update import TrafficLogUpdate


class TrafficLogRepository:

    @staticmethod
    def get(traffic_log_id: str) -> TrafficLogRead:
        """Retrieve a single TrafficLog by its unique id"""

        document = traffic_log_collection.find_one(
            {"_id": ObjectId(traffic_log_id)}
        )
        if not document:
            raise TrafficLogNotFoundException(traffic_log_id)

        return TrafficLogRead(**document)

    @staticmethod
    def create(create: TrafficLogCreate) -> (ObjectId, TrafficLogRead):
        """Create a TrafficLog and return its Read object"""

        result = traffic_log_collection.insert_one(create)
        assert result.acknowledged

        return result.inserted_id, TrafficLogRepository.get(result.inserted_id)

    @staticmethod
    def update(traffic_log_id: str, update: TrafficLogUpdate) -> TrafficLogRead:
        """Update a TrafficLog by giving only the fields to update"""

        new_traffic_log = {k: v for k, v in update.dict().items() if v is not None}
        new_traffic_log = jsonable_encoder(new_traffic_log, exclude_unset=True)

        result = traffic_log_collection.find_one_and_update(
            {"_id": ObjectId(traffic_log_id)},
            {"$set": new_traffic_log},
            return_document=ReturnDocument.AFTER
        )

        if not result:
            raise TrafficLogNotFoundException(identifier=traffic_log_id)

        return TrafficLogRead(**result)

    @staticmethod
    def delete(traffic_log_id: str):
        """Delete a TrafficLog given its unique id"""

        result = traffic_log_collection.find_one_and_delete(
            {"_id": ObjectId(traffic_log_id)}
        )

        if not result:
            raise TrafficLogNotFoundException(identifier=traffic_log_id)
