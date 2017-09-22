import json
from apscheduler.schedulers.background import BackgroundScheduler
from src import app
from src.config import application_config as config 
from src.connectors.sqs_helper import SQSHelper 
from src.responder import MessageProcessor

scheduler = BackgroundScheduler()

class Scheduler():

    def __init__(self, *args, **kwargs):
        self.sqs_client = SQSHelper()
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.message_listener, "interval", seconds=5)

    def start_jobs(self):
        self.scheduler.start() 

    def message_listener(self):
        messages = self.sqs_client.fetch_messages()
        if messages == []:
            print("No new messages found")
        else:
            self._process_messages(messages)

    def _process_messages(self, messages):

        for message in messages:
            parsed_message = json.loads(message['Body'])
            print("Incoming Message")
            print(parsed_message)
            print("************")
            # change hard coded values to class and factory
            if (parsed_message["meta"]["senderType"] == 0):
                MessageProcessor(parsed_message).respond_to_message()
            else: 
                pass
            try:
                self.sqs_client.delete_message(message["ReceiptHandle"])
            except Exception as e:
                print(e)
                raise

