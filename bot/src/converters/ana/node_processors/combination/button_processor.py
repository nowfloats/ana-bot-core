"""
This module handles buttons inside combination node of ana studio output
Author: https://github.com/velutha
"""
import json
from src.config import ana_config as config
from src.models.types import MessageTypeWrapper as MessageType, InputTypeWrapper as InputType, ButtonTypeWrapper as ButtonType
from src.models.message import MessageContentWrapper as MessageContent, MessageDataWrapper as MessageData
from src.models.inputs import TextInputWrapper as TextInput
from src.logger import logger

class ButtonProcessor():

    def __init__(self, state):
        self.state = state
        self.click_inputs = config["click_input_types"]
        self.text_inputs = config["text_input_types"]

    def process(self, buttons):

        click_elements = [button for button in buttons if button["ButtonType"] in self.click_inputs]
        text_elements = [button for button in buttons if button["ButtonType"] in self.text_inputs]

        messages_data = []


        if click_elements != [] and text_elements == []:
            messages_data = self.__process_click_inputs(click_elements, mandatory=1)
        elif click_elements != [] and text_elements != []:
            messages_data = self.__process_click_inputs(click_elements, mandatory=0)
        elif click_elements == [] and text_elements != []:
            messages_data = self.__process_text_inputs(text_elements)

        return messages_data

    @classmethod
    def __process_click_inputs(cls, data, mandatory):

        button_heading = None
        elem_message_data = []
        elem_options = []

        message_type = MessageType.get_value("INPUT")
        input_type = InputType.get_value("OPTIONS")

        for button in data:
            button_type = button.get("ButtonType", "")
            if button_type == "OpenUrl":
                button_heading = "Choose an option" # to be compatible with fb quick_replies
                option = {
                    "title": button.get("ButtonName", ""),
                    "value": json.dumps({"url": button["Url"], "value": button["_id"]}),
                    "type": ButtonType.get_value("URL")
                    }
            elif button_type == "NextNode":
                button_heading = "Choose an option" # to be compatible with fb quick_replies
                option = {
                    "title": button.get("ButtonName", button.get("ButtonText", "")),
                    "value": button.get("_id", ""),
                    "type": ButtonType.get_value("QUICK_REPLY")
                    }

            elem_options.append(option)

        if elem_options != []:
            message_content = MessageContent(
                inputType=input_type,
                mandatory=mandatory,
                options=elem_options,
                text=button_heading
                ).trim()
            message_data = MessageData(
                type=message_type,
                content=message_content
                ).trim()
            elem_message_data.append(message_data)

        return elem_message_data

    @classmethod
    def __process_text_inputs(cls, data):

        elem_message_data = []

        for button in data:
            button_type = button.get("ButtonType")
            message_type = ""
            input_type = ""
            input_attr = None
            content = None

            message_type = MessageType.get_value("INPUT")

            if button_type == "GetText":
                input_type = InputType.get_value("TEXT")
                input_attr = TextInput(placeHolder=button.get("PlaceholderText", "")).trim()
            elif button_type == "GetNumber":
                input_type = InputType.get_value("NUMERIC")
            elif button_type == "GetPhoneNumber":
                input_type = InputType.get_value("PHONE")
            elif button_type == "GetEmail":
                input_type = InputType.get_value("EMAIL")
            elif button_type == "GetLocation":
                input_type = InputType.get_value("LOCATION")
            elif button_type == "GetAddress":
                input_type = InputType.get_value("ADDRESS")
            elif button_type == "GetDate":
                input_type = InputType.get_value("DATE")
            elif button_type == "GetTime":
                input_type = InputType.get_value("TIME")
            elif button_type == "GetItemFromSource":
                pass
            else:
                logger.warning("Undefined Text Input Type" + str(button_type))

            content = MessageContent(
                inputType=input_type,
                textInputAttr=input_attr,
                mandatory=1,
                ).trim()
            message_data = MessageData(
                type=message_type,
                content=content
                ).trim()
            elem_message_data.append(message_data)


        return elem_message_data
