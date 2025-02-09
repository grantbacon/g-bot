import requests
from signalbot import Context, regex_triggered

from commands import GCommand
from dotenv import dotenv_values

config = dotenv_values(".env")

DEEPSEEK_API_KEY = config["DEEPSEEK_API_KEY"]
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


class DeepSeekCommand(GCommand):
    def describe(self) -> str:
        return ".ds <input> - Interact with DeepSeek's platform API"

    def call_deepseek_api(self, user_input: str) -> str:
        """Sends the user's input to DeepSeek's API and returns the response."""
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "deepseek-chat",
            "max_tokens": 2048,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            "stream": False,
        }

        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse the API response
            response_data = response.json()
            return (
                response_data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "No response from DeepSeek API.")
            )

        except requests.exceptions.RequestException as e:
            return f"Server is busy.. please try again later [{e}]."
        except Exception as e:
            return f"An error occurred: {e}"

    @regex_triggered(r"^\.ds")
    async def handle(self, context: Context):
        await super().handle(context)
        user_input = context.message.text.split(".ds", 1)[
            1
        ].strip()  # Extract the input after ".ds"
        await context.start_typing()
        api_response = self.call_deepseek_api(user_input)
        await context.stop_typing()
        await context.reply(api_response)
