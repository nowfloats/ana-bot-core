import re
from src.logger import logger
from src.utils import Util

class AnaHelper():

    @staticmethod
    def is_condition_match(left_operand, operator, right_operand):

        match = 0

        if left_operand is None or right_operand is None:
            return match
        
        if isinstance(left_operand, int) or isinstance(right_operand, int):
            left_operand = int(left_operand)
            right_operand = int(right_operand)
        
        isFloat = False
        try:
            _left_operand = float(left_operand)
            _right_operand = float(right_operand)
            isFloat = True
        except Exception as err:
            pass

        if isFloat:
            left_operand = _left_operand
            right_operand = _right_operand
        else: # assume as string
            left_operand = str(left_operand)
            right_operand = str(right_operand)

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
        variable_data = state.get("var_data", {})
        logger.debug("variable_data" + str(variable_data)) 
        logger.debug("text" + str(text)) 
        if type(variable_data) is dict:
            all_matches = re.findall(r"\[~(.*?)\]|{{(.*?)}}", text)
            for matches in all_matches:
                for match in matches:
                    logger.debug("match: " + str(match))
                    if variable_data.get(match, None) is not None:
                        text = text.replace("[~" + match + "]", variable_data[match]).replace("{{" + match + "}}",variable_data[match])
                    else:
                        logger.debug("No exact match") 
                        root_key = re.split('\.|\[', match)[0]
                        logger.debug("match: " + str(match))
                        logger.debug("root_key: " + str(root_key))
                        if variable_data.get(root_key, None) is None:
                            continue
                        variable_value = Util.deep_find({ root_key:variable_data[root_key] }, match)
                        logger.debug("match: " + str(match))
                        logger.debug("variable_value: " + str(variable_value))
                        text = text.replace("[~" + match + "]", str(variable_value)).replace("{{" + match + "}}", str(variable_value))
            return text
        return text
