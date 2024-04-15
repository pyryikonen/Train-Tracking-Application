import requests
from gtts import gTTS  # Google Text-to-Speech library
import os
from datetime import datetime, timedelta
import time

# Function to fetch data from the API
def fetch_train_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

# Function to generate announcement text
def generate_announcement(train_data):
    announcements = []
    for train_list in train_data:
        for train in train_list:
            target_time = datetime.fromisoformat(train['Time Table Rows'][1]['Scheduled Time'].rstrip('Z')) - timedelta(minutes=2)
            announcement_time = target_time.strftime('%Y-%m-%d %H:%M:%S')
            announcement = f"Attention passengers! Train number {train['Train Number']} is {train['Direction']} at {train['Station']} at {train['Time Table Rows'][1]['Scheduled Time']}. Please be ready. Thank you!"
            announcements.append((announcement, announcement_time))
    return announcements

# Function to convert text to speech and save the announcements as audio files
def save_announcements_as_audio(announcements):
    for i, (announcement, _) in enumerate(announcements):
        tts = gTTS(text=announcement, lang='en')
        tts.save(f"announcement_{i}.mp3")

# Function to play the announcements at the specified time
def play_announcements(announcements):
    for _, announcement_time in announcements:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if current_time == announcement_time:
            os.system(f"start announcement_{i}.mp3")

# Main function
def main():
    api_url = "https://junakuulutus.onrender.com/live-trains/HKI"
    while True:
        train_data = fetch_train_data(api_url)
        if train_data:
            announcements = generate_announcement(train_data['arriving'])  # Process arriving trains
            announcements += generate_announcement(train_data['departing'])  # Process departing trains
            save_announcements_as_audio(announcements)
            play_announcements(announcements)
        time.sleep(10)  # Sleep for 10 minutes (600 seconds)

if __name__ == "__main__":
    main()
