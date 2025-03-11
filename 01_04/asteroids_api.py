import requests
from datetime import datetime
import json

# API used to check for asteroids headed toward Earth
# Documentation: https://api.nasa.gov/

# Replace with your API key
API_KEY = 'DEMO_KEY'
NASA_BASE_URL = 'https://api.nasa.gov/neo/rest/v1/feed'

# JSON helper function
def stringToJSON(message, count):
    #json string data
    asteroid_string = '{"count":' + count + ', "message": "' + message + '"}'

    return asteroid_string

def get_asteroid_count():
    today = datetime.today().strftime('%Y-%m-%d')
    params = {"start_date": today, "end_date": today, "api_key": API_KEY}

    response = requests.get(NASA_BASE_URL, params=params)
    api_data = response.json()
    return str(len(api_data))
  
try:
    today = datetime.today().strftime('%Y-%m-%d')
    params = {"start_date": today, "end_date": today, "api_key": API_KEY}

    #construct request and call api
    response = requests.get(NASA_BASE_URL, params=params)
    api_data = response.json()

    message = "No asteroids headed toward Earth."

    for key in api_data:
      if key == 'is_potentially_hazardous_asteroid' and api_data[key] == True: 
          message = "Dangerous asteroid(s) headed toward Earth. Take cover." 
      else:
          message = "Asteroids headed toward Earth but none of them pose any danger."

    #convert string to  object
    json_object = json.loads(stringToJSON(message, get_asteroid_count()))
    print(json_object)
except Exception as e:
    print(e)
    print("The NASA API, NeoWs (Near Earth Object Web Service), is currently down. Please try your request again later.")