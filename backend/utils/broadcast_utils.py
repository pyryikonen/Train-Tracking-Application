from gtts import gTTS
from datetime import datetime
import json

arriving_audio_file_path = None
departing_audio_file_path = None

# Load station data from passenger_traffic_stations.json
with open('passenger_traffic_stations.json', 'r', encoding='utf-8') as file:
    station_data = json.load(file)


def get_station_name(station_short_code):
    """
     Retrieves the name of a station based on its shortcode.

     Parameters:
     - station_short_code (str): The shortcode of the station.

     Returns:
     - str: The name of the station if found, otherwise 'Unknown'.
     """
    for station in station_data:
        if station['stationShortCode'] == station_short_code:
            return station['stationName']
    return 'Unknown'


def construct_arrival_broadcast(traindata_list):
    """
      Constructs an audio file for train arrival announcement.

      Parameters:
      - traindata_list (list): A list of dictionaries containing train data.

      Returns:
      - str: The file path of the constructed audio file.
      """
    global arriving_audio_file_path

    for traindata in traindata_list:
        train_type = traindata.get('Train Type', 'Unknown')
        if train_type is None:
            print("Train Type key not found in traindata")
            continue

        train_number = traindata.get('Train Number')
        time_table_rows = traindata.get('Time Table Rows', [])

        # Extract stations and scheduled times
        first_station = time_table_rows[0]['Station']
        target_station = time_table_rows[1]['Station']
        last_station = time_table_rows[2]['Station']

        first_station_name = get_station_name(first_station)
        target_station_name = get_station_name(target_station)

        scheduled_time_target = time_table_rows[1]['Scheduled Time']
        track_number = time_table_rows[1].get('Track Number', 'Unknown')  # Extract track number

        time_24hr_target = f'{datetime.strptime(scheduled_time_target, "%Y-%m-%dT%H:%M:%S.%fZ").hour:02}:{datetime.strptime(scheduled_time_target, "%Y-%m-%dT%H:%M:%S.%fZ").minute:02}'

        train_number_as_text = str(train_number)

        # Check if the target station is the same as the arrival station
        if last_station == target_station:
            arriving_text = f'(Juna {train_type}-{train_number_as_text}) saapuu asemalle {target_station_name}, raiteelle {track_number}, kello {time_24hr_target}. Tämä on junan {train_number_as_text} päätepysäkki.'
        else:
            arriving_text = f'(Juna {train_type}-{train_number_as_text}) asemalta {first_station_name} pysähtyy asemalle {target_station_name}, raiteelle {track_number} kello {time_24hr_target}.'

        arriving_tts = gTTS(arriving_text, lang='fi')
        arriving_audio_file_path = f"static/departure_train_announcement_{train_number}.wav"
        arriving_tts.save(arriving_audio_file_path)

    return arriving_audio_file_path


def construct_departure_broadcast(traindata_list):
    """
       Constructs an audio file for train departure announcement.

       Parameters:
       - traindata_list (list): A list of dictionaries containing train data.

       Returns:
       - str: The file path of the constructed audio file.
       """
    global departing_audio_file_path

    for traindata in traindata_list:

        train_type = traindata.get('Train Type', 'Unknown')

        if train_type is None:
            continue

        train_number = traindata.get('Train Number')
        time_table_rows = traindata.get('Time Table Rows', [])

        # Extract stations and scheduled times
        first_station = time_table_rows[0]['Station']
        target_station = time_table_rows[1]['Station']
        last_station = time_table_rows[2]['Station']

        target_station_name = get_station_name(target_station)
        last_station_name = get_station_name(last_station)

        scheduled_time_target = time_table_rows[1]['Scheduled Time']
        track_number = time_table_rows[1].get('Track Number', 'Unknown')  # Extract track number

        time_24hr_target = f'{datetime.strptime(scheduled_time_target, "%Y-%m-%dT%H:%M:%S.%fZ").hour:02}:{datetime.strptime(scheduled_time_target, "%Y-%m-%dT%H:%M:%S.%fZ").minute:02}'

        train_number_as_text = str(train_number)

        # Departing train announcement
        departing_text = f'(Juna {train_type}-{train_number_as_text}) raiteelta {track_number} kohti {last_station_name} lähtee kello {time_24hr_target}'

        departing_tts = gTTS(departing_text, lang='fi')
        departing_audio_file_path = f"static/departure_train_announcement_{train_number}.wav"
        departing_tts.save(departing_audio_file_path)

    return departing_audio_file_path
