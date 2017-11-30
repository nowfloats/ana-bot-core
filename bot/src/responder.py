"""
Message lifecycle goes here, receiving to responding
__author__: https://github.com/velutha
"""
import uuid
from src.utils import Util
from src.models.sender_type import SenderTypeCustom as SenderType
from src.converters.converter import Converter
from src.event_logger import EventLogger
from src.logger import logger
from src.models.user import User
from src.models.business import Business

class MessageProcessor():

    def __init__(self, message):

        self.meta_data = message["meta"]
        self.message_data = message["data"]

        self.sender_id = self.meta_data["sender"]["id"]
        self.recipient_id = self.meta_data["recipient"]["id"]

        self.state = self.__get_current_state(self.meta_data)
        self.meta_data["sessionId"] = self.state.get("session_id")

    def respond_to_message(self):

        messages_data = Converter(self.state).get_messages(meta_data=self.meta_data, message_data=self.message_data)
        messages = messages_data.get("messages", [])
        event_data = messages_data.get("event_data", {})

        agent_messages = [message["message"] for message in messages if message["sending_to"] == "AGENT"]
        user_messages = [message["message"] for message in messages if message["sending_to"] == "USER"]

        agent_response = Util.send_messages(messages=agent_messages, sending_to="AGENT")
        user_response = Util.send_messages(messages=user_messages, sending_to="USER")

        if agent_response or user_response:
            self.__update_state(meta_data=self.meta_data, state=self.state)
            self.__log_event(meta_data=self.meta_data, state=self.state, data=event_data)
            logger.info("User state updated with" + str(self.state))

        return

    @classmethod
    def __get_current_state(cls, meta_data):

        sender_type = SenderType.get_name(meta_data["senderType"])

        if sender_type == "AGENT":
            user_id = meta_data["recipient"]["id"]
            business_id = meta_data["sender"]["id"]
        else:
            user_id = meta_data["sender"]["id"]
            business_id = meta_data["recipient"]["id"]

        session_id = meta_data.get("sessionId", str(uuid.uuid4()))
        state = User(user_id).get_session_data(session_id)

        flow_data = Business(business_id).get_business_data()
        current_state = Util.merge_dicts(state, flow_data)

        return current_state

    @classmethod
    def __update_state(cls, state, meta_data):

        sender_type = SenderType.get_name(meta_data["senderType"])

        if sender_type == "AGENT":
            # no need to update user state
            return
        user_id = meta_data["sender"]["id"]
        session_id = meta_data["sessionId"]
        state_saved = User(user_id).set_state(session_id, state, meta_data)
        return state_saved

    @classmethod
    def __log_event(cls, meta_data, state, data):

        sender_type = SenderType.get_name(meta_data["senderType"])

        if sender_type == "AGENT":
            # no need to log any event as of now
            return
        EventLogger().log(meta_data=meta_data, data=data, state=state)
