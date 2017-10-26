import requests
from src import app
from src.models.business import Business

class ChatFlowController():

    def __init__(self):
        pass

    @staticmethod
    def populate_flows(business_id):

        business_data = Business(business_id).get_details()
        if business_data is None:
            return {"message": "business not found"}


        url = business_data["flow_url"]
        flow_id = business_data["flow_id"]

        try:
            response = requests.get(url)
        except Exception as e:
            print("Error fetching chat flow")
            print(e)
            return {"message": "failure"}

        nodes = response.json()
        data_saved_to_cache = Business(business_id).save_node_data_to_cache(flow_id = flow_id, nodes = nodes)
        return {"message": "success"} if data_saved_to_cache else {"message": "failure"} 
