from src.thrift_models.ttypes import MessageContent, MessageData, MessageMeta, Message, Media, Item, Option 

class Option(Option):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def trim(self):
        obj = {}
        for key, value in self.__dict__.items():
            if value != None:
                obj[key] = value
        return obj

class Item(Item):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def trim(self):
        obj = {}
        for key, value in self.__dict__.items():
            if value != None:
                obj[key] = value
        return obj

class Media(Media):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def trim(self):
        obj = {}
        for key, value in self.__dict__.items():
            if value != None:
                obj[key] = value
        return obj

class MessageContent(MessageContent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def trim(self):
        obj = {}
        for key, value in self.__dict__.items():
            if value != None:
                obj[key] = value
        return obj

class MessageData(MessageData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def trim(self):
        obj = {}
        for key, value in self.__dict__.items():
            if value != None:
                obj[key] = value
        return obj

class MessageMeta(MessageMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def trim(self):
        obj = {}
        for key, value in self.__dict__.items():
            if value != None:
                obj[key] = value
        return obj

class Message(Message):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def trim(self):
        obj = {}
        for key, value in self.__dict__.items():
            if value != None:
                obj[key] = value
        return obj
