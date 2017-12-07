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

    def get_messages_data(self, node_data):

        node_type = node_data.get("NodeType", "")

        node_processor_map = {
            "Combination": CombinationProcessor,
            "ApiCall": ApiCallProcessor,
            "Condition": ConditionProcessor,
            "Card": CardProcessor,
            "HandoffToAgent": AgentHandOffProcessor
            }

        if node_type in ["Combination"]:
            Processor = node_processor_map.get(node_type)
            data = Processor(self.state).process_node(node_data)

        elif node_type in ["ApiCall", "Condition"]:
            Processor = node_processor_map.get(node_type)
            next_node_data = Processor(self.state).get_next_node(node_data)
            data = self.get_messages_data(next_node_data.get("data"))
            # this should ideally not happen here this
            # change current_node_id thing in converter
            # both should use the same method
            self.state["current_node_id"] = next_node_data.get("id")

        elif node_type == "HandoffToAgent":
            data = {}

        else:
            raise "Unknown Node Type. Fatal Error"


        messages = data.get("messages", [])
        events = data.get("events", [])

        return {"messages": messages, "events": events}
