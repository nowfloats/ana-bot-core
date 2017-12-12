from flask import jsonify
from src.models.business import Business
from src.logger import logger

class ChatFlowController():

    def __init__(self):
        pass

    @staticmethod
    def populate_flows(business_id):

        business_data = Business(business_id).get_details()
        if business_data is None:
            return {"message": "business not found"}

        nodes = business_data.get("flow", [])

        if nodes == []:
            logger.error(f"Flow not found or empty")
            return jsonify(message="failure")

        data_saved_to_cache = Business(business_id).save_business_data_to_cache(business_data=business_data, nodes=nodes)
        return jsonify(message="success") if data_saved_to_cache else jsonify(message="failure")
