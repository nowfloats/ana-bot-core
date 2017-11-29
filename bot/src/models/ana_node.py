"""
Model for output from ana studio
"""
import json
from src import ANA_CACHE

class AnaNode():

    def __init__(self, node_key):
        self.node_key = node_key

    def get_contents(self, node_key):

        response = ANA_CACHE.get(node_key)

        if response is None:
            print("Data not found for", node_key)
            return {}
        try:
            response_dict = json.loads(response)
            return response_dict
        except Exception as err:
            print(err)
            raise

        # handle response not found or empty ideally this should never happen

    def get_next_node_data(self, flow_id, message_content):
        current_node_contents = self.get_contents(self.node_key)
        input_data = message_content["content"]["input"]
        event_data = {}
        user_input = {}
        node_key = ""

        node_type = current_node_contents.get("NodeType")
        if node_type == "HandoffToAgent":
            return {"node_id": self.node_key, "input_data": user_input}

        # not really neat change it to objects once all buttons are handled
        if "val" in input_data.keys():
            button_contents = self._extract_button_elements(current_node_contents)
            # next_node_buttons = [button for button in button_contents if button.get("ButtonType") in ["NextNode", "OpenUrl"]]
            # button_contents = current_node_contents["Buttons"]
            for button in button_contents:
                # checking both type and ButtonType to handle Carousel Buttons
                button_type = button.get("ButtonType", button.get("Type"))
                var_name = current_node_contents.get("VariableName")
                if button_type in ["NextNode", "OpenUrl"]:
                    current_node_id = input_data["val"]
                    if button["_id"] == current_node_id:
                        if var_name:
                            user_input[var_name] = button.get("VariableValue", "")
                        node_id = button["NextNodeId"]
                        node_key = flow_id + "." + node_id
                        event_data = {
                            "type_of_event": "click",
                            "node_data": current_node_contents,
                            "event_data": button
                            }
                        break
                elif button_type in ["GetText", "GetNumber", "GetPhoneNumber", "GetEmail"]:
                    if var_name:
                        user_input[var_name] = input_data["val"]
                    node_id = button["NextNodeId"]
                    node_key = flow_id + "." + node_id

                    event_data = {
                        "type_of_event": "click",
                        "node_data": current_node_contents,
                        "event_data": button
                        }

                    break
            if node_key:
                pass
            else:
                node_key = self.node_key

        elif "input" in input_data.keys():
            # input_value = input_data["input"]
            button_contents = current_node_contents["Buttons"]
            node_id = ""
            for button in button_contents:
                button_type = button.get("ButtonType", button.get("Type"))
                if button_type in ["GetText", "GetNumber", "GetPhoneNumber", "GetEmail", "GetDate"]:
                    var_name = current_node_contents.get("VariableName", "DEFAULT_VAR")
                    user_input[var_name] = input_data["input"]
                    node_id = button["NextNodeId"]
                    event_data = {
                        "type_of_event": "click",
                        "node_data": current_node_contents,
                        "event_data": button
                        }
                    break
            if node_id != "":
                node_key = flow_id + "." + node_id
            else:
                node_key = self.node_key
        elif "location" in input_data.keys():
            button_contents = current_node_contents["Buttons"]
            node_id = ""
            for button in button_contents:
                button_type = button.get("ButtonType", button.get("Type"))
                if button_type == "GetLocation":
                    var_name = current_node_contents.get("VariableName", "DEFAULT_VAR")
                    user_input[var_name] = input_data["location"]
                    node_id = button["NextNodeId"]
                    event_data = {
                        "type_of_event": "click",
                        "node_data": current_node_contents,
                        "event_data": button
                        }
                    break
            if node_id != "":
                node_key = flow_id + "." + node_id
            else:
                node_key = self.node_key
        elif "address" in input_data.keys():
            button_contents = current_node_contents["Buttons"]
            node_id = ""
            for button in button_contents:
                button_type = button.get("ButtonType", button.get("Type"))
                if button_type == "GetAddress":
                    var_name = current_node_contents.get("VariableName", "DEFAULT_VAR")
                    user_input[var_name] = input_data["address"]
                    node_id = button["NextNodeId"]
                    event_data = {
                        "type_of_event": "click",
                        "node_data": current_node_contents,
                        "event_data": button
                        }
                    break
            if node_id != "":
                node_key = flow_id + "." + node_id
            else:
                node_key = self.node_key
        elif "date" in input_data.keys():
            button_contents = current_node_contents["Buttons"]
            node_id = ""
            for button in button_contents:
                button_type = button.get("ButtonType", button.get("Type"))
                if button_type == "GetDate":
                    var_name = current_node_contents.get("VariableName", "DEFAULT_VAR")
                    user_input[var_name] = input_data["date"]
                    node_id = button["NextNodeId"]
                    event_data = {
                        "type_of_event": "click",
                        "node_data": current_node_contents,
                        "event_data": button
                        }
                    break
            if node_id != "":
                node_key = flow_id + "." + node_id
            else:
                node_key = self.node_key
        elif "time" in input_data.keys():
            button_contents = current_node_contents["Buttons"]
            node_id = ""
            for button in button_contents:
                button_type = button.get("ButtonType", button.get("Type"))
                if button_type == "GetTime":
                    var_name = current_node_contents.get("VariableName", "DEFAULT_VAR")
                    user_input[var_name] = input_data["time"]
                    node_id = button["NextNodeId"]
                    event_data = {
                        "type_of_event": "click",
                        "node_data": current_node_contents,
                        "event_data": button
                        }
                    break
            if node_id != "":
                node_key = flow_id + "." + node_id
            else:
                node_key = self.node_key
        else:
            print("Unknown input data found", input_data)

        return {"node_id": node_key, "input_data": user_input, "event_data": event_data}

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
