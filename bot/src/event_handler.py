"""
This module handles acting on "events" in message object
Author: https://github.com/velutha
"""
import json
from src.models.types import EventTypeWrapper as EventType
from src.logger import logger
from src.utils import Util

class MessageEventHandler(object):

    def __init__(self, state):
        self.state = state

    def handle_events(self, events):
        for event in events:
            event_type = EventType.get_name(event.get("type"))
            handler_method = getattr(self, "handle_%s"%event_type.lower(), None)

            if handler_method is None:
                logger.error(f"Unknown event encountered in message {event}")
            else:
                handler_method(event)

        return 1

    def handle_set_session_data(self, event):

        data = event.get("data", "{}")

        try:
            dict_data = json.loads(data)
            var_data = self.state.get("var_data", {})
            final_var_data = Util.merge_dicts(var_data, dict_data)
            self.state["var_data"] = final_var_data
        except ValueError:
            logger.error(f"Set session data payload is not in json format {data}")

        return 1
