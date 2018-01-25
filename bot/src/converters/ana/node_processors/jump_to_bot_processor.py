"""
This module handles when chat jumps from one bot to another
Author: https://github.com/velutha
"""
from src.models.ana_node import AnaNode

class JumpToBotProcessor():

    def __init__(self, state):
        self.state = state

    def get_next_node(self, node_data):

        new_flow_id = node_data.get("TargetBotId")
        self.state["flow_id"] = new_flow_id
        next_node_id = node_data.get("TargetNodeId")
        next_node_key = new_flow_id + "." + next_node_id
        next_node_data = AnaNode(next_node_key).get_contents()
        return {"id": next_node_key, "data": next_node_data}

    def process_node(self, node_data):
        pass
