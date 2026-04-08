from anthropic import Anthropic


class ClaudeClient:
    def __init__(self, api_key: str = None, model: str = "claude-haiku-4-5-20251001"):
        """
        Initialize Claude client
        """
        self.client = Anthropic(api_key=api_key) if api_key else Anthropic()
        self.model = model

    def chat(self, messages, system_message=None, temperature=1.0, max_tokens=1000):
        """
        Send chat request to Claude
        """
        params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature
        }

        if system_message:
            params["system"] = system_message

        response = self.client.messages.create(**params)

        return self._extract_text(response)

    def _extract_text(self, response):
        """
        Extract text from Claude response
        """
        try:
            return response.content[0].text
        except (IndexError, AttributeError):
            return ""