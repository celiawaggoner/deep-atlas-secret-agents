import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

# OpenWeatherMap API URL
OPENWEATHERMAP_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to call the weather API and return the weather info for a city
def get_weather(city_name):
    if not OPENWEATHERMAP_API_KEY:
        raise ValueError("OPENWEATHERMAP_API_KEY is not set in the environment variables.")

    params = {"q": city_name, "appid": OPENWEATHERMAP_API_KEY, "units": "imperial"}

    response = requests.get(OPENWEATHERMAP_BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        city = data['name']
        # return f"Summarize: {data}. Give a 1 sentence summary of the weather in {city}."
        return data
    else:
        return "Sorry, I couldn't retrieve the weather for that location."
