import time
import pdb
from src.converters.ana.ana_converter import Converter as AnaConverter
from src.converters.agent.agent_converter import Converter as AgentConverter

from src.thrift_models.ttypes import MessageType, InputType, MediaType, ButtonType
from src.models.message import MessageContent, MessageData, Message, Media
from src.models.inputs import Option, Item, TextInput
from src.event_logger import EventLogger

from src.models.message import MessageMeta, Message

class Converter():

    def __init__(self, state):
        self.state = state
        pass

    def get_messages(self, node_data, meta_data, message_content,*args, **kwargs):
        # pass to ana converter first
        # if ana responds with a message pass this message back
        # if not then pass to ai converter
        outgoing_messages = []
        messages = AnaConverter(self.state).get_messages_data(node_data, message_content)
        messages_data = messages.get("messages", [])
        event_data = messages.get("events", {})

        if messages_data == []:
            # empty messages from flow, construct agent message
            incoming_message = Message(meta=meta_data, data=message_content).trim()
            messages.append({"message" :incoming_message, "send_to": "AGENT"})

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
            outgoing_messages.append({"message" : input_message, "send_to": "USER"})

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
                outgoing_messages.append({"message" :message, "send_to": "USER"})
            
        return {"messages": outgoing_messages, "event_data": event_data}

    def get_agent_messages(self, meta_data, message_content):

        messages = []
        messages_data = AgentConverter(self.state).get_messages_data(message_content)

        meta_data = MessageMeta(
                recipient=meta_data["recipient"],
                sender=meta_data["sender"],
                sessionId=meta_data["sessionId"],
                responseTo=meta_data["id"],
                senderType=3 #change this hardcoded
                ).trim()
        for message_data in messages_data: 
            message = Message(meta=meta_data, data=message_data).trim()
            messages.append(message)

        return messages
