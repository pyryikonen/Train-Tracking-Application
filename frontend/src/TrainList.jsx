import React from 'react';
import passengerTrafficStations from './passenger_traffic_stations.json'; // Importing data for passenger traffic stations
import './App.css';
import TrainAnnouncement from './TrainAnnouncement';
import { AnnouncementProvider } from './AnnouncementContext';
import AnnouncementPlayer from './AnnouncementPlayer';

// Function to format time string to Finnish time format
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

// TrainList component responsible for rendering the list of arriving and departing trains
const TrainList = ({
  arrivingTrains,
  departingTrains,
  selectedStation,
  timeZone,
}) => {
  const currentTime = new Date();
  currentTime.setHours(currentTime.getHours() + 3); // Adjusting to local time (GMT+3)

  // Functions to get destination, first station, and last station of a train
  const getDestinationStation = (train) => {
    const timeTableRows = train['Time Table Rows'];
    return timeTableRows[timeTableRows.length - 1].Station;
  };

  const getFirstStation = (train) => {
    const timeTableRows = train['Time Table Rows'];
    return timeTableRows[0].Station;
  };

  const getLastStation = (train) => {
    const timeTableRows = train['Time Table Rows'];
    return timeTableRows[timeTableRows.length - 1].Station;
  };

  // Function to get full station name from its short code
  const getStationName = (shortCode) => {
    const station = passengerTrafficStations.find(
      (station) => station.stationShortCode === shortCode
    );
    return station ? station.stationName : '';
  };

  // Filtering arriving trains based on selected station and current time
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

  // Filtering departing trains based on selected station and current time
  const filteredDepartingTrains = departingTrains
    .filter((train) => {
      const row = train['Time Table Rows'].find(
        (row) => row.Station === selectedStation
      );
      if (getLastStation(train) !== selectedStation) {
        return row && new Date(row['Scheduled Time']) > currentTime;
      } else {
        return null;
      }
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
    <AnnouncementProvider>
      <AnnouncementPlayer />
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
            const lastStation = getLastStation(train);
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
                    arrival={true}
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
                    {train['Train Type']} {train['Train Number']} -
                    Saapumisaikaa ei saatavilla - Määränpää:{' '}
                    {destinationStation}
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
                  <TrainAnnouncement
                    arrival={false}
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
                    {train['Train Type']} {train['Train Number']} - Lähtöaikaa
                    ei saatavilla - Määränpää: {destinationStation}
                  </li>
                </div>
              );
            }
          })}
        </ul>
      </div>
    </AnnouncementProvider>
  );
};

export default TrainList;
