from flask import Flask, jsonify, send_file, request
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
    formatted_departing_trains = format_live_trains_response(station_shortcode, live_trains_data['departing'], "departing")
    # Return the formatted data as JSON response
    return jsonify({'arriving': formatted_arriving_trains, 'departing': formatted_departing_trains})


@app.route('/single-announcement/<date_object>/<int:train_number>/<station_shortcode>', methods=['GET'])
def get_single_announcement(date_object, train_number, station_shortcode):
    print(f"Received request for single announcement with dateandtime: {date_object}, train_number: {train_number}, station_shortcode: {station_shortcode}")

    # Validate dateandtime format
    try:
        # Parse dateandtime to datetime object
        dt_obj = datetime.strptime(date_object, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Extract date and time from datetime object
        departure_date = dt_obj.strftime('%Y-%m-%d')
        departure_time = dt_obj.strftime('%H:%M:%S')
    except ValueError:
        print("Invalid dateandtime format.")
        return jsonify({'error': 'Invalid dateandtime format. Use YYYY-MM-DDTHH:MM:SS.sssZ.'}), 400

    train_data = get_train_data(departure_date, train_number, departure_time, station_shortcode)

    if not train_data:
        print("Train not found or timetable row not matching the specified departure_time")
        return jsonify({'error': 'Train not found or timetable row not matching the specified departure_time'}), 404

    print("Successfully fetched train data.")

    # Construct broadcast using the matched timetable row
    announcement_path = broadcast_utils.construct_broadcast(train_data)

    # Send the .wav file as a response
    return send_file(announcement_path, mimetype="audio/wav", as_attachment=True, download_name=f"train_announcement.wav")



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
