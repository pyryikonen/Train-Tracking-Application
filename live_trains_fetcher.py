import requests
import json
import time


# Function to fetch live train information for a given station
def fetch_live_trains(station_shortcode, arriving_trains=200, departing_trains=200):
    url_arriving = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station_shortcode}?arriving_trains={arriving_trains}&include_nonstopping=false&train_categories=Commuter,Long-distance"
    url_departing = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station_shortcode}?arriving_trains={departing_trains}&include_nonstopping=false&train_categories=Commuter,Long-distance"

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


# Function to fetch live train information periodically
def fetch_live_trains_periodically():
    while True:
        for station_shortcode in major_stations:
            try:
                print("fetching trains to live cache")
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
