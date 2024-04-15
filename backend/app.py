from flask import Flask, jsonify, send_file
from flask_cors import CORS

from utils.live_trains_utils import get_train_data
from utils import live_trains_utils, broadcast_utils
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing


# Route to get live trains for a specific station
@app.route('/live-trains/<station_shortcode>')
def get_live_trains(station_shortcode):
    live_trains_data = live_trains_utils.fetch_live_trains(station_shortcode)
    formatted_arriving_trains = format_live_trains_response(station_shortcode, live_trains_data['arriving'], 'arriving')
    formatted_departing_trains = format_live_trains_response(station_shortcode, live_trains_data['departing'])
    # Return the formatted data as JSON response
    return jsonify({'arriving': formatted_arriving_trains, 'departing': formatted_departing_trains})

@app.route('/single-announcement/<departure_date>/<int:train_number>/<departure_time>', methods=['GET'])
def get_single_announcement(departure_date, train_number, departure_time):
    print(
        f"Received request for single announcement with departure_date: {departure_date}, train_number: {train_number}, departure_time: {departure_time}")

    # Validate departure_date format
    try:
        datetime.strptime(departure_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid departure_date format.")
        return jsonify({'error': 'Invalid departure_date format. Use YYYY-MM-DD.'}), 400

    # Validate departure_time format
    try:
        datetime.strptime(departure_time, '%H:%M:%S')
    except ValueError:
        print("Invalid departure_time format.")
        return jsonify({'error': 'Invalid departure_time format. Use HH:MM:SS.'}), 400

    train_data = get_train_data(departure_date, train_number, departure_time)

    if not train_data:
        print("Train not found or timetable row not matching the specified departure_time")
        return jsonify({'error': 'Train not found or timetable row not matching the specified departure_time'}), 404

    print("Successfully fetched train data.")

    # Construct broadcast using the matched timetable row
    announcement_path = broadcast_utils.construct_broadcast(train_data)

    # Send the .wav file as a response
    return send_file(announcement_path, mimetype="audio/wav", as_attachment=True)

# Remove the scheduled_time and actual_time formatting from broadcast_utils
# The announcement_path construction in broadcast_utils should directly use the scheduledTime and actualTime from train_data



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
                    'Scheduled Time': first_station['scheduledTime'],
                    'Track Number': first_station.get('commercialTrack'),
                },
                {
                    'Station': target_station['stationShortCode'],
                    'Scheduled Time': target_station['scheduledTime'],
                    'Track Number': target_station.get('commercialTrack'),
                },
                {
                    'Station': last_station['stationShortCode'],
                    'Scheduled Time': last_station['scheduledTime'],
                    'Track Number': last_station.get('commercialTrack'),
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
                'Time Table Rows': sorted_time_table_rows,
                'Actual Time': target_station.get('actualTime'),
                'Difference in Minutes': target_station.get('differenceInMinutes')
            }

            formatted_trains.append(formatted_train)

    return formatted_trains


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # You may want to set debug=False for production
