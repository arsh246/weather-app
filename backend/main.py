from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
from google.cloud import firestore

# Load environment variables
load_dotenv()

# Firestore setup
db = firestore.Client()
weather_collection = db.collection("weather_searches")
# Test Firestore connection
try:
    # Get the list of collections (just as a test)
    collections = db.collections()
    for collection in collections:
        print("Firestore collection:", collection.id)
except Exception as e:
    print("Error connecting to Firestore:", str(e))

# FastAPI setup
app = FastAPI()

# OpenWeather API Key
API_KEY = os.getenv("OPENWEATHER_API_KEY")
print("OpenWeather API Key:", API_KEY)  # Debugging line
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.get("/weather/{city}")
def get_weather(city: str):
    """Fetches current weather data for a given city."""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="City not found")

    data = response.json()
    weather_data = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "weather": data["weather"][0]["description"],
    }

    # Store in Firestore
    weather_collection.add(weather_data)

    return weather_data
