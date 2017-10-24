import os 
import uuid

application_config = {
        "CHATCORE_QUEUE_URL" : os.environ.get("CHATCORE_QUEUE_URL"),
        "GATEWAY_URL": os.environ.get("GATEWAY_URL"),
        "AWS_ACCESS_KEY_ID" : os.environ.get("AWS_ACCESS_KEY_ID"),
        "AWS_ACCESS_SECRET_KEY" : os.environ.get("AWS_ACCESS_SECRET_KEY"),
        "AWS_REGION" : os.environ.get("AWS_REGION")
        }

default_business_id = os.environ.get("DEFAULT_BUSINESS_ID")
default_flow_api = os.environ.get("DEFAULT_FLOW_API")
default_flow_id = os.environ.get("DEFAULT_FLOW_ID")
print(default_flow_id)
print(default_flow_api)
# each object represents config for one business
flow_config = {
        "first_node_key": "GET_STARTED_NODE",
        "default_flow_api": os.environ.get("DEFAULT_FLOW_API"),
        "default_flow_id": default_flow_id,
        "default_business_id": default_business_id,
        "archived_node_ids": ["INIT_CHAT_NODE", "SEND_CHAT_HISTORY_TO_SERVER", "GET_CHAT_TEXT_NODE", "SEND_CHAT_TEXT_NODE","CONTINUE_CHAT_NODE"],  
        "flows": {
            default_business_id: {
                "flow_id": default_flow_id,
                "api": default_flow_api,
                "business_name": "BLUME_VENTURES"
                },
            "demo-automobiles": {
                "flow_id": "e8f95226-f376-4e89-a8c5-a169b94bb18d",
                "api": "http://ria.nowfloatsdev.com/websitesamples/api/Conversation/chat?projectId=59ea2acab02a292edc83d5d2",
                "business_name": "DEMO_AUTOMOBILES"
            },
            "demo-ecommerce": {
                "flow_id": "22cf9e4a-46e3-46d2-a7f9-514d92bc3269",
                "api": "http://ria.nowfloatsdev.com/websitesamples/api/Conversation/chat?projectId=59ea3dc7b02a292edc83d69d",
                "business_name": "DEMO_ECOMMERCE",
            },
            "713199095512917": {
                "flow_id": "51a3a2e2-7387-4cfe-8cee-4715190891b6",
                "api": "https://nfanabots.withfloats.com/nfbots/api/conversation/chat?projectid=59b2a49cc7d8bf405c4116f9",
                "business_name": "getkitsune-com"
                },
            "demo-real-estate": {
                "flow_id": "3ce278ad-caec-44a1-8a97-d31394eadf97",
                "api": "http://ria.nowfloatsdev.com/websitesamples/api/Conversation/chat?projectId=59ea3d46b02a292edc83d670",
                "business_name": "DEMO_REALESTATE"
            }
            }
        }

ana_config = {
        "click_input_types" : ["NextNode", "OpenUrl", "GetFile", "GetAudio", "PostText", "GetImage", "GetAgent"],
        "text_input_types" : ["GetText", "GetEmail", "GetNumber", "GetPhoneNumber", "GetItemFromSource"],
        "ana_section_types" : ["Image", "Text", "Graph", "Gif", "Audio", "Video", "Link", "EmbeddedHtml","Carousel"],
        "ana_node_types" : ["Combination", "ApiCall"],
        "ana_button_types" : ["PostText", "OpenUrl","GetText", "GetAddress", "GetNumber", "GetPhoneNumber","GetEmail","GetImage","GetAudio","GetVideo","GetItemFromSource","NextNode","DeepLink","GetAgent","ApiCall","ShowConfirmation","FetchChatFlow","GetDate","GetTime","GetDateTime","GetLocation"]
        }
