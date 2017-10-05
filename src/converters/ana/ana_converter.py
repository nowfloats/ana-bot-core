from src.config import ana_config
from src.thrift_models.ttypes import MessageType, InputType
from src.models.message import MessageContent, MessageData, Message
import json

class Converter():

    def __init__(self, *args, **kwargs):
        self.messages = []
        # self.section_types = ana_config.section_types
        # self.node_types = ana_config.node_types
        # self.button_types = ana_config.button_types
        pass

    def get_messages_data(self, node_data, message_content):
        if (node_data == {}): 
            return []
        node_type = node_data["NodeType"]
        messages = []
        if node_type == "Combination":
            sections_data = node_data["Sections"]
            buttons_data = node_data["Buttons"]
            sections_response = self.convert_sections(sections_data)
            buttons_response = self.convert_buttons(buttons_data)
            messages = sections_response + buttons_response
        elif node_type == "ApiCall":
            pass
        return messages

    def convert_sections(self,data):
        messages_data = []
        for section in data:
            if section["SectionType"] == "Text":
                message_type = MessageType._NAMES_TO_VALUES["SIMPLE"]
                text = section["Text"]
                message_content = MessageContent(text=text).trim()
                # print(message_content)
                message_data = MessageData(type=message_type, content=message_content).trim()
                messages_data.append(message_data)
                pass
            elif section["SectionType"] == "Carousel":
                pass
        return messages_data
        
    def convert_buttons(self,data):
        next_node_elem_message_data = []
        other_elem_message_data = []
        next_node_elements = []
        other_elements = []

        for button in data:
            if button["ButtonType"] == "NextNode":
                next_node_elements.append(button)
            if button["ButtonType"] in ["GetText", "GetNumber", "GetPhoneNumber", "GetEmail"]:
                other_elements.append(button)

        next_node_elem_message_type = MessageType._NAMES_TO_VALUES["INPUT"]
        next_node_elem_input_type = InputType._NAMES_TO_VALUES["OPTIONS"]
        next_node_elem_options = []

        # print(next_node_elements)
        for button in next_node_elements:
            option = {
                    "title": button["ButtonName"],
                    "value": button.get("NextNodeId", "")
                    }
            next_node_elem_options.append(option)

        if (next_node_elem_options != []):
            next_node_elem_content = MessageContent(
                    inputType=next_node_elem_input_type,
                    mandatory=1,
                    options=next_node_elem_options
                    ).trim()
            next_node_message_data = MessageData(
                    type=next_node_elem_message_type,
                    content=next_node_elem_content
                    ).trim()
            next_node_elem_message_data.append(next_node_message_data)

        # other_elem_data = []
        # for button in other_elements:
            # button_type = button["ButtonType"]
            # if button_type == "GetText":
                # content = MessageContent(
                        # inputType=InputType._NAMES_TO_VALUES["TEXT"],
                        # mandatory=1,
                        # )
                # pass
            # elif button_type == "GetNumber":
                # pass
            # elif button_type == "GetPhoneNumber":
                # pass
            # elif button_type == "GetEmail":
                # pass
            # else:
                # print(e)
                # raise

        messages_data = next_node_elem_message_data + other_elem_message_data
        # for next_node_elements
        # take out nextnode elements and convert them into input.options
        # remaining element as another input element accordingly
        return messages_data

# "ana_section_types" : ["Image", "Text", "Graph", "Gif", "Audio", "Video", "Link", "EmbeddedHtml","Carousel"],
# "ana_node_types" : ["Combination", "ApiCall"],
# "ana_button_types" : ["PostText", "OpenUrl","GetText", "GetAddress", "GetNumber", "GetPhoneNumber","GetEmail","GetImage","GetAudio","GetVideo","GetItemFromSource","NextNode","DeepLink","GetAgent","ApiCall","ShowConfirmation","FetchChatFlow","GetDate","GetTime","GetDateTime","GetLocation"]


# Image, Audio, Video, Gif -> Simple Message with Media Content
# Text, Link, EmbeddedHtml -> Simple Message with Text content ?? what for link and embeddedhtml 
# Carousel -> Carousel Message

# OpenUrl -> Input.Options
# GetAddress -> Input.Address

# GetText -> Input.Text
# GetNumber -> Input.Numeric
# GetPhoneNumber -> Input.Phone
# GetEmail -> Input.Email

# GetImage, GetAudio, GetVideo -> Input.Media
# GetDate -> Input.Date
# GetTime -> Input.Time
# GetDateTime ??
# GetLocation -> Input.Location
# NextNode -> Input.options
# GetItemFromSource,NextNode, GetAgent, DeepLink, GetAgent, ApiCall, ShowConfirmation, FetchChatFlow #handle with different scenario
