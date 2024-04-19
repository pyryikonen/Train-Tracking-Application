import React from 'react';
import passengerTrafficStations from './passenger_traffic_stations.json';
import './App.css';

const formatTime = (timeString) => {
  const date = new Date(timeString);
  date.setHours(date.getHours() - 3);
  const options = {
    hour: 'numeric',
    minute: 'numeric',
    hour12: false,
  };
  return date.toLocaleTimeString('fi-FI', options);
};

const TrainList = ({
  arrivingTrains,
  departingTrains,
  selectedStation,
  timeZone,
}) => {
  const currentTime = new Date();
  currentTime.setHours(currentTime.getHours() + 3);

  const getDestinationStation = (train) => {
    const timeTableRows = train['Time Table Rows'];
    return timeTableRows[timeTableRows.length - 1].Station;
  };

  const getFirstStation = (train) => {
    const timeTableRows = train['Time Table Rows'];
    return timeTableRows[0].Station;
  };

  const getStationName = (shortCode) => {
    const station = passengerTrafficStations.find(
      (station) => station.stationShortCode === shortCode
    );
    return station ? station.stationName : '';
  };

  const filteredArrivingTrains = arrivingTrains
    .filter((train) => {
      const row = train['Time Table Rows'].find(
        (row) => row.Station === selectedStation
      );
      return row && new Date(row['Scheduled Time']) > currentTime;
    })
    .sort(
      (a, b) =>
        new Date(
          a['Time Table Rows'].find((row) => row.Station === selectedStation)[
            'Scheduled Time'
          ]
        ) -
        new Date(
          b['Time Table Rows'].find((row) => row.Station === selectedStation)[
            'Scheduled Time'
          ]
        )
    )
    .slice(0, 5);

  const filteredDepartingTrains = departingTrains
    .filter((train) => {
      const row = train['Time Table Rows'].find(
        (row) => row.Station === selectedStation
      );
      return row && new Date(row['Scheduled Time']) > currentTime;
    })
    .sort(
      (a, b) =>
        new Date(
          a['Time Table Rows'].find((row) => row.Station === selectedStation)[
            'Scheduled Time'
          ]
        ) -
        new Date(
          b['Time Table Rows'].find((row) => row.Station === selectedStation)[
            'Scheduled Time'
          ]
        )
    )
    .slice(0, 5);

  return (
    <div className='train-list-container'>
      <h2 className='title-direction'>Saapuvat junat:</h2>
      <div className='category-header'>
        <div className='category'>Juna</div>
        <div className='category'>Aika</div>
        <div className='category'>Raide</div>
        <div className='category'>Lähtöasema</div>
        <div className='category'>Määränpää</div>
      </div>
      <ul className='train-list'>
        {filteredArrivingTrains.map((train) => {
          const timeTableRow = train['Time Table Rows'].find(
            (row) => row.Station === selectedStation
          );
          const destinationStation = getDestinationStation(train);
          const firstStation = getFirstStation(train);
          const destinationStationName = getStationName(destinationStation);
          if (timeTableRow) {
            const scheduledTime = formatTime(
              timeTableRow['Scheduled Time'],
              timeZone
            );
            const trackNumber = timeTableRow['Track Number'];
            return (
              <div className='train' key={train.TrainNumber}>
                <li className='train-row'>
                  <div className='category'>
                    {train['Train Type']} {train['Train Number']}{' '}
                  </div>
                  <div className='category'>{scheduledTime} </div>
                  <div className='category'> {trackNumber} </div>
                  <div className='category'>
                    {' '}
                    {getStationName(firstStation)}{' '}
                  </div>{' '}
                  <div className='category'>{destinationStationName}</div>
                </li>
              </div>
            );
          } else {
            return (
              <div className='train' key={train.TrainNumber}>
                <li>
                  {train['Train Type']} {train['Train Number']} - Saapumisaikaa
                  ei saatavilla - Määränpää: {destinationStation}
                </li>
              </div>
            );
          }
        })}
      </ul>
      <h2 className='title-direction'>Lähtevät junat:</h2>
      <ul className='train-list'>
        {filteredDepartingTrains.map((train) => {
          const timeTableRow = train['Time Table Rows'].find(
            (row) => row.Station === selectedStation
          );
          const destinationStation = getDestinationStation(train);
          const firstStation = getFirstStation(train);
          const destinationStationName = getStationName(destinationStation);
          if (timeTableRow) {
            const scheduledTime = formatTime(
              timeTableRow['Scheduled Time'],
              timeZone
            );
            const trackNumber = timeTableRow['Track Number'];
            return (
              <div className='train' key={train.TrainNumber}>
                <li className='train-row'>
                  <div className='category'>
                    {train['Train Type']} {train['Train Number']}{' '}
                  </div>
                  <div className='category'>{scheduledTime} </div>
                  <div className='category'> {trackNumber} </div>
                  <div className='category'>
                    {' '}
                    {getStationName(firstStation)}{' '}
                  </div>{' '}
                  <div className='category'>{destinationStationName}</div>
                </li>
              </div>
            );
          } else {
            return (
              <div className='train' key={train.TrainNumber}>
                <li>
                  {train['Train Type']} {train['Train Number']} - Lähtöaikaa ei
                  saatavilla - Määränpää: {destinationStation}
                </li>
              </div>
            );
          }
        })}
      </ul>
    </div>
  );
};

export default TrainList;
