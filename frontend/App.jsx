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

  useEffect(() => {
    const fetchTrains = async () => {
      if (selectedStation) {
        try {
          const response = await axios.get(
            `http://localhost:5001/live-trains/${selectedStation}`
          );
          setArriving(response.data.arriving);
          setDeparting(response.data.departing);
          console.log('Fetched train data:', response.data);
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
          arrivingTrains={arrivingTrains}
          departingTrains={departingTrains}
          selectedStation={selectedStation}
          timeZone='Europe/Helsinki'
        />
      )}
    </div>
  );
};

export default App;
