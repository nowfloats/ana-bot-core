import os
from redis import StrictRedis, exceptions as RedisExceptions
from rediscluster import StrictRedisCluster, exceptions as RedisClusterExceptions
from src.logger import logger

class RedisHelper():

    def __init__(self):

        self.session_node = [{"host": os.environ.get("SESSION_REDIS_HOST") or "0.0.0.0", "port": os.environ.get("SESSION_REDIS_PORT") or "30001"}]
        self.ana_redis_host = os.environ.get("ANA_REDIS_HOST") or "0.0.0.0"
        self.ana_redis_port = os.environ.get("ANA_REDIS_PORT") or 6379

    def create_ana_client(self):
        redis_client = StrictRedis(host=self.ana_redis_host, db=1, port=self.ana_redis_port, encoding="utf-8", decode_responses=True)
        try:
            redis_client.get("None")
        except RedisExceptions.ConnectionError as err:
            logger.error("Error connecting to redis\n" + str(err))
            raise
        logger.info("Connected to ana redis")
        return redis_client

    def create_session_client(self):
        
        if os.environ.get('ENV', 'PROD') == 'LOCAL':
            redis_client = StrictRedis(host=self.ana_redis_host, db=1, port=self.ana_redis_port, encoding="utf-8", decode_responses=True)
            try:
                redis_client.get("None")
            except RedisExceptions.ConnectionError as err:
                logger.error("Error connecting to redis\n" + str(err))
                raise
            logger.info("Connected to ana redis")
            return redis_client
        else: 
            redis_client = StrictRedisCluster(startup_nodes=self.session_node, encoding="utf-8", decode_responses=True,\
            skip_full_coverage_check=True)
            try:
                redis_client.get("None")
            except RedisClusterExceptions.RedisClusterException as err:
                logger.error("Error connecting to redis cluster\n" + str(err))
                raise
            logger.info("Connected to session redis cluster")
            return redis_client
            pass
        