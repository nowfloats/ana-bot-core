"""
Message lifecycle goes here, receiving to responding
All the higher level logic should exist here
Author: https://github.com/velutha
"""
from src import EventLogPool
from src.utils import Util
from src.models.types import SenderTypeWrapper as SenderType
from src.converters.converter import Converter
from src.event_logger import EventLogger
from src.event_handler import MessageEventHandler
# from src.logger import logger
from src.models.user import User
from src.models.business import Business

class MessageProcessor():

    def __init__(self, message):

        self.meta_data = message["meta"]
        self.message_data = message.get("data", {})
        self.events = message.get("events", [])

        self.sender_id = self.meta_data["sender"]["id"]
        self.recipient_id = self.meta_data["recipient"]["id"]

        self.state = self.__get_current_state(self.meta_data)
        self.meta_data["sessionId"] = self.state.get("session_id")

    def respond_to_message(self):
        """
        This method is responsible for getting the messages to respond with
        Also covers analytics events for those messages for e.g. click, view
        """

        MessageEventHandler(self.state).handle_events(events=self.events)
        data = Converter(self.state).get_messages(meta_data=self.meta_data, message_data=self.message_data)

        outgoing_messages = data.get("messages", [])
        events_to_publish = data.get("publish_events", [])

        agent_messages = [message["message"] for message in outgoing_messages if message["sending_to"] == "AGENT"]
        user_messages = [message["message"] for message in outgoing_messages if message["sending_to"] == "USER"]

        agent_response = Util.send_messages(messages=agent_messages, sending_to="AGENT")
        user_response = Util.send_messages(messages=user_messages, sending_to="USER")

        if agent_response or user_response:

            self.__update_state(meta_data=self.meta_data, state=self.state)
            self.__log_events(meta_data=self.meta_data, state=self.state, events=events_to_publish)

        return 1

    def respond_to_events(self):
        return {}

    @classmethod
    def __get_current_state(cls, meta_data):
        """
        Gets state of the user in conversation which gives info about where he is in conversation
        Gets info the flow/business to which user belongs to
        For e.g. current_node_id of flow exists in state
        """

        sender_type = SenderType.get_name(meta_data["senderType"])

        if sender_type == "AGENT":
            user_id = meta_data["recipient"]["id"]
            business_id = meta_data["sender"]["id"]
        else:
            user_id = meta_data["sender"]["id"]
            business_id = meta_data["recipient"]["id"]

        state = User(user_id).get_session_data(meta_data=meta_data)
        flow_id = meta_data.get("flowId")

        business_id = flow_id if flow_id else business_id
        flow_data = Business(business_id).get_business_data()
        current_state = Util.merge_dicts(state, flow_data)

        return current_state

    @classmethod
    def __update_state(cls, state, meta_data):
        """
        This methods updates the state of the user after the message is sent
        For e.g. updating current_node_id
        For now agent is stateless, state corresponds to only user
        """

        sender_type = SenderType.get_name(meta_data["senderType"])

        if sender_type == "AGENT":
            # no need to update user state
            return

        user_id = meta_data["sender"]["id"]
        session_id = meta_data["sessionId"]
        state_saved = User(user_id).set_state(session_id, state, meta_data)

        return state_saved

    @classmethod
    def __log_events(cls, meta_data, state, events):
        """
        While the user is responded with messages, there will be some analytics events
        which are recorded for e.g. 'click' event for user clicking the button
        No analytics events are recorded for messages sent by agent as of now
        """

        sender_type = SenderType.get_name(meta_data["senderType"])

        if sender_type == "AGENT":
            # no need to log any event as of now
            return

        type_of_event = "analytics"

        for event in events:
            data = {
                "meta_data": meta_data,
                "state_data": state,
                "event_data": event
                }
            EventLogPool.submit(EventLogger().log_event(type_of_event=type_of_event, data=data))

        return 1
