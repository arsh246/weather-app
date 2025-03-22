import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SearchBar from './components/SearchBar';
import WeatherCard from './components/WeatherCard';
import ErrorMessage from './components/ErrorMessage';
import './App.css';
import Footer from "./components/footer";

// Components for login/signup
const LoginForm = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:8000/login', { email, password });
      localStorage.setItem('authToken', response.data.idToken);  // Store token
      onLogin();  // On successful login, change the login status
    } catch (err) {
      console.error(err);
      alert('Login failed, please try again.');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

const SignupForm = ({ onSignup }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = async () => {
    try {
      const response = await axios.post('http://localhost:8000/signup', { email, password });
      localStorage.setItem('authToken', response.data.idToken);  // Store token
      onSignup();  // On successful signup, change the login status
    } catch (err) {
      console.error(err);
      alert('Signup failed, please try again.');
    }
  };

  return (
    <div>
      <h2>Sign Up</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleSignup}>Sign Up</button>
    </div>
  );
};

const App = () => {
  const [city, setCity] = useState('');
  const [weatherData, setWeatherData] = useState(null);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isSignup, setIsSignup] = useState(false); // Manage between login/signup form

  // Check if user is already authenticated (if token exists in localStorage)
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

    // Get weather for the current location using Geolocation API
  const handleGetCurrentLocationWeather = async () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (position) => {
          const { latitude, longitude } = position.coords;
          try {
            setError(null); // Reset error before making a request
            const token = localStorage.getItem('authToken');
            const response = await axios.get(
              `http://localhost:8000/weather/current?lat=${latitude}&lon=${longitude}&id_token=${token}`
            );
            setWeatherData(response.data);
          } catch (err) {
            setWeatherData(null);
            setError('Unable to retrieve weather for your current location!');
          }
        });
      } else {
        setError('Geolocation is not supported by this browser.');
      }
   };

  const handleSearch = async () => {
    if (!city) {
      setError('Please enter a city!');
      return;
    }
    try {
      setError(null); // Reset error before making a request
      const token = localStorage.getItem('authToken');
      const response = await axios.get(`http://localhost:8000/weather/${city}?id_token=${token}`);
      setWeatherData(response.data);
    } catch (err) {
      setWeatherData(null);
      setError('City not found or something went wrong!');
    }
  };

  // Login or signup callback functions
  const handleLogin = () => setIsAuthenticated(true);
  const handleSignup = () => setIsAuthenticated(true);

  // Logout callback
  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
  };

  return (
    <div>
      {!isAuthenticated ? (
        // Show login/signup page if user is not authenticated
        <div>
          {isSignup ? (
            <SignupForm onSignup={handleSignup} />
          ) : (
            <LoginForm onLogin={handleLogin} />
          )}
          <button onClick={() => setIsSignup(!isSignup)}>
            {isSignup ? 'Already have an account? Login' : "Don't have an account? Sign Up"}
          </button>
        </div>
      ) : (
        // Show weather search page if user is authenticated
        <div>
          <h1>Weather App</h1>
          <button onClick={handleLogout}>Logout</button>
          <SearchBar value={city} onChange={(e) => setCity(e.target.value)} onSearch={handleSearch} />
          <button onClick={handleGetCurrentLocationWeather}>Get Current Location Weather</button>
          <ErrorMessage message={error} />
          <WeatherCard weatherData={weatherData} />
        </div>
      )}
      {/* Footer Component */}
      <Footer />
    </div>
  );
};

export default App;
