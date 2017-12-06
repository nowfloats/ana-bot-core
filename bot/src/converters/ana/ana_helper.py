from src.logger import logger

class AnaHelper():

    @classmethod
    def is_condition_match(cls, left_operand, operator, right_operand):

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
            match = int(left_operand) % int(right_operand)

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
            match = int(left_operand) > int(values[0]) and int(left_operand) < int(values[1])
        else:
            logger.error(f"Unknown operator found {operator}")

        return match
