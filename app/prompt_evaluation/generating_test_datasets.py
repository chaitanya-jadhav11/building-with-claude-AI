from dotenv import load_dotenv
from anthropic import Anthropic
import json

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"

# Helper functions
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages, system=None, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "stop_sequences": stop_sequences,
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text


def generate_dataset():
    prompt = """
    Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
    that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
    each representing task that requires Python, JSON, or a Regex to complete.
    
    Example output:
    ```json
    [
        {
            "task": "Description of task",
        },
        ...additional
    ]
    ```
    
    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
    * Focus on tasks that do not require writing much code
    
    Please generate 3 objects.
"""
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    add_assistant_message(messages, "''")
    return json.loads(text)

def main():
    print("Hello, main!")
    dataset = generate_dataset()
    with open("app/prompt_evaluation/dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)

    print(dataset)


# Run this file to generate a dataset for prompt evaluation. The dataset will consist of tasks that require Python, JSON, or Regex solutions for AWS-related tasks. You can modify the prompt in the generate_dataset function to customize the types of tasks you want in the dataset.
# uv run python -m app.prompt_evaluation.generating_test_datasets
if __name__ == "__main__":
    main()
