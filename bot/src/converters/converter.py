"""
Module which constructs messages to send
"""
from src.models.ana_node import AnaNode
from src.config import flow_config

from src.converters.ana.ana_converter import Converter as AnaConverter
from src.converters.agent.agent_converter import Converter as AgentConverter

from src.models.types import SenderTypeWrapper as SenderType
from src.models.message import Message, MessageMeta

class Converter():

    def __init__(self, state):
        self.state = state

    def get_messages_and_events(self, meta_data, message_data):

        messages = {}
        sender_type = SenderType.get_name(meta_data["senderType"])

        if sender_type == "AGENT":
            messages = self.get_agent_messages(meta_data, message_data)
        else:
            node_data = self.__get_node(message_data=message_data)
            messages = self.get_user_messages(node_data, meta_data, message_data)

        return messages

    def get_user_messages(self, node_data, meta_data, message_data):

        outgoing_messages = []
        user_messages = []
        agent_messages = []

        messages = AnaConverter(self.state).get_messages_data(node_data)
        messages_data = messages.get("messages", [])
        events_data = messages.get("events", {})

        if messages_data == []:
            # no messages from ana flow, send incoming message to agent
            incoming_message = Message(meta=meta_data, data=message_data).trim()
            agent_messages = [{"message" :incoming_message, "sending_to": "AGENT"}]

            # get messages to send to user when agent is connected
            user_messages_data = AgentConverter.get_agent_connected_messages()
        else:
            user_messages_data = messages_data

        messages = self.__construct_user_messages(meta_data=meta_data, messages_data=user_messages_data)
        user_messages = [{"message": message, "sending_to": "USER"} for message in messages]

        outgoing_messages = user_messages + agent_messages

        return {"messages": outgoing_messages, "events": events_data}

    def get_agent_messages(self, meta_data, message_data):

        messages = []
        messages_data = AgentConverter(self.state).get_messages_data(message_data)

        meta_data = MessageMeta(
            recipient=meta_data["recipient"],
            sender=meta_data["sender"],
            sessionId=meta_data["sessionId"],
            responseTo=meta_data["id"],
            senderType=SenderType.get_value("AGENT")
            ).trim()

        for data in messages_data:
            message = Message(meta=meta_data, data=data).trim()
            messages.append({"message": message, "sending_to": "USER"})

        return messages

    def __get_node(self, message_data):

        get_started_node = self.state["flow_id"] + "." + flow_config["first_node_key"]
        next_node_id = get_started_node

        if bool(self.state.get("current_node_id")):
            # user already in ana flow
            current_node_id = self.state.get("current_node_id", get_started_node) # give first_node as default
            next_node_data = AnaNode(current_node_id).get_next_node_data(self.state["flow_id"], message_data)

            # event_data = next_node_data.get("event_data", {})
            # if event_data != {}:
                # EventLogger().log(meta_data=self.meta_data, data=event_data, flow_data=self.flow_data)
            next_node_id = next_node_data["node_id"]
            self.state["new_var_data"] = next_node_data["input_data"]

        self.state["current_node_id"] = next_node_id
        node = AnaNode(next_node_id).get_contents()

        return node

    @classmethod
    def __construct_user_messages(cls, meta_data, messages_data):

        outgoing_messages = []
        message_meta_data = MessageMeta(
            sender=meta_data["recipient"],
            recipient=meta_data["sender"],
            sessionId=meta_data["sessionId"],
            responseTo=meta_data["id"],
            senderType=SenderType.get_value("ANA")
            ).trim()
        for message_data in messages_data:
            message = Message(meta=message_meta_data, data=message_data).trim()
            outgoing_messages.append(message)
        return outgoing_messages
