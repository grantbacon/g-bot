import base64
import requests
from datetime import datetime
from commands import GCommand
from signalbot import triggered, Context


class GarfieldCommand(GCommand):
    def describe(self) -> str:
        return ".garfield - get today's Garfield comic"

    @triggered(".garfield", case_sensitive=False)
    async def handle(self, context: Context):
        await super().handle(context)

        # Get today's date
        today = datetime.today()
        year, month, day = today.year, today.month, today.day

        # Construct the URL
        url = f"https://www.gocomics.com/garfield/{year}/{month:02d}/{day:02d}"

        # Make the GET request
        response = requests.get(url, stream=True)

        # Search for the unique div.comic element and extract data-image
        html_content = response.text
        comic_div_start = html_content.find('<div class="comic')

        if comic_div_start != -1:
            # Find the start of the data-image attribute within the div
            data_image_start = html_content.find('data-image="', comic_div_start)

            if data_image_start != -1:
                data_image_start += len('data-image="')
                data_image_end = html_content.find('"', data_image_start)
                comic_url = html_content[data_image_start:data_image_end]

                # Download the GIF image
                image_response = requests.get(comic_url, stream=True)
                if image_response.status_code == 200:
                    # Convert the image to base64
                    image_data = image_response.content
                    base64_image = base64.b64encode(image_data).decode("utf-8")
                    data_uri = f"data:image/gif;base64,{base64_image}"

                    # Reply with the base64 attachment
                    message = f"Garfield by Jim Davis - {year}/{month:02d}/{day:02d}"
                    await context.start_typing()
                    await context.reply(message, base64_attachments=[data_uri])
                    await context.stop_typing()
                else:
                    await context.start_typing()
                    await context.reply("Failed to download the comic image.")
                    await context.stop_typing()
            else:
                await context.start_typing()
                await context.reply("Could not find the comic")
                await context.stop_typing()
        else:
            await context.start_typing()
            await context.reply("Could not find the Garfield comic.")
            await context.stop_typing()
