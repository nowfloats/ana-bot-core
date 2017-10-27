import json
import os
from flask import Response
from flask import request
from functools import wraps
from src import app
from src.models.user import User
from src.controllers.chatflow_controller import ChatFlowController
from src.controllers.session_controller import SessionController
from src.controllers.business_controller import BusinessController
from src.responder import MessageProcessor

@app.route("/health-check")
def hello_world():
    json_data = json.dumps({"status" : "UP"})
    response = Response(json_data, status=200)
    return response

# move validation methods to somewhere else
def validate_business_params(func):
    def validate_business(*args, **kwargs):
        business_id = request.args.get("business_id")
        if business_id is None:
            message = json.dumps({"message": "business_id missing"}) 
            response = Response(message, status=400, mimetype="application/json")
            return response
        return func(*args, *kwargs)
    return validate_business

@app.route("/api/refreshChatFlows")
@validate_business_params
def populate_ana_flows():

    business_id = request.args.get("business_id")
    data = ChatFlowController.populate_flows(business_id)
    json_data = json.dumps(data)

    response = Response(json_data, status=200, mimetype="application/json")
    return response

def validate_session_params(func):
    @wraps(func)
    def validate_session(*args, **kwargs):
        user_id = request.args.get("user_id")
        if user_id is None:
            message = json.dumps({"message": "user_id missing"}) 
            response = Response(message, status=400, mimetype="application/json")
            return response
        return func(*args, *kwargs)
    return validate_session

@app.route("/api/clearSessions", endpoint="clear_sessions")
@validate_session_params
def clear_sessions():

    user_id = request.args.get("user_id")
    session_response = SessionController.clear_sessions(user_id) 
    json_response = json.dumps(session_response)
    response = Response(json_response, status=200, mimetype="application/json")

    return response

@app.route("/api/message", methods=["POST"])
def message_handler():

    message = request.get_json()
    print("Message Received")
    print(message)
    print("****************")
    response = MessageProcessor(message).start()
    return "OK"

@app.route("/api/business", endpoint="get_business")
@validate_business_params
def get_business():
    business_id = request.args.get("business_id")
    data = BusinessController.get_business(business_id)

    if (data == {}):
        response = Response(status="404", mimetype="application/json")
    else:
        json_data = json.dumps(data)
        response = Response(json_data, status=200, mimetype="application/json")
    return response

@app.route("/api/business", methods=["POST"])
def business_handler():

    business_data = request.get_json()
    business_response = BusinessController.create_business(business_data) 
    json_response = json.dumps(business_response)
    response = Response(json_response, status=200, mimetype="application/json")

    return response
