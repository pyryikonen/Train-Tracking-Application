import requests
import json
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Read station information from stations.json file
with open('passenger_traffic_stations.json', 'r', encoding='utf-8') as file:
    stations_data = json.load(file)

# Extract station shortcodes
major_stations = [station['stationShortCode'] for station in stations_data]


# Function to fetch live train information for a given station
def fetch_live_trains(station_shortcode, minutes_before_departure=15, minutes_after_departure=15,
                      minutes_before_arrival=15, minutes_after_arrival=15, arrived_trains=5, departing_trains=5):
    url_arriving = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station_shortcode}?arriving_trains={arrived_trains}&minutes_before_arrival={minutes_before_arrival}&minutes_after_arrival={minutes_after_arrival}"
    url_departing = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station_shortcode}?departing_trains={departing_trains}&minutes_before_departure={minutes_before_departure}&minutes_after_departure={minutes_after_departure}"

    try:
        response_arriving = requests.get(url_arriving)
        response_departing = requests.get(url_departing)

        response_arriving.raise_for_status()
        response_departing.raise_for_status()

        arriving_trains = response_arriving.json()
        departing_trains = response_departing.json()

        return {'arriving': arriving_trains, 'departing': departing_trains}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching live trains for station {station_shortcode}: {e}")
        return {'arriving': [], 'departing': []}


# Function to format live train information response
def format_live_trains_response(station_shortcode, live_trains, direction):
    formatted_trains = []

    for train in live_trains:
        formatted_train = {
            'Station': station_shortcode,
            'Direction': direction,
            'Train Number': train['trainNumber'],
            'Departure Date': train['departureDate'],
            'Operator': train['operatorShortCode'],
            'Train Type': train['trainType'],
            'Time Table Rows': [],
            'Actual Time': None,  # Add actualTime field
            'Difference in Minutes': None  # Add differenceInMinutes field
        }

        for row in train['timeTableRows']:
            formatted_row = {
                'Station': row['stationShortCode'],
                'Scheduled Time': row['scheduledTime']
            }
            formatted_train['Time Table Rows'].append(formatted_row)

            if row.get('actualTime') is not None:
                formatted_train['Actual Time'] = row['actualTime']
                formatted_train['Difference in Minutes'] = row['differenceInMinutes']

        formatted_trains.append(formatted_train)

    return formatted_trains



live_trains_cache = {}


# Function to fetch live trains periodically
def fetch_live_trains_periodically():
    global live_trains_cache
    while True:
        for station_shortcode in major_stations:
            live_trains_cache[station_shortcode] = fetch_live_trains(station_shortcode)
        time.sleep(900)  # 900 seconds = 15 minutes


# Route to get live trains for a specific station
@app.route('/live-trains/<station_shortcode>')
def get_live_trains(station_shortcode):
    global live_trains_cache
    if station_shortcode in live_trains_cache:
        arriving_trains = live_trains_cache[station_shortcode]['arriving']
        departing_trains = live_trains_cache[station_shortcode]['departing']

        formatted_arriving_trains = format_live_trains_response(station_shortcode, arriving_trains, 'arriving')
        formatted_departing_trains = format_live_trains_response(station_shortcode, departing_trains, 'departing')

        return jsonify({'arriving': formatted_arriving_trains, 'departing': formatted_departing_trains, })
    else:
        return jsonify({"error": "Station not found"}), 404


if __name__ == '__main__':
    # Start a separate thread to fetch live trains periodically
    fetch_thread = threading.Thread(target=fetch_live_trains_periodically)
    fetch_thread.daemon = True
    fetch_thread.start()

    # Run Flask app
    app.run(debug=True, port=5001)  # You may want to set debug=False for production
