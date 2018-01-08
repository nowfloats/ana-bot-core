"""
This module handles acting on "events" in message object
Author: https://github.com/velutha
"""
import json
from src.models.types import EventTypeWrapper as EventType, MessageTypeWrapper as MessageType, InputTypeWrapper as InputType
from src.logger import logger
from src.utils import Util
from src.converters.converter import Converter

class MessageEventHandler(object):

    def __init__(self, state, meta_data, message_data):
        self.state = state
        self.meta_data = meta_data
        self.message_data = message_data

    def handle_events(self, events):
        reponses = []
        for event in events:
            event_type = EventType.get_name(event.get("type"))
            handler_method = getattr(self, "handle_%s" % event_type.lower(), None)

            if handler_method is None:
                logger.error(f"Unknown event encountered in message {event}")
            else:
                resp = handler_method(event) # for synchronous events, return the response
                if resp:
                    reponses.extend(resp)
                    pass
        return reponses

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
    
    def handle_intent_to_handover(self, event):
        try:
            data = Converter(self.state).get_messages(meta_data=self.meta_data, message_data=self.message_data, event="INTENT_TO_HANDOVER")
            outgoing_messages = data.get("messages",[]) 
            # publish_events = data.get("publish_events",[])

            # As a response to intent to handover event, Agent Panel expects input type messages in response
            messages_to_return = [item for item in outgoing_messages if item['sending_to'] == "AGENT" and item['message']['data'].get('type', None) == MessageType.get_value("INPUT")] # and item['message']['data']['content'].get('inputType', None) == InputType.get_value("OPTIONS")

            # if messages_to_return and publish_events:
            #     Util.log_events(meta_data=self.meta_data, state=self.state, events=publish_events, message_event=None)
            #     pass

            return messages_to_return
        except ValueError:
            logger.error(f"Error in INTENT_TO_HANDOVER get_messages with data: {data}")

        return None

    def handle_handover(self, event):
        try:
            data = Converter(self.state).get_messages(meta_data=self.meta_data, message_data=self.message_data, event="HANDOVER")
            outgoing_messages = data.get("messages",[]) 
            # publish_events = data.get("publish_events",[])
            
            user_messages = [message["message"] for message in outgoing_messages if message["sending_to"] == "USER"]
            user_response = Util.send_messages(messages=user_messages, sending_to="USER")

            if user_response:
                Util.update_state(meta_data=self.meta_data, state=self.state, event="HANDOVER")
                # Util.log_events(meta_data=self.meta_data, state=self.state, events=publish_events, message_event="HANDOVER")

        except ValueError:
            logger.error(f"Error in HANDOVER get_messages with data: {data}")

        return None

