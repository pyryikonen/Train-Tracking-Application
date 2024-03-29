import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function TrainList() {
  const [trains, setTrains] = useState([]);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [formattedDate, setFormattedDate] = useState('');
  const [selectedStation, setSelectedStation] = useState('Tampere'); //{selectedStation}

  useEffect(() => {
    async function fetchTrains() {
      try {
        const response = await axios.get(
          'http://localhost:5000/api/arriving_trains'
        );
        setTrains(response.data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchTrains();

    //Tämänhetkisen ajan esittäminen ja päivittäminen testaamiseen
    const intervalId = setInterval(() => {
      const date = new Date();
      date.setUTCHours(date.getUTCHours() + 2);
      setCurrentTime(date);
      setFormattedDate(date.toISOString());
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  const upcomingTrains = trains.filter((train) => {
    const scheduledArrivalTime = new Date(
      train.scheduledArrivalTime
    ).toISOString();
    return scheduledArrivalTime > formattedDate;
  });

  const sorted = upcomingTrains.sort((a, b) => {
    return a.scheduledArrivalTime > b.scheduledArrivalTime
      ? 1
      : b.scheduledArrivalTime > a.scheduledArrivalTime
      ? -1
      : 0;
  });

  const nextTrains = sorted.slice(0, 5);

  return (
    <div className='train-list-container'>
      <h3>Tämänhetkinen aika: {formattedDate}</h3>
      <div className='dropdown'>
        <select
          onChange={(e) => setSelectedStation(e.target.value)}
          value={selectedStation}
        >
          <option disabled>Valitse asema</option>
          <option value='Tampere'>Tampere</option>
          <option value='Helsinki'>Helsinki</option>
          <option value='Oulu'>Oulu</option>
        </select>
      </div>
      <ul className='train-list'>
        {nextTrains.length === 0 ? (
          <li>Ei tulevia junia</li>
        ) : (
          nextTrains.map((train, index) => (
            <div className='train' key={index}>
              <li>
                Junan numero: {train.trainNumber}, Lähtöpäivä:{' '}
                {train.departureDate}, Oletettu saapumisaika:{' '}
                {train.scheduledArrivalTime}
              </li>
            </div>
          ))
        )}
      </ul>
    </div>
  );
}

// stations.map((station) => (
//   <option value={station} key={station}>
//     {station}
//   </option>
// ));

function App() {
  return (
    <div className='App'>
      <TrainList />
    </div>
  );
}

export default App;
