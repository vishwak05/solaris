import joblib

# Set up a cache directory for predictions
memory = joblib.Memory(location='cache/energy_predictions', verbose=0)

@memory.cache
def predict_energy_usage(weather_forecast):
    """
    Predicts energy usage based on weather forecast data with ML model.
    """
    try:
        model = joblib.load("C:/Users/vishw/Projects/Solaris/ml_models/household_energy_model.pkl")

        predictions = model.predict(weather_forecast)

        return predictions
    
    except Exception as e:
        print(f"Error in predicting energy demand:  {e}")
        raise RuntimeError(f"Failed to predict energy usage: {e}")

def fetch_energy_predictions(weather_forecast):
    """
    Fetchs the energy predictions made by ML model from forecast weather and combines into single DataFrame
    """
    try:
        prediction_df = weather_forecast[['temperature', 'humidity', 'precipitation', 'cloud_cover', 'is_day']].copy()
        
        predictions = predict_energy_usage(prediction_df)

        weather_forecast['energy_demand'] = predictions
        weather_forecast['energy_demand'] = weather_forecast['energy_demand'].astype('float64').round(2)

        return weather_forecast
    
    except Exception as e:
        print(f"Error in generating energy predictions:  {e}")
        raise RuntimeError(f"Failed to fetch energy predictions and merge forecast weather")