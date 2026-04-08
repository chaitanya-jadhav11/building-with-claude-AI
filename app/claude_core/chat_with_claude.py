from dotenv import load_dotenv
from llm.claude_client import ClaudeClient

load_dotenv()
messages = []

# Add the initial user question
def add_user_message(messages, text):
    user_message = {
        "role": "user",
        "content": text
    }
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {
        "role": "assistant",
        "content": text
    }
    messages.append(assistant_message)


def chat_with_claude(claude):
    while True:
        # get user input
        user_input = input(">  ")
        print(">", user_input)
        # Add the initial user question
        add_user_message(messages, user_input)
        system_prompt = """
        You are a patient math tutor.
        Do not directly answer a student's questions.
        Guide them to a solution step by step.
        """

        # Get Claude's response
        answer = claude.chat(messages, system_prompt, temperature=0.7, max_tokens=1000)
        # Add Claude's response to the conversation history
        add_assistant_message(messages, answer)
        print("final answer {}".format(answer))


def main():
    claude = ClaudeClient()
    print("Hello, main!")

    # Run the chat with Claude in a loop to allow multiple interactions
    # this will test system prompt and conversation history
    chat_with_claude(claude)


# Run this file to chat with Claude. You can ask it math questions and it will guide you to a solution step by step without directly giving you the answer.
# uv run python -m app.claude_core.chat_with_claude

if __name__ == "__main__":
    main()

