import os
import pandas as pd
from dotenv import load_dotenv
import requests_cache
from retry_requests import retry

def get_env_vars():
    """
    Loads latitude, longitude, and tilt from the env module.
    Raises an exception if any variable is missing.
    """
    try:
        # Load environment variables from .env file
        load_dotenv()
        lat = os.getenv('LATITUDE')
        lon = os.getenv('LONGITUDE')
        tilt = os.getenv('PANEL_TILT')

        if lat is None or lon is None or tilt is None:
            raise RuntimeError("Missing required environment variables: LAT, LON, or TILT.")

        return lat, lon, tilt
    
    except AttributeError as e:
        print(f"Error in getting environment variable:  {e}")
        raise RuntimeError(f"Missing required environment variable: {e}")

def fetch_weather_forecast():
    """
    Fetches weather forecast data from the Open-Meteo API,
    caches responses, and returns hourly forecast of 5 days.
    """
    lat, lon, tilt = get_env_vars()
    cache_dir = 'cache'
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, 'weather_forecast')
    cache_session = requests_cache.CachedSession(cache_path, expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

    forecast_api_url = (
        "https://api.open-meteo.com/v1/forecast"
    )
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,cloud_cover,wind_speed_10m,wind_direction_10m,is_day,shortwave_radiation,global_tilted_irradiance",
        "timezone": "Asia/Kolkata",
        "tilt": tilt
    }

    try:
        response = retry_session.get(forecast_api_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'hourly' not in data or 'time' not in data['hourly']:
            raise ValueError("API response missing required 'hourly' or 'time' fields.")
        
        return data['hourly']
        
    except Exception as e:
        print(f"Error fetching weather forecast: {e}")
        raise RuntimeError(f"Failed to fetch weather forecast: {e}")

def process_weather_forecast(weather_forecast):
    """
    Formats the weather forecast into DataFrame to predict energy_usage by ML model
    """
    try:
        forecast_df = pd.DataFrame(weather_forecast)
        forecast_df['time'] = pd.to_datetime(forecast_df['time'])
        forecast_df.set_index('time', inplace=True)

        forecast_df.rename(columns={
            'temperature_2m': 'temperature',
            'relative_humidity_2m': 'humidity',
            'precipitation_probability': 'precipitation_prob',
            'wind_speed_10m': 'wind_speed',
            'wind_direction_10m': 'wind_direction',
            'shortwave_radiation': 'GHI',
            'global_tilted_irradiance': 'GTI',
        }, inplace=True)

        return forecast_df
    
    except Exception as e:
        print(f"Error in processing weather forecast:  {e}")
        raise RuntimeError(f"Failed to convert weather dictionary to DataFrame: {e}")