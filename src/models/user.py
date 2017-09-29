import uuid
import json
from pprint import pprint
from src import app

# class Session():

    # def __init__(self, *args, **kwargs):
        # pass

class User():

    def __init__(self, user_id, session_id, *args, **kwargs):
        self.user_key = user_id + "." + session_id
        # super().__init__(*args, **kwargs)

    def get_session_data(self):

        response = {}
        session_data = app.redis_client.hgetall(self.user_key)
        for key, value in session_data.items():
            response[str(key, "utf-8")] = str(value, "utf-8")
        return response

    def set_state(self, state):
        try:
            print(self.user_key)
            print(state)
            new_state = {}
            # print(state["var_data"])
            new_var_data = state.get("var_data", {})
            print("new_var_data is", new_var_data)
            new_state["last_node_id"] = state["last_node_id"]
            for key in new_var_data.keys():
                new_state[key] = new_var_data[key]
            print("new_state set is", new_state)
            app.redis_client.hmset(self.user_key, new_state)
            return 1
        except Exception as e:
            print(e)
            pass

    def create_session(self):
        pass

    def update_state(self):
        pass
