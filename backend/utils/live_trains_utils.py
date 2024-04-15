import pytz
import requests
import json
import time
from datetime import datetime


def format_time(utc_time):
    # Convert UTC time to datetime object
    utc_datetime = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%S.%fZ')

    # Convert to local time (assuming Helsinki timezone for Finnish trains)
    local_tz = pytz.timezone('Europe/Helsinki')
    local_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(local_tz)

    # Format the local time
    return local_datetime.strftime('%Y-%m-%d %H:%M:%S')


# Function to fetch live train information for a given station
def fetch_live_trains(station_shortcode, arriving_trains=200, departing_trains=200):
    url_arriving = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station_shortcode}?arriving_trains={arriving_trains}&include_nonstopping=false&train_categories=Commuter,Long-distance"
    url_departing = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station_shortcode}?departing_trains={departing_trains}&include_nonstopping=false&train_categories=Commuter,Long-distance"

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


def get_train_data(departure_date, train_number, departure_time):
    url = f"https://rata.digitraffic.fi/api/v1/trains/{departure_date}/{train_number}?include_deleted=false&version=0"

    try:
        response = requests.get(url)
        response.raise_for_status()
        train_data_list = response.json()

        # Check if train data is found and not empty
        if not train_data_list or not isinstance(train_data_list, list):
            print("No train data found or train_data_list is not a list")
            return None
        print("in live trains utils")

        # Convert departure_time to the expected UTC format
        departure_time_utc = f"{departure_date}T{departure_time}.000Z"


        # Search through all train data for a matching timetable row
        for train_data in train_data_list:
            matching_row = next((row for row in train_data.get('timeTableRows', [])
                                 if row.get('scheduledTime', '').startswith(departure_time_utc)),
                                None)

            formatted_departure_time = format_time(departure_time_utc)

            print(f"Checking train number {train_number}, scheduled time {formatted_departure_time}...")

            # Log rows for debugging
            print(f"Rows for train number {train_number}:")
            for row in train_data.get('timeTableRows', []):
                formatted_time = format_time(row.get('scheduledTime', ''))
                print(f"Scheduled Time: {formatted_time}, Actual Time: {format_time(row.get('actualTime', ''))}")

            if matching_row:
                # Construct a new train data dictionary with only the matching timetable row
                train_data['timeTableRows'] = [matching_row]
                return train_data

        print("No matching timetable row found")
        return None

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
