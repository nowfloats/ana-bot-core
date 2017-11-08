import boto3
import json
from src.config import application_config as config 

class KinesisHelper():

    def __init__(self,*args, **kwargs):
        try:
            self.aws_key = config["AWS_ACCESS_KEY_ID"]
            self.aws_secret = config["AWS_ACCESS_SECRET_KEY"]
            self.aws_region = config["AWS_REGION"]
            self.stream_name = config["KINESIS_STREAM_NAME"]
            self.client = boto3.client(
                    "kinesis",
                    aws_access_key_id=self.aws_key,
                    aws_secret_access_key=self.aws_secret,
                    region_name=self.aws_region
                    )
		
        except Exception as e:
            # handle this case
            print(e)
            raise

    def log_message(self, data=None, key = "core-chat-events"):
        if (data == None):
            return 
        json_data = json.dumps(data)
        response = self.client.put_records(
                Records = [
                    {
                        "Data": json_data,
                        "PartitionKey": key

                    }
                ],
                StreamName = self.stream_name
            )
        # check response and handle error
        return
        # print(response)

