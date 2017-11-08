from src.models.business import Business
from src.controllers.chatflow_controller import ChatFlowController

class BusinessController():

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def create_business(data):

        business_id = data["business_id"]
        business_data = {}
        business_data["flow"] = data["flow"]
        business_data["business_name"] = data["business_name"]
        create_business = Business(business_id).save(business_data)
        print("Created business details")

        data_saved_to_cache = ChatFlowController.populate_flows(business_id)
        return {"message": "success"} if create_business else {"message": "failure"} 

    @staticmethod
    def get_business(business_id):
        business_data = Business(business_id).get_details()
        return business_data
