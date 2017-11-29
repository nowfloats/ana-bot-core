"""
Model for business entity, one bot is one business
"""
import datetime
import uuid
import json
from src import ANA_CACHE, DB
from src.config import flow_config as config

class Business():

    def __init__(self, business_id):

        self.business_id = business_id
        self.CACHE = ANA_CACHE
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.collection = DB.business_data

    # all cache and db methods should merge together
    # have persistent layer load cache if not found in cache
    def get_business_data(self):

        business_object = self.CACHE.hgetall(self.business_id)
        return business_object

    def get_details(self):
        business_object = self.collection.find_one({"business_id": self.business_id})
        if business_object is None:
            return {}
        response_keys = ["business_id", "flow", "business_name", "flow_id"]
        business_details = {key: value for key, value in business_object.items() if key in response_keys}
        return business_details

    def save_business_data_to_cache(self, business_data, nodes):

        if business_data == {}:
            return False

        flow_id = business_data["flow_id"]
        node_dict = {}

        business_keys = ["flow_id", "business_name"]
        business_data_to_save = {key : business_data[key] for key in business_keys}

        for node in nodes:
            if node["Id"] not in config["archived_node_ids"]:
                if node.get("IsStartNode", False):
                    get_started_key = flow_id + "." + config["first_node_key"]
                    node_dict[get_started_key] = json.dumps(node)
                key = flow_id + "." + node["Id"]
                node_dict[key] = json.dumps(node)

        try:
            self.CACHE.mset(node_dict)
            print("Node data written to cache for flow ", flow_id)
            self.CACHE.hmset(self.business_id, business_data_to_save)
            print("Business data written to cache for flow ", flow_id)
            return True
        except Exception as err:
            print("Error writing to cache")
            print(err)
            return False

    def save(self, data):

        match_query = {"business_id" : self.business_id}

        update_document = {}
        flow_id = str(uuid.uuid4())
        update_document["flow"] = data["flow"]
        update_document["business_name"] = data["business_name"]
        update_document["updated_at"] = self.updated_at

        try:
            self.collection.update_one(
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
        except Exception as err:
            print(err)
            return False
