import requests


def fetch_live_trains(station_shortcode, minutes_before_departure=15, minutes_after_departure=15,
                      minutes_before_arrival=15, minutes_after_arrival=15):
    url = f"https://rata.digitraffic.fi/api/v1/live-trains/station/{station_shortcode}?minutes_before_departure={minutes_before_departure}&minutes_after_departure={minutes_after_departure}&minutes_before_arrival={minutes_before_arrival}&minutes_after_arrival={minutes_after_arrival}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        live_trains = []

        print("Live trains at station:", station_shortcode)
        for train in data:
            live_trains.append(train)  # Append train information to the list

        return live_trains

    except requests.exceptions.RequestException as e:
        print("Error fetching live trains:", e)
        return []

def format_live_trains_response(live_trains):
    formatted_trains = []

    for train in live_trains:
        formatted_train = {
            'Train Number': train['trainNumber'],
            'Departure Date': train['departureDate'],
            'Operator': train['operatorShortCode'],
            'Train Type': train['trainType'],
            'Time Table Rows': []
        }

        for row in train['timeTableRows']:
            formatted_row = {
                'Station': row['stationShortCode'],
                'Scheduled Time': row['scheduledTime']
            }
            formatted_train['Time Table Rows'].append(formatted_row)

        formatted_trains.append(formatted_train)

    return formatted_trains


# Call the function to fetch live trains at station HKI
live_trains = fetch_live_trains("TPE")

# Assuming live_trains is the list of live trains fetched
formatted_live_trains = format_live_trains_response(live_trains)

# Print the formatted response
for train in formatted_live_trains:
    print(train)
