"""
Application init file
"""
import os
import redis
import pymongo
from pymongo import MongoClient
from flask import Flask
from src.connectors.redis_helper import RedisHelper
from src.thread_pool import ThreadPoolExecutorStackTraced

app = Flask(__name__)

SESSION_CACHE = RedisHelper().session_redis_client

ANA_CACHE = RedisHelper().ana_redis_client

DB_CONNECTION = os.environ.get("DB_CONNECTION") or "mongodb://localhost:27027/anachatdb"

MONGO_CLIENT = MongoClient(
    host=os.environ.get("DB_CONNECTION"),
    maxPoolSize=None,
    serverSelectionTimeoutMS=100,
    connectTimeoutMS=20000
    )

message_pool = ThreadPoolExecutorStackTraced(max_workers=20)

try:
    MONGO_CLIENT.server_info()
    DB = MONGO_CLIENT["anachatdb"]
    print("Connected to anachatdb")

except pymongo.errors.ServerSelectionTimeoutError as err:
    print("Error connecting to mongodb\n", err)
    raise

except:
    print("Server could not start.\n Unexpected error occured")
    raise
