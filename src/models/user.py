import uuid
import pdb
import json
from src import app


class User():

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id 

    def get_session_data(self, session_id):

        response = {}
        user_session_key = self.user_id + "." + "sessions"
        sessions = app.redis_client.lrange(user_session_key, 0 , -1)
        user_sessions = [str(session,'utf-8') for session in sessions]

        if session_id in user_sessions:
            self.session_id = session_id
            self.session_data = app.redis_client.hgetall(session_id)
        else:
            self.session_id = str(uuid.uuid4())
            create_session = app.redis_client.lpush(user_session_key, self.session_id)
            self.session_data = {}

        response["session_id"] = self.session_id
        for key, value in self.session_data.items():
            response[str(key, "utf-8")] = str(value, "utf-8")

        return response

    def set_state(self, session_id, state):
        try:
            new_state = {}
            new_var_data = state.get("var_data", {})
            # add timestamp to state here
            new_state["current_node_id"] = state["current_node_id"]
            for key in new_var_data.keys():
                new_state[key] = new_var_data[key]
            app.redis_client.hmset(session_id, new_state)
            # also persist data here
            return 1
        except Exception as e:
            print(e)
            pass

    def create_session(self):
        pass
