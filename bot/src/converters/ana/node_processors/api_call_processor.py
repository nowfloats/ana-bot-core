from functools import reduce
import requests
from src.converters.ana.ana_helper import AnaHelper
from src.models.ana_node import AnaNode
from src.logger import logger
from src.utils import Util

class ApiCallProcessor():

    def __init__(self, state):
        self.state = state

    def get_next_node(self, node_data):

        next_node_data = {}

        api_response = self.__make_api_call(node_data)
        next_node_data = self.__validate_api_response(response=api_response, node_data=node_data)

        return next_node_data

    @staticmethod
    def __make_api_call(node_data):

        api_url = node_data.get("ApiUrl")
        api_method = node_data.get("ApiMethod")

        api_headers = {}
        headers = node_data.get("Headers", "").split("\n")
        for header_line in headers:
            header_key_values = header_line.split(":")[:2]
            api_headers[header_key_values[0]] = header_key_values[1]

        api_body = node_data.get("Body", {})
        response = requests.request(method=api_method, url=api_url, headers=api_headers, data=api_body)
        if response.status_code == 200:
            api_response = response.json()
        else:
            logger.error(f"ApiCall did not return status code 200 {node_data['Id']}")

        return api_response

    def __validate_api_response(self, response, node_data):

        if response is None:
            return {"id": "", "data": {}}

        next_node_key = ""
        variable_data = self.state.get("var_data", {})
        buttons = node_data.get("Buttons")

        if isinstance(response, dict):
            # json response from api

            for button in buttons:
                match_keys = button.get("ConditionMatchKey").split(".")
                variable_name = match_keys.pop(0)

                final_var_data = Util.merge_dicts(variable_data, {variable_name : response})

                match_operator = button.get("ConditionOperator")
                match_value = button.get("ConditionMatchValue")

                import pdb
                pdb.set_trace()
                variable_value = self.__deep_match(final_var_data, match_keys)
                pdb.set_trace()

                condition_matched = AnaHelper().is_condition_match(variable_value, match_operator, match_value)
                if condition_matched:
                    next_node_id = button["NextNodeId"]
                    break

            next_node_key = self.state.get("flow_id", "") + "." + next_node_id
            next_node_data = AnaNode(next_node_key).get_contents()
        else:
            # string response from api
            for button in buttons:
                match_keys = button.get("ConditionMatchKey").split(".")
                variable_name = match_keys.pop(0)

                final_var_data = Util.merge_dicts(variable_data, {variable_name : response})

                match_operator = button.get("ConditionOperator")
                match_value = button.get("ConditionMatchValue")

                variable_value = self.__deep_match(final_var_data, match_keys)
                import pdb
                pdb.set_trace()

                condition_matched = AnaHelper().is_condition_match(variable_value, match_operator, match_value)
                if condition_matched:
                    next_node_id = button["NextNodeId"]
                    break

            next_node_key = self.state.get("flow_id", "") + "." + next_node_id
            next_node_data = AnaNode(next_node_key).get_contents()

        return {"id": next_node_key, "data": next_node_data}

    @classmethod
    def __deep_match(cls, dictionary, *keys):
        return reduce(lambda d, key: d.get(key, None) if d else None, keys, dictionary)
