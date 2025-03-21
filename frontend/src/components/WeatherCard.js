import React from 'react';

const WeatherCard = ({ weatherData }) => {
  if (!weatherData) return null;

  return (
    <div>
      <h3>{weatherData.city}</h3>
      <p>Temperature: {weatherData.temperature}°C</p>
      <p>Weather: {weatherData.weather}</p>
      <p>Humidity: {weatherData.humidity}%</p>
      <p>Wind: {weatherData.wind_speed} km/h</p>
    </div>
  );
};

export default WeatherCard;
