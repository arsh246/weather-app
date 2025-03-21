
# Weather Search App

This is a full-stack application that allows users to search for weather information by city. The app supports user authentication using Firebase, weather data retrieval from OpenWeather API, and location-based services using Google Maps API. Users can also view related YouTube videos for their searched city.

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: React.js
- **Database**: Firestore (Firebase)
- **Authentication**: Firebase Authentication
- **Weather API**: OpenWeather API
- **Location API**: Google Maps API
- **Video API**: YouTube Data API
- **State Management**: React Hooks

## Features

- **User Authentication**: Users can sign up, log in, and manage their account using Firebase Authentication.
- **Weather Search**: Users can search for the current weather in a specific city.
- **YouTube Integration**: Display related YouTube videos about the searched city.
- **History**: Users can view their previous weather searches stored in Firestore.
- **Weather History Management**: Users can update and delete previous weather search entries.

## Backend

The backend is built with **FastAPI**, providing a set of RESTful APIs to handle authentication and weather data. Firestore is used to store user-specific weather search history.

### Setup

1. **Install Dependencies**:
   Install Python dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file in the backend root directory with the following variables:
   ```env
   OPENWEATHER_API_KEY=<your_openweather_api_key>
   GOOGLE_MAPS_API_KEY=<your_google_maps_api_key>
   YOUTUBE_API_KEY=<your_youtube_api_key>
   FIREBASE_WEB_API_KEY=<your_firebase_web_api_key>
   ```

3. **Firebase Setup**:
   - Create a Firebase project and download the Firebase Admin SDK credentials JSON.
   - Place the credentials file in the `backend/` directory as `firebase_creds.json`.

4. **Run the Backend**:
   Start the backend server using `uvicorn`:
   ```bash
   uvicorn backend.main:app --reload
   ```

   The backend will be available at `http://localhost:8000`.

## Frontend

The frontend is built with **React** and provides a UI for users to sign up, log in, search for weather, and view related videos.

### Setup

1. **Install Dependencies**:
   Install frontend dependencies using `npm`:
   ```bash
   npm install
   ```

2. **Run the Frontend**:
   Start the frontend development server:
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`.

### Key Components

- **LoginForm**: Component for user login.
- **SignupForm**: Component for user signup.
- **SearchBar**: Component to search for a city.
- **WeatherCard**: Displays weather data for a city.
- **ErrorMessage**: Displays error messages.

## API Endpoints

### User Authentication

- **POST /signup**: Register a new user.
- **POST /login**: Log in a user and receive an authentication token.

### Weather Data

- **GET /weather/{city}**: Get weather data for a city.
- **GET /history**: Retrieve a user's weather search history.
- **PUT /update/{entry_id}**: Update a weather search history entry.
- **DELETE /delete/{entry_id}**: Delete a weather search history entry.
- **GET /export/json**: Export a user's weather search history as JSON.

### Google Maps & YouTube Integration

- **GET /location/{city}**: Get location (latitude, longitude) for a given city using Google Maps API.
- **GET /youtube/{city}**: Get YouTube videos related to a given city.

## Authentication

Authentication is handled via Firebase. When a user logs in, they receive a Firebase ID token that must be included in all authenticated API requests. The token can be stored in localStorage and sent with each request.

## Folder Structure

```bash
.
├── backend/
│   ├── firebase_creds.json       # Firebase credentials file
│   ├── main.py                   # FastAPI app
│   ├── requirements.txt          # Backend dependencies
│   └── .env                      # Environment variables
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/           # React components
│   │   └── App.js                # Main React component
│   ├── package.json              # Frontend dependencies
│   └── .env                      # Frontend environment variables
└── README.md                     # Project documentation
```

## Contribution

Feel free to fork the repository, create a new branch, and submit a pull request for any improvements or bug fixes.


