import os
import redis
from pymongo import MongoClient
from src import app
from settings import *
from src import config
from src import routes
from src.connectors.redis_helper import RedisHelper

redis_helper = RedisHelper()
app.redis_client = redis_helper.redis_client

if __name__ == "__main__":

    host = os.environ.get("HOST") or "0.0.0.0"
    port = os.environ.get("PORT") or 5000
    db_connection = os.environ.get("DB_CONNECTION") or "mongodb://localhost:27017"

    mongo_client = MongoClient(host=db_connection, maxPoolSize=None, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)

    try:
        mongo_client.server_info()
        app.db = mongo_client["anachatdb"] 
        print("Connected to anachatdb")
        app.redis_client.get("None")
        print("Connected to Redis")
        app.run(host=host, port=port)

    except redis.exceptions.ConnectionError as e:
        print("Error connecting to redis\n",e)

    except Exception as e:
        print("Server could not start.\nException caught as: ",e)
