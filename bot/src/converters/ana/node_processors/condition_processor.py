"""
This module handles Condition node in ANA studio
Author: https://github.com/velutha
"""
from src.converters.ana.ana_helper import AnaHelper
from src.models.ana_node import AnaNode
from src.utils import Util

class ConditionProcessor():

    def __init__(self, state):
        self.state = state

    def get_next_node(self, node_data):

        next_node_id = ""
        variable_data = self.state.get("var_data", {})
        buttons = node_data.get("Buttons")

        for button in buttons:
            match_keys = button.get("ConditionMatchKey").split(".")
            match_operator = button.get("ConditionOperator")
            match_value = button.get("ConditionMatchValue")

            variable_value = Util.deep_find(variable_data, match_keys)

            condition_matched = AnaHelper().is_condition_match(variable_value, match_operator, match_value)
            if condition_matched:
                next_node_id = button["NextNodeId"]
                break

        next_node_key = self.state.get("flow_id", "") + "." + next_node_id
        node_data = AnaNode(next_node_key).get_contents()
        return {"id" : next_node_key, "data": node_data}
