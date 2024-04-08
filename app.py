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
    formatted_departing_trains = format_live_trains_response(station_shortcode, live_trains_data['departing'],
                                                             'departing')

    # Return the formatted data as JSON response
    return jsonify({'arriving': formatted_arriving_trains, 'departing': formatted_departing_trains})


def format_live_trains_response(station_shortcode, live_trains, direction):
    formatted_trains = []

    for train in live_trains:
        target_station = [row for row in train['timeTableRows'] if row.get('stationShortCode') == station_shortcode]
        if target_station:  # Check if target_station list is not empty
            target_station = target_station[0]  # Take the first matching station

            # Get the first and last stations
            first_station = train['timeTableRows'][0]
            last_station = train['timeTableRows'][-1]

            # Create a list of stations containing only the first, target, and last stations
            time_table_rows = [
                {
                    'Station': first_station['stationShortCode'],
                    'Scheduled Time': first_station['scheduledTime']
                },
                {
                    'Station': target_station['stationShortCode'],
                    'Scheduled Time': target_station['scheduledTime']
                },
                {
                    'Station': last_station['stationShortCode'],
                    'Scheduled Time': last_station['scheduledTime']
                }
            ]

            # Sort the timetable rows by scheduled time
            sorted_time_table_rows = sorted(time_table_rows, key=lambda x: x['Scheduled Time'])

            formatted_train = {
                'Station': station_shortcode,
                'Direction': direction,
                'Train Number': train['trainNumber'],
                'Departure Date': train['departureDate'],
                'Operator': train['operatorShortCode'],
                'Train Type': train['trainType'],
                'Track Number': train.get('commercialTrack'),
                'Time Table Rows': sorted_time_table_rows,
                'Actual Time': target_station.get('actualTime'),
                'Difference in Minutes': target_station.get('differenceInMinutes')
            }

            formatted_trains.append(formatted_train)

    return formatted_trains


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # You may want to set debug=False for production
