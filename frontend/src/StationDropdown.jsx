import React from 'react';

const StationDropdown = ({ stations, onSelectStation }) => {
  return (
    <select onChange={(e) => onSelectStation(e.target.value)}>
      <option value='' disabled>
        Valitse Asema
      </option>
      {stations.map((station) => (
        <option key={station.stationShortCode} value={station.stationShortCode}>
          {station.stationName}
        </option>
      ))}
    </select>
  );
};

export default StationDropdown;
