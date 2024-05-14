import React, { useState, useEffect } from 'react';
import axios from 'axios';
import passengerTrafficStations from './passenger_traffic_stations.json';
import StationDropdown from './StationDropdown';
import TrainList from './TrainList';
import './App.css';

const App = () => {
  const [selectedStation, setSelectedStation] = useState('');
  const [arrivingTrains, setArriving] = useState([]);
  const [departingTrains, setDeparting] = useState([]);
  const [currentTime, setCurrentTime] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Function to fetch train data when selectedStation changes
    const fetchTrains = async () => {
      if (selectedStation) {
        setIsLoading(true); // Set loading status to true
        try {
          // Fetching train data from the API based on the selected station
          const response = await axios.get(
            `https://junakuulutus.onrender.com/live-trains/${selectedStation}`
          );
          // Updating state with the fetched arriving and departing trains
          setArriving(response.data.arriving);
          setDeparting(response.data.departing);
          console.log('Fetched train data:', response.data);
        } catch (error) {
          console.error('Error fetching train data:', error);
        }
        setIsLoading(false); // Set loading status to false after fetching data
      }
    };

    fetchTrains(); // Call the fetchTrains function when selectedStation changes
  }, [selectedStation]);

  useEffect(() => {
    // Function to update currentTime every second
    const intervalId = setInterval(() => {
      const now = new Date();
      // Formatting current time as HH:mm:ss
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      const seconds = now.getSeconds().toString().padStart(2, '0');
      setCurrentTime(`${hours}:${minutes}:${seconds}`);
    }, 1000); // Update time every second

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className='content'>
      <h1>{currentTime}</h1>
      <StationDropdown
        stations={passengerTrafficStations}
        onSelectStation={setSelectedStation}
      />
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        selectedStation && (
          <TrainList
            arrivingTrains={arrivingTrains}
            departingTrains={departingTrains}
            selectedStation={selectedStation}
            timeZone='Europe/Helsinki'
          />
        )
      )}
    </div>
  );
};

export default App;
