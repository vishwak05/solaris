import os
import json
import pandas as pd
from dotenv import load_dotenv
from solar_utils import weather_forecaster, energy_predictor, battery_manager

def load_battery_state(file_path='cache/battery_state.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            battery_data = json.load(f)
        return battery_data
    else:
        return None  # Or defaults

def save_battery_state(battery, file_path='cache/battery_state.json'):
    battery_data = {
        'battery_capacity': battery.capacity,
        'battery_charge': battery.current_charge,
        'battery_percentage': (battery.current_charge / battery.capacity) * 100,
        'battery_charge_cycles': battery.charge_cycles,
        'total_battery_charged': battery.total_charged
    }
    with open(file_path, 'w') as f:
        json.dump(battery_data, f, indent=4)

def decision_making(testing = False):
    '''
    Make a decision on energy source selection and battery decision
    '''
    try:
        load_dotenv()
        panel_capacity = float(os.getenv('PANEL_CAPACITY'))
        panel_area = float(os.getenv('PANEL_AREA'))
        panel_efficiency = float(os.getenv('PANEL_EFFICIENCY'))
        panel_tilt = float(os.getenv('PANEL_TILT'))
        battery_capacity = float(os.getenv('BATTERY_CAPACITY'))
        battery_degradation_rate = float(os.getenv('DEGRADATION_RATE'))

        if testing:
            forecast_df = pd.read_csv("C:/Users/vishw/Projects/Solaris/datasets/weather_data.csv")
        else:
            weather_forecast = weather_forecaster.fetch_weather_forecast()
            forecast_df = weather_forecaster.process_weather_forecast(weather_forecast)
        
        forecast_data = energy_predictor.fetch_energy_predictions(forecast_df)
        
        # Calculate solar output (capped at panel capacity)
        forecast_data['solar_output_calc'] = (forecast_data['GTI'] * panel_efficiency * panel_area) / 1000
        forecast_data['solar_output'] = round(forecast_data[['solar_output_calc']].clip(upper=panel_capacity), 2)

        battery_state = load_battery_state()

        if battery_state:
            battery = battery_manager.BatteryModule(
                capacity=battery_state['battery_capacity'],
                degradation_rate=battery_degradation_rate,
                current_charge=battery_state['battery_charge'],
                charge_cycles=battery_state['battery_charge_cycles'],
                total_charged=battery_state['total_battery_charged']
            )
        else:
            battery = battery_manager.BatteryModule(battery_capacity, battery_degradation_rate)

        energy_demand = forecast_data['energy_demand'].iloc[0]
        solar_output = forecast_data['solar_output'].iloc[0]

        decisions = []
        battery_curr_capacity = []
        battery_levels = []
        battery_percentages = []
        battery_status = []
        battery_charge_rates = []
        battery_total_charged = []

         # Loop over each row of forecast data
        for _, row in forecast_data.iterrows():
            energy_demand = row['energy_demand']
            solar_output = row['solar_output']

            if energy_demand <= solar_output:
                # Use solar energy, charge battery with surplus
                decisions.append('solar')
                surplus_energy = solar_output - energy_demand
                if surplus_energy > battery.max_charge_rate:
                    battery.charge(battery.max_charge_rate)
                else:
                    battery.charge(surplus_energy)
                battery_status.append('Charging')

            elif battery.current_charge >= (energy_demand - solar_output):
                # Use battery to meet the remaining demand
                decisions.append('battery')
                if (energy_demand - solar_output) > battery.max_discharge_rate:
                    battery.discharge(battery.max_discharge_rate)
                else:
                    battery.discharge(energy_demand - solar_output)
                battery_status.append('Discharging')

            else:
                # Use grid if solar + battery cannot meet demand
                decisions.append('grid')
                battery_status.append('Idle')

            # Record battery state
            battery_curr_capacity.append(round(battery.capacity,2))
            battery_levels.append(round(battery.current_charge,2))
            battery_percentages.append(round(battery.battery_percentage,2))
            battery_charge_rates.append(round(battery.charge_cycles,2))
            battery_total_charged.append(round(battery.total_charged,2))

        # Add new columns to DataFrame
        forecast_data['decision'] = decisions
        forecast_data['battery_capacity'] = battery_curr_capacity
        forecast_data['battery_charge'] = battery_levels
        forecast_data['battery_percentage'] = battery_percentages
        forecast_data['battery_status'] = battery_status
        forecast_data['battery_charge_cycles'] = battery_charge_rates
        forecast_data['total_battery_charged'] = battery_total_charged

        return forecast_data  # Optional: return for further use

    except Exception as e:
        print("Error making decision of energy source", {e})
        raise RuntimeError(f"Failed to make a decision at energy source selection: {e}")