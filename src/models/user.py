import uuid
import json
from pprint import pprint
from src import app


class User():

    def __init__(self, user_id, session_id, *args, **kwargs):
        self.user_key = user_id + "." + session_id

    def get_session_data(self):

        response = {}
        session_data = app.redis_client.hgetall(self.user_key)
        for key, value in session_data.items():
            response[str(key, "utf-8")] = str(value, "utf-8")
        return response

    def set_state(self, state):
        try:
            new_state = {}
            new_var_data = state.get("var_data", {})
            new_state["current_node_id"] = state["current_node_id"]
            for key in new_var_data.keys():
                new_state[key] = new_var_data[key]
            app.redis_client.hmset(self.user_key, new_state)
            return 1
        except Exception as e:
            print(e)
            pass

    def create_session(self):
        pass
