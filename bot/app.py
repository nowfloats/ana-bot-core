"""
This is the entry point to bot-core server
Author: https://github.com/velutha
"""
import os
from src import app, message_pool
from src.validator import Validator
from flask import request, jsonify
from src.controllers.business_controller import BusinessController
from src.controllers.chatflow_controller import ChatFlowController
from src.controllers.session_controller import SessionController
from src.responder import MessageProcessor

@app.route("/health-check")
def hello_world():
    status_message = {"status": "UP"}
    return jsonify(status_message)

@app.route("/api/refreshChatFlows")
@Validator.validate_business_params
def populate_ana_flows():

    business_id = request.args.get("business_id")
    response = ChatFlowController.populate_flows(business_id)

    return response

@app.route("/api/clearSessions", endpoint="clear_sessions")
@Validator.validate_session_params
def clear_sessions():

    user_id = request.args.get("user_id")
    response = SessionController.clear_sessions(user_id)

    return response

@app.route("/api/message", methods=["POST"])
def message_handler():

    message = request.get_json()

    print("Message Received")
    print(message)
    print("****************")

    handle_message = message_pool.submit(MessageProcessor(message).respond_to_message)
    print(handle_message.exception())
    return jsonify(status="received")

@app.route("/api/business", methods=["POST"])
def business_handler():

    business_data = request.get_json()
    response = BusinessController.create_business(business_data)

    return response

@app.route("/api/business", methods=["GET"], endpoint="get_business")
@Validator.validate_business_params
def get_business():
    business_id = request.args.get("business_id")
    response = BusinessController.get_business(business_id)

    return response

if __name__ == "__main__":

    HOST = os.environ.get("HOST") or "0.0.0.0"
    PORT = os.environ.get("PORT") or 9500

    app.run(host=HOST, port=PORT)
