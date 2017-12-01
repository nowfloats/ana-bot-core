from src.thrift_models.ttypes import MessageType, InputType, SenderType

class SenderTypeWrapper(SenderType):

    @staticmethod
    def get_name(sender_type):
        return SenderType._VALUES_TO_NAMES[sender_type]

    @staticmethod
    def get_value(name):
        return SenderType._NAMES_TO_VALUES[name]

class MessageTypeWrapper(MessageType):

    @staticmethod
    def get_name(message_type):
        return MessageType._VALUES_TO_NAMES[message_type]

    @staticmethod
    def get_value(name):
        return MessageType._NAMES_TO_VALUES[name]

class InputTypeWrapper(InputType):

    @staticmethod
    def get_name(input_type):
        return InputType._VALUES_TO_NAMES[input_type]

    @staticmethod
    def get_value(name):
        return InputType._NAMES_TO_VALUES[name]
