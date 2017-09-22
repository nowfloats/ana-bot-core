import urllib.request
import json
from src import app
from src.config import flow_config as config

class RefreshChatFlows():

    def __init__(self):
        pass

    def populate_flows(self):
        redis_client = app.redis_client
        for business_id, flow_data in config["flows"].items(): 
            url = flow_data["api"]
            flow_id = flow_data["flow_id"]
            # handle request failure
            response = urllib.request.urlopen(url)
            body = response.read()
            nodes = json.loads(body)
            node_dict = {}
            for node in nodes:
                if node["Id"] not in config["archived_node_ids"]: 
                    if node["IsStartNode"] == True:
                        key = flow_id + "." + config["first_node_key"]
                    else: 
                        key = flow_id + "." + node["Id"]
                    node_dict[key] = json.dumps(node)
            # handle redis_write failure
            redis_client.mset(node_dict)
        return {"message": "success"}
