import re
import json
from src.logger import logger
from src.utils import Util

class AnaHelper():

    @staticmethod
    def is_condition_match(left_operand, operator, right_operand):

        match = 0

        if left_operand is None or right_operand is None:
            return match

        if isinstance(left_operand, bool):

            left_operand = "true" if left_operand else "false"

        elif isinstance(left_operand, float):

            try:
                left_operand = float(left_operand)
                right_operand = float(right_operand)
            except ValueError:
                left_operand = str(left_operand)
                right_operand = str(right_operand)

        elif isinstance(left_operand, int):

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
            match = right_operand in left_operand

        elif operator == "IsNull":
            match = bool(left_operand) is False

        elif operator == "Between":
            values = right_operand.split(",")[:2]
            match = left_operand > values[0] and left_operand < values[1]
        else:
            logger.error(f"Unknown operator found {operator}")

        return match

    @staticmethod
    def verb_replacer(text, state):
        if text is None:
            return text
        variable_data = state.get("var_data", {})

        logger.debug(f"variable_data {variable_data} {variable_data.__class__}")
        logger.debug(f"text received for replacing verbs is {text}")

        # if isinstance(variable_data, str):
            # variable_data = json.loads(variable_data)

        all_matches = re.findall(r"\[~(.*?)\]|{{(.*?)}}", text)

        for matches in all_matches:
            for match in matches:
                logger.debug(f"match: {match}")
                if variable_data.get(match, None) is not None:
                    logger.debug(f"Match exists in variable_data {variable_data[match]}")
                    variable_value = variable_data[match]
                    variable_value = str(AnaHelper.escape_json_text(variable_value))
                    text = text.replace("[~" + match + "]", variable_value).replace("{{" + match + "}}", variable_value)
                    logger.debug(f"Text just after replacing is {text}")
                else:
                    logger.debug("No exact match")
                    root_key = re.split(r"\.|\[", match)[0]
                    logger.debug(f"match: {match}")
                    logger.debug(f"root_key: {root_key}")
                    if variable_data.get(root_key, None) is None:
                        continue
                    variable_value = Util.deep_find({root_key:variable_data[root_key]}, match)
                    variable_value = str(AnaHelper.escape_json_text(variable_value))
                    logger.debug(f"match: {match}")
                    logger.debug(f"variable_value: {variable_value}")
                    text = text.replace("[~" + match + "]", str(variable_value)).replace("{{" + match + "}}", str(variable_value))
        logger.debug(f"Text after replacing verbs is {text}")
        return text

    @staticmethod
    def escape_json_text(text):
        if isinstance(text, str):
            text = text.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")
        return text
