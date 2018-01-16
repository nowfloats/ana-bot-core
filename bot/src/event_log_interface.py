from src.connectors.kinesis_helper import KinesisHelper
from src.config import application_config as config
from src.logger import logger

class EventLogInterface():

    @classmethod
    def log_message(cls, *args, **kwargs):

        if config.get("IS_AWS_ENABLED") == "TRUE":
            KinesisHelper().log_message(*args, *kwargs)
        else:
            logger.info("Since AWS is disabled, any publish event is just being logged")
        return
