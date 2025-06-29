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
- Scikit-learn
- Requests
- Chart.js

## Installation
1. Clone the repository:
    ```
    git clone https://github.com/vishwak05/solaris.git
    cd solaris
    ```
2. Create a virtual environment:
    ```
    python -m venv venv
    ```

3. Activate the virtual environment:
    ```
    venv/scripts/activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Project Structure:
Create folders which are not present.
```
solaris/
├── datasets/                   # Datasets of Household energy consumption and weather data
├── ml_models/                  # Trained ML models
├── notebooks/                  # .ipynb notebooks for data processing and model building
├── solar_utils/                # Utils file for business logic
│   ├── weather_forecaster.py   # Fetchs weather forecast
│   ├── energy_predictor.py     # Predicts energy demand based on weather
│   └── battery_manager.py      # Battery module to replicate real battery
├── static/                     # Static elemets for web-page
│   ├── images/                 # Images for web-page
│   └── styles.css
├── templates/                  # Templates for web-page
├── decision_maker.py           # Creates decisions based on weather and demand
├── app.py                      # To run Flask server and access web-page
├── .env
├── README.md
└── requirements.txt
```

## Usage

1. Download "*Household Electric Power Consumption*" dataset by *"UCI Machine Learning"* from Kaggle:

    Dataset link: https://www.kaggle.com/datasets/uciml/electric-power-consumption-data-set
    
2. Place the dataset in `/datasets` directory within project folder:
    ```
    /solaris/datasets
    ```

3. Run the notebooks present in `notebooks/` folder:
    - Run `data_preprocessing.ipynb` to preprocess, perform Exploratory Data Analysis, and create .csv files of datasets.

    - Run `train_models.ipynb` to train the models using .csv files and save the model as `household_energy_model.pkl` in `ml_models/` folder.
    
    - Run `utils.ipynb` to emulate the functions of `solar_utils/` files for your own understanding (*Not required*).

4. Start the server:

    Start the flask server executing the command `flask run` or `python app.py` in terminal within project directory.

4. Access the Application:

    Navigate to http://127.0.0.1:5000 in your browser to access the application.

## Open-Meteo API Usage
1. Use the free APIs provided by open-meteo.com for archive and forecast data 

   Note: Use caching to prevent exhausting the request pool of API

2. Location used for this project: **Hyderabad, India**
    - Latitude: **17.375**
    - Longitude: **78.474**

## API Endpoints:

**API Endpoint for Decisions data:**
```
GET /api/decisions
```

**API Response Format:**

A 5-day hourly forecast of decisions.
```
[
  {
    "GHI": 0.0,
    "GTI": 0.0,
    "battery_capacity": 20.0,
    "battery_charge": 9.16,
    "battery_charge_cycles": 2.0,
    "battery_percentage": 45.8,
    "battery_status": "Discharging",
    "cloud_cover": 100,
    "decision": "battery",
    "energy_demand": 0.84,
    "humidity": 76,
    "is_day": 0,
    "precipitation": 0.0,
    "precipitation_prob": 0,
    "solar_output": 0.0,
    "solar_output_calc": 0.0,
    "temperature": 26.0,
    "time": "2025-06-29 00:00:00",
    "total_battery_charged": 0.0,
    "wind_direction": 240,
    "wind_speed": 12.1
  },...
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
Create a `.env` file in project root

The Longitude and Latitude are by default set to **Hyderabad, India** (Lat=**17.375**, Log=**78.474**)
```
# Location Details
LATITUDE = 17.375
LONGITUDE = 78.474
TIMEZONE = "Asia/Kolkata"

# Solar Panel Details
PANEL_CAPACITY = 4
PANEL_AREA = 20
PANEL_TYPE = "MonoCrystalline"
PANEL_EFFICIENCY = 0.18
PANEL_TILT = 15

# Battery Details
BATTERY_CAPACITY = 20.0
DEGRADATION_RATE = 0.002

```

## Packages Used
- **axios**: For making HTTP requests in JavaScript.
- **chart.js**: For making Graphs and Charts in JavaScript.
- **dotenv**: For managing environment variables.
- **pandas**: For data manipulation and analysis in Python.
- **matplotlib**: For creating visualizations in Python.
- **seaborn**: For statistical data visualization for correlation matrix.
- **scikit-learn**: For building and evaluating machine learning models in Python.
- **xgboost**: For high-performance gradient boosting machine learning models.
- **joblib**: For saving and loading ML models and handling large data efficiently.
- **flask**: For building web applications and RESTful APIs in Python.
- **requests_cache**: For caching HTTP requests using the requests library to improve performance.
- **retry_requests**: For adding retry logic to requests in case of network failures or timeouts.

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
- [Open-Meteo](https://open-meteo.com/) for their free Archive and Forecast API.
- Contributors and the open-source community.
