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
                    "type": "base64",
                    "data": file_base64,
                    "media_type": "application/pdf",
                },
                "title": "earth.pdf",
                "citations": {"enabled": True}
            },
        ])

        response = chat(messages)
        print ("response with citations:", response)

        """
         Expected output should look like:
         
         response with citations: Message(id='x', container=None, content=[TextBlock
         (citations=[CitationPageLocation(cited_text="Earth\r\nThe Blue Marble, Apollo 17, December 1972\r\nDesignations\r\nAlternative\r\nnames\r\nThe world · The globe ·\r\nTerra · Tellus · Gaia ·\r\nMother Earth · 
         Sol III\r\nAdjectives Earthly · Terrestrial · Terran\r\n· Tellurian\r\nSymbol and\r\nOrbital chaxxxxxxxxxxal)\r\n365.256 363 004 d\r\n[2]\r\n(1.000 017 420 96 aj)\r\nAverage orbital\r\nspeed\r\n29.7827 km/s\r\n[3]\r\nMean anomaly 358.617°\r\nInclination 7.155° –
          Sun's equator;\r\nEarth\r\nEarth is the third planet from the Sun and the only\r\nastronomical object known to harbor life. This is\r\nenabled by Earth being an ocean world, the only one in\r\nthe Solar System sustaining liquid surface water. 
          Almost\r\nall of Earth's water is contained in its global ocean,\r\ncovering 70.8% of Earth's crust. ", document_index=0, document_title='earth.pdf', end_page_number=2, file_id=None, start_page_number=1, type='page_location')], 
          text='Earth is the third planet from the Sun and the only known astronomical object to harbor life, enabled by being an ocean world with liquid surface water covering 70.8% of its crust.', type='text')], model='claude-haiku-4-5-20251001', 
          role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, 
          cache_read_input_tokens=0, inference_geo='not_available', input_tokens=11200, output_tokens=66, server_tool_use=None, service_tier='standard'))
         
         
        """




# uv run -m app.claude_advance_capabilities.citations_example
if __name__ == "__main__":
    main()
