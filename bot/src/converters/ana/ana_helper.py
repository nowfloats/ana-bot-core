import re
from src.logger import logger

class AnaHelper():

    @staticmethod
    def is_condition_match(left_operand, operator, right_operand):

        match = 0

        if left_operand is None or right_operand is None:
            return match

        if isinstance(left_operand, int) or isinstance(right_operand, int):
            left_operand = int(left_operand)
            right_operand = int(right_operand)

        if operator == "EqualTo":
            match = left_operand == right_operand

        elif operator == "NotEqualTo":
            match = left_operand != right_operand

        elif operator == "GreaterThan":
            match = left_operand > right_operand

        elif operator == "LessThan":
            match = left_operand < right_operand

        elif operator == "GreaterThanOrEqualTo":
            match = left_operand >= right_operand

        elif operator == "LessThanOrEqualTo":
            match = left_operand <= right_operand

        elif operator == "Mod":
            match = left_operand % right_operand

        elif operator == "In":
            values = right_operand.split(",")
            match = left_operand in values

        elif operator == "NotIn":
            values = right_operand.split(",")
            match = left_operand not in values

        elif operator == "StartsWith":
            match = left_operand.startswith(right_operand)

        elif operator == "EndsWith":
            match = left_operand.endswith(right_operand)

        elif operator == "Contains":
            match = left_operand in right_operand

        elif operator == "Between":
            values = right_operand.split(",")[:2]
            match = left_operand > values[0] and left_operand < values[1]
        else:
            logger.error(f"Unknown operator found {operator}")

        return match

    @staticmethod
    def verb_replacer(text, state):
        variable_data = state.get("var_data", {})
        if type(variable_data) is dict:
            matches = re.findall(r"\[~(.*?)\]|{{(.*?)}}", text)
            for match in matches:
                if len(match) > 0:
                    match = match[0]
                if variable_data.get(match, None) is not None:
                    text = text.replace("[~" + match + "]", variable_data[match]).replace("{{" + match + "}}",variable_data[match])
                else:
                    root_key = re.split('\.|\[', match)[0]
                    if variable_data.get(root_key, None) is None:
                        continue
                    variable_value = Util.deep_find({ root_key:variable_data[root_key] }, match)
                    text = text.replace("[~" + match + "]", variable_value).replace("{{" + match + "}}", variable_value)
            return text
        return text
