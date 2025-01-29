# Live Trains Web Application

This web application fetches live train information for specific stations and presents it in a user-friendly format. It provides real-time data on arriving and departing trains, including scheduled times, train types, and destinations.

**At this time the application is deployed separately in different servers (backend & frontend) on render. So to use it you need to wake up both of these**

backend: https://junakuulutus.onrender.com/live-trains/TPE

backend tts voice route example: 

https://junakuulutus.onrender.com/single-announcement/2024-04-20T06:22:00.000Z/24/TPE

https://junakuulutus.onrender.com/single-announcement/{date-object}/{train-number}/{station-shortcode}

(Only works with future or ongoing trains) 

frontend: https://trains-7w3b.onrender.com/

## Features

- Allows users to select a station from a dropdown menu to view live train information.
- Displays a list of arriving and departing trains for the selected station, including train type, train number, scheduled time, and destination.
- Updates the displayed information periodically to keep it current.
- Supports multiple stations for users to choose from.
- Generates live announcements using Text-to-Speech (TTS) to inform the user about trains arriving and or departing at the selected station.

## Usage

1. **Install dependencies:**

   - Ensure that you have the necessary Python dependencies installed. You can use pip to install them:

     ```
     pip install ...
     ```
2. **Start the server:**
   
   - Once dependencies are installed and the application is configured, you can start the server. For example, if you're using Flask:

     ```
     python app.py
     ```

     If you're using a production-ready server like Gunicorn, you might use a command like this:

     ```
     gunicorn -w 4 app:app
     ```
