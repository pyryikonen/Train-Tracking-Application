import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import time

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
              }
            }
          }
        }
    """ % datetime.today().strftime('%Y-%m-%d')

    try:
        response = requests.post(url, json={'query': query})
        response.raise_for_status()
        data = response.json()
        arriving_trains = []
        for train in data['data']['trainsByDepartureDate']:
            for row in train['timeTableRows']:
                if row['station']['name'] == 'Tampere':
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


# Create scheduler
scheduler = BlockingScheduler()

# Schedule to fetch arriving trains every 5 minutes
scheduler.add_job(fetch_arriving_trains, 'interval', minutes=5)

# Start the scheduler
try:
    scheduler.start()
except KeyboardInterrupt:
    pass
