from flask import jsonify
from src import SESSION_CACHE

class SessionController():

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def clear_sessions(user_id):
        # shift this to user model
        user_key = user_id + "." + "sessions"
        sessions = SESSION_CACHE.lrange(user_key, 0, -1)

        if sessions == []:
            return jsonify(message="no_sessions_found")

        sessions.append(user_key)
        clear_sessions = SESSION_CACHE.delete(*sessions)

        if clear_sessions:
            return jsonify(message="sessions_cleared")

        return jsonify(message="could_not_clear_sessions"), 500
