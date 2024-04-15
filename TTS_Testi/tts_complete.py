import requests
from gtts import gTTS
import datetime
import time
import threading

def fetch_trains():
	# API endpoint URL
	url = "https://junakuulutus.onrender.com/live-trains/TPE"

	# Send GET request to the API endpoint
	response = requests.get(url)

	# Check if the request was successful (status code 200)
	if response.status_code == 200:
		# Load JSON data from the response
		data = response.json()

		# Traverse through the dictionary
	train_data_dict = {}

	for direction, trains in data.items():
		direction_trains = []
		for train in trains:
			train_dict = {
				"Actual Time": train["Actual Time"],
				"Departure Date": train["Departure Date"],
				"Difference in Minutes": train["Difference in Minutes"],
				"Operator": train["Operator"],
				"Station": train["Station"],
				"Time Table Rows": [
					{"Scheduled Time": row["Scheduled Time"], "Station": row["Station"], "Track Number": row["Track Number"]}
					for row in train["Time Table Rows"]
				],
				"Train Number": train["Train Number"],
				"Train Type": train["Train Type"],
			}
			direction_trains.append(train_dict)
		train_data_dict[direction.capitalize()] = direction_trains

def add_space(string):
    # Join each character with a space
    spaced_string = ' '.join(string)
    return spaced_string

def construct_broadcast(traindata):
	train_type = traindata['Train Type']
	train_number = traindata['Train Number']
	departure_station = traindata["Time Table Rows"][2]["Station"]
	arriving_station = traindata["Time Table Rows"][0]["Station"]
	stop_station = traindata["Time Table Rows"][1]["Station"]
	scheduled_time = traindata["Time Table Rows"][1]["Scheduled Time"]
	train_number_as_text = str(train_number)
     
	departure_station = add_space(departure_station)
	arriving_station = add_space(arriving_station)
	stop_station = add_space(stop_station)

	# Parse the scheduled time string
	parsed_time = datetime.datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M:%S.%fZ')

	# Extract hour and minute components
	hour = parsed_time.hour
	minute = parsed_time.minute

	# Format as 24-hour time string
	time_24hr = f'{hour:02}:{minute:02}'

	# Text that is pronounced
	my_text = f'({train_type}-{train_number_as_text}) asemalta {departure_station} asemalle {arriving_station} pysähtyy asemalle {stop_station} kello {time_24hr}.'

	print(my_text)

	# gTTS initialization
	tts = gTTS(my_text, lang= 'fi', slow=True)

	# File path for the output
	tts.save("output.wav")
	

def check_schedule(traindata):
    # Get the current time
    current_time = datetime.datetime.now()
    
    

    for train in traindata:
        # Parse the scheduled time string for the stop station
        scheduled_time = train["Time Table Rows"][1]["Scheduled Time"]
        parsed_time = datetime.datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        

        # Calculate the time difference between current time and scheduled time
        time_difference = parsed_time - current_time
        
        print(time_difference)

        # Convert time difference to minutes
        minutes_difference = time_difference.total_seconds() / 60

        # Check if the train is between 10-2 minutes in the future
        if 2 <= minutes_difference <= 10:
            # Construct and save the broadcast
            print("Constructing broadcast for {train}")
            construct_broadcast(train)

def fetch_trains_periodically():
    while True:
        fetch_trains()
        time.sleep(600)

def check_schedule_periodically():
    while True:
        check_schedule(trains)
        time.sleep(60)
    
def main():
    fetch_trains()
	# Creating threads for fetching trains and checking schedule
    fetch_thread = threading.Thread(target=fetch_trains_periodically)
    schedule_thread = threading.Thread(target=check_schedule_periodically)

    # Starting the threads
    fetch_thread.start()
    schedule_thread.start()

    # Waiting for threads to finish (which they won't in this case)
    fetch_thread.join()
    schedule_thread.join()

main()
#construct_broadcast(trains[0])