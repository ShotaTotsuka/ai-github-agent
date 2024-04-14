import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv(verbose=True)

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

bedrock_runtime = session.client("bedrock-runtime", region_name="us-east-1")

prompt_config = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4096,
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "日本の総理大臣は？"},
            ],
        }
    ],
}

body = json.dumps(prompt_config)

modelId = "anthropic.claude-3-haiku-20240307-v1:0"
accept = "application/json"
contentType = "application/json"

response = bedrock_runtime.invoke_model(
    body=body, modelId=modelId, accept=accept, contentType=contentType
)
response_body = json.loads(response.get("body").read())

results = response_body.get("content")[0].get("text")
print(results)
print("長さ: ",len(results))
