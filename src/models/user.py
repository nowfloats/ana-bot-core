import uuid
import pdb
import datetime
import json
import time
from src import app
from src.utils import Util
from src.thrift_models.ttypes import Medium

class User():

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id 

    def get_session_data(self, session_id):

        response = {}
        user_session_key = self.user_id + "." + "sessions"
        user_sessions = app.redis_client.lrange(user_session_key, 0 , -1)

        if session_id in user_sessions:
            self.session_id = session_id
            self.session_data = app.redis_client.hgetall(session_id)
        else:
            self.session_id = str(uuid.uuid4())
            create_session = app.redis_client.lpush(user_session_key, self.session_id)
            self.session_data = {}

        response["session_id"] = self.session_id

        for key, value in self.session_data.items():
            response[key] = value

        return response

    def set_state(self, session_id, state, meta_data, flow_data):
        try:
            new_state = {}
            current_state = app.redis_client.hgetall(session_id)

            new_var_data = state.get("new_var_data", {})
            current_var_data = current_state.get("var_data", "{}")
            final_var_data = Util.merge_dicts(new_var_data, json.loads(current_var_data))

            channel_type = meta_data["sender"]["medium"]
            channel = Medium._VALUES_TO_NAMES[channel_type]
            business_name = flow_data.get("business_name", "")
            timestamp = int(time.time()) 

            new_state["current_node_id"] = state["current_node_id"]
            new_state["timestamp"] = timestamp
            new_state["var_data"] = json.dumps(final_var_data)

            app.redis_client.hmset(session_id, new_state)
            self._persist_data(var_data=new_var_data, session_id = session_id, channel = channel, business_name = business_name)

            return 1
        except Exception as e:
            print(e)
            raise

    def _persist_data(self, var_data = {} , session_id = "", channel = "", business_name = ""):
        # change this method to perform async
        if (var_data == {}):
            return 1
        object_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow()
        collection = app.db["user_data"]
        document = {
                "_id": object_id,
                "user_id" : self.user_id,
                "session_id": session_id,
                "data": var_data,
                "channel": channel,
                "business_name": business_name,
                "timestamp": timestamp
                }
        try:
            saved_document_id = collection.insert_one(document).inserted_id
            print("Variable data saved with object_id", saved_document_id)
            return 1
        except Exception as e:
            print(e)
            raise
