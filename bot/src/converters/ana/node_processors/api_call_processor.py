"""
This module handles ApiCall node in ANA studio
Author: https://github.com/velutha
"""
import re
import json
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
        next_node_data = self.__handle_api_response(response=api_response, node_data=node_data)

        return next_node_data

    def __make_api_call(self, node_data):

        api_url = node_data.get("ApiUrl", "")
        api_method = node_data.get("ApiMethod")
        api_url = AnaHelper.verb_replacer(text=api_url, state=self.state)

        api_headers = {}
        headers = node_data.get("Headers", "").split("\n")
        for header_line in headers:
            header_key_values = header_line.split(":")[:2]
            if len(header_key_values) == 2:
                api_headers[header_key_values[0]] = header_key_values[1]

        logger.debug(f"api headers: {api_headers}")
        api_body = node_data.get("RequestBody", "")
        if api_body:
            api_body = AnaHelper.verb_replacer(text=api_body, state=self.state)

        logger.debug(f"api_body: {api_body}")
        response = requests.request(method=api_method, url=api_url, headers=api_headers, data=api_body)

        logger.debug(f"api response: {response}")
        if response.status_code == 200:
            try:
                api_response = response.json()
            except Exception as err:
                api_response = response.text
        else:
            api_response = None
            logger.error(f"ApiCall did not return status code 200 {node_data['Id']}")

        return api_response

    def __handle_api_response(self, response, node_data):

        variable_data = json.loads(self.state.get("var_data", "{}"))
        variable_name = node_data["VariableName"]
        logger.debug(f"Variable Name is {variable_name}")
        logger.debug(f"Response from api is {response} {response.__class__}")
        logger.debug(f"Variable Data is {variable_data} {variable_data.__class__}")
        if bool(response) is True:
            variable_data = Util.merge_dicts(variable_data, {variable_name : response})
            self.state["var_data"] = variable_data

        next_node_id = self.__get_next_node_id(data=variable_data, state=self.state, node_data=node_data)
        next_node_key = self.state.get("flow_id", "") + "." + next_node_id
        next_node_data = AnaNode(next_node_key).get_contents()

        return {"id": next_node_key, "data": next_node_data}

    @classmethod
    def __get_next_node_id(cls, data, state, node_data):

        next_node_id = node_data.get('NextNodeId', '') # Fallback node id

        for button in node_data.get('Buttons', []):
            root_key = re.split('\.|\[', button.get("ConditionMatchKey"))[0]
            if data.get(root_key, None) is None:
                continue
            logger.debug(f"rootKey %s {root_key}")
            path = button.get("ConditionMatchKey")
            obj = {root_key:data[root_key]}
            variable_value = Util.deep_find(obj, path)

            match_operator = button.get("ConditionOperator")
            match_value = AnaHelper.verb_replacer(text=button.get("ConditionMatchValue", ""), state=state)

            condition_matched = AnaHelper.is_condition_match(variable_value, match_operator, match_value)

            if condition_matched:
                next_node_id = button["NextNodeId"]
                break

        return next_node_id
