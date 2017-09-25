import os
import redis

class RedisHelper():

    def __init__(self, *args, **kwargs):
        try:
            host = os.environ.get("REDIS_HOST")
            port = os.environ.get("REDIS_PORT")
            self.redis_client = redis.StrictRedis(host=host, port=port, db=1)
        except Exception as e:
            print(e)

    def set_data(self, name, value):
        response = self.redis_client.set(name, value)
        return response
