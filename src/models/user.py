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
            app.redis_client.hmset(self.user_key, state)
            return 1
        except Exception as e:
            print(e)
            pass

    def create_session(self):
        pass

    def update_state(self):
        pass
