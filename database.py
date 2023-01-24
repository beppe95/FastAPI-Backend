from pymongo import mongo_client

from config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
