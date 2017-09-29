import json
import pdb
from src import app

class AnaNode():
    def __init__(self, node_key, *args, **kwargs):
        self.node_key = node_key

    def get_contents(self, node_key):
        # print("Getting contents for", self.node_id)
        print("node_key in get_contents is", node_key)
        response = app.redis_client.get(node_key)
        # print(response)
        if (response == None):
            return {}
        try:

            response_dict = json.loads(response)
            return response_dict
        except Exception as e:
            print(e)
            raise

        # handle response not found or empty ideally this should never happen

    def get_next_node_id(self, flow_id, message_content):
        current_node_contents = self.get_contents(self.node_key)
        input_data = message_content["content"]["input"]
        node_key = ""
        if "val" in input_data.keys():
            print("I am coming here")
            button_contents = current_node_contents["Buttons"]
            print(button_contents)
            for button in button_contents:
                if button["ButtonType"] in ["GetText", "GetNumber", "GetPhoneNumber", "GetEmail"]:
                    node_id = button["NextNodeId"]
                    node_key = flow_id + "." + node_id
                    print("Broke here")
                    break
            print("Also here")
            node_id = input_data["val"]
            if (node_key):
                pass
            else:
                node_key = flow_id + "." + node_id
        else: 
            input_value = input_data["input"]
            button_contents = current_node_contents["Buttons"]
            node_id = ""
            for button in button_contents:
                if button["ButtonType"] in ["GetText", "GetNumber", "GetPhoneNumber", "GetEmail"]:
                    node_id = button["NextNodeId"]
                    break
            if node_id != "":
                node_key = flow_id + "." + node_id
            else:
                node_key = self.node_key
        return node_key

