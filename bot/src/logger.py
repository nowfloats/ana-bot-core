import logging

log_format = '[%(levelname)s] [%(asctime)s] > %(message)s'

logging.basicConfig(level=logging.INFO, format=log_format)

logger = logging.getLogger()
