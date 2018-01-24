from src.converters.agent.agent_converter import Converter as AgentConverter
# from src.converters.ana.node_processors.combination.combination_processor import CombinationProcessor

class AgentHandOffProcessor():

    def __init__(self, state):
        self.state = state

    def get_next_node(self, node_data):

        # return the same node_data since it's handoffagent node, it is
        # the final node to process
        next_node_key = self.state.get("flow_id", "") + "." + node_data.get("Id")
        return {"id" : next_node_key, "data": node_data}

    @classmethod
    def process_node(cls, message_data, node_data):
        # agent_messages_data = [{"message" : message_data, "sending_to":
        # "AGENT"}]
        # if message_data:
        agent_messages = [message_data]
        # else:
            # agent_messages = []
            # pass
        # agent_messages = [message_data]
        user_messages = AgentConverter.get_agent_connected_messages()
        # return_messages = []
        # if node_data and event == "INTENT_TO_HANDOVER":
            # messages = CombinationProcessor(self.state).process_node(node_data)
            # agent_messages.extend(messages["user_messages"])
            # pass
        return {"user_messages": user_messages, "agent_messages": agent_messages}
