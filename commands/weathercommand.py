from commands import GCommand
from geopy.geocoders import Nominatim
from signalbot import regex_triggered, Context
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

OPENWEATHERMAP_API_KEY = config["OPENWEATHERMAP_API_KEY"]
OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# User agent for geocoding
USER_AGENT = "weather-command g-bot"


def get_weather(location) -> str:
    # Geocode the location to get coordinates
    gl = Nominatim(user_agent=USER_AGENT)
    try:
        gloc = gl.geocode(location)
        if not gloc:
            return "Location not found."

        # Fetch weather data using OpenWeatherMap API
        params = {
            "lat": gloc.latitude,
            "lon": gloc.longitude,
            "appid": OPENWEATHERMAP_API_KEY,
            "units": "imperial",  # Use "metric" for Celsius
        }
        response = requests.get(OPENWEATHERMAP_API_URL, params=params)
        response.raise_for_status()  # Raise an error for bad status codes

        weather_data = response.json()

        # Extract relevant weather information
        temperature = weather_data["main"]["temp"]
        weather_description = weather_data["weather"][0]["description"]
        city = weather_data["name"]

        return f"{city}: {weather_description}, Temperature: {temperature}°F"

    except requests.exceptions.RequestException as e:
        return f"Failed to fetch weather data: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


class WeatherCommand(GCommand):
    def weather_message(self, location) -> str:
        return "Weather for " + location + ": " + get_weather(location)

    def describe(self) -> str:
        return ".weather <zip/location> - tells the weather"

    @regex_triggered(r"^\.weather\s.+")
    async def handle(self, context: Context):
        await super().handle(context)
        location = context.message.text.split("weather", 1)[1].strip()
        await context.start_typing()
        await context.reply(self.weather_message(location))
        await context.stop_typing()
