import os
import redis

class RedisHelper():

    def __init__(self, *args, **kwargs):
        try:
            host = os.environ.get("REDIS_HOST")
            port = os.environ.get("REDIS_PORT")
            # print("Hey in redis")
            # print("Hey redis connected and flushed db")
            self.redis_client = redis.StrictRedis(host=host, port=port, db=0)
            print("Hey redis connected")

        except Exception as e:
            print(e)

