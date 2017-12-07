"""
This module handles combination node of ana studio output
Author: https://github.com/velutha
"""
from src.converters.ana.node_processors.combination.section_processor import SectionProcessor
from src.converters.ana.node_processors.combination.button_processor import ButtonProcessor

class CombinationProcessor():

    def __init__(self, state):
        self.state = state

    def process_node(self, node_data):

        sections = node_data.get("Sections", [])
        buttons = node_data.get("Buttons", [])
        sections_response = SectionProcessor(self.state).process(sections)
        buttons_response = ButtonProcessor(self.state).process(buttons)
        messages = sections_response + buttons_response

        event_log_data = {
            "node_data" : node_data,
            "type_of_event": "view",
            "event_data" : {}
            }

        return {"messages": messages, "events": [event_log_data]}

    # def verb_replacer(self, text):
        # variable_data = self.state.get("var_data", {})
        # matches = re.findall("\[~(.*?)\]", text)
        # variable_names = variable_data.keys()
        # final_text = text
        # for match in matches:
            # if match in variable_names:
                # key = "[~" + match + "]"
                # final_text = text.replace(key, variable_data[match])
        # return final_text

    # def convert_sections(self, data):
        # messages_data = []

        # section_processor_map = {
            # "Text": self.__text_processor,
            # "Image": self.__image_processor,
            # "Gif": self.__image_processor,
            # "EmbeddedHtml": self.__link_processor,
            # "Link": self.__link_processor,
            # "Video": self.__video_processor,
            # "Carousel": self.__carousel_processor
            # }

        # for section in data:
            # section_type = section.get("SectionType", "")
            # processor = section_processor_map[section_type]
            # if processor is None:
                # logger.error(f"Unknown section type found {section_type}")
            # else:
                # message_data = processor(section)
                # messages_data.append(message_data)

        # return messages_data

    # def convert_buttons(self, data):

        # click_elements = [button for button in data if button["ButtonType"] in self.click_inputs]
        # text_elements = [button for button in data if button["ButtonType"] in self.text_inputs]

        # messages_data = []


        # if click_elements != [] and text_elements == []:
            # messages_data = self._process_click_inputs(click_elements, mandatory=1)
        # elif click_elements != [] and text_elements != []:
            # messages_data = self._process_click_inputs(click_elements, mandatory=0)
        # elif click_elements == [] and text_elements != []:
            # messages_data = self._process_text_inputs(text_elements)

        # return messages_data

    # def __text_processor(self, data):

        # message_type = MessageType.get_value("SIMPLE")
        # text = data.get("Text", "")
        # final_text = self.verb_replacer(text)
        # message_content = MessageContent(text=final_text, mandatory=1).trim()
        # message_data = MessageData(type=message_type, content=message_content).trim()

        # return message_data

    # def __image_processor(self, data):

        # message_type = MessageType.get_value("SIMPLE")
        # media_type = MediaType.get_value("IMAGE")
        # url = data.get("Url", "")
        # encoded_url = furl(url).url
        # preview_url = data.get("PreviewUrl", "")
        # text = data.get("Title", "")
        # final_text = self.verb_replacer(text)
        # media_content = Media(type=media_type, url=encoded_url, previewUrl=preview_url).trim()
        # message_content = MessageContent(text=final_text, media=media_content, mandatory=1).trim()
        # message_data = MessageData(type=message_type, content=message_content).trim()

        # return message_data

    # @classmethod
    # def __link_processor(cls, data):

        # message_type = MessageType.get_value("SIMPLE")
        # text = data["Url"]
        # message_content = MessageContent(text=text, mandatory=1).trim()
        # message_data = MessageData(type=message_type, content=message_content).trim()

        # return message_data

    # def __video_processor(self, data):

        # message_type = MessageType.get_value("SIMPLE")
        # media_type = MediaType.get_value("VIDEO")
        # url = data.get("Url", "")
        # encoded_url = furl(url).url
        # preview_url = data.get("PreviewUrl", "")
        # text = data.get("Title", "")
        # final_text = self.verb_replacer(text)
        # media_content = Media(type=media_type, url=encoded_url, previewUrl=preview_url).trim()
        # message_content = MessageContent(text=final_text, media=media_content, mandatory=1).trim()
        # message_data = MessageData(type=message_type, content=message_content).trim()

        # return message_data

    # @classmethod
    # def __carousel_processor(cls, data):

        # message_type = MessageType.get_value("CAROUSEL")
        # section_items = data.get("Items", [])
        # item_elements = []
        # for section_item in section_items:
            # media_type = MediaType.get_value("IMAGE")
            # image_url = section_item.get("ImageUrl", "")
            # title = section_item.get("Title", "")
            # description = section_item.get("Caption", "")
            # encoded_url = furl(image_url).url
            # media_content = Media(type=media_type, url=encoded_url).trim()
            # buttons = section_item.get("Buttons", [])
            # options = []
            # for button in buttons:
                # if button["Type"] == "OpenUrl":
                    # button_title = button.get("Text", "")
                    # button_value = json.dumps({"url": button["Url"], "value": button["_id"]})
                    # button_type = ButtonType.get_value("URL")
                # else:
                    # button_title = button.get("Text", "")
                    # button_value = button["_id"]
                    # button_type = ButtonType.get_value("ACTION")
                # option_element = Option(title=button_title, value=button_value, type=button_type).trim()
                # options.append(option_element)

            # item_element = Item(title=title, desc=description, media=media_content, options=options).trim()
            # item_elements.append(item_element)
        # message_content = MessageContent(items=item_elements, mandatory=1).trim()
        # message_data = MessageData(type=message_type, content=message_content).trim()

        # return message_data


    # @staticmethod
    # def _process_click_inputs(data, mandatory):

        # button_heading = None
        # elem_message_data = []
        # elem_options = []

        # message_type = MessageType.get_value("INPUT")
        # input_type = InputType.get_value("OPTIONS")

        # for button in data:
            # button_type = button.get("ButtonType", "")
            # if button_type == "OpenUrl":
                # button_heading = "Choose an option" # to be compatible with fb quick_replies
                # option = {
                    # "title": button.get("ButtonName", ""),
                    # "value": json.dumps({"url": button["Url"], "value": button["_id"]}),
                    # "type": ButtonType.get_value("URL")
                    # }
            # elif button_type == "NextNode":
                # button_heading = "Choose an option" # to be compatible with fb quick_replies
                # option = {
                    # "title": button.get("ButtonName", button.get("ButtonText", "")),
                    # "value": button.get("_id", ""),
                    # "type": ButtonType.get_value("QUICK_REPLY")
                    # }

            # elem_options.append(option)

        # if elem_options != []:
            # message_content = MessageContent(
                # inputType=input_type,
                # mandatory=mandatory,
                # options=elem_options,
                # text=button_heading
                # ).trim()
            # message_data = MessageData(
                # type=message_type,
                # content=message_content
                # ).trim()
            # elem_message_data.append(message_data)

        # return elem_message_data

    # @staticmethod
    # def _process_text_inputs(data):

        # elem_message_data = []

        # for button in data:
            # button_type = button.get("ButtonType")
            # message_type = ""
            # input_type = ""
            # input_attr = None
            # content = None

            # message_type = MessageType.get_value("INPUT")

            # if button_type == "GetText":
                # input_type = InputType.get_value("TEXT")
                # input_attr = TextInput(placeHolder=button.get("PlaceholderText", "")).trim()
            # elif button_type == "GetNumber":
                # input_type = InputType.get_value("NUMERIC")
            # elif button_type == "GetPhoneNumber":
                # input_type = InputType.get_value("PHONE")
            # elif button_type == "GetEmail":
                # input_type = InputType.get_value("EMAIL")
            # elif button_type == "GetLocation":
                # input_type = InputType.get_value("LOCATION")
            # elif button_type == "GetAddress":
                # input_type = InputType.get_value("ADDRESS")
            # elif button_type == "GetDate":
                # input_type = InputType.get_value("DATE")
            # elif button_type == "GetTime":
                # input_type = InputType.get_value("TIME")
            # elif button_type == "GetItemFromSource":
                # pass
            # else:
                # logger.warning("Undefined Text Input Type" + str(button_type))

            # content = MessageContent(
                # inputType=input_type,
                # textInputAttr=input_attr,
                # mandatory=1,
                # ).trim()
            # message_data = MessageData(
                # type=message_type,
                # content=content
                # ).trim()
            # elem_message_data.append(message_data)


        # return elem_message_data
