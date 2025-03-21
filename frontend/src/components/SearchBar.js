import React from 'react';

const SearchBar = ({ value, onChange, onSearch }) => {
  return (
    <div>
      <input
        type="text"
        placeholder="Enter city"
        value={value}
        onChange={onChange}
      />
      <button onClick={onSearch}>Get Weather</button>
    </div>
  );
};

export default SearchBar;
