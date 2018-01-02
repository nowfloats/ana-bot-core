from src.converters.agent.agent_converter import Converter as AgentConverter

class AgentHandOffProcessor():

    def __init__(self, state):
        self.state = state

    @classmethod
    def process_node(self, message_data):
        # agent_messages_data = [{"message" : message_data, "sending_to": "AGENT"}]
        agent_messages = [message_data]
        user_messages = AgentConverter.get_agent_connected_messages()

        return {"user_messages": user_messages, "agent_messages": agent_messages}
