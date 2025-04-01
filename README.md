# Solaris: Intelligent Energy Management System

A web-based application for optimizing solar energy usage in smart homes by predicting energy demand, monitoring weather conditions, and dynamically managing solar energy, battery storage, and grid usage.

## Features
- Real-time weather forecasts with irradiance calculation
- Automated energy usage recommendations
- Solar energy and battery metrics visualization
- Dynamic web interface with Flask
- OpenWeather API integration for weather data
- Modular API for irradiance and weather data retrieval
- User-friendly dashboards and reports

## Prerequisites
- Python 3.8+
- Flask
- Requests
- Node.js (npm)
- Chart.js

## Installation
1. Clone the repository:
    ```
    git clone https://github.com/vishwak05/solaris.git
    cd solaris
    ```
2. Create a virtual environment
    ```
    python -m venv venv
    venv/scripts/activate
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```
    python app.py
    ```
2. Access the Application
    Navigate to http://127.0.0.1:5000 in your browser to access the application

## OpenWeather API Usage
1. Obtain an API key from [OpenWeather](https://openweathermap.org/api).
2. Add your API key to the environment variables:
      Add it to a `.env` file:
      ```
      OPENWEATHER_API_KEY=your_api_key
      ```
3. Location used for this project: **Hyderabad, India**
    - Latitude: **17.375**
    - Longitude: **78.474**

**API Endpoint for Weather Data:**

```
GET /api/weather
```

**API Response Format:**

A 5-day Forecast of weather metrics with 3-hour increments.
```
[
  {
    "datetime": "2025-03-22 12:00:00",
    "temperature": 32.5,
    "humidity": 60,
    "wind_speed": 5.4,
    "precipitation": 0.0,
    "cloud_cover": 20,
    "theta_z": 30.5,
    "irradiance": 870.34
  },
  ...
]
```

## Pages
- **Home Page**: ```/``` 

    Overview and introduction to application.

- **Dashboard**: ```/dashboard```

    Visualize solar production, battery usage, and weather data metrics.

- **Reports**: ```/reports```
    
    Generate detailed reports for different time periods (day, week, month, year).

- **Forecasts**: ```/forecasts```

    Predict Day-ahead temperature and solar irradiance for better planning.

- **Status**: ```/status```

    Monitor the health and performance of solar panels and batteries.

## Structure of .env file
Create a ```.env``` file in ```/solaris/``` path

The Longitude and Latitude are by default set to **Hyderabad, India** (Lat=**17.375**, Log=**78.474**)
```
OPENWEATHER_API_KEY = your_api_key
LATITUDE = your_location_latitude
LONGITUDE = your_location_longitude
```

## Packages Used
- **axios**: For making HTTP requests (Node.js).
- **chart.js**: For making Graphs and Charts.
- **dotenv**: For managing environment variables.
- **express**: For creating the server.
- **requests**: For HTTP requests (Python).
- **flask**: For backend API.

## Contributing
1. Fork the repository.
2. Create a new branch:
    ```
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```
    git commit -m "Add feature-name"
    ```
4. Push to the branch:
    ```
    git push origin feature-name
    ```
5. Open a pull request.


## Acknowledgments
- [OpenWeather](https://openweathermap.org/) for their API.
- Contributors and the open-source community.
