import os
import redis

class RedisHelper():

    def __init__(self):
        try:
            session_redis_host = os.environ.get("SESSION_REDIS_HOST") or "0.0.0.0"
            session_redis_port = os.environ.get("SESSION_REDIS_PORT") or 6379
            self.session_redis_client = redis.StrictRedis(host=session_redis_host, port=session_redis_port, encoding="utf-8", decode_responses=True)

            ana_redis_host = os.environ.get("ANA_REDIS_HOST") or "0.0.0.0"
            ana_redis_port = os.environ.get("ANA_REDIS_PORT") or 6379
            self.ana_redis_client = redis.StrictRedis(host=ana_redis_host, db=1, port=ana_redis_port, encoding="utf-8", decode_responses=True)
        except Exception as err:
            print(err)
