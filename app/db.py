from pymongo import MongoClient
from app.config import settings

_client = MongoClient(settings.MONGODB_URI)
_db = _client[settings.MONGODB_DB]

def candidates_coll():
    return _db["candidates"]
