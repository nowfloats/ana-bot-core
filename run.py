import os
from src import app
from settings import *
from src import config
from src import routes
from src.connectors.redis_helper import RedisHelper
from src.listener import Scheduler

app.redis_client = RedisHelper().redis_client

if __name__ == "__main__":
    host = os.environ.get("HOST") or "0.0.0.0"
    port = os.environ.get("PORT") or 5000
    Scheduler().start_jobs()
    app.run(host=host, port=port)
