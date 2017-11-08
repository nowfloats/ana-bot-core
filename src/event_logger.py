import pdb
import time
from src.thrift_models.ttypes import SenderType
from src.connectors.kinesis_helper import KinesisHelper

class EventLogger(KinesisHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log(self,meta_data= {}, event_data = {}, flow_data = {}):

        event_type = event_data.get("type_of_event")
        pdb.set_trace()
        if (event_type == None):
            return

        if (event_type == "view"):

            node_data = event_data.get("node_data")
            event_channel_type = meta_data["sender"]["medium"]
            event_channel = SenderType._VALUES_TO_NAMES(event_channel_type)

            final_event_data = {
                    "business_name" : flow_data.get("business_name"),
                    "event_channel": event_channel,
                    "user_id": meta_data["sender"]["id"],
                    "session_id": meta_data.get("sessionId"),
                    "event_name": "view",
                    "node_id": node_data.get("Id"),
                    "node_name": node_data.get("Name"),
                    "node_type": node_data.get("NodeType"),
                    "button_id": None,
                    "button_type": None,
                    "timestamp": time.time() 
                    }
            self.log_message(data = final_event_data)
            return

        if (event_type == "click"):
            print("Click event recorded")
            print(event_data)
            print("###################")
            return

        # meta_data = None,node_data = None, type_of_event = None, event_data = None
        # if (type_of_event == None):
            # return

        # if (type_of_event == "view"):
            # print("View event recorded")
            # KinesisHelper().log_message(node_data)
            # print(node_data)
            # print(event_data)
            # return

        # if (type_of_event == "click"): 
            # print("Click event recorded")
            # KinesisHelper().log_message(node_data)
            # print(node_data)
            # print(event_data)
            # return
