from src.converters.agent.agent_converter import Converter as AgentConverter
from src.converters.ana.node_processors.combination.combination_processor import CombinationProcessor

class AgentHandOffProcessor():

    def __init__(self, state):
        self.state = state

    #@classmethod
    def process_node(self, message_data, node_data):
        # agent_messages_data = [{"message" : message_data, "sending_to":
        # "AGENT"}]
        if message_data:
            agent_messages = [message_data]
        else:
            agent_messages = []
            pass
        user_messages = AgentConverter.get_agent_connected_messages()
        return_messages = []
        if node_data:
            messages = CombinationProcessor(self.state).process_node(node_data)
            agent_messages.extend(messages["user_messages"])
            pass
        return {"user_messages": user_messages, "agent_messages": agent_messages }
