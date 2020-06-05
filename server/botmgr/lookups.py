import json
import os
import requests
import time

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

api_key = os.getenv('OPEN_WEATHER_API_KEY')
weather_url = "http://api.openweathermap.org/data/2.5/weather?"

def lookup_weather(response: dict) -> str:
    address: dict = response['queryResult']['parameters']['address']
    location: str = address['city']

    response = requests.get(weather_url + "appid=" + api_key + "&q=" + location).json()

    if response["cod"] != "404":
        current_temperature = response["main"]["temp"]
        current_temperature = (current_temperature - 273.15) * (9.0 / 5.0) + 32.0

        sentence: str = 'The current weather in ' + location + ' is ' + \
            "{:.2f}".format(current_temperature) + u"\N{DEGREE SIGN}" + 'F and ' + response["weather"][0]["description"] + '.'
        return sentence
    else: 
        return 'Unable to find out the weather for ' + location

geolocator = Nominatim(user_agent="AI_TEAM_7")
tf = TimezoneFinder()
time_url = "http://worldtimeapi.org/api/timezone/"

def lookup_time(response: dict) -> str:
    location: str = response['queryResult']['outputContexts'][0]['parameters']['location.original']

    if location is None or location == '':
        time_res = int(time.time())
        return "The current time is " + time.strftime("%H:%M %Z", time.localtime(time_res)) + "."
    else:
        geocode = geolocator.geocode(location)
        tz = tf.timezone_at(lng=geocode.longitude, lat=geocode.latitude)
        time_response = requests.get(time_url + tz).json()
        time_res = time_response['datetime'].split('T')[1].split(':')
        print(time_response)
        return "The current time in " + str(location) + " is " + str(time_res[0]) + ":" + str(time_res[1]) + " " + time_response['abbreviation'] + "."