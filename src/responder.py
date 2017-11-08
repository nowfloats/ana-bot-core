import requests
import uuid
import json
import threading
import pdb
from furl import furl
from src.thrift_models.ttypes import SenderType
from src.models.user import User
from src.models.business import Business
from src.models.ana_node import AnaNode
from src.event_logger import EventLogger
from src.config import flow_config
from src.config import application_config
from src.converters.converter import Converter

class MessageProcessor(threading.Thread):

    def __init__(self, message, *args, **kwargs):

        threading.Thread.__init__(self)

        self.message = message
        self.meta_data = message["meta"]
        self.message_content = message["data"]

        self.user_id = self.meta_data["sender"]["id"]
        self.business_id = self.meta_data["recipient"]["id"]

        self.flow_data = Business(self.business_id).get_business_data()
        # self.flow_data = flow_config["flows"].get(self.business_id, {})
        self.flow_id = self.flow_data.get("flow_id", flow_config["default_flow_id"])

        self.sender_type = SenderType._VALUES_TO_NAMES[self.message["meta"]["senderType"]]
        self.state = self._get_state()

    def run(self):

        # convert this into objects
        if (self.flow_id == ""):
            print("Could not find flow")
            return 


        if (self.sender_type == "AGENT"):
            messages = Converter(self.state).get_agent_messages(self.meta_data, self.message_content)
            response = self._respond_with_messages(messages)
            return
        else:
            node = self._get_node()
            messages_data = Converter(self.state).get_messages(node,self.meta_data, self.message_content)
            messages = messages_data.get("messages")
            event_data = messages_data.get("event_data")

            agent_messages = [message["message"] for message in messages if message["send_to"] == "AGENT"]
            user_messages = [message["message"] for message in messages if message["send_to"] == "USER"]

            agent_response = self._send_to_agent(agent_messages)
            user_response = self._respond_with_messages(user_messages)

            if (agent_response or user_response):
                User(self.user_id).set_state(self.session_id, self.state, self.meta_data, self.flow_data)
                EventLogger().log(meta_data = self.meta_data, data = event_data, flow_data = self.flow_data)
                print("User state updated with", self.state)
            return


    def _get_state(self):

        if (self.sender_type == "AGENT"):
            user_id = self.business_id
        else:
            user_id = self.user_id

        session_id = self.meta_data.get("sessionId", str(uuid.uuid4()))

        state = User(user_id).get_session_data(session_id)

        self.session_id = state["session_id"]
        self.meta_data["sessionId"] = self.session_id

        state["flow_id"] = self.flow_id

        return state

    def _get_node(self):

        if bool(self.state):
            first_node_id = self.flow_id + "." + flow_config["first_node_key"]
            node_id = self.state.get("current_node_id", first_node_id) # give first_node as default
            next_node_data = AnaNode(node_id).get_next_node_data(self.flow_id, self.message_content)

            event_data = next_node_data.get("event_data", {})
            if (event_data != {}):
                EventLogger().log(meta_data = self.meta_data, data = event_data, flow_data = self.flow_data)

            next_node_id = next_node_data["node_id"]
            self.state["new_var_data"] = next_node_data["input_data"]
            self.state["current_node_id"] = next_node_id
            node = AnaNode(next_node_id).get_contents(next_node_id)
        else:
            first_node_id = self.flow_id + "." + flow_config["first_node_key"]
            next_node_id =  self.flow_id + "." + flow_config["first_node_key"]
            self.state["current_node_id"] = next_node_id
            node = AnaNode(next_node_id).get_contents(next_node_id)

        return node

    def _respond_with_messages(self, messages):
        url = application_config["GATEWAY_URL"]
        headers = {"Content-Type" : "application/json"}
        if len(messages) == 0:
            print("No messages to send")
            return 0
        for message in messages:
            print(message)
            json_message = json.dumps(message)
            try:
                response = requests.post(url, headers=headers, data=json_message)
                print(response)
            except Exception as e:
                print(e)
                return 0
        return 1

    def _send_to_agent(self, messages):
        url = application_config["AGENT_URL"]
        headers = {"Content-Type" : "application/json"}
        if len(messages) == 0:
            print("No messages to send to agent")
            return 0
        for message in messages:
            print(message)
            json_message = json.dumps(message)
            try:
                response = requests.post(url, headers=headers, data=json_message)
                print(response)
            except Exception as e:
                print(e)
                return 0
        return 1

