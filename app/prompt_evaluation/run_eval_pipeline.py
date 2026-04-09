from dotenv import load_dotenv
from anthropic import Anthropic
import json
from statistics import mean

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


# Function to grade a test case + output using a model
def grade_by_model(test_case, output):
    eval_prompt = f"""
    You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.
    
    Original Task:
    <task>
    {test_case["task"]}
    </task>
    
    Solution to Evaluate:
    <solution>
    {output}
    </solution>
    
    Output Format
    Provide your evaluation as a structured JSON object with the following fields, in this specific order:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement
    - "reasoning": A concise explanation of your overall assessment
    - "score": A number between 1-10
    
    Respond with JSON. Keep your response concise and direct.
    Example response shape:
    {{
        "strengths": string[],
        "weaknesses": string[],
        "reasoning": string,
        "score": number
    }}
        """

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)


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


def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
    Please solve the following task:

    {test_case["task"]}
    """

    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output


def run_test_case(test_case):
    output = run_prompt(test_case)

    # Grade the output
    model_grade = grade_by_model(test_case, output)
    score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    return {
        "output": output,
        "test_case": test_case,
        "score": score,
        "reasoning": reasoning
    }

def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean([result["score"] for result in results])
    print(f"Average score: {average_score}")

    return results



def main():
    print("Hello, main!")

    with open("app/prompt_evaluation/dataset.json", "r") as f:
        dataset = json.load(f)

    results = run_eval(dataset)
    print(json.dumps(results, indent=2))

# Run this file to execute the evaluation pipeline on the dataset. It will print the results of each test case, including the output and score.
# uv run python -m app.prompt_evaluation.run_eval_pipeline
if __name__ == "__main__":
    main()
