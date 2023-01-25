from pymongo import MongoClient

from config.database_setting import database_settings

client = MongoClient(database_settings.URI)
traffic_log_collection = client[database_settings.MONGO_DATABASE][database_settings.LOGS_COLLECTION]
