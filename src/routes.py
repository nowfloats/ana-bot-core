import json
from flask import Response
from flask import request
from src import app
from src.services.refresh_chatflows import RefreshChatFlows as ChatFlowController
from src.responder import MessageProcessor

@app.route("/health-check")
def hello_world():
    return "OK"

@app.route("/api/message", methods=["POST"])
def message_handler():
    message = request.get_json()
    response = MessageProcessor(message).start()
    return "OK"

@app.route("/service/refreshChatFlows")
def populate_ana_flows():

    data = ChatFlowController().populate_flows()
    json_data = json.dumps(data)

    response = Response(json_data, status=200, mimetype="application/json")
    return response
