import requests
import schedule
import time

# Function to fetch arriving trains at Tampere station using GraphQL
def fetch_arriving_trains():
    url = 'https://rata.digitraffic.fi/api/v2/graphql/graphiql'
    query = """
        query {
            trainsByDepartureDate(
                departureDate: "2024-03-26", 
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
                    station {
                        name
                    }
                    scheduledTime
                }
            }
        }
    """
    try:
        response = requests.post(url, json={'query': query})
        data = response.json()
        process_arriving_trains(data)
    except requests.exceptions.RequestException as e:
        print("Error fetching arriving trains:", e)

# Function to process arriving trains data and track train journeys
def process_arriving_trains(data):
    arriving_trains = data['data']['trainsByDepartureDate']
    print("Arriving trains at Tampere station:")
    for train in arriving_trains:
        train_number = train['trainNumber']
        departure_date = train['departureDate']
        scheduled_arrival = train['timeTableRows'][-1]['scheduledTime']
        print(f"Train {train_number} scheduled to arrive at Tampere station on {departure_date} at {scheduled_arrival}")
        # Add logic here to track train journeys and update application data

# Schedule periodic fetching of arriving trains
schedule.every(5).minutes.do(fetch_arriving_trains)

# Main loop to run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
