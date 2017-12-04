"""
Messages being sent to agent are constructed here
Author: https://github.com/velutha
"""
from src.models.message import MessageContent, MessageData
from src.models.inputs import TextInput
from src.models.types import MessageTypeWrapper as MessageType, InputTypeWrapper as InputType

class Converter():

    def __init__(self, state):
        self.state = state

    @classmethod
    def get_messages_data(cls, message_data):

        messages_data = []
        messages_data.append(message_data)

        other_messages_data = cls.get_agent_connected_messages()
        messages_data = messages_data + other_messages_data

        return messages_data

    @staticmethod
    def get_agent_connected_messages():
        messages_data = []

        message_type = MessageType.get_value("INPUT")
        input_type = InputType.get_value("TEXT")
        input_attr = TextInput(placeHolder="Talk to our Agent").trim()

        content = MessageContent(
            inputType=input_type,
            textInputAttr=input_attr,
            mandatory=1,
            ).trim()
        input_message_data = MessageData(
            type=message_type,
            content=content
            ).trim()

        messages_data.append(input_message_data)
        return messages_data
