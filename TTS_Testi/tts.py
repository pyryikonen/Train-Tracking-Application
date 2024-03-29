from gtts import gTTS
import datetime

# Example data for prototype
train_type = 'IC'
train_number = '922'
departure_station = 'TPE'
arriving_station = 'LPÄ'
scheduled_time = '2024-03-29T13:22:00.000Z'

# Parse the scheduled time string
parsed_time = datetime.datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M:%S.%fZ')

# Extract hour and minute components
hour = parsed_time.hour
minute = parsed_time.minute

# Format as 24-hour time string
time_24hr = f'{hour:02}:{minute:02}'

# Text that is pronounced
my_text = f'{train_type}-{train_number} saapuu asemalta {departure_station} asemalle {arriving_station} kello {time_24hr}.'

# gTTS initialization
tts = gTTS(my_text, lang= 'fi', slow=False)

# File path for the output
tts.save('output.wav')