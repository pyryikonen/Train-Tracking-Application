import json

input_file_path = 'stations.json'
output_file_path = 'passenger_traffic_stations.json'

def remove_asema(station_name):
    return station_name.replace("asema", "").strip()

def filter_passenger_traffic(input_file_path, output_file_path):
    passenger_traffic_stations = []
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            if isinstance(item, dict) and item.get('passengerTraffic') == True:
                filtered_item = {
                    "passengerTraffic": item.get("passengerTraffic"),
                    "longitude": item.get("longitude"),
                    "latitude": item.get("latitude"),
                    "stationShortCode": item.get("stationShortCode"),
                    "stationName": remove_asema(item.get("stationName"))
                }
                passenger_traffic_stations.append(filtered_item)
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(passenger_traffic_stations, outfile, indent=4, ensure_ascii=False)

# Example usage:
filter_passenger_traffic(input_file_path, output_file_path)
