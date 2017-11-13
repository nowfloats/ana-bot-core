"""
Application init file
"""
import os
import redis
import pymongo
from pymongo import MongoClient
from flask import Flask
from settings import *
from src.connectors.redis_helper import RedisHelper

app = Flask(__name__)

CACHE = RedisHelper().redis_client

MONGO_CLIENT = MongoClient(
    host=os.environ.get("DB_CONNECTION"),
    maxPoolSize=None,
    serverSelectionTimeoutMS=100,
    connectTimeoutMS=20000
    )

try:
    MONGO_CLIENT.server_info()
    DB = MONGO_CLIENT["anachatdb"]
    print("Connected to anachatdb")
    CACHE.get("None")
    print("Connected to Redis")

except redis.exceptions.ConnectionError as err:
    print("Error connecting to redis\n", err)

except pymongo.errors.ServerSelectionTimeoutError as err:
    print("Error connecting to mongodb\n", err)

except:
    print("Server could not start.\n Unexpected error occured")
    raise
