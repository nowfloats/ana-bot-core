"""
This module handles Condition node in ANA studio
Author: https://github.com/velutha
"""
import re
from src.converters.ana.ana_helper import AnaHelper
from src.models.ana_node import AnaNode
from src.utils import Util

class ConditionProcessor():

    def __init__(self, state):
        self.state = state

    def get_next_node(self, node_data):

        next_node_id = node_data.get('NextNodeId', '') #Fallback node id
        variable_data = self.state.get("var_data", {})
        buttons = node_data.get("Buttons")

        for button in buttons:

            root_key = re.split(r'\.|\[', button.get("ConditionMatchKey"))[0]

            if variable_data.get(root_key) is None:
                continue

            path = button.get("ConditionMatchKey")
            obj = {root_key:variable_data[root_key]}
            variable_value = Util.deep_find(obj, path)

            match_operator = button.get("ConditionOperator")
            match_value = AnaHelper.verb_replacer(text=button.get("ConditionMatchValue", ""), state=self.state)

            condition_matched = AnaHelper.is_condition_match(variable_value, match_operator, match_value)
            if condition_matched:
                next_node_id = button["NextNodeId"]
                break

        next_node_key = self.state.get("flow_id", "") + "." + next_node_id
        node_data = AnaNode(next_node_key).get_contents()
        return {"id" : next_node_key, "data": node_data}
