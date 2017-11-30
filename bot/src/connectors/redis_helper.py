import os
from redis import StrictRedis, exceptions as RedisExceptions
from rediscluster import StrictRedisCluster, exceptions as RedisClusterExceptions

class RedisHelper():

    def __init__(self):
        try:
            session_node = [{"host": os.environ.get("SESSION_REDIS_HOST") or "0.0.0.0", "port": os.environ.get("SESSION_REDIS_PORT") or "30001"}]
            self.session_redis_client = StrictRedisCluster(startup_nodes=session_node, encoding="utf-8", decode_responses=True,\
                    skip_full_coverage_check=True)

            ana_redis_host = os.environ.get("ANA_REDIS_HOST") or "0.0.0.0"
            ana_redis_port = os.environ.get("ANA_REDIS_PORT") or 6379
            self.ana_redis_client = StrictRedis(host=ana_redis_host, db=1, port=ana_redis_port, encoding="utf-8", decode_responses=True)

            self.session_redis_client.get("None")
            print("Connected to session redis cluster")

            self.ana_redis_client.get("None")
            print("Connected to ana redis")

        except RedisExceptions.ConnectionError as err:
            print("Error connecting to redis\n", err)
            raise

        except RedisClusterExceptions.RedisClusterException as err:
            print("Error connecting to redis cluster\n", err)
            raise
