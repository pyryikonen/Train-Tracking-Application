import React from 'react';
import Select from 'react-select';
import './App.css';

const StationDropdown = ({ stations, onSelectStation }) => {
  const options = stations.map((station) => ({
    value: station.stationShortCode,
    label: station.stationName,
  }));

  const handleChange = (selectedOption) => {
    onSelectStation(selectedOption.value);
  };

  return (
    <div className='station-dropdown'>
      <Select
        options={options}
        onChange={handleChange}
        isSearchable
        placeholder='Valitse Asema'
        styles={{
          control: (base) => ({
            ...base,
            width: 220,
            margin: '0 auto',
            color: 'black',
          }),
          singleValue: (base) => ({
            ...base,
            color: 'black',
          }),
        }}
      />
    </div>
  );
};

export default StationDropdown;
