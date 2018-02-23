"""
Chat Flow data controller
Author: https:github.com/velutha
"""
from flask import jsonify
from src.models.business import Business
from src.models.chat_flow import ChatFlow
# from src.logger import logger

class ChatFlowController():

    def __init__(self):
        pass

    # @staticmethod
    # def populate_flows(business_id):

        # business_data = Business(business_id).get_details()
        # if business_data is None:
            # return {"message": "business not found"}

        # nodes = business_data.get("flow", [])

        # if nodes == []:
            # logger.error(f"Flow not found or empty")
            # return jsonify(message="failure")

        # data_saved_to_cache = Business(business_id).save_business_data_to_cache(business_data=business_data, nodes=nodes)
        # return jsonify(message="success") if data_saved_to_cache else jsonify(message="failure")

    @staticmethod
    def populate_flows_new(data):

        business_data = {}
        business_id = data["businessId"]
        flow_id = data["id"]
        business_data["business_id"] = business_id
        business_data["flow_id"] = data["id"]
        business_data["business_name"] = data.get("businessName", "")
        business_data["flow_name"] = data["name"]
        business_data["user_id"] = data["userId"]
        nodes = data["flow"]

        business_data_saved = Business(business_id).save(business_data)
        flow_data_saved = ChatFlow(flow_id).save(nodes)
        return jsonify(message="success") if business_data_saved and flow_data_saved else jsonify(message="failure")
