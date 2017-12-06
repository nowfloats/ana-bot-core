from src.logger import logger
from src.models.ana_node import AnaNode

class ConditionProcessor():

    def __init__(self, state):
        self.state = state

    def process_node(self, node_data):

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

            condition_matched = self.__is_condition_match(variable_value, match_operator, match_value)
            if condition_matched:
                next_node_id = button["NextNodeId"]
                break

        node_key = self.state.get("flow_id", "") + "." + next_node_id
        node_data = AnaNode(node_key).get_contents()
        return node_data

    @classmethod
    def __is_condition_match(cls, left_operand, operator, right_operand):

        match = 0

        if operator == "EqualTo":
            match = int(left_operand) == int(right_operand)

        elif operator == "NotEqualTo":
            match = int(left_operand) != int(right_operand)

        elif operator == "GreaterThan":
            match = int(left_operand) > int(right_operand)

        elif operator == "LessThan":
            match = int(left_operand) < int(right_operand)

        elif operator == "GreaterThanOrEqualTo":
            match = int(left_operand) >= int(right_operand)

        elif operator == "LessThanOrEqualTo":
            match = int(left_operand) <= int(right_operand)

        elif operator == "Mod":
            pass
        elif operator == "In":
            pass
        elif operator == "NotIn":
            pass
        elif operator == "StartsWith":
            pass
        elif operator == "EndsWith":
            pass
        elif operator == "Contains":
            pass
        elif operator == "Between":
            pass
        else:
            logger.error(f"Unknown operator found {operator}")

        return match
