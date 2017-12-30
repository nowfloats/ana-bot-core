import time
from src.models.types import MediumWrapper as Medium, EventTypeWrapper as EventType
from src.models.message import MessageWrapper as Message, EventWrapper as Event
from src.connectors.kinesis_helper import KinesisHelper
from src.logger import logger

class EventLogger(KinesisHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log_event(self, type_of_event, data):

        logger_method = getattr(self, "log_%s"%type_of_event.lower(), None)

        if logger_method is None:
            logger.error(f"Unknown event type published {type_of_event}")

        message_logged = logger_method(data)
        return message_logged

    def log_session_start(self, data):

        final_event_data = {}

        event_type = EventType.get_value("SESSION_STARTED")
        events = Event(type=event_type).trim()
        event_data = Message(meta=data, events=events).trim()

        final_event_data = {
            "meta" : {
                "topic": "SESSION"
                },
            "data": event_data
            }

        self.log_message(key="session", data=final_event_data)
        logger.info("SESSION_STARTED event logged with data" + str(final_event_data))
        return 1

    def log_analytics(self, data):

        final_event_data = {}

        event_data = data.get("event_data")
        event_node_data = event_data.get("node_data")
        click_event_data = event_data.get("event_data")

        meta_data = data.get("meta_data")
        state_data = data.get("state_data")

        event_type = event_data.get("type_of_event")
        event_channel_type = meta_data["sender"]["medium"]
        event_channel = Medium.get_name(event_channel_type)

        final_event_data = {
            "business_name" : state_data.get("business_name"),
            "business_id": meta_data["recipient"]["id"],
            "event_channel": event_channel,
            "user_id": meta_data["sender"]["id"],
            "session_id": meta_data.get("sessionId"),
            "event_name": event_type,
            "node_id": event_node_data.get("Id"),
            "node_name": event_node_data.get("Name"),
            "node_type": event_node_data.get("NodeType"),
            "button_id": click_event_data.get("_id"),
            "button_type": click_event_data.get("ButtonType", click_event_data.get("Type")),
            "button_name": click_event_data.get("ButtonName", click_event_data.get("Text")),
            "timestamp": int(time.time())
            }

        log_data = {
            "meta": {
                "topic": "analytics"
                },
            "data": final_event_data
            }

        self.log_message(key="analytics", data=log_data)
        logger.info("Analytics event logged with data" + str(log_data))
        return 1

    # def log(self, meta_data, event, state):

        # event_type = event.get("type_of_event")
        # if event == {}:
            # return 0

        # node_data = event.get("node_data")
        # click_data = event.get("event_data")
        # event_channel_type = meta_data["sender"]["medium"]
        # event_channel = Medium.get_name(event_channel_type)

        # final_event_data = {
            # "business_name" : state.get("business_name"),
            # "business_id": meta_data["recipient"]["id"],
            # "event_channel": event_channel,
            # "user_id": meta_data["sender"]["id"],
            # "session_id": meta_data.get("sessionId"),
            # "event_name": event_type,
            # "node_id": node_data.get("Id"),
            # "node_name": node_data.get("Name"),
            # "node_type": node_data.get("NodeType"),
            # "button_id": click_data.get("_id"),
            # "button_type": click_data.get("ButtonType", click_data.get("Type")),
            # "button_name": click_data.get("ButtonName", click_data.get("Text")),
            # "timestamp": int(time.time())
            # }

        # self.log_message(key="analytics", data=final_event_data)
        # logger.info(str(event_type) + " event logged with data" + str(final_event_data))
        # return 1
