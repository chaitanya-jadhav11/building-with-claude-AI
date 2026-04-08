from anthropic import Anthropic
from dotenv import load_dotenv
from app.utils.constants import MODEL

load_dotenv()
messages = []


def response_streaming_basic():
    print("response_streaming_basic test")
    user_messages = {
        "role": "user",
        "content": "Generate a one sentence movie idea"
    }
    messages.append(user_messages)

    params = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": messages,

    }
    client = Anthropic()
    stream = client.messages.create(**params, stream=True)
    for event in stream:
        print(event)

        """
        OUTPUT
        RawMessageStartEvent(message=Message(id='msg_011RMHEJeHMX6wzctibMhwkZ', container=None, content=[], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason=None, stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
                cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=13, output_tokens=1, server_tool_use=None, service_tier='standard')), type='message_start') RawContentBlockStartEvent(content_block=TextBlock(citations=None, text='', type='text'), index=0,type='content_block_start')
        RawContentBlockDeltaEvent(delta=TextDelta(text='#', type='text_delta'), index=0, type='content_block_delta')
        RawContentBlockDeltaEvent( delta=TextDelta(text=' Movie Idea\n\nA deaf parkour expert must navigate a cr', type='text_delta'), index=0,type='content_block_delta')
        RawContentBlockDeltaEvent(delta=TextDelta(text='umbling skyscraper to rescue her sister while being hun', type='text_delta'), index=0, type='content_block_delta')
        RawContentBlockDeltaEvent(delta=TextDelta(text='ted by a villain who relies entirely on sound-based surveillance systems.', type='text_delta'), index=0, type='content_block_delta')
        RawContentBlockStopEvent(index=0, type='content_block_stop') RawMessageDeltaEvent(delta=Delta(container=None, stop_details=None, stop_reason='end_turn', stop_sequence=None),type='message_delta', usage=MessageDeltaUsage(cache_creation_input_tokens=0, cache_read_input_tokens=0,input_tokens=13, output_tokens=44, server_tool_use=None))
        RawMessageStopEvent(type='message_stop')
        """


def response_simplified_text_streaming():
    print("response_simplified_text_streaming test")
    user_messages = {
        "role": "user",
        "content": "Generate a one sentence movie idea"
    }
    messages.append(user_messages)

    params = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": messages,

    }
    client = Anthropic()
    with client.messages.stream(**params) as stream:
        for text in stream.text_stream:
            print(text, end="")

        """
        OUTPUT
        A brilliant but disgraced architect discovers that the buildings she designs can manipulate people's emotions, and she must decide whether to use this power to save her dying daughter or expose the technology before it's weaponized by a shadowy corporation.
        """


def response_get_complete_message():
    print("response_get_complete_message test")
    user_messages = {
        "role": "user",
        "content": "Generate a one sentence movie idea"
    }
    messages.append(user_messages)

    params = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": messages,

    }
    client = Anthropic()
    with client.messages.stream(**params) as stream:
        for text in stream.text_stream:
            pass

        final_message = stream.get_final_message()
        print(final_message)
        """
        OUTPUT
        response_simplified_text_streaming test
        ParsedMessage(id='msg_01NvFhJtGfanmHkyWsi7nPtj', container=None, content=[ParsedTextBlock(citations=None, text='# Movie Idea\n\nA cynical food critic discovers that the elderly woman running a small neighborhood restaurant is actually a time-traveler who has been perfecting the same meal for 200 years.',
        type='text', parsed_output=None)], model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, 
        ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=13, output_tokens=44, server_tool_use=None, service_tier='standard'))
        """


def main():
    print("Hello, main!")

    response_streaming_basic()

    response_simplified_text_streaming()

    response_get_complete_message()


# Run this file to test different ways of streaming responses from the Claude API. You should see the raw events, the simplified text stream, and the final message object in the output.
# uv run python -m app.claude_core.response_streaming
if __name__ == "__main__":
    main()
