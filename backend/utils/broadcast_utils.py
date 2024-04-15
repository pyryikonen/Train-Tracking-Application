from gtts import gTTS
from datetime import datetime
import json

i = 0  # Global variable for announcement file numbering

# Load station data from passenger_traffic_stations.json
with open('passenger_traffic_stations.json', 'r', encoding='utf-8') as file:
    station_data = json.load(file)

def get_station_name(station_short_code):
    for station in station_data:
        if station['stationShortCode'] == station_short_code:
            return station['stationName']
    return 'Unknown'

def construct_broadcast(traindata):
    print("Entering broadcast_utils")

    # Debugging: Print traindata to see its content
    print("Train Data:", traindata)

    train_type = traindata.get('trainType', 'Unknown')
    print("Train Type:", train_type)

    if train_type is None:
        print("trainType key not found in traindata")
        return None

    train_number = traindata.get('trainNumber')
    time_table_rows = traindata.get('timeTableRows', [])

    # Filter time_table_rows to get the first departure and last arriving stations
    departures = [row for row in time_table_rows if row['type'] == 'DEPARTURE']
    arrivals = [row for row in time_table_rows if row['type'] == 'ARRIVAL']

    if departures:
        departure_station_code = departures[0].get('stationShortCode', 'Unknown')
        scheduled_time = departures[0].get('scheduledTime', 'Unknown')
    else:
        departure_station_code = 'Unknown'
        scheduled_time = 'Unknown'

    if arrivals:
        stop_station_code = arrivals[-1].get('stationShortCode', 'Unknown')
    else:
        stop_station_code = 'Unknown'

    departure_station = get_station_name(departure_station_code)
    stop_station = get_station_name(stop_station_code)

    train_number_as_text = str(train_number)

    parsed_time = datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    time_24hr = f'{parsed_time.hour:02}:{parsed_time.minute:02}'

    my_text = f'({train_type}-{train_number_as_text}) asemalta {departure_station} pysähtyy asemalle {stop_station} kello {time_24hr}.'

    print(my_text)

    tts = gTTS(my_text, lang='fi', slow=True)

    global i
    audio_file_path = f"static/train_announcement{i}.wav"
    i += 1

    tts.save(audio_file_path)

    return audio_file_path
