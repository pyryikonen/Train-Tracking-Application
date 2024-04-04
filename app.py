from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import live_trains_fetcher  # Import the fetch_live_trains function from live_trains_fetcher.py

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Route to get live trains for a specific station
@app.route('/live-trains/<station_shortcode>')
def get_live_trains(station_shortcode):
    # Fetch live train data for the specified station
    live_trains_data = live_trains_fetcher.fetch_live_trains(station_shortcode)

    # Format the live train data
    formatted_arriving_trains = format_live_trains_response(station_shortcode, live_trains_data['arriving'], 'arriving')
    formatted_departing_trains = format_live_trains_response(station_shortcode, live_trains_data['departing'], 'departing')

    # Return the formatted data as JSON response
    return jsonify({'arriving': formatted_arriving_trains, 'departing': formatted_departing_trains})

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

        # Get the first and last stations
        first_station = train['timeTableRows'][0]
        last_station = train['timeTableRows'][-1]

        formatted_row_first = {
            'Station': first_station['stationShortCode'],
            'Scheduled Time': first_station['scheduledTime']
        }

        formatted_row_last = {
            'Station': last_station['stationShortCode'],
            'Scheduled Time': last_station['scheduledTime']
        }

        formatted_train['Time Table Rows'].append(formatted_row_first)
        formatted_train['Time Table Rows'].append(formatted_row_last)

        if last_station.get('actualTime') is not None:
            formatted_train['Actual Time'] = last_station['actualTime']
            formatted_train['Difference in Minutes'] = last_station['differenceInMinutes']

        formatted_trains.append(formatted_train)

    return formatted_trains

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # You may want to set debug=False for production
