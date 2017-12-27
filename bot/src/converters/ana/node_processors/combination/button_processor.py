"""
This module handles buttons inside combination node of ana studio output
Author: https://github.com/velutha
"""
import json
from src.config import ana_config as config
from src.models.types import MessageTypeWrapper as MessageType, InputTypeWrapper as InputType, ButtonTypeWrapper as ButtonType,\
        MediaTypeWrapper as MediaType
from src.models.message import MessageContentWrapper as MessageContent, MessageDataWrapper as MessageData
from src.models.inputs import TextInputWrapper as TextInput, OptionWrapper as Option, ListItemWrapper as ListItem
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

        button_heading = "Choose an option"
        elem_options = [cls.__process_click_button(button) for button in data]

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

        elem_message_data = [cls.__process_input_button(button) for button in data]

        return elem_message_data

    @classmethod
    def __process_click_button(cls, button):
        button_type = button.get("ButtonType", "")

        title = button.get("ButtonName", button.get("ButtonText", ""))

        if button_type == "OpenUrl":
            value = json.dumps({"url": button["Url"], "value": button["_id"]})
            type_of_button = ButtonType.get_value("URL")
        elif button_type == "NextNode":
            value = button["_id"]
            type_of_button = ButtonType.get_value("QUICK_REPLY")

        option = Option(title=title, value=value, type=type_of_button).trim()
        return option

    @classmethod
    def __process_input_button(cls, button):

        button_type = button.get("ButtonType")

        if button_type == "GetItemFromSource":
            message_data = cls.__process_getitem_button(button)
            return message_data

        message_type = ""
        input_type = ""
        input_attr = None
        content = None

        message_type = MessageType.get_value("INPUT")
        input_attr = TextInput(placeHolder=button.get("PlaceholderText", "")).trim()

        button_type_map = config["button_map"]

        elem_type = button_type_map.get(button_type)
        if elem_type is None:
            logger.warning("Undefined Input Type" + str(button_type))

        type_of_input = elem_type["input_type"]
        type_of_media = elem_type["media_type"]

        input_type = InputType.get_value(type_of_input)
        media_type = MediaType.get_value(type_of_media)

        content = MessageContent(
            inputType=input_type,
            mediaType=media_type,
            textInputAttr=input_attr,
            mandatory=1,
            ).trim()
        message_data = MessageData(
            type=message_type,
            content=content
            ).trim()

        return message_data

    @classmethod
    def __process_getitem_button(cls, data):

        source = data.get("ItemsSource")
        values = list(map(lambda x: ListItem(text=x.split(":")[0], value=x.split(":")[1]).trim(), source.split(",")))
        button_text = data.get("ButtonName")

        message_type = MessageType.get_value("INPUT")
        input_type = InputType.get_value("LIST")
        is_multiple = 1 if data.get("AllowMultiple") else 0

        content = MessageContent(
            inputType=input_type,
            text=button_text,
            multiple=is_multiple,
            mandatory=1,
            values=values
            ).trim()

        message_data = MessageData(
            type=message_type,
            content=content
            ).trim()

        return message_data
