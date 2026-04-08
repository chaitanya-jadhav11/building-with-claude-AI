from anthropic import Anthropic
from dotenv import load_dotenv
from app.utils.constants import MODEL
import json

load_dotenv()
messages = []


def structured_data_response():
    print("structured_data_response test")

    add_user_message("Generate a very short event bridge rule as json")
    add_assistant_message("```json")

    params = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": messages,

    }
    client = Anthropic()
    res = client.messages.create(**params, stop_sequences=["```"])
    output =json.loads(res.content[0].text.strip())
    print(output)

    """
    OUTPUT

     {
        "Name": "MyRule",
        "EventPattern": {
            "source": ["aws.ec2"],
            "detail-type": ["EC2 Instance State-change Notification"],
            "detail": {
                "state": ["running"]
            }
        },
        "State": "ENABLED",
        "Targets": [
            {
                "Arn": "arn:aws:lambda:us-east-1:123456789012:function:MyFunction",
                "Id": "1"
            }
        ]
    }
    """    

# Add the initial user question
def add_user_message(text):
    user_message = {
        "role": "user",
        "content": text
    }
    messages.append(user_message)


def add_assistant_message(text):
    assistant_message = {
        "role": "assistant",
        "content": text
    }
    messages.append(assistant_message)



def main():
    print("Hello, main!")
    structured_data_response()


# Run this file to test structured data response from Claude. You should see a json response that is not wrapped in markdown code blocks.
# uv run python -m app.claude_core.structured_data_response
if __name__ == "__main__":
    main()
