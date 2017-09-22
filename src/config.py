import os 

application_config = {
        "CHATCORE_QUEUE_URL" : os.environ.get("CHATCORE_QUEUE_URL"),
        "GATEWAY_URL": os.environ.get("GATEWAY_URL"),
        "AWS_ACCESS_KEY_ID" : os.environ.get("AWS_ACCESS_KEY_ID"),
        "AWS_ACCESS_SECRET_KEY" : os.environ.get("AWS_ACCESS_SECRET_KEY"),
        "AWS_REGION" : os.environ.get("AWS_REGION")
        }

# each object represents config for one business
flow_config = {
        "first_node_key": "GET_STARTED_NODE",
        "archived_node_ids": ["INIT_CHAT_NODE", "SEND_CHAT_HISTORY_TO_SERVER", "GET_CHAT_TEXT_NODE", "SEND_CHAT_TEXT_NODE","CONTINUE_CHAT_NODE"],  
        "flows": {
            "1213618262009721": {
                "flow_id": "e90df634-3b77-4820-bb22-7d55ad5ae4e8",
                "api": "http://nfanabots.withfloats.com/nfbots/api/Conversation/chat?projectId=59b2a49cc7d8bf405c4116f9"
                }
            },
            "0c49ed3b-9967-4fbe-b1c6-f60d305c92fe": {
                "flow_id": "d59f4a94-c5dc-46c6-a93c-7b95d33fe967",
                "api": "http://ria.nowfloatsdev.com/lookup-bot/api/Conversation/chat?projectId=59af8dea8165d615f0d8c755"
            }
        }

ana_config = {
        "ana_section_types" : ["Image", "Text", "Graph", "Gif", "Audio", "Video", "Link", "EmbeddedHtml","Carousel"],
        "ana_node_types" : ["Combination", "ApiCall"],
        "ana_button_types" : ["PostText", "OpenUrl","GetText", "GetAddress", "GetNumber", "GetPhoneNumber","GetEmail","GetImage","GetAudio","GetVideo","GetItemFromSource","NextNode","DeepLink","GetAgent","ApiCall","ShowConfirmation","FetchChatFlow","GetDate","GetTime","GetDateTime","GetLocation"]
        }
