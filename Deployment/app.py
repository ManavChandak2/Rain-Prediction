from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

# Using raw strings to specify the file path
file_path = r"E:\Rain Prediction\Code\rain_XGBnew_model.pkl"

# Load the model from the file
with open(file_path, 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__, template_folder="template")

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == "POST":
        try:
            # DATE
            date = request.form['date']
            day = float(pd.to_datetime(date, format="%Y-%m-%d").day)
            month = float(pd.to_datetime(date, format="%Y-%m-%d").month)
            
            # MinTemp
            minTemp = float(request.form['mintemp'])
            # MaxTemp
            maxTemp = float(request.form['maxtemp'])
            # Rainfall
            rainfall = float(request.form['rainfall'])
            # Evaporation
            evaporation = float(request.form['evaporation'])
            # Sunshine
            sunshine = float(request.form['sunshine'])
            # Wind Gust Speed
            windGustSpeed = float(request.form['windgustspeed'])
            # Wind Speed 9am
            windSpeed9am = float(request.form['windspeed9am'])
            # Wind Speed 3pm
            windSpeed3pm = float(request.form['windspeed3pm'])
            # Humidity 9am
            humidity9am = float(request.form['humidity9am'])
            # Humidity 3pm
            humidity3pm = float(request.form['humidity3pm'])
            # Pressure 9am
            pressure9am = float(request.form['pressure9am'])
            # Pressure 3pm
            pressure3pm = float(request.form['pressure3pm'])
            # Temperature 9am
            temp9am = float(request.form['temp9am'])
            # Temperature 3pm
            temp3pm = float(request.form['temp3pm'])
            # Cloud 9am
            cloud9am = float(request.form['cloud9am'])
            # Cloud 3pm
            cloud3pm = float(request.form['cloud3pm'])
            # Location
            location = request.form['location']
            location_map = {
                'Portland': 1, 'Cairns': 2, 'Walpole': 3, 'Dartmoor': 4, 'MountGambier': 5, 'NorfolkIsland': 6,
                'Albany': 7, 'Witchcliffe': 8, 'CoffsHarbour': 9, 'Sydney': 10, 'Darwin': 11, 'MountGinini': 12,
                'NorahHead': 13, 'Ballarat': 14, 'GoldCoast': 15, 'SydneyAirport': 16, 'Hobart': 17, 'Watsonia': 18,
                'Newcastle': 19, 'Wollongong': 20, 'Brisbane': 21, 'Williamtown': 22, 'Launceston': 23, 'Adelaide': 24,
                'MelbourneAirport': 25, 'Perth': 26, 'Sale': 27, 'Melbourne': 28, 'Canberra': 29, 'Albury': 30,
                'Penrith': 31, 'Nuriootpa': 32, 'BadgerysCreek': 33, 'Tuggeranong': 34, 'PerthAirport': 35,
                'Bendigo': 36, 'Richmond': 37, 'WaggaWagga': 38, 'Townsville': 39, 'PearceRAAF': 40, 'SalmonGums': 41,
                'Moree': 42, 'Cobar': 43, 'Mildura': 44, 'Katherine': 45, 'AliceSprings': 46, 'Nhil': 47, 'Woomera': 48,
                'Uluru': 49
            }
            location = location_map.get(location, 0)  # Default to 0 if not found
            # Wind Dir 9am
            windDir9am = request.form['winddir9am']
            windDir_map = {
                'NNW': 0, 'N': 1, 'NW': 2, 'NNE': 3, 'WNW': 4, 'W': 5, 'WSW': 6, 'SW': 7,
                'SSW': 8, 'NE': 9, 'S': 10, 'SSE': 11, 'ENE': 12, 'SE': 13, 'ESE': 14, 'E': 15
            }
            windDir9am = windDir_map.get(windDir9am, 0)
            # Wind Dir 3pm
            windDir3pm = request.form['winddir3pm']
            windDir3pm = windDir_map.get(windDir3pm, 0)
            # Wind Gust Dir
            windGustDir = request.form['windgustdir']
            windGustDir = windDir_map.get(windGustDir, 0)
            # Rain Today
            rainToday = request.form['raintoday']
            rainToday = 1 if rainToday == 'Yes' else 0

            input_lst = [[location, minTemp, maxTemp, rainfall, evaporation, sunshine, windGustDir, windGustSpeed,
                          windDir9am, windDir3pm, windSpeed9am, windSpeed3pm, humidity9am, humidity3pm, pressure9am,
                          pressure3pm, cloud9am, cloud3pm, temp9am, temp3pm, rainToday, month, day]]
            pred = model.predict(input_lst)

            # Provide a valid response
            if pred == 1:
                     return render_template('after_rainy.html')
            else:
                return render_template('after_sunny.html')

        except Exception as e:
            return jsonify({"error": str(e)})

# Ensure the Flask app runs
if __name__ == "__main__":
    app.run(debug=True)
