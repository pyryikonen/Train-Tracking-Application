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


def construct_arrival_broadcast(traindata_list):
    print("Entering construct_arrival_broadcast")
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

        first_station_name = get_station_name(first_station)
        target_station_name = get_station_name(target_station)

        scheduled_time_target = time_table_rows[1]['Scheduled Time']

        time_24hr_target = f'{datetime.strptime(scheduled_time_target, "%Y-%m-%dT%H:%M:%S.%fZ").hour:02}:{datetime.strptime(scheduled_time_target, "%Y-%m-%dT%H:%M:%S.%fZ").minute:02}'

        train_number_as_text = str(train_number)

        arriving_text = f'({train_type}-{train_number_as_text}) asemalta {first_station_name} pysähtyy asemalle {target_station_name} kello {time_24hr_target}.'

        arriving_tts = gTTS(arriving_text, lang='fi', slow=True)
        arriving_audio_file_path = f"static/departure_train_announcement_{train_number}.wav"
        arriving_tts.save(arriving_audio_file_path)

    return departing_audio_file_path


def construct_departure_broadcast(traindata_list):
    global departing_audio_file_path
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

        # Extract stations and scheduled times
        target_station = time_table_rows[1]['Station']
        last_station = time_table_rows[2]['Station']

        target_station_name = get_station_name(target_station)
        last_station_name = get_station_name(last_station)

        scheduled_time_target = time_table_rows[1]['Scheduled Time']

        time_24hr_target = f'{datetime.strptime(scheduled_time_target, "%Y-%m-%dT%H:%M:%S.%fZ").hour:02}:{datetime.strptime(scheduled_time_target, "%Y-%m-%dT%H:%M:%S.%fZ").minute:02}'

        train_number_as_text = str(train_number)

        # Departing train announcement
        departing_text = f'({train_type}-{train_number_as_text}) asemalta {target_station_name} lähtee asemalle {last_station_name} kello {time_24hr_target}.'
        print(departing_text)

        departing_tts = gTTS(departing_text, lang='fi', slow=True)
        departing_audio_file_path = f"static/departure_train_announcement_{train_number}.wav"
        departing_tts.save(departing_audio_file_path)

    return departing_audio_file_path
