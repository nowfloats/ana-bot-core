from src.thrift_models.ttypes import SenderType

class SenderTypeCustom(SenderType):

    @staticmethod
    def get_name(sender_type):
        return SenderType._VALUES_TO_NAMES[sender_type]
