import React from 'react';

const FilterButtons = () => {
  const filters = [
    { label: 'Price', icon: 'fas fa-dollar-sign' },
    { label: 'Rooms', icon: 'fas fa-door-open' },
    { label: 'Size', icon: 'fas fa-ruler-combined' },
  ];

  const handleFilterClick = (filterLabel) => {
    // Placeholder functionality as per HTML example
    alert(`Filter button "${filterLabel}" clicked. Filter functionality is for demonstration and not implemented in this prototype.`);
  };

  return (
    <div className="flex flex-wrap gap-2 md:gap-4 mt-4 md:mt-0">
      {filters.map((filter) => (
        <button 
          key={filter.label}
          type="button" 
          onClick={() => handleFilterClick(filter.label)}
          className="filter-button py-3 px-5 bg-secondary-color border border-border-color rounded-md cursor-pointer text-sm text-text-dark transition-colors duration-300 hover:bg-gray-200 hover:border-gray-400 flex items-center flex-grow md:flex-grow-0"
        >
          <i className={`${filter.icon} mr-2`}></i> {filter.label}
        </button>
      ))}
    </div>
  );
};

export default FilterButtons;
