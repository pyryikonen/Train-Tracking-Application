from flask import Flask, jsonify, send_file
from flask_cors import CORS

from utils.live_trains_utils import get_train_data
from utils import live_trains_utils, broadcast_utils
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

announcement_path = None


@app.route('/live-trains/<station_shortcode>')
def get_live_trains(station_shortcode):
    """
        Retrieves live train data for a specific station.

        Parameters:
        - station_shortcode (str): The shortcode of the station.

        Returns:
        - dict: A dictionary containing live train data for arriving and departing trains.
        """
    live_trains_data = live_trains_utils.fetch_live_trains(station_shortcode)
    formatted_arriving_trains = format_live_trains_response(station_shortcode, live_trains_data['arriving'], 'arriving')
    formatted_departing_trains = format_live_trains_response(station_shortcode, live_trains_data['departing'],
                                                             "departing")
    # Return the formatted data as JSON response
    return jsonify({'arriving': formatted_arriving_trains, 'departing': formatted_departing_trains})


@app.route('/arrival-announcement/<date_object>/<int:train_number>/<station_shortcode>', methods=['GET'])
def get_arrival_announcement(date_object, train_number, station_shortcode):
    """
     Retrieves the audio announcement for a train arrival.

     Parameters:
     - date_object (str): The date and time of the announcement in ISO format.
     - train_number (int): The train number.
     - station_shortcode (str): The shortcode of the station.

     Returns:
     - file: An audio file containing the announcement.
     """
    return get_announcement(date_object, train_number, station_shortcode, 'arrival')


@app.route('/departure-announcement/<date_object>/<int:train_number>/<station_shortcode>', methods=['GET'])
def get_departure_announcement(date_object, train_number, station_shortcode):
    """
    Retrieves the audio announcement for a train departure.

    Parameters:
    - date_object (str): The date and time of the announcement in ISO format.
    - train_number (int): The train number.
    - station_shortcode (str): The shortcode of the station.

    Returns:
    - file: An audio file containing the announcement.
    """
    return get_announcement(date_object, train_number, station_shortcode, 'departure')


def get_announcement(date_object, train_number, station_shortcode, announcement_type):
    """
    Retrieves an audio announcement for train arrival or departure.

    Parameters:
    - date_object (str): The date and time of the announcement in ISO format.
    - train_number (int): The train number.
    - station_shortcode (str): The shortcode of the station.
    - announcement_type (str): The type of announcement ('arrival' or 'departure').

    Returns:
    - file: An audio file containing the announcement.
    """
    global announcement_path

    # Validate date_object format
    try:
        dt_obj = datetime.strptime(date_object, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Extract date and time from datetime object
        announcement_date = dt_obj.strftime('%Y-%m-%d')
        announcement_time = dt_obj.strftime('%H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid date_object format. Use YYYY-MM-DDTHH:MM:SS.sssZ.'}), 400

    if announcement_type == 'arrival':
        train_data = get_train_data(announcement_date, train_number, announcement_time, station_shortcode)
    elif announcement_type == 'departure':
        train_data = get_train_data(announcement_date, train_number, announcement_time, station_shortcode)
    else:
        return jsonify({'error': 'Invalid announcement_type. Use either "arrival" or "departure".'}), 400

    if not train_data:
        return jsonify({'error': 'Train not found or timetable row not matching the specified departure_time'}), 404

    # Construct broadcast using the matched timetable row
    if announcement_type == 'arrival':
        announcement_path = broadcast_utils.construct_arrival_broadcast(train_data)
    elif announcement_type == 'departure':
        announcement_path = broadcast_utils.construct_departure_broadcast(train_data)

    return send_file(announcement_path, mimetype="audio/wav", as_attachment=True,
                     download_name=f"{announcement_type}_train_announcement.wav")


def format_live_trains_response(station_shortcode, live_trains, direction):
    """
    Formats live train data into a structured response.

    Parameters:
    - station_shortcode (str): The shortcode of the station.
    - live_trains (list): A list of live train data.
    - direction (str): The direction of trains ('arriving' or 'departing').

    Returns:
    - list: A list of dictionaries containing formatted live train data.
    """
    formatted_trains = []

    for train in live_trains:
        target_station = [row for row in train['timeTableRows'] if row.get('stationShortCode') == station_shortcode]
        if target_station:  # Check if target_station list is not empty
            target_station = target_station[0]  # Take the first matching station

            # Get the first and last stations
            first_station = train['timeTableRows'][0]
            last_station = train['timeTableRows'][-1]

            # Create a list of stations containing only the first, target, and last stations
            # Target station is the station that the user selects in the ui to listen
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
