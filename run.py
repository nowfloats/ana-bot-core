import os
import redis
import couchdb
from src import app
from settings import *
from src import config
from src import routes
from src.connectors.redis_helper import RedisHelper
from src.services.refresh_chatflows import RefreshChatFlows

redis_helper = RedisHelper()
app.redis_client = redis_helper.redis_client

if __name__ == "__main__":
    host = os.environ.get("HOST") or "0.0.0.0"
    port = os.environ.get("PORT") or 5000
    db_url = os.environ.get("DB_CONNECTION") or "http://localhost:5984"
    try:
        app.couch = couchdb.Server(db_url)
        app.redis_client.get("None")
        # app.redis_client.flushdb()
        # RefreshChatFlows().populate_flows()
        app.run(host=host, port=port)
    except redis.exceptions.ConnectionError as e:
        print("Error connecting to redis\n",e)
    except Exception as e:
        print("Server could not start.\n Exception caught as: ",e)
