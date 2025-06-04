import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

const SearchBar = ({ searchTerm, onSearchTermChange, onSearch }) => {
  const handleSearchClick = (e) => {
    e.preventDefault(); // Prevent form submission if wrapped in a form
    if (onSearch) {
      onSearch();
    } else {
      // Placeholder functionality as per HTML example
      alert("Search functionality is for demonstration and not implemented in this prototype.");
    }
  };

  return (
    <div className="search-input-group flex-grow flex">
      <input 
        type="text" 
        placeholder="Search by city, neighborhood, or address..."
        value={searchTerm}
        onChange={onSearchTermChange} 
        className="w-full py-3 px-4 border border-border-color border-r-0 rounded-l-md text-base focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
      />
      <button 
        type="button" 
        onClick={handleSearchClick}
        className="py-3 px-6 bg-primary text-white-color border-0 rounded-r-md cursor-pointer text-base transition-colors duration-300 hover:bg-blue-700"
      >
        <FontAwesomeIcon icon={faSearch} />
      </button>
    </div>
  );
};

export default SearchBar;
