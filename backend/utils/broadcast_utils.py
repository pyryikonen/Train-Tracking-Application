from gtts import gTTS
from datetime import datetime
import json

# Load station data from passenger_traffic_stations.json
with open('passenger_traffic_stations.json', 'r', encoding='utf-8') as file:
    station_data = json.load(file)

def get_station_name(station_short_code):
    for station in station_data:
        if station['stationShortCode'] == station_short_code:
            return station['stationName']
    return 'Unknown'

def construct_broadcast(traindata_list):
    print("Entering broadcast_utils")


    for traindata in traindata_list:
        print("Train Data:", traindata)

        train_type = traindata.get('Train Type', 'Unknown')
        print("Train Type:", train_type)

        if train_type is None:
            print("Train Type key not found in traindata")
            continue

        train_number = traindata.get('Train Number')
        time_table_rows = traindata.get('Time Table Rows', [])

        # Print timeTableRows for debugging
        print("TimeTableRows:")
        for row in time_table_rows:
            print(row)

        # Extract stations and scheduled times
        first_station = time_table_rows[0]['Station']
        target_station = time_table_rows[1]['Station']
        last_station = time_table_rows[2]['Station']

        first_station_name = get_station_name(first_station)
        target_station_name = get_station_name(target_station)
        last_station_name = get_station_name(last_station)

        scheduled_time_first = time_table_rows[0]['Scheduled Time']
        scheduled_time_target = time_table_rows[1]['Scheduled Time']
        scheduled_time_last = time_table_rows[2]['Scheduled Time']

        time_24hr_first = f'{datetime.strptime(scheduled_time_first, "%Y-%m-%dT%H:%M:%S.%fZ").hour:02}:{datetime.strptime(scheduled_time_first, "%Y-%m-%dT%H:%M:%S.%fZ").minute:02}'
        time_24hr_target = f'{datetime.strptime(scheduled_time_target, "%Y-%m-%dT%H:%M:%S.%fZ").hour:02}:{datetime.strptime(scheduled_time_target, "%Y-%m-%dT%H:%M:%S.%fZ").minute:02}'
        time_24hr_last = f'{datetime.strptime(scheduled_time_last, "%Y-%m-%dT%H:%M:%S.%fZ").hour:02}:{datetime.strptime(scheduled_time_last, "%Y-%m-%dT%H:%M:%S.%fZ").minute:02}'

        train_number_as_text = str(train_number)

        my_text = f'({train_type}-{train_number_as_text}) asemalta {first_station_name} pysähtyy asemalle {target_station_name} kello {time_24hr_target}.'

        print(my_text)

        tts = gTTS(my_text, lang='fi', slow=True)

        audio_file_path = f"static/train_announcement_{train_number}.wav"

        tts.save(audio_file_path)

    return audio_file_path
