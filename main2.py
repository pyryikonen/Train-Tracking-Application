import requests

# Define the GraphQL endpoint URL
graphql_endpoint = 'https://rata.digitraffic.fi/api/v2/graphql/graphql/'

# Define the GraphQL query
graphql_query = '''


'''

# Make the GraphQL request
response = requests.post(graphql_endpoint, json={'query': graphql_query})

# Parse the JSON response
data = response.json()

# Check if the response contains errors
if 'errors' in data:
    print('GraphQL query error:')
    for error in data['errors']:
        print(error['message'])
else:
    # Process the data as needed
    station = data['data']['station']
    print(f"Station: {station['name']}")
    for train in station['trains']:
        print(f"Train Number: {train['trainNumber']}, Departure Date: {train['departureDate']}")
        print(f"Operator: {train['operator']['shortCode']}, Train Type: {train['trainType']}, Category: {train['trainCategory']}")
        print("Stops:")
        for row in train['timeTableRows']:
            print(f"Station: {row['stationShortCode']}, Scheduled Time: {row['scheduledTime']}, Actual Time: {row.get('actualTime')}, Type: {row['type']}")
        print("\n")
