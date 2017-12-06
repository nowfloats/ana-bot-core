from src.models.ana_node import AnaNode
from src.converters.ana.ana_helper import AnaHelper

class ConditionProcessor():

    def __init__(self, state):
        self.state = state

    def get_next_node(self, node_data):

        next_node_id = ""
        variable_data = self.state.get("var_data", {})
        variables = variable_data.keys()
        buttons = node_data.get("Buttons")

        for button in buttons:
            match_key = button.get("ConditionMatchKey")
            match_operator = button.get("ConditionOperator")
            match_value = button.get("ConditionMatchValue")

            variable_value = ""
            if match_key in variables:
                variable_value = variable_data[match_key]

            condition_matched = AnaHelper().is_condition_match(variable_value, match_operator, match_value)
            if condition_matched:
                next_node_id = button["NextNodeId"]
                break

        next_node_key = self.state.get("flow_id", "") + "." + next_node_id
        node_data = AnaNode(next_node_key).get_contents()
        return {"id" : next_node_key, "data": node_data}
