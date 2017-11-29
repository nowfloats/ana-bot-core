"""
Module which converts output from ana studio to platform's message format
Author: https://github.com/velutha
"""
import json
import re
from furl import furl
from src.config import ana_config
from src.thrift_models.ttypes import MessageType, InputType, MediaType, ButtonType
from src.models.message import MessageContent, MessageData, Media
from src.models.inputs import Option, Item, TextInput
from .node_processors.combination_processor import CombinationProcessor
from .node_processors.api_call_processor import ApiCallProcessor
from .node_processors.condition_processor import ConditionProcessor
from .node_processors.card_processor import CardProcessor
from .node_processors.handoff_agent_processor import AgentHandOffProcessor

class Converter():

    def __init__(self, state):
        self.state = state

    def get_messages_data(self, node_data):

        node_type = node_data.get("NodeType", "")

        node_processor_map = {
            "Combination": CombinationProcessor,
            "ApiCall": ApiCallProcessor,
            "Condition": ConditionProcessor,
            "Card": CardProcessor,
            "HandoffToAgent": AgentHandOffProcessor
            }

        Processor = node_processor_map.get(node_type, None)

        if Processor is None:
            raise "Unknown Node Type. Fatal Error"

        data = Processor(self.state).process_node(node_data)

        messages = data.get("messages")
        events = data.get("events")

        return {"messages": messages, "events": events}
