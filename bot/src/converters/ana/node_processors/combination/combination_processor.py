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
