from flask import current_app, g
from werkzeug.local import LocalProxy

from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.write_concern import WriteConcern
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo.read_concern import ReadConcern


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)
    APP_DB_URI = current_app.config["APP_DB_URI"]
    APP_DB_NAME = current_app.config["APP_NS"]
    if db is None:
        db = g._database = MongoClient(
        APP_DB_URI,
        username="root", 
        password="abcd1234",
        maxPoolSize=50,     # Set the maximum connection pool size to 50 active connections.
        w='majority',   # Set the write timeout limit to 2500 milliseconds.
        wtimeout=2500
        )[APP_DB_NAME]
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)