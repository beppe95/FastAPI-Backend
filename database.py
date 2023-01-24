from pymongo import mongo_client

from config.database_setting import database_settings

client = mongo_client.MongoClient(database_settings.DATABASE_URL)
