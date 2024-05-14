import requests
import json
import time

headers = {'Digitraffic-User': 'TamkOpiskelijat/junakuulutukset 1.0'}


def fetch_live_trains(station_shortcode, arriving_trains=200, departing_trains=200):
    """
       Fetches live train information for a given station.

       Parameters:
       - station_shortcode (str): The shortcode of the station.
       - arriving_trains (int): Number of arriving trains to fetch (default is 200).
       - departing_trains (int): Number of departing trains to fetch (default is 200).

       Returns:
       - dict: A dictionary containing live train data for arriving and departing trains.
       """
    url_arriving = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station_shortcode}?arriving_trains={arriving_trains}&include_nonstopping=false&train_categories=Commuter,Long-distance"
    url_departing = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station_shortcode}?departing_trains={departing_trains}&include_nonstopping=false&train_categories=Commuter,Long-distance"

    try:
        response_arriving = requests.get(url_arriving, headers=headers)
        response_departing = requests.get(url_departing, headers=headers)

        response_arriving.raise_for_status()
        response_departing.raise_for_status()

        arriving_trains = response_arriving.json()
        departing_trains = response_departing.json()

        return {'arriving': arriving_trains, 'departing': departing_trains}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching live trains for station {station_shortcode}: {e}")
        return {'arriving': [], 'departing': []}


def get_train_data(departure_date, train_number, departure_time, station_shortcode):
    """
       Retrieves train data based on departure date, train number, and departure time.

       Parameters:
       - departure_date (str): The departure date in 'YYYY-MM-DD' format.
       - train_number (int): The train number.
       - departure_time (str): The departure time in 'HH:MM:SS' format.
       - station_shortcode (str): The shortcode of the station.

       Returns:
       - list: A list of dictionaries containing train data.
       """
    # Convert departure_time to the expected UTC format
    # YYYY-MM-DDTHH:MM:SS.sssZ
    departure_time_utc = f"{departure_date}T{departure_time}.000Z"

    url = f"https://rata.digitraffic.fi/api/v1/trains/{departure_date}/{train_number}?include_deleted=false&version=0"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        train_data_list = response.json()

        if not train_data_list or not isinstance(train_data_list, list):
            print("No train data found or train_data_list is not a list")
            return None

        formatted_trains = []

        # Search through all train data for a matching timetable row
        for train_data in train_data_list:
            matching_row = next((row for row in train_data.get('timeTableRows', [])
                                 if row.get('scheduledTime', '').startswith(departure_time_utc)),
                                None)

            print(f"Checking train number {train_number}, scheduled time {departure_time_utc}...")

            if matching_row:
                target_station = next((row for row in train_data.get('timeTableRows', [])
                                       if row.get('stationShortCode') == station_shortcode),
                                      None)

                if target_station:
                    # Create a list of stations containing only the first, target, and last stations
                    time_table_rows = [
                        {
                            'Station': train_data['timeTableRows'][0]['stationShortCode'],
                            'Scheduled Time': train_data['timeTableRows'][0]['scheduledTime'],
                            'Track Number': train_data['timeTableRows'][0].get('commercialTrack'),
                        },
                        {
                            'Station': target_station['stationShortCode'],
                            'Scheduled Time': target_station['scheduledTime'],
                            'Track Number': target_station.get('commercialTrack'),
                        },
                        {
                            'Station': train_data['timeTableRows'][-1]['stationShortCode'],
                            'Scheduled Time': train_data['timeTableRows'][-1]['scheduledTime'],
                            'Track Number': train_data['timeTableRows'][-1].get('commercialTrack'),
                        }
                    ]

                    # Sort the timetable rows by scheduled time
                    sorted_time_table_rows = sorted(time_table_rows, key=lambda x: x['Scheduled Time'])

                    formatted_train = {
                        'Station': station_shortcode,
                        'Train Number': train_data['trainNumber'],
                        'Departure Date': train_data['departureDate'],
                        'Operator': train_data['operatorShortCode'],
                        'Train Type': train_data.get('trainType', 'Unknown'),
                        'Time Table Rows': sorted_time_table_rows,
                        'Actual Time': target_station.get('actualTime'),
                        'Difference in Minutes': target_station.get('differenceInMinutes')
                    }

                    formatted_trains.append(formatted_train)

        return formatted_trains if formatted_trains else None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching train data for train number {train_number} on departure date {departure_date}: {e}")
        return None


# Function to fetch live train information periodically
def fetch_live_trains_periodically():
    while True:
        for station_shortcode in major_stations:
            try:
                live_trains_cache[station_shortcode] = fetch_live_trains(station_shortcode)
            except requests.HTTPError as e:
                if e.response.status_code == 429:  # Rate limit exceeded
                    # Wait for an increasingly longer period before retrying
                    sleep_duration = 2 ** (int(e.response.headers.get('Retry-After', 5)) + 1)
                    print(f"Rate limit exceeded. Retrying in {sleep_duration} seconds.")
                    time.sleep(sleep_duration)
                else:
                    print(f"Error fetching live trains for station {station_shortcode}: {e}")
            time.sleep(1)  # Sleep between individual requests
        time.sleep(10)  # Sleep between iterations


if __name__ == "__main__":
    # Read station information from stations.json file
    with open('passenger_traffic_stations.json', 'r', encoding='utf-8') as file:
        stations_data = json.load(file)

    # Extract station shortcodes
    major_stations = [station['stationShortCode'] for station in stations_data]

    # Initialize live trains cache
    live_trains_cache = {}

    fetch_live_trains_periodically()
