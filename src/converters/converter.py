import time
import pdb
from src.converters.ana.ana_converter import Converter as AnaConverter
from src.models.message import MessageMeta, Message

class Converter():

    def __init__(self):
        pass

    @classmethod
    def get_messages(cls, node_data, meta_data, message_content, *args, **kwargs):
        # pass to ana converter first
        # if ana responds with a message pass this message back
        # if not then pass to ai converter
        messages = []
        messages_data = AnaConverter().get_messages_data(node_data, message_content)
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
        return messages
