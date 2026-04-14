# Load env variables and create client
from dotenv import load_dotenv
from anthropic import Anthropic
# Helper functions
from anthropic.types import Message


from app.utils.constants import MODEL

load_dotenv()

client = Anthropic()
model = MODEL



# Magic string to trigger redacted thinking
thinking_test_str = "ANTHROPIC_MAGIC_STRING_TRIGGER_REDACTED_THINKING_46C9A13E193C177646C7398A98432ECCCE4C1253D5E2D82641AC0E52CC2876CB"


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
    thinking_budget=1024
):
    params = {
        "model": model,
        "max_tokens": 4000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    if thinking:
        params["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking_budget
        }

    message = client.messages.create(**params)
    return message


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])


def main():
    print("Running extended thinking example...")

    messages = []
    add_user_message(messages, "Write a one paragraph about recursion.")
    response = chat(messages, thinking= True)
    print(response)


# uv run -m app.claude_advance_capabilities.extended_thinking
if __name__ == "__main__":
    main()


"""
Expected output:

Message(id='msg_01A2Gx9MaUMiXq8oGrt2f3mq', container=None, content=[
ThinkingBlock
(signature='xxxxxxxxxxxxxx'

thinking='The user is asking for a one-paragraph explanation of recursion. I should cover the key concept of what recursion is, provide an example or clarification, and explain how it works in a clear and concise way.
\n\nLet me write a paragraph that explains:\n- What recursion is\n- The basic mechanism (function calling itself)\n- Key components (base case and recursive case)\n- Maybe a brief example or application', type='thinking'), 

TextBlock(citations=None, text='# Recursion\n\nRecursion is a programming technique where a function calls itself to solve a problem by breaking it down into smaller, similar subproblems. A recursive function must have a base case—a condition that stops the recursion—and
 a recursive case that moves toward that base case by calling itself with modified parameters. For example, calculating the factorial of a number (n!) can be solved recursively: the factorial of n equals n multiplied by the factorial of n-1,
with the base case being that the factorial of 0 or 1 is 1. Recursion is particularly useful for problems that have a naturally recursive structure, such as traversing tree structures, searching through directories, or solving mathematical sequences,
though it requires careful design to avoid infinite loops and excessive memory usage from call stack buildup.', type='text')],

model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), 
cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=44, output_tokens=273, server_tool_use=None, service_tier='standard'))


"""
