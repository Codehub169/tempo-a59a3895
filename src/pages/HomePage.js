import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faMapMarkerAlt, faEuroSign, faRulerCombined, faDoorOpen, faArrowRight, faDollarSign } from '@fortawesome/free-solid-svg-icons';

// Placeholder for ListingCard component - will be created in a later batch
const ListingCard = ({ listing }) => {
    let comparisonClass = '';
    let comparisonText = '';
    const liberalisationPointsThreshold = 136; // Example threshold

    if (listing.wwsPoints >= liberalisationPointsThreshold) {
        comparisonClass = 'neutral';
        comparisonText = 'Likely liberalized';
    } else if (listing.advertisedRent > listing.maxLegalRent) {
        comparisonClass = 'overpriced';
        comparisonText = 'Overpriced';
    } else {
        comparisonClass = 'fair';
        comparisonText = 'Fair Price';
    }

    return (
        <div className="listing-card bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 ease-in-out hover:transform hover:-translate-y-1 hover:shadow-lg flex flex-col">
            <img src={listing.image} alt={listing.title} className="listing-card-image w-full h-48 object-cover" />
            <div className="listing-card-content p-5 flex-grow flex flex-col">
                <h3 className="listing-title font-secondary text-xl font-semibold mb-1 text-text-dark">{listing.title}</h3>
                <p className="listing-location text-sm text-text-light mb-3 flex items-center">
                    <FontAwesomeIcon icon={faMapMarkerAlt} className="mr-2 text-primary-color" /> {listing.location}
                </p>
                <div className="listing-specs flex justify-between text-sm text-text-light mb-4 pb-4 border-b border-dashed border-border-color">
                    <span className="flex items-center"><FontAwesomeIcon icon={faEuroSign} className="mr-2 text-primary-color w-4" /> {listing.advertisedRent.toLocaleString()}/mo</span>
                    <span className="flex items-center"><FontAwesomeIcon icon={faRulerCombined} className="mr-2 text-primary-color w-4" /> {listing.size} m²</span>
                    <span className="flex items-center"><FontAwesomeIcon icon={faDoorOpen} className="mr-2 text-primary-color w-4" /> {listing.rooms} room(s)</span>
                </div>
                <div className="listing-wws-summary bg-secondary-color p-3 rounded-md mb-4 text-xs">
                    <p className="wws-points mb-1 flex justify-between">WWS Points: <strong className="text-primary-color">{listing.wwsPoints}</strong></p>
                    <p className="max-legal-rent mb-1 flex justify-between">Max Legal Rent: <strong className="text-accent-color">€{listing.maxLegalRent.toLocaleString('nl-NL', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong></p>
                    <p className="advertised-rent mb-2 flex justify-between">Advertised Rent: <strong className="text-text-dark">€{listing.advertisedRent.toLocaleString('nl-NL', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong></p>
                    <span className={`rent-comparison-badge inline-block px-2 py-1 rounded text-xs font-semibold w-full text-center border ${comparisonClass === 'fair' ? 'bg-green-100 text-accent-color border-accent-color' : comparisonClass === 'overpriced' ? 'bg-red-100 text-error-color border-error-color' : 'bg-gray-100 text-text-light border-border-color'}`}>
                        {comparisonText}
                    </span>
                </div>
                <Link to={`/listing/${listing.id}`} className="view-details-btn bg-primary-color text-white text-center py-2 px-4 rounded-md font-medium transition-colors duration-300 hover:bg-blue-700 mt-auto">
                    View Details <FontAwesomeIcon icon={faArrowRight} className="ml-2" />
                </Link>
            </div>
        </div>
    );
};


const HomePage = () => {
    // Mock data, replace with API call later
    const [listings, setListings] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    const listingsData = [
        {
            id: 1,
            title: "Charming Canal View Apartment",
            location: "Amsterdam Centrum",
            image: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YXBhcnRtZW50JTIwaW50ZXJpb3J8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=400&q=60",
            advertisedRent: 1850,
            size: 75, // m²
            rooms: 2,
            wwsPoints: 140,
            maxLegalRent: 1050.75
        },
        {
            id: 2,
            title: "Modern Loft in De Pijp",
            location: "Amsterdam De Pijp",
            image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8YXBhcnRtZW50JTIwaW50ZXJpb3J8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=400&q=60",
            advertisedRent: 2200,
            size: 90,
            rooms: 3,
            wwsPoints: 165,
            maxLegalRent: 1250.50
        },
        {
            id: 3,
            title: "Spacious Family Home",
            location: "Utrecht Oost",
            image: "https://images.unsplash.com/photo-1493809842364-78817add7ffb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGFwYXJ0bWVudCUyMGV4dGVyaW9yfGVufDB8fDB8fHww&auto=format&fit=crop&w=400&q=60",
            advertisedRent: 2400,
            size: 120,
            rooms: 4,
            wwsPoints: 170, 
            maxLegalRent: 1380.00 
        },
        {
            id: 4,
            title: "Cozy Studio near Station",
            location: "Rotterdam Centraal",
            image: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGFwYXJ0bWVudCUyMGV4dGVyaW9yfGVufDB8fDB8fHww&auto=format&fit=crop&w=400&q=60",
            advertisedRent: 1100,
            size: 45,
            rooms: 1,
            wwsPoints: 125,
            maxLegalRent: 850.20
        }
    ];

    useEffect(() => {
        // Simulate API call
        setListings(listingsData);
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        alert(`Search functionality for "${searchTerm}" is for demonstration and not implemented in this prototype.`);
    };

    const handleFilterClick = (filterName) => {
        alert(`Filter button "${filterName}" clicked. Filter functionality is for demonstration and not implemented in this prototype.`);
    }

    return (
        <>
            <section 
                className="hero-section bg-cover bg-center text-text-dark py-16 text-center"
                style={{backgroundImage: "linear-gradient(rgba(0, 123, 255, 0.05), rgba(0, 123, 255, 0.05)), url('https://images.unsplash.com/photo-1560185007-c5ca91ba2960?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80')"}}
            >
                <div className="container max-w-4xl">
                    <h1 className="font-secondary text-4xl md:text-5xl font-bold mb-3">Find Your Fair Rent in the Netherlands</h1>
                    <p className="text-lg md:text-xl mb-8 text-text-light max-w-2xl mx-auto">Transparent listings with integrated WWS point system. Know your rights, find the right price.</p>
                    
                    <form onSubmit={handleSearch} className="search-filter-bar bg-white p-4 md:p-6 rounded-lg shadow-lg -mb-10 relative z-10 md:flex md:gap-4 md:items-center">
                        <div className="search-input-group flex-grow flex mb-3 md:mb-0">
                            <input 
                                type="text" 
                                placeholder="Search by city, neighborhood, or address..." 
                                className="w-full py-3 px-4 border border-border-color border-r-0 rounded-l-md text-base focus:outline-none focus:border-primary-color focus:ring-1 focus:ring-primary-color"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                            <button type="submit" className="py-3 px-6 bg-primary-color text-white border-0 rounded-r-md cursor-pointer text-base transition-colors duration-300 hover:bg-blue-700">
                                <FontAwesomeIcon icon={faSearch} />
                            </button>
                        </div>
                        <div className="filter-buttons flex flex-wrap gap-2 justify-center md:justify-start">
                            <button type="button" onClick={() => handleFilterClick('Price')} className="filter-button py-3 px-4 bg-secondary-color border border-border-color rounded-md cursor-pointer text-sm text-text-dark transition-colors duration-300 hover:bg-gray-200 hover:border-gray-400">
                                <FontAwesomeIcon icon={faDollarSign} className="mr-2" /> Price
                            </button>
                            <button type="button" onClick={() => handleFilterClick('Rooms')} className="filter-button py-3 px-4 bg-secondary-color border border-border-color rounded-md cursor-pointer text-sm text-text-dark transition-colors duration-300 hover:bg-gray-200 hover:border-gray-400">
                                <FontAwesomeIcon icon={faDoorOpen} className="mr-2" /> Rooms
                            </button>
                            <button type="button" onClick={() => handleFilterClick('Size')} className="filter-button py-3 px-4 bg-secondary-color border border-border-color rounded-md cursor-pointer text-sm text-text-dark transition-colors duration-300 hover:bg-gray-200 hover:border-gray-400">
                                <FontAwesomeIcon icon={faRulerCombined} className="mr-2" /> Size
                            </button>
                        </div>
                    </form>
                </div>
            </section>

            <section className="listings-section py-12 pt-20 bg-gray-50">
                <div className="container">
                    <h2 className="section-title font-secondary text-3xl font-semibold mb-8 text-center">Featured Listings</h2>
                    {listings.length > 0 ? (
                        <div className="listing-grid grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                            {listings.map(listing => (
                                <ListingCard key={listing.id} listing={listing} />
                            ))}
                        </div>
                    ) : (
                        <p className="text-center text-text-light">No listings available at the moment. Please check back later.</p>
                    )}
                </div>
            </section>
        </>
    );
};

export default HomePage;
