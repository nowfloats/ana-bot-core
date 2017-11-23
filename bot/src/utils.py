import json
import requests
import pdb
from src.config import application_config

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
            print("No messages to send to", sending_to)
            return 0
        for message in messages:
            print(message)
            json_message = json.dumps(message)
            try:
                response = requests.post(url, headers=headers, data=json_message)
                print(response)
            except Exception as err:
                print(err)
                return 0
        return 1
