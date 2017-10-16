import requests
import uuid
import json
import threading
import pdb
from furl import furl
from pprint import pprint
from src.models.user import User
from src.models.ana_node import AnaNode
from src.config import flow_config
from src.config import application_config
from src.converters.converter import Converter

class MessageProcessor(threading.Thread):

    def __init__(self, message, *args, **kwargs):
        threading.Thread.__init__(self)
        self.meta_data = message["meta"]
        self.message_content = message["data"]
        self.user_id = self.meta_data["sender"]["id"]
        self.business_id = self.meta_data["recipient"]["id"]
        flow_data = flow_config["flows"].get(self.business_id, {})
        self.flow_id = flow_data.get("flow_id", flow_config["default_flow_id"])
        self.state = self._get_state()

    def run(self):
        if (self.flow_id == ""):
            print("Could not find flow")
            return 
        node = self._get_node()
        messages = Converter(self.state).get_messages(node,self.meta_data, self.message_content)
        response = self._respond_with_messages(messages)
        if (response):
            User(self.user_id).set_state(self.session_id, self.state)
            print("User state updated with", self.state)
        else:
            print("Could not respond back")

    def _get_state(self):
        user_id = self.meta_data["sender"]["id"]
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
            next_node_id = next_node_data["node_id"]
            self.state["new_var_data"] = next_node_data["input_data"]
            self.state["current_node_id"] = next_node_id
            node = AnaNode(next_node_id).get_contents(next_node_id)
        else:
            next_node_id =  self.flow_id + "." + flow_config["first_node_key"]
            self.state["current_node_id"] = next_node_id
            node = AnaNode(next_node_id).get_contents(next_node_id)

        return node

    def _respond_with_messages(self, messages):
        url = application_config["GATEWAY_URL"]
        headers = {"Content-Type" : "application/json"}
        if len(messages) == 0:
            print("No messages to send")
            return 1
        for message in messages:
            pprint(message)
            json_message = json.dumps(message)
            try:
                response = requests.post(url, headers=headers, data=json_message)
                print(response)
            except Exception as e:
                print(e)
                return 0
        return 1
