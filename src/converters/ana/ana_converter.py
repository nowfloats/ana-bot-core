import json
import urllib.parse
import pdb
import re
from furl import furl
from src.config import ana_config
from src.thrift_models.ttypes import MessageType, InputType, MediaType, ButtonType
from src.models.message import MessageContent, MessageData, Message, Media
from src.models.inputs import Option, Item, TextInput

class Converter():

    def __init__(self, state,*args, **kwargs):
        self.messages = []
        self.state = state
        # self.section_types = ana_config.section_types
        # self.node_types = ana_config.node_types
        # self.button_types = ana_config.button_types
        pass

    def process_text(self, text):
        data = self.state.get("var_data", "{}")
        variable_data = json.loads(data)
        current_variable_data = self.state["new_var_data"]
        variable_data.update(current_variable_data)
        matches = re.findall("\[~(.*?)\]", text)
        variable_names = variable_data.keys()
        final_text = text
        for match in matches:
            if match in variable_names:
                key = "[~" + match + "]"
                final_text = text.replace(key, variable_data[match])
        return final_text

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
        # after the types are handled remove if else clauses
        # convert to objects, preferably using factory pattern
        for section in data:
            section_type = section["SectionType"]
            if section_type == "Text":
                message_type = MessageType._NAMES_TO_VALUES["SIMPLE"]
                text = section["Text"]
                final_text = self.process_text(text)
                message_content = MessageContent(text=final_text, mandatory=1).trim()
                message_data = MessageData(type=message_type, content=message_content).trim()
                messages_data.append(message_data)

            elif section_type in ["Image","Gif"]:
                message_type = MessageType._NAMES_TO_VALUES["SIMPLE"]
                media_type = MediaType._NAMES_TO_VALUES["IMAGE"]
                url = section.get("Url","")
                encoded_url = furl(url).url
                preview_url = section.get("PreviewUrl","")
                text = section.get("Title", "")
                final_text = self.process_text(text)
                media_content = Media(type=media_type, url=encoded_url, previewUrl=preview_url).trim() 
                message_content = MessageContent(text=final_text, media=media_content, mandatory=1).trim()
                message_data = MessageData(type=message_type, content=message_content).trim()
                messages_data.append(message_data)

            elif section_type in ["EmbeddedHtml", "Link"]:
                message_type = MessageType._NAMES_TO_VALUES["SIMPLE"]
                text = section["Url"]
                message_content = MessageContent(text=text, mandatory=1).trim()
                message_data = MessageData(type=message_type, content=message_content).trim()
                messages_data.append(message_data)

            elif section_type == "Carousel":
                message_type = MessageType._NAMES_TO_VALUES["CAROUSEL"]
                section_items = section["Items"]
                item_elements = []
                for section_item in section_items:
                    media_type = MediaType._NAMES_TO_VALUES["IMAGE"]
                    image_url = section_item["ImageUrl"]
                    title = section_item["Title"]
                    description = section_item["Caption"]
                    encoded_url = furl(image_url).url
                    media_content = Media(type=media_type, url=encoded_url).trim()
                    buttons = section_item["Buttons"]
                    options = []
                    for button in buttons:
                        if button["Type"] == "OpenUrl":
                            button_title = button["Text"]
                            button_value = json.dumps({"url": button["Url"], "value": button["_id"]})
                            button_type = ButtonType._NAMES_TO_VALUES["URL"]
                        else:
                            button_title = button["Text"]
                            button_value = button["_id"]
                            button_type = ButtonType._NAMES_TO_VALUES["ACTION"]
                        option_element = Option(title=button_title, value=button_value, type=button_type).trim()
                        options.append(option_element)

                    item_element = Item(title=title, desc=description, media=media_content,options=options).trim() 
                    item_elements.append(item_element)
                message_content = MessageContent(items = item_elements, mandatory=1).trim()
                message_data = MessageData(type=message_type, content=message_content).trim()
                messages_data.append(message_data)

        return messages_data
        
    def convert_buttons(self,data):

        next_node_elem_message_data = []
        next_node_elements = []
        next_node_elem_options = []

        open_url_elements = []
        open_url_elem_message_data = []
        open_url_elem_options = []

        other_elements = []
        other_elem_message_data = []

        click_inputs = ["NextNode", "OpenUrl", "GetFile", "GetAudio", "PostText", "GetImage", "GetAgent"]
        text_inputs = ["GetText", "GetEmail", "GetNumber", "GetPhoneNumber", "GetItemFromSource"]

        click_elements = [button for button in data if button["ButtonType"] in click_inputs]
        text_elements = [button for button in data if button["ButtonType"] in text_inputs]

        messages_data = []

        if len(click_elements) !=0 and len(text_elements) == 0:
            messages_data = self._process_click_inputs(click_elements, mandatory=1)
            pass
        elif len(click_elements) !=0 and len(text_elements) != 0:
            messages_data = self._process_click_inputs(click_elements, mandatory=0)
            pass
        elif len(click_elements) ==0 and len(text_elements) != 0:
            messages_data = self._process_text_inputs(text_elements)
            pass

        return messages_data

    def _process_click_inputs(self, data, mandatory):

        button_heading = None
        elem_message_data = []
        elem_options = []

        message_type = MessageType._NAMES_TO_VALUES["INPUT"]
        input_type = InputType._NAMES_TO_VALUES["OPTIONS"]

        for button in data:
            button_type = button["ButtonType"]
            if (button_type == "OpenUrl"):
                option = {
                        "title": button["ButtonName"],
                        "value": json.dumps({"url": button["Url"], "value": button["_id"]}),
                        "type": ButtonType._NAMES_TO_VALUES["URL"]
                        }
            elif (button_type == "NextNode"):
                button_heading = "Select one" # to be compatible with fb quick_replies 
                option = {
                        "title": button["ButtonName"],
                        "value": button.get("_id", ""),
                        "type": ButtonType._NAMES_TO_VALUES["QUICK_REPLY"]
                        }
            elem_options.append(option)

        if (len(elem_options) != 0):
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

    def _process_text_inputs(self, data):

        elem_message_data = []

        for button in data:
            button_type = button.get("ButtonType")
            message_type = ""
            input_type = ""
            input_attr = None
            content = None

            if button_type == "GetText":
                message_type = MessageType._NAMES_TO_VALUES["INPUT"]
                input_type = InputType._NAMES_TO_VALUES["TEXT"] 
                input_attr = TextInput(placeHolder= button.get("PlaceholderText", "")).trim()
            elif button_type == "GetNumber":
                message_type = MessageType._NAMES_TO_VALUES["INPUT"]
                input_type = InputType._NAMES_TO_VALUES["NUMERIC"] 
            elif button_type == "GetPhoneNumber":
                message_type = MessageType._NAMES_TO_VALUES["INPUT"]
                input_type = InputType._NAMES_TO_VALUES["PHONE"] 
            elif button_type == "GetEmail":
                message_type = MessageType._NAMES_TO_VALUES["INPUT"]
                input_type = InputType._NAMES_TO_VALUES["EMAIL"] 
            else:
                print(e)
                raise

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
