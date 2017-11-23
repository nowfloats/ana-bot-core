"""
Module which constructs messages to send
"""
from src.models.ana_node import AnaNode
from src.config import flow_config

from src.converters.ana.ana_converter import Converter as AnaConverter
from src.converters.agent.agent_converter import Converter as AgentConverter

from src.thrift_models.ttypes import MessageType, InputType, SenderType
from src.models.message import MessageContent, MessageData, Message, MessageMeta
from src.models.inputs import TextInput

class Converter():

    def __init__(self, state):
        self.state = state

    def get_messages(self, meta_data, message_data):

        messages = {}
        sender_type = SenderType._VALUES_TO_NAMES[meta_data["senderType"]]

        if sender_type == "AGENT":
            messages = self.get_agent_messages(meta_data, message_data=message_data)
        else:
            node = self._get_node(message_data=message_data)
            messages = self.get_user_messages(node, meta_data, message_data)

        return messages

    def get_user_messages(self, node_data, meta_data, message_content):

        outgoing_messages = []
        messages = AnaConverter(self.state).get_messages_data(node_data)
        messages_data = messages.get("messages", [])
        event_data = messages.get("events", {})

        if messages_data == []:
            # empty messages from flow, construct agent message
            incoming_message = Message(meta=meta_data, data=message_content).trim()
            outgoing_messages.append({"message" :incoming_message, "sending_to": "AGENT"})

            message_type = MessageType._NAMES_TO_VALUES["INPUT"]
            input_type = InputType._NAMES_TO_VALUES["TEXT"]
            input_attr = TextInput(placeHolder="Talk to our Agent").trim()

            user_meta_data = MessageMeta(
                sender=meta_data["recipient"],
                recipient=meta_data["sender"],
                sessionId=meta_data["sessionId"],
                responseTo=meta_data["id"],
                senderType=1 #change this hardcoded
                ).trim()
            content = MessageContent(
                inputType=input_type,
                textInputAttr=input_attr,
                mandatory=1,
                ).trim()
            input_message_data = MessageData(
                type=message_type,
                content=content
                ).trim()
            input_message = Message(meta=user_meta_data, data=input_message_data).trim()
            outgoing_messages.append({"message" : input_message, "sending_to": "USER"})

        else:
            meta_data = MessageMeta(
                sender=meta_data["recipient"],
                recipient=meta_data["sender"],
                sessionId=meta_data["sessionId"],
                responseTo=meta_data["id"],
                senderType=1 #change this hardcoded
                ).trim()
            for message_data in messages_data:
                message = Message(meta=meta_data, data=message_data).trim()
                outgoing_messages.append({"message" :message, "sending_to": "USER"})

        return {"messages": outgoing_messages, "event_data": event_data}

    def get_agent_messages(self, meta_data, message_data):

        messages = []
        messages_data = AgentConverter(self.state).get_messages_data(message_data)

        meta_data = MessageMeta(
            recipient=meta_data["recipient"],
            sender=meta_data["sender"],
            sessionId=meta_data["sessionId"],
            responseTo=meta_data["id"],
            senderType=3 #change this hardcoded
            ).trim()
        for data in messages_data:
            message = Message(meta=meta_data, data=data).trim()
            messages.append({"message": message, "sending_to": "USER"})

        return messages

    def _get_node(self, message_data):

        get_started_node = self.state["flow_id"] + "." + flow_config["first_node_key"]

        if bool(self.state.get("current_node_id")):

            node_id = self.state.get("current_node_id", get_started_node) # give first_node as default
            next_node_data = AnaNode(node_id).get_next_node_data(self.state["flow_id"], message_data)

            # event_data = next_node_data.get("event_data", {})
            # if event_data != {}:
                # EventLogger().log(meta_data=self.meta_data, data=event_data, flow_data=self.flow_data)
            next_node_id = next_node_data["node_id"]
            self.state["new_var_data"] = next_node_data["input_data"]
            self.state["current_node_id"] = next_node_id
            node = AnaNode(next_node_id).get_contents(next_node_id)
        else:
            next_node_id = get_started_node
            self.state["current_node_id"] = next_node_id
            node = AnaNode(next_node_id).get_contents(next_node_id)

        return node
