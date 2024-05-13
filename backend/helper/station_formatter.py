import json

input_file_path = '../stations.json'
output_file_path = '../passenger_traffic_stations_2.json'


def remove_station(station_name):
    """
     Removes the word 'asema' from a station name and strips any leading or trailing whitespace.

     Parameters:
     - station_name (str): The name of the station.

     Returns:
     - str: The station name without the word 'asema' and stripped of leading and trailing whitespace.
     """
    return station_name.replace("asema", "").strip()


def filter_passenger_traffic(input_file_path, output_file_path):
    """
    Filters stations from an input JSON file based on passenger traffic and saves the result to an output file.

    Parameters:
    - input_file_path (str): The path to the input JSON file containing station data.
    - output_file_path (str): The path to save the filtered station data.

    Returns:
    - None
    """
    passenger_traffic_stations = []
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            if isinstance(item, dict) and item.get('passengerTraffic') == True:
                filtered_item = {
                    "stationShortCode": item.get("stationShortCode"),
                    "stationName": remove_station(item.get("stationName"))
                }
                passenger_traffic_stations.append(filtered_item)
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(passenger_traffic_stations, outfile, indent=4, ensure_ascii=False)
