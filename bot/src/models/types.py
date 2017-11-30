from src.thrift_models.ttypes import MessageType, InputType, SenderType

class SenderTypeWrapper(SenderType):

    @staticmethod
    def get_name(sender_type):
        return SenderType._VALUES_TO_NAMES[sender_type]

class MessageTypeWrapper(MessageType):

    @staticmethod
    def get_name(message_type):
        return MessageType._VALUES_TO_NAMES[message_type]

class InputTypeWrapper(InputType):

    @staticmethod
    def get_name(input_type):
        return InputType._VALUES_TO_NAMES[input_type]
