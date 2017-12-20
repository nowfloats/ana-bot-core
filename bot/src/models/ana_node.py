"""
Model for output from ana studio
"""
import json
from src import ANA_CACHE
from src.logger import logger
from src.config import ana_config as config

class AnaNode():

    def __init__(self, node_key):
        self.node_key = node_key

    def get_contents(self):

        response = ANA_CACHE.get(self.node_key)

        if response is None:
            logger.warning("Data not found for" + str(self.node_key))
            return {}
        try:
            response_dict = json.loads(response)
            return response_dict
        except Exception as err:
            logger.error(err)
            raise
        # handle response not found or empty ideally this should never happen

    def get_next_node_data(self, flow_id, message_content):

        current_node_contents = self.get_contents()
        input_data = message_content["content"]["input"]

        node_type = current_node_contents.get("NodeType")
        # current node is agent node, so continue as is
        if node_type == "HandoffToAgent":
            return {"node_id": self.node_key, "input_data": {}}


        next_node_data = self.__get_next_node_data(input_data=input_data, node_content=current_node_contents)

        next_node_id = next_node_data.get("node_id", "")
        node_key = flow_id + "." + next_node_id if next_node_id != "" else self.node_key

        events = next_node_data["event_data"]
        user_input = next_node_data["user_input"]

        return {"node_id": node_key, "input_data": user_input, "events": events}


    @classmethod
    def __get_next_node_data(cls, input_data, node_content):

        next_node_id = ""
        event_data = []
        user_input = {}
        var_name = node_content.get("VariableName")

        button_contents = cls._extract_button_elements(node_content)

        click_buttons = cls._get_button_elements(buttons=button_contents, type_of_button="click")
        input_buttons = cls._get_button_elements(buttons=button_contents, type_of_button="input")

        input_key = list(input_data.keys())[0]


        if input_key == "val":

            for button in click_buttons:
                current_node_id = input_data["val"]
                if button["_id"] == current_node_id:
                    if var_name:
                        user_input[var_name] = button.get("VariableValue", "")
                    next_node_id = button["NextNodeId"]
                    event_data.append({
                        "type_of_event": "click",
                        "node_data": node_content,
                        "event_data": button
                        })
                    break

            if next_node_id == "":
                for button in input_buttons:
                    if var_name:
                        user_input[var_name] = input_data["val"]
                    next_node_id = button["NextNodeId"]
                    event_data.append({
                        "type_of_event": "click",
                        "node_data": node_content,
                        "event_data": button
                        })
                    break

            # for button in button_contents:
                # button_type = button.get("ButtonType", button.get("Type"))
                # var_name = node_content.get("VariableName")
                # if button_type in ["NextNode", "OpenUrl"]:
                    # current_node_id = input_data["val"]
                    # if button["_id"] == current_node_id:
                        # if var_name:
                            # user_input[var_name] = button.get("VariableValue", "")
                        # next_node_id = button["NextNodeId"]
                        # event_data.append({
                            # "type_of_event": "click",
                            # "node_data": node_content,
                            # "event_data": button
                            # })
                        # break
                # elif button_type in ["GetText", "GetNumber", "GetPhoneNumber", "GetEmail"]:
                    # if var_name:
                        # user_input[var_name] = input_data["val"]
                    # next_node_id = button["NextNodeId"]
                    # event_data.append({
                        # "type_of_event": "click",
                        # "node_data": node_content,
                        # "event_data": button
                        # })

                    # break
        else:

            valid_button_types = cls.__get_button_types(input_key)

            for button in button_contents:
                button_type = button.get("ButtonType", button.get("Type"))
                if button_type in valid_button_types:
                    var_name = node_content.get("VariableName", "DEFAULT_VAR")
                    user_input[var_name] = input_data[input_key]
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
            logger.error("Unknown input type found " + input_type)

        button_types = input_to_button_types_map.get(input_type, [])

        return button_types
