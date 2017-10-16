from src.models.user import User
from src import app
import pdb

class SessionController():
    
    def __init__(self, *args, **kwargs):
        pass

    def clear_sessions(self, user_id):
        user_key =  user_id + "." + "sessions"
        sessions = app.redis_client.lrange(user_key,0, -1)
        if (len(sessions) == 0):
            return {"message": "no_sessions_found"}
        sessions.append(user_key)
        clear_sessions = app.redis_client.delete(*sessions)
        if (clear_sessions):
            return {"message": "sessions_cleared"}
