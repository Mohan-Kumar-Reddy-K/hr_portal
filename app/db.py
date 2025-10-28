from pymongo import MongoClient # to connect to a MongoDB database
from app.config import settings # object from config module

_client = MongoClient(settings.MONGODB_URI) # Creates a MongoDB client instance & _client is a global variable so the connection stays open for reuse.
_db = _client[settings.MONGODB_DB] # _db now represents the database object

def candidates_coll():
    return _db["candidates"] # function that returns the collection named "candidates".
