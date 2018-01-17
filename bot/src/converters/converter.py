"""
Module which constructs messages to send
"""
import json
from src.config import flow_config
from src.models.ana_node import AnaNode
from src.utils import Util

from src.converters.ana.ana_converter import Converter as AnaConverter
from src.converters.agent.agent_converter import Converter as AgentConverter

from src.models.types import SenderTypeWrapper as SenderType
from src.models.message import MessageWrapper as Message, MessageMetaWrapper as MessageMeta

class Converter():

    def __init__(self, state):
        self.state = state

    def get_messages(self, meta_data, message_data):
        """
        Depending on whether the sender is agent/user, this method
        constructs messages to send with each message given a tag 'sending_to'
        """
        messages = {}

        if message_data == {}:
            return messages

        sender = SenderType.get_name(meta_data["senderType"])

        if sender == "AGENT":
            messages = self.get_agent_messages(meta_data, message_data)
        else:
            data = self.__get_node(message_data=message_data)
            node_data = data.get("node")
            messages = self.get_user_messages(node_data, meta_data, message_data)
            messages["publish_events"] = messages.get("events", []) + data.get("publish_events", [])

        return messages

    def get_user_messages(self, node_data, meta_data, message_data):
        """
        This method gets messages to send if the sender of incoming_message is user.
        It tries to get messages from ANA studio flow (AnaConverter)
        If ANA does not give any messages, they are connected to agent
        In future AI middle layer will come here
        """

        outgoing_messages = []
        user_messages = []
        agent_messages = []

        messages = AnaConverter(self.state).get_messages_data(node_data=node_data, message_data=message_data)
        events_data = messages.get("publish_events", [])

        outgoing_user_messages_data = messages.get("user_messages", [])
        outgoing_agent_messages_data = messages.get("agent_messages", [])

        user_messages = self.__construct_messages(meta_data=meta_data, messages_data=outgoing_user_messages_data, sending_to="USER")
        agent_messages = self.__construct_messages(meta_data=meta_data, messages_data=outgoing_agent_messages_data, sending_to="AGENT")

        outgoing_messages = user_messages + agent_messages

        return {"messages": outgoing_messages, "publish_events": events_data}

    def get_agent_messages(self, meta_data, message_data):
        """
        This method gets messages to send if the sender of incoming_message is from agent
        """

        messages = []
        messages_data = AgentConverter(self.state).get_messages_data(message_data).get("user_messages", [])

        meta_data = MessageMeta(recipient=meta_data["recipient"],
                                sender=meta_data["sender"],
                                sessionId=meta_data["sessionId"],
                                responseTo=meta_data["id"],
                                flowId=meta_data.get("flowId"),
                                senderType=SenderType.get_value("AGENT")).trim()

        for data in messages_data:
            message = Message(meta=meta_data, data=data).trim()
            messages.append({"message": message, "sending_to": "USER"})

        return {"messages" : messages}

    def __get_node(self, message_data):
        """
        Get next_node(ANA output node) to send to user depending on current_node
        and the incoming message. If it's a first time user, next_node is first_node
        """

        get_started_node = self.state.get("flow_id", "") + "." + flow_config["first_node_key"]
        next_node_id = get_started_node
        event_data = []

        if bool(self.state.get("current_node_id")):
            # user already in ana flow
            current_node_id = self.state.get("current_node_id", get_started_node) # give first_node as default
            next_node_data = AnaNode(current_node_id).get_next_node_data(message_data, self.state)

            event_data = next_node_data.get("publish_events", [])
            next_node_id = next_node_data["node_id"]

            var_data = json.loads(self.state.get("var_data", "{}"))
            new_var_data = next_node_data.get("input_data", {})
            final_var_data = Util.merge_dicts(var_data, new_var_data)
            self.state["var_data"] = final_var_data
            self.state["new_var_data"] = new_var_data

        self.state["current_node_id"] = next_node_id
        node = AnaNode(next_node_id).get_contents()

        return {"node": node, "publish_events": event_data}

    def __get_current_node(self):
        """
        Gets the current node based on the state
        """

        get_started_node = self.state.get("flow_id", "") + "." + flow_config["first_node_key"]
        current_node_id = self.state.get("current_node_id", get_started_node) # give first_node as default

        node = AnaNode(current_node_id).get_contents()

        return {"node": node, "publish_events": []}

    @classmethod
    def __construct_messages(cls, meta_data, messages_data, sending_to):
        """
        This method constructs messages that are being sent
        """

        if sending_to is None:
            return []

        if sending_to == "USER":
            if meta_data['senderType'] == SenderType.get_value("AGENT"):
                # If agent is the sender of incoming message, don't swap the sender and recipient
                recipient = meta_data["recipient"]
                sender = meta_data["sender"]
                sender_type = SenderType.get_value("ANA")
            else:
                recipient = meta_data["sender"]
                sender = meta_data["recipient"]
                sender_type = SenderType.get_value("ANA")
        elif sending_to == "AGENT":
            recipient = meta_data["recipient"]
            sender = meta_data["sender"]
            sender_type = SenderType.get_value("USER")

        outgoing_messages = []
        message_meta_data = MessageMeta(sender=sender,
                                        recipient=recipient,
                                        sessionId=meta_data["sessionId"],
                                        flowId=meta_data.get("flowId"),
                                        responseTo=meta_data["id"],
                                        senderType=sender_type).trim()

        outgoing_messages = [Message(meta=message_meta_data, data=data).trim() for data in messages_data]

        messages = [{"sending_to": sending_to, "message": message} for message in outgoing_messages]

        return messages
