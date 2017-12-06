import json
import requests
from src.config import application_config
from src.logger import logger

class Util(object):

    @staticmethod
    def merge_dicts(*args):
        result = {}
        for dictionary in args:
            result.update(dictionary)
        return result

    @staticmethod
    def send_messages(messages, sending_to):

        # change whoever is passing sending_to to accept from common sender_type
        endpoints = {"USER": application_config["GATEWAY_URL"], \
                "AGENT": application_config["AGENT_URL"]}
        url = endpoints[sending_to]

        headers = {"Content-Type" : "application/json"}
        if messages == []:
            logger.info("No messages to send to" + str(sending_to))
            return 0
        #This is deliberately synchronous to maintain order of messages being sent
        for message in messages:
            logger.info(message)
            json_message = json.dumps(message)
            try:
                response = requests.post(url, headers=headers, data=json_message)
                logger.info(response)
            except Exception as err:
                logger.error(err)
                return 0
        return 1
