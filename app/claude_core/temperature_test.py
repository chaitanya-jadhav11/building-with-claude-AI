from dotenv import load_dotenv
from llm.claude_client import ClaudeClient




load_dotenv()
messages = []

def temperature_test(claude):
    print("Temperature test")
    system_prompt="You are a helpful assistant."
    user_messages = {
        "role": "user",
        "content": "Generate a one sentence movie idea"
    }
    messages.append(user_messages)
    answer = claude.chat(messages, system_prompt, temperature=1.0, max_tokens=1000)
    print("Temperature 0.0: {}".format(answer))

    # Output 1 - temperature 0.0:
    # cynical time-traveling insurance adjuster must prevent catastrophic accidents across history while falling in love with a fellow agent who believes every disaster is actually meant to happen.
    # Output 2 t
    # A cynical time-traveling insurance adjuster must prevent catastrophic accidents across history while falling in love with a fellow agent who believes every disaster is actually meant to happen.


    #output 1 - temperature 1.0:
    #A burned-out video game designer discovers that the unfinished game she abandoned ten years ago has mysteriously become real, and the only way to save the world from her creation is to finally complete it.
    #output 2 - temperature 1.0:
    # A brilliant but disgraced chef must assemble a ragtag team of culinary misfits to win an underground cooking competition and save her family restaurant from being demolished.


def main():
    print("Hello, main!")
    claude = ClaudeClient()
    # testing temperature
    temperature_test(claude)

# Run this file to test the temperature parameter of the Claude API. You should see different outputs for temperature 0.0 and 1.0.
#  uv run python -m app.claude_core.temperature_test
if __name__ == "__main__":
    main()