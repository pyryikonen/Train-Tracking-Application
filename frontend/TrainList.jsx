import React from 'react';

// Date object automaattisesti olettaa string arvon utc +0 ja muuntaa paikalliseksi eli lisää +3 tuntia suomessa, joten vähennetään 3 tuntia? Onko tappaa olla muuttamatta?? (.toUTCString())?
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

const TrainList = ({ trains, selectedStation, timeZone }) => {
  return (
    <div className='train-list-container'>
      <div>
        <h2>Saapuvat junat:</h2>
        <ul className='train-list'>
          {trains.map((train) => {
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
                    {scheduledTime}
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
    </div>
  );
};

export default TrainList;
