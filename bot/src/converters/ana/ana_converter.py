"""
Module which converts output from ana studio to platform's message format
Author: https://github.com/velutha
"""
from .node_processors.combination.combination_processor import CombinationProcessor
from .node_processors.api_call_processor import ApiCallProcessor
from .node_processors.condition_processor import ConditionProcessor
from .node_processors.card_processor import CardProcessor
from .node_processors.handoff_agent_processor import AgentHandOffProcessor

class Converter():

    def __init__(self, state):
        self.state = state

    def get_messages_data(self, node_data, message_data, event):
        """
        This method is responsible for converting ANA studio output to
        the platform's message structure depending on type of ANA node
        For any new type of node , type and it's corresponding class
        should be added to dict below in a factory pattern
        """

        node_type = node_data.get("NodeType", "Combination")

        node_processor_map = {
            "Combination": CombinationProcessor,
            "ApiCall": ApiCallProcessor,
            "Condition": ConditionProcessor,
            "Card": CardProcessor,
            "HandoffToAgent": AgentHandOffProcessor
            }

        user_messages = []
        agent_messages = []

        Processor = node_processor_map.get(node_type)

        if node_type in ["Combination"]:
            data = Processor(self.state).process_node(node_data)

        elif node_type in ["ApiCall", "Condition"]:
            next_node_data = Processor(self.state).get_next_node(node_data)
            data = self.get_messages_data(next_node_data.get("data"), message_data, event)
            # this should ideally not happen here this
            # change current_node_id thing in converter
            # both should use the same method
            self.state["current_node_id"] = next_node_data.get("id")

        elif node_type == "HandoffToAgent":
            data = Processor(self.state).process_node(message_data, node_data, event)
        else:
            raise "Unknown Node Type. Fatal Error"


        user_messages = data.get("user_messages", [])
        agent_messages = data.get("agent_messages", [])
        events = data.get("events", [])
        # messages = data.get("messages", [])

        return {"user_messages": user_messages, "agent_messages": agent_messages, "publish_events": events}
