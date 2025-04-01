from flask import Flask, render_template, request, jsonify
import requests
import datetime
import math, os
from dotenv import load_dotenv

load_dotenv()

# OpenWeather API Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
LAT = float(os.getenv("LATITUDE", 17.375))  # Default to Hyderabad if not set
LON = float(os.getenv("LONGITUDE", 78.474))

app = Flask(__name__)

# Constants
I0 = 1367  # Extraterrestrial Solar Radiation (W/m²)

# Function to calculate solar zenith angle
def solar_zenith_angle(lat, lon, timestamp):
    """
    Calculate Solar Zenith Angle (SZA) for a given timestamp and location.
    """
    # Convert timestamp to UTC
    dt = datetime.datetime.fromtimestamp(timestamp)

    # Approximate day of the year
    day_of_year = dt.timetuple().tm_yday

    # Solar declination angle (δ) in radians
    declination = 23.45 * math.sin(math.radians((360/365) * (day_of_year - 81)))

    # Hour angle (H) in degrees
    hour_angle = (dt.hour - 12) * 15  # 15 degrees per hour

    # Solar zenith angle (SZA) calculation
    lat_rad = math.radians(lat)
    decl_rad = math.radians(declination)
    hour_rad = math.radians(hour_angle)

    cos_theta_z = math.sin(lat_rad) * math.sin(decl_rad) + math.cos(lat_rad) * math.cos(decl_rad) * math.cos(hour_rad)
    theta_z = math.degrees(math.acos(max(min(cos_theta_z, 1), -1)))

    return theta_z

# API Endpoint for Irradiance Calculation
@app.route("/api/weather", methods=["GET"])
def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data"}), 500
    
    data = response.json()
    weather = []
    for forecast in data['list']:
        timestamp = forecast['dt']
        temp = forecast["main"]["temp"]
        humidity = forecast["main"]["humidity"]
        wind_speed = forecast["wind"]["speed"]
        precipitation = forecast.get("rain", {}).get("3h", 0)  # Rain in last 3 hours (default 0)
        cloud_cover = forecast['clouds']['all']
        theta_z = solar_zenith_angle(LAT, LON, timestamp)
        GHI_0 = I0 * max(0, math.cos(math.radians(theta_z)))
        GHI = GHI_0 * (1 - 0.75 * (cloud_cover / 100) ** 3)
        weather.append({
            "datetime": datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            "temperature": temp,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "precipitation": precipitation,
            "cloud_cover": cloud_cover,
            "theta_z": theta_z,
            "irradiance": GHI
        })
    return jsonify(weather)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Dashboard Page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Reports Page
@app.route("/reports")
def reports():
    return render_template("reports.html")

# Forecasts Page
@app.route("/forecasts")
def forecasts():
    return render_template("forecasts.html");

# Status Page
@app.route("/status")
def status():
    return render_template("status.html")

if __name__ == "__main__":
    app.run(debug=True)
