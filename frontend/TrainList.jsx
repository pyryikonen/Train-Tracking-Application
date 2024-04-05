import React from 'react';

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

  const filteredArrivingTrains = arrivingTrains
    .filter(
      (train) =>
        new Date(
          train['Time Table Rows'].find(
            (row) => row.Station === selectedStation
          )['Scheduled Time']
        ) > currentTime
    )
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
    .filter(
      (train) =>
        new Date(
          train['Time Table Rows'].find(
            (row) => row.Station === selectedStation
          )['Scheduled Time']
        ) > currentTime
    )
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
      <div>
        <h2>Saapuvat junat:</h2>
        <ul className='train-list'>
          {filteredArrivingTrains.map((train) => {
            const timeTableRow = train['Time Table Rows'].find(
              (row) => row.Station === selectedStation
            );
            if (timeTableRow) {
              const scheduledTime = formatTime(
                timeTableRow['Scheduled Time'],
                timeZone
              );
              return (
                <div className='train' key={train.TrainNumber}>
                  <li>
                    {train['Train Type']} {train['Train Number']} - Saapuu{' '}
                    {scheduledTime}{' '}
                  </li>
                </div>
              );
            } else {
              return (
                <div className='train' key={train.TrainNumber}>
                  <li>
                    {train['Train Type']} {train['Train Number']} -
                    Saapumisaikaa ei saatavilla
                  </li>
                </div>
              );
            }
          })}
        </ul>
      </div>
      <div>
        <h2>Lähtevät junat:</h2>
        <ul className='train-list'>
          {filteredDepartingTrains.map((train) => {
            const timeTableRow = train['Time Table Rows'].find(
              (row) => row.Station === selectedStation
            );
            if (timeTableRow) {
              const scheduledTime = formatTime(
                timeTableRow['Scheduled Time'],
                timeZone
              );
              return (
                <div className='train' key={train.TrainNumber}>
                  <li>
                    {train['Train Type']} {train['Train Number']} - Lähtee{' '}
                    {scheduledTime}
                  </li>
                </div>
              );
            } else {
              return (
                <div className='train' key={train.TrainNumber}>
                  <li>
                    {train['Train Type']} {train['Train Number']} - Lähtöaikaa
                    ei saatavilla
                  </li>
                </div>
              );
            }
          })}
        </ul>
      </div>
    </div>
  );
};

export default TrainList;
