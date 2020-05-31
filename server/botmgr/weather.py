import json
import os
import requests

api_key = os.getenv('OPEN_WEATHER_API_KEY')
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def handle(response: dict) -> str:
    address: dict = response['queryResult']['parameters']['address']
    return query(address['city'])

def query(location: str) -> str:
    response = requests.get(base_url + "appid=" + api_key + "&q=" + location).json()

    if response["cod"] != "404":
        current_temperature = response["main"]["temp"]
        current_temperature = (current_temperature - 273.15) * (9.0 / 5.0) + 32.0

        sentence: str = 'The current weather in ' + location + ' is ' + \
            "{:.2f}".format(current_temperature) + u"\N{DEGREE SIGN}" + 'F and ' + response["weather"][0]["description"] + '.'
        return sentence
    else: 
        return 'Unable to find out the weather for ' + location 