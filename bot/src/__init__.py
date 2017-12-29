"""
Application init file
"""
import os
import redis
import pymongo
from pymongo import MongoClient
from flask import Flask
from src.logger import logger
from src.connectors.redis_helper import RedisHelper
from src.thread_pool import ThreadPoolExecutorStackTraced

app = Flask(__name__)

SESSION_CACHE = RedisHelper().create_session_client()

ANA_CACHE = RedisHelper().create_ana_client()

DB_CONNECTION = os.environ.get("DB_CONNECTION") or "mongodb://localhost:27027/anachatdb"

MONGO_CLIENT = MongoClient(
    host=os.environ.get("DB_CONNECTION"),
    maxPoolSize=None,
    serverSelectionTimeoutMS=100,
    connectTimeoutMS=20000
    )

MessageHandlerPool = ThreadPoolExecutorStackTraced(max_workers=20)
EventLogPool = ThreadPoolExecutorStackTraced(max_workers=2)

try:
    MONGO_CLIENT.server_info()
    DB = MONGO_CLIENT["anachatdb"]
    logger.info("Connected to anachatdb")

except pymongo.errors.ServerSelectionTimeoutError as err:
    logger.error("Error connecting to mongodb\n" + str(err))
    raise

except:
    logger.critical("Server could not start.\n Unexpected error occured")
    raise
