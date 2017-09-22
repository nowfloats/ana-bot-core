from flask import Response
import json
from src import app
from src.services.refresh_chatflows import RefreshChatFlows as ChatFlowController

@app.route("/health-check")
def hello_world():
    return "OK"

@app.route("/service/refreshChatFlows")
def populate_ana_flows():

    data = ChatFlowController().populate_flows()
    json_data = json.dumps(data)

    response = Response(json_data, status=200, mimetype="application/json")
    return response
