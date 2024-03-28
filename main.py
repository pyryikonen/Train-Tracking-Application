import requests
from datetime import datetime

# Function to fetch arriving trains to Tampere
def fetch_arriving_trains():
    url = 'https://rata.digitraffic.fi/api/v2/graphql/graphql'
    query = """
        {
          trainsByDepartureDate(
            departureDate: "%s",
            where: {
              timeTableRows: {
                contains: {
                  station: {
                    shortCode: { equals: "TPE" }
                  }
                }
              }
            }
          ) {
            trainNumber
            departureDate
            timeTableRows {
              scheduledTime
              station {
                name
                shortCode
              }
            }
          }
        }
    """ % datetime.today().strftime('%Y-%m-%d')

    try:
        # Construct the request
        request = requests.Request('POST', url, json={'query': query}).prepare()

        # Print the full request content
        print("Full request:")
        print("URL:", request.url)
        print("Method:", request.method)
        print("Headers:", request.headers)
        print("Body:", request.body)

        # Send the request
        response = requests.post(url, json={'query': query})
        response.raise_for_status()
        data = response.json()
        arriving_trains = []
        for train in data['data']['trainsByDepartureDate']:
            for row in train['timeTableRows']:
                if row['station']['shortCode'] == 'TPE':  # Check shortCode for Tampere
                    arriving_trains.append({
                        'trainNumber': train['trainNumber'],
                        'departureDate': train['departureDate'],
                        'scheduledArrivalTime': row['scheduledTime']
                    })
        print("Arriving trains to Tampere:")
        for train in arriving_trains:
            print(train)
    except requests.exceptions.RequestException as e:
        print("Error fetching arriving trains:", e)

# Call the function directly for testing
fetch_arriving_trains()
