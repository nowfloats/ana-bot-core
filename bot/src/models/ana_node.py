"""
Model for output from ana studio
"""
import json
from src import CACHE
from src.logger import logger
from src.config import ana_config as config
from src.converters.ana.ana_helper import AnaHelper

class AnaNode():

    def __init__(self, node_key):
        self.node_key = node_key

    def get_contents(self):

        response = CACHE.get(self.node_key)

        if response is None:
            logger.warning(f"Data not found for {self.node_key}")
            return {}
        try:
            response_dict = json.loads(response)
            return response_dict
        except Exception as err:
            logger.error(err)
            raise
        # handle response not found or empty ideally this should never happen

    def get_next_node_data(self, message_content, state):

        current_node_contents = self.get_contents()
        input_data = message_content["content"]["input"]

        next_node_data = self.__get_next_node_data(input_data=input_data, node_content=current_node_contents, state=state)

        next_node_id = next_node_data.get("node_id", "")
        node_key = state.get("flow_id", "")+ "." + next_node_id if next_node_id != "" else self.node_key

        events = next_node_data["event_data"]
        user_input = next_node_data["user_input"]

        return {"node_id": node_key, "input_data": user_input, "publish_events": events}


    @classmethod
    def __get_next_node_data(cls, input_data, node_content, state):

        # TODO cleanup required here too many loops and variables
        next_node_id = ""
        event_data = []
        user_input = {}
        var_name = node_content.get("VariableName", "")

        button_contents = cls._extract_button_elements(node_content)

        click_buttons = cls._get_button_elements(buttons=button_contents, type_of_button="click")
        input_buttons = cls._get_button_elements(buttons=button_contents, type_of_button="input")

        input_key = list(input_data.keys())[0]

        if input_key == "val":

            for button in click_buttons:
                current_node_id = input_data["val"]
                if button["_id"] == current_node_id:
                    if var_name:
                        var_val = button.get("VariableValue", "")
                        user_input[var_name] = AnaHelper.verb_replacer(text=var_val, state=state)
                    next_node_id = button["NextNodeId"]
                    event_data.append({
                        "type_of_event": "click",
                        "node_data": node_content,
                        "event_data": button
                        })
                    break

            if next_node_id == "":
                for button in input_buttons:
                    button_type = button.get("ButtonType", button.get("Type"))

                    if button_type == "GetNumber":
                        input_value = float(input_data["val"])
                    else:
                        input_value = str(input_data["val"])

                    if var_name:
                        user_input[var_name] = input_value
                    next_node_id = button["NextNodeId"]
                    event_data.append({
                        "type_of_event": "click",
                        "node_data": node_content,
                        "event_data": button
                        })
                    break

        else:

            valid_button_types = cls.__get_button_types(input_key)

            for button in button_contents:
                button_type = button.get("ButtonType", button.get("Type"))
                if button_type in valid_button_types:
                    if button_type == "GetNumber":
                        input_value = int(input_data[input_key])
                    else:
                        input_value = str(input_data[input_key])

                    if var_name:
                        user_input[var_name] = input_value
                    next_node_id = button["NextNodeId"]
                    event_data.append({
                        "type_of_event": "click",
                        "node_data": node_content,
                        "event_data": button
                        })
                    break

        return {"node_id": next_node_id, "event_data": event_data, "user_input": user_input}

    @classmethod
    def _extract_button_elements(cls, data):

        node_buttons = data.get("Buttons", [])
        sections = data.get("Sections", [])
        section_buttons = []

        for section in sections:
            if section["SectionType"] == "Carousel":
                section_items = section["Items"]
                for item in section_items:
                    button_element = item.get("Buttons", [])
                    section_buttons = section_buttons + button_element
        return node_buttons + section_buttons

    @classmethod
    def _get_button_elements(cls, buttons, type_of_button):

        button_elements = []
        valid_button_types = []

        if type_of_button == "click":
            valid_button_types = config["click_input_types"]
        elif type_of_button == "input":
            valid_button_types = config["text_input_types"]

        for button in buttons:
            button_type = button.get("ButtonType", button.get("Type"))
            if button_type in valid_button_types:
                button_elements.append(button)

        return button_elements

    @classmethod
    def __get_button_types(cls, input_type):

        input_to_button_types_map = {
            "input": ["GetText", "GetNumber", "GetPhoneNumber", "GetEmail", "GetDate"],
            "location": ["GetLocation"],
            "address": ["GetAddress"],
            "date": ["GetDate"],
            "time": ["GetTime"],
            "media": ["GetImage", "GetFile, GetAudio, GetVideo"]
            }

        if input_type not in input_to_button_types_map.keys():
            logger.error(f"Unknown input type found {input_type}")

        button_types = input_to_button_types_map.get(input_type, [])

        return button_types
