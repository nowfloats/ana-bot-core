"""
User session data controller
Author: https:github.com/velutha
"""
from flask import jsonify
from src import CACHE

class SessionController():

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def clear_sessions(user_id):
        # shift this to user model
        user_key = user_id + "." + "sessions"
        sessions = CACHE.lrange(user_key, 0, -1)

        if sessions == []:
            return jsonify(message="no_sessions_found")

        sessions.append(user_key)
        clear_sessions = CACHE.delete(*sessions)

        if clear_sessions:
            return jsonify(message="sessions_cleared")

        return jsonify(message="could_not_clear_sessions"), 500
