from flask import Flask, render_template
from decision_maker import decision_making

app = Flask(__name__)

@app.route("/api/decisions")
def fetch_decisions():
    try:
        forecasted_data = decision_making()
        forecasted_data.reset_index(inplace=True)

        if 'time' in forecasted_data.columns:
            forecasted_data['time'] = forecasted_data['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        return forecasted_data.to_dict("records")
    except Exception as e:
        print(f"Error in fetch_decisions: {e}")
        return {}

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
