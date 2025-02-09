import requests
from signalbot import Context, regex_triggered

from commands import GCommand
from dotenv import dotenv_values

config = dotenv_values(".env")
DEEPSEEK_API_KEY = config["DEEPSEEK_API_KEY"]
DEEPSEEK_API_URL = "https://api.deepseek.com/user/balance"


class BalanceCommand(GCommand):
    def describe(self) -> str:
        return ".bal - Get remaining balance for DeepSeek's platform API"

    def call_deepseek_api(self) -> str:
        """Sends the user's input to DeepSeek's API and returns the response."""
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(
                DEEPSEEK_API_URL,
                headers=headers,
            )
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse the API response
            response_data = response.json()
            balance_info = response_data.get("balance_infos", [{}])[0]
            balance = balance_info.get("total_balance", "0.00")
            currency = balance_info.get("currency", "USD?")
            return f"${balance} {currency} balance remaining!"

        except requests.exceptions.RequestException as e:
            return f"Failed to call DeepSeek API: {e}"
        except Exception as e:
            return f"An error occurred: {e}"

    @regex_triggered(r"^\.bal")
    async def handle(self, context: Context):
        await super().handle(context)
        await context.start_typing()
        api_response = self.call_deepseek_api()
        await context.stop_typing()
        await context.reply(api_response)  # Send the API response back to the user
