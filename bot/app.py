"""
This is the entry point bot-core server
Author: https://github.com/velutha
"""
import os
import redis
import pymongo
from pymongo import MongoClient
from settings import *
from src import app, routes
from src.connectors.redis_helper import RedisHelper

app.redis_client = RedisHelper().redis_client

if __name__ == "__main__":

    HOST = os.environ.get("HOST") or "0.0.0.0"
    PORT = os.environ.get("PORT") or 5000
    DB_CONNECTION = os.environ.get("DB_CONNECTION") or "mongodb://localhost:27017"

    MONGO_CLIENT = MongoClient(
        host=DB_CONNECTION,
        maxPoolSize=None,
        serverSelectionTimeoutMS=100,
        connectTimeoutMS=20000
        )

    try:
        MONGO_CLIENT.server_info()
        app.db = MONGO_CLIENT["anachatdb"]
        print("Connected to anachatdb")
        app.redis_client.get("None")
        print("Connected to Redis")
        app.run(host=HOST, port=PORT)

    except redis.exceptions.ConnectionError as err:
        print("Error connecting to redis\n", err)

    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Error connecting to mongodb\n", err)

    except:
        print("Server could not start.\n Unexpected error occured")
        raise
