import time
import pdb
from src.converters.ana.ana_converter import Converter as AnaConverter
from src.converters.agent.agent_converter import Converter as AgentConverter
from src.models.message import MessageMeta, Message

class Converter():

    def __init__(self, state):
        self.state = state
        pass

    def get_messages(self, node_data, meta_data, message_content,*args, **kwargs):
        # pass to ana converter first
        # if ana responds with a message pass this message back
        # if not then pass to ai converter
        messages = []
        messages_data = AnaConverter(self.state).get_messages_data(node_data, message_content)

        if messages_data == None:
            incoming_message = Message(meta=meta_data, data=message_content).trim()
            messages.append(incoming_message)
            return {"messages": messages, "send_to": "AGENT"}
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
                messages.append(message)
            return {"messages": messages, "send_to": "USER"}

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
