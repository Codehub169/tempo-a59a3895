import React from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMapMarkerAlt, faEuroSign, faRulerCombined, faDoorOpen, faArrowRight } from '@fortawesome/free-solid-svg-icons';

const ListingCard = ({ listing }) => {
  if (!listing) {
    return null; // Or some placeholder/error component
  }

  const { 
    id, 
    image, 
    title, 
    location, 
    advertisedRent, 
    size, 
    rooms, 
    wwsPoints, 
    maxLegalRent 
  } = listing;

  let comparisonClass = '';
  let comparisonText = '';
  const liberalisationPointsThreshold = 136; // As per HTML example

  if (wwsPoints >= liberalisationPointsThreshold) {
    comparisonClass = 'neutral';
    comparisonText = 'Likely liberalized';
  } else if (advertisedRent > maxLegalRent) {
    comparisonClass = 'overpriced';
    comparisonText = 'Overpriced';
  } else {
    comparisonClass = 'fair';
    comparisonText = 'Fair Price';
  }

  return (
    <div className="listing-card bg-white-color rounded-lg shadow-md overflow-hidden transition-transform duration-300 ease-in-out hover:transform hover:-translate-y-1 hover:shadow-lg flex flex-col">
      <img src={image || 'https://placehold.co/400x200/007bff/white?text=Apartment&font=poppins'} alt={title} className="listing-card-image w-full h-48 object-cover" />
      <div className="listing-card-content p-5 flex-grow flex flex-col">
        <h3 className="listing-title font-secondary text-xl font-semibold mb-1 text-text-dark">{title}</h3>
        <p className="listing-location text-sm text-text-light mb-3 flex items-center">
          <FontAwesomeIcon icon={faMapMarkerAlt} className="mr-2 text-primary" /> {location}
        </p>
        <div className="listing-specs flex justify-between text-sm text-text-light mb-4 pb-4 border-b border-dashed border-border-color">
          <span className="flex items-center"><FontAwesomeIcon icon={faEuroSign} className="mr-2 text-primary w-4" /> &euro;{advertisedRent.toLocaleString('nl-NL')}/mo</span>
          <span className="flex items-center"><FontAwesomeIcon icon={faRulerCombined} className="mr-2 text-primary w-4" /> {size} m&sup2;</span>
          <span className="flex items-center"><FontAwesomeIcon icon={faDoorOpen} className="mr-2 text-primary w-4" /> {rooms} room(s)</span>
        </div>
        <div className="listing-wws-summary bg-secondary p-3 rounded-md mb-4 text-xs">
          <p className="wws-points flex justify-between mb-1">WWS Points: <strong className="text-primary">{wwsPoints}</strong></p>
          <p className="max-legal-rent flex justify-between mb-1">Max Legal Rent: <strong className="text-accent">&euro;{maxLegalRent.toLocaleString('nl-NL', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong></p>
          <p className="advertised-rent flex justify-between">Advertised Rent: <strong className="text-text-dark">&euro;{advertisedRent.toLocaleString('nl-NL', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong></p>
          <span className={`rent-comparison-badge inline-block px-2 py-1 rounded text-xs font-semibold mt-2 w-full text-center border ${comparisonClass === 'fair' ? 'bg-green-100 text-accent border-accent' : comparisonClass === 'overpriced' ? 'bg-red-100 text-error border-error' : 'bg-gray-100 text-text-light border-border-color'}`}>
            {comparisonText}
          </span>
        </div>
        <Link 
          to={`/listing/${id}`}
          className="view-details-btn mt-auto block bg-primary text-white-color text-center py-2 px-4 rounded-md font-medium transition-colors duration-300 hover:bg-blue-700"
        >
          View Details <FontAwesomeIcon icon={faArrowRight} className="ml-2" />
        </Link>
      </div>
    </div>
  );
};

export default ListingCard;
