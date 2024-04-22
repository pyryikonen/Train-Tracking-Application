import React, { useState } from 'react';
import passengerTrafficStations from './passenger_traffic_stations.json';
import './App.css';
import TrainAnnouncement from './TrainAnnouncement';

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
    .slice(0, 10);

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
    .slice(0, 10);

  return (
    <div className='train-list-container'>
      <h2 className='title-direction'>Saapuvat junat</h2>
      <ul className='train-list'>
        <li className='train-row'>
          <div className='categoryTitle'>Juna</div>
          <div className='categoryTitle'>Aika</div>
          <div className='categoryTitle'>Raide</div>
          <div className='categoryTitle'>Lähtöasema</div>
          <div className='categoryTitle'>Määränpää</div>
        </li>
      </ul>
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
              <div className='train' key={train['Train Number'] + 'arr'}>
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
                <TrainAnnouncement
                  trainNumber={train['Train Number']}
                  stationShortCode={selectedStation}
                  arrivalDepartureTime={timeTableRow['Scheduled Time']}
                />
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
      <h2 className='title-direction'>Lähtevät junat</h2>
      <ul className='train-list'>
        <li className='train-row'>
          <div className='categoryTitle'>Juna</div>
          <div className='categoryTitle'>Aika</div>
          <div className='categoryTitle'>Raide</div>
          <div className='categoryTitle'>Lähtöasema</div>
          <div className='categoryTitle'>Määränpää</div>
        </li>
      </ul>
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
              <div className='train' key={train['Train Number'] + 'dep'}>
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
