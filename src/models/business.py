import datetime
import uuid
import json
from src import app
from src.config import flow_config as config

class Business():

    def __init__(self, business_id, *args, **kwargs):

        self.business_id = business_id
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.collection = app.db.business_data

    def get_details(self, *args, **kwargs):
        business_object = self.collection.find_one({"business_id": self.business_id})
        return business_object

    def save_business_data_to_cache(self, business_data = {}, nodes = []):

        if business_data == {}:
            return False 

        flow_id = business_data["flow_id"]
        redis_client = app.redis_client
        node_dict = {}

        business_data_to_save = {
                business_data["business_id"] : {
                    "flow_id" : flow_id,
                    "business_name" : business_data["business_name"]
                    }
                }
        for node in nodes:
            if node["Id"] not in config["archived_node_ids"]: 
                if node["IsStartNode"] == True:
                    key = flow_id + "." + config["first_node_key"]
                else: 
                    key = flow_id + "." + node["Id"]
                node_dict[key] = json.dumps(node)

        try: 
            redis_client.mset(node_dict)
            print("Node data written to cache")
            redis_client.mset(business_data_to_save)
            print("Business data written to cache")
            return True
        except Exception as e:
            print("Error writing to cache")
            print(e)
            return False

    def save(self, data):

        match_query = { "business_id" : self.business_id }

        update_document = {}
        flow_id = str(uuid.uuid4())
        update_document["flow_url"] = data["flow_url"]
        update_document["business_name"] = data["business_name"]
        update_document["updated_at"] = self.updated_at

        try:
            business_object = self.collection.update_one(
                match_query,
                {
                    "$set": update_document,
                    "$setOnInsert": {
                        "flow_id": flow_id,
                        "created_at": self.created_at
                    }
                },
                upsert=True)

            return True
        except Exception as e:
            print(e)
            return False
