import React, { useState, useEffect } from 'react';
import axios from 'axios';
import passengerTrafficStations from './passenger_traffic_stations.json';
import StationDropdown from './StationDropdown';
import TrainList from './TrainList';
import './App.css';

const App = () => {
  const [selectedStation, setSelectedStation] = useState('');
  const [trains, setTrains] = useState([]);
  const [currentTime, setCurrentTime] = useState('');

  useEffect(() => {
    const fetchTrains = async () => {
      if (selectedStation) {
        try {
          const response = await axios.get(
            `http://localhost:5001/live-trains/${selectedStation}`
          );
          console.log(response.data);
          setTrains(response.data.arriving.slice(0, 5));
        } catch (error) {
          console.error('Error fetching train data:', error);
        }
      }
    };

    fetchTrains();
  }, [selectedStation]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      const now = new Date();
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      const seconds = now.getSeconds().toString().padStart(2, '0');
      setCurrentTime(`${hours}:${minutes}:${seconds}`);
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className='content'>
      <h1>{currentTime}</h1>
      <StationDropdown
        stations={passengerTrafficStations}
        onSelectStation={setSelectedStation}
      />
      {selectedStation && (
        <TrainList
          trains={trains}
          selectedStation={selectedStation}
          timeZone='Europe/Helsinki'
        />
      )}
    </div>
  );
};

export default App;
