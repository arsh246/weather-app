from fastapi import FastAPI, HTTPException, Depends
import requests
import os
from dotenv import load_dotenv
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, auth
from pydantic import BaseModel
from typing import List

# Load environment variables
load_dotenv()

# Load Firebase credentials
cred = credentials.Certificate("backend/firebase_creds.json")
firebase_admin.initialize_app(cred)

# Firestore setup
db = firestore.Client()
weather_collection = db.collection("weather_searches")

# Test Firestore connection
try:
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


FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")

# Models
class UserSignup(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# --------- User Authentication Routes ---------

@app.post("/signup")
def signup(user: UserSignup):
    """Registers a new user in Firebase Authentication."""
    print("Signup route hit")
    try:
        user_record = auth.create_user(email=user.email, password=user.password)
        return {"message": "User created successfully", "uid": user_record.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
def login(user: UserLogin):
    """Logs in a user and returns an authentication token."""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": user.email, "password": user.password, "returnSecureToken": True}
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return response.json()

def verify_token(id_token: str):
    """Verifies Firebase authentication token."""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    

@app.get("/history", response_model=List[dict])
def get_weather_history(id_token: str = Depends(verify_token)):
    """Retrieve stored weather searches for the authenticated user."""
    try:
        user_ref = db.collection("users").document(id_token)
        searches_ref = user_ref.collection("searches")
        docs = searches_ref.stream()

        history = []
        for doc in docs:
            history.append({**doc.to_dict(), "id": doc.id})

        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   
    
class UpdateWeatherRequest(BaseModel):
    temperature: float
    weather: str

@app.put("/update/{entry_id}")
def update_weather(entry_id: str, update_data: UpdateWeatherRequest, id_token: str = Depends(verify_token)):
    """Update a weather record by ID for the authenticated user."""
    try:
        user_ref = db.collection("users").document(id_token)
        searches_ref = user_ref.collection("searches").document(entry_id)

        # Check if document exists
        if not searches_ref.get().exists:
            raise HTTPException(status_code=404, detail="Record not found")

        # Update the record
        searches_ref.update(update_data.dict())

        return {"message": "Record updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete("/delete/{entry_id}")
def delete_weather(entry_id: str, id_token: str = Depends(verify_token)):
    """Delete a stored weather search by ID for the authenticated user."""
    try:
        user_ref = db.collection("users").document(id_token)
        searches_ref = user_ref.collection("searches").document(entry_id)

        # Check if document exists
        if not searches_ref.get().exists:
            raise HTTPException(status_code=404, detail="Record not found")

        # Delete the record
        searches_ref.delete()

        return {"message": "Record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Google Maps API Integration
MAPS_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def get_location_info(city: str):
    """Fetches location data (latitude, longitude) from Google Maps API."""
    params = {"address": city, "key": os.getenv("GOOGLE_MAPS_API_KEY")}
    response = requests.get(MAPS_API_URL, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch location information")
    
    data = response.json()
    
    if "results" not in data or len(data["results"]) == 0:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Extract relevant data (latitude, longitude)
    location = data["results"][0]["geometry"]["location"]
    return {
        "city": city,
        "latitude": location["lat"],
        "longitude": location["lng"]
    }

# YouTube API Integration
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

def get_youtube_videos(city: str):
    """Fetches YouTube videos related to a given city."""
    params = {
        "part": "snippet",
        "q": city,
        "type": "video",
        "key": os.getenv("YOUTUBE_API_KEY"),
        "maxResults": 3  
    }
    
    response = requests.get(YOUTUBE_API_URL, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch YouTube videos")
    
    data = response.json()
    
    if "items" not in data or len(data["items"]) == 0:
        raise HTTPException(status_code=404, detail="No videos found for this location")
    
    # Extract video information
    videos = []
    for item in data["items"]:
        video = {
            "title": item["snippet"]["title"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            "description": item["snippet"]["description"]
        }
        videos.append(video)
    
    return videos


# --------- Protected Weather API Route ---------
@app.get("/weather/{city}")
def get_weather(city: str, id_token: str = Depends(verify_token)):
    """Fetches current weather data for a given city (Authenticated Users Only)."""
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="City not found")

    data = response.json()
    weather_data = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "weather": data["weather"][0]["description"],
        "user_id": id_token  # Storing which user requested it
    }
    # Fetch location info from Google Maps API
    location_info = get_location_info(city)
    
    # Fetch related YouTube videos
    youtube_videos = get_youtube_videos(city)

    # Store in Firestore under user's document
    user_ref = db.collection("users").document(id_token)
    user_ref.collection("searches").add(weather_data)

        # Combine the weather data, location info, and YouTube videos
    weather_data.update(location_info)
    weather_data["youtube_videos"] = youtube_videos

    return weather_data

@app.get("/export/json")
def export_weather_history_json(id_token: str = Depends(verify_token)):
    """Export user's weather search history as JSON."""
    try:
        user_ref = db.collection("users").document(id_token)
        searches_ref = user_ref.collection("searches")
        docs = searches_ref.stream()

        history = []
        for doc in docs:
            history.append(doc.to_dict())

        return history

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
