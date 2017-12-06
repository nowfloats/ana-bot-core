import uuid
import datetime
import json
import time
from src import SESSION_CACHE, DB
from src.logger import logger
from src.models.types import MediumWrapper as Medium

class User():

    def __init__(self, user_id):
        self.user_id = user_id
        self.CACHE = SESSION_CACHE

    def get_session_data(self, session_id):

        response = {}
        session_data = {}
        user_session_key = self.user_id + "." + "sessions"
        user_sessions = self.CACHE.lrange(user_session_key, 0, -1)

        # initializing session if it does not exist
        session_id = str(uuid.uuid4()) if session_id is None else session_id

        if session_id in user_sessions:
            session_data = self.CACHE.hgetall(session_id)
        else:
            # create session in cache
            self.CACHE.lpush(user_session_key, session_id)

        response["session_id"] = session_id

        for key, value in session_data.items():
            response[key] = value

        return response

    def set_state(self, session_id, state, meta_data):
        try:
            new_state = {}
            final_var_data = state.get("var_data", {})
            new_var_data = state.get("new_var_data", {})

            channel_type = meta_data["sender"]["medium"]
            channel = Medium.get_name(channel_type)
            business_name = state.get("business_name", "")
            timestamp = int(time.time())

            new_state["current_node_id"] = state["current_node_id"]
            new_state["timestamp"] = timestamp
            new_state["var_data"] = json.dumps(final_var_data)

            self.CACHE.hmset(session_id, new_state)
            logger.info(f"User state with session_id {session_id} updated with state {new_state}")
            self._persist_data(var_data=new_var_data, session_id=session_id, channel=channel, business_name=business_name)

            return 1
        except Exception as err:
            logger.error(err)
            raise

    def _persist_data(self, var_data, session_id="", channel="", business_name=""):
        # change this method to perform async
        if var_data == {}:
            return 1
        object_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow()
        collection = DB["user_data"]
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
            logger.info(f"Variable data saved with object_id {saved_document_id}")
            return 1
        except Exception as err:
            logger.error(err)
            raise
