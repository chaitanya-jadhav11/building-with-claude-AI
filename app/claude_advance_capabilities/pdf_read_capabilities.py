# Load env variables and create client
import base64
from dotenv import load_dotenv
from anthropic import Anthropic
# Helper functions
from anthropic.types import Message
from app.utils.constants import MODEL

load_dotenv()

client = Anthropic()
model = MODEL


def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


def chat(
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
):
    params = {
        "model": model,
        "max_tokens": 4000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if thinking:
        params["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking_budget,
        }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])





def main():
    print("Running vision capabilities example...")


    prompt = """
    Summarize the document in one sentence"
    """

    with open("app/claude_advance_capabilities/images/earth.pdf", "rb") as f:
        file_bytes = f.read()
        file_base64 = base64.b64encode(file_bytes).decode("utf-8")

        messages = []

        add_user_message(messages, [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "document",
                "source": {
                    "type" : "base64",
                    "data": file_base64,
                    "media_type": "application/pdf",
                }
            },
        ])

        response = chat(messages)
        print ("response:", text_from_message(response))




# uv run -m app.claude_advance_capabilities.pdf_read_capabilities
# The PDF reading capabilities example.

if __name__ == "__main__":
    main()
