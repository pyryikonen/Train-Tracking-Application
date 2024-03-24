import requests

# Define the base URL of the API
base_url = 'https://rata.digitraffic.fi/api/v1'

# Define the endpoint for retrieving information about arriving and departing trains
endpoint = '/live-trains/station/'

# Define the station shortcode
station_shortcode = 'HKI'  # Example: Helsinki station

# Define parameters for the API call
params = {
    'arrived_trains': 1,         # Maximum number of arrived trains to retrieve
    'arriving_trains': 1,        # Maximum number of arriving trains to retrieve
    'departed_trains': 1,        # Maximum number of departed trains to retrieve
    'departing_trains': 1,       # Maximum number of departing trains to retrieve
    'train_categories': 'Commuter,Long-distance',  # Filter by train categories
    'include_nonstopping': False,  # Exclude trains that do not stop at the station
    'version': 159123295871       # Version number for caching (optional)
}

# Make the API call
response = requests.get(base_url + endpoint + station_shortcode, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Process the data as needed
    train_info = []
    for train in data:
        train_data = {
            'trainNumber': train['trainNumber'],
            'departureDate': train['departureDate'],
            'operatorShortCode': train['operatorShortCode'],
            'trainType': train['trainType'],
            'trainCategory': train['trainCategory'],
            'runningCurrently': train['runningCurrently'],
            'cancelled': train['cancelled'],
            'timetableType': train['timetableType'],
            'stops': []
        }
        for row in train['timeTableRows']:
            stop_info = {
                'stationShortCode': row['stationShortCode'],
                'scheduledTime': row.get('scheduledTime'),
                'actualTime': row.get('actualTime'),
                'type': row['type']
            }
            train_data['stops'].append(stop_info)
        train_info.append(train_data)

    # Print or process train_info as needed
    for train in train_info:
        print(f"Train Number: {train['trainNumber']}, Departure Date: {train['departureDate']}")
        print(f"Operator: {train['operatorShortCode']}, Train Type: {train['trainType']}, Category: {train['trainCategory']}")
        print("Stops:")
        for stop in train['stops']:
            print(f"Station: {stop['stationShortCode']}, Scheduled Time: {stop['scheduledTime']}, Actual Time: {stop['actualTime']}, Type: {stop['type']}")
        print("\n")
else:
    print('Error:', response.status_code)
