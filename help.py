import json

file_path = 'stations.json'  # Replace 'stations.json' with the path to your JSON file

def count_passenger_traffic(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        array_count = 0
        for item in data:  # Iterate over the array
            if isinstance(item, dict):
                print(item)  # Debug print to check the structure of each item
                if item.get('passengerTraffic') == True:
                    array_count += 1
    return array_count

# Example usage:
num_passenger_traffic = count_passenger_traffic(file_path)
print("Number of objects with passenger traffic:", num_passenger_traffic)
