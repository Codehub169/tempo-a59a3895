import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
    faMapMarkerAlt, faRulerCombined, faDoorOpen, faWater, faUtensils, faWifi, 
    faTshirt, faThermometerHalf, faCouch, faWind, faSoap, faArrowsAltV, 
    faConciergeBell, faLayerGroup, faTree, faChild, faBookReader, faParking, 
    faLeaf, faBusAlt, faBlender, faSortAmountUpAlt, faCity, faPaw, faArchive,
    faMapMarkedAlt, faEnvelope, faInfoCircle
} from '@fortawesome/free-solid-svg-icons';

const listingsData = {
    1: {
        id: 1,
        title: "Charming Canal View Apartment",
        location: "Amsterdam Centrum",
        images: [
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YXBhcnRtZW50JTIwaW50ZXJpb3J8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjJ8fGFwYXJ0bWVudCUyMGludGVyaW9yJTIwbGl2aW5nJTIwcm9vbXxlbnwwfHwwfHx8MA%3D&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1616046229478-9901c5536a45?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTF8fGFwYXJ0bWVudCUyMGludGVyaW9yJTIwYmVkcm9vbXxlbnwwfHwwfHx8MA%3D&auto=format&fit=crop&w=400&q=80"
        ],
        advertisedRent: 1850,
        size: 75,
        rooms: 2,
        wwsPoints: 140,
        maxLegalRent: 1050.75,
        description: "Experience the charm of Amsterdam in this beautifully renovated 2-room apartment with stunning canal views. Located in the heart of the city, you're steps away from shops, restaurants, and cultural attractions. The apartment features a modern kitchen, a bright living space, and a comfortable bedroom. Perfect for a single professional or a couple.",
        amenities: [
            { name: "Canal View", icon: faWater },
            { name: "Modern Kitchen", icon: faUtensils },
            { name: "Wi-Fi Included", icon: faWifi },
            { name: "Washer", icon: faTshirt }, 
            { name: "Central Heating", icon: faThermometerHalf },
            { name: "Furnished", icon: faCouch }
        ],
        wwsBreakdown: [
            { item: "Surface Area (75 m&sup2;)", points: 60 },
            { item: "Energy Label (B)", points: 25 },
            { item: "Kitchen Amenities", points: 15 },
            { item: "Bathroom Standard", points: 10 },
            { item: "WOZ Value (Location)", points: 25 },
            { item: "Outdoor Space (Balcony)", points: 5 }
        ]
    },
    2: { 
        id: 2,
        title: "Modern Loft in De Pijp",
        location: "Amsterdam De Pijp",
        images: [
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8YXBhcnRtZW50JTIwaW50ZXJpb3J8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8bW9kZXJuJTIwYXBhcnRtZW50JTIwaW50ZXJpb3J8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1505691938895-1758d7feb511?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8YmVkcm9vbSUyMGludGVyaW9yfGVufDB8fDB8fHww&auto=format&fit=crop&w=400&q=80"
        ],
        advertisedRent: 2200,
        size: 90,
        rooms: 3,
        wwsPoints: 165,
        maxLegalRent: 1250.50,
        description: "Spacious and stylish loft apartment in the vibrant De Pijp district. This 3-room apartment boasts high ceilings, large windows offering plenty of natural light, and a contemporary design. Features an open-plan living area, fully equipped kitchen, two well-sized bedrooms, and a modern bathroom. Includes a lovely balcony overlooking the street. Ideal for those seeking a trendy urban lifestyle.",
        amenities: [
            { name: "Balcony", icon: faWind },
            { name: "Dishwasher", icon: faSoap }, 
            { name: "High Ceilings", icon: faArrowsAltV },
            { name: "Open Kitchen", icon: faConciergeBell }, 
            { name: "Wooden Floors", icon: faLayerGroup } 
        ],
        wwsBreakdown: [
            { item: "Surface Area (90 m&sup2;)", points: 75 },
            { item: "Energy Label (A)", points: 35 },
            { item: "Kitchen Deluxe", points: 20 },
            { item: "Luxury Bathroom", points: 15 },
            { item: "WOZ Value (Prime Location)", points: 20 }
        ]
    },
     3: {
        id: 3,
        title: "Spacious Family Home",
        location: "Utrecht Oost",
        images: [
            "https://images.unsplash.com/photo-1493809842364-78817add7ffb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGFwYXJ0bWVudCUyMGV4dGVyaW9yfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1513584684374-8BAB748fbf90?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGFwYXJ0bWVudCUyMGV4dGVyaW9yfGVufDB8fDB8fHww&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1570129477492-45c003edd2be?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8aG91c2V8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=400&q=80"
        ],
        advertisedRent: 2400,
        size: 120, 
        rooms: 4,
        wwsPoints: 170,
        maxLegalRent: 1380.00,
        description: "A wonderful family home in a quiet, green neighborhood of Utrecht. Features a large living room, separate dining area, modern kitchen, three bedrooms, a study, and a garden. Perfect for families looking for space and comfort. Close to schools, parks, and public transport.",
        amenities: [
            { name: "Garden", icon: faTree },
            { name: "Family Friendly", icon: faChild },
            { name: "Study Room", icon: faBookReader },
            { name: "Parking", icon: faParking },
            { name: "Quiet Area", icon: faLeaf }
        ],
        wwsBreakdown: [
            { item: "Surface Area (120 m&sup2;)", points: 90 },
            { item: "Energy Label (A+)", points: 40 },
            { item: "Full Kitchen & Bath", points: 20 },
            { item: "WOZ Value (Utrecht)", points: 15 },
            { item: "Garden (50m2)", points: 5 }
        ]
    },
    4: {
        id: 4,
        title: "Cozy Studio near Station",
        location: "Rotterdam Centraal",
         images: [
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGFwYXJ0bWVudCUyMGV4dGVyaW9yfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1600585152220-90363fe7e115?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTd8fHN0dWRpbyUyMGFwYXJ0bWVudHxlbnwwfHwwfHx8MA%3D&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1594489980100-c6a94f365602?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjN8fHN0dWRpbyUyMGFwYXJ0bWVudHxlbnwwfHwwfHx8MA%3D&auto=format&fit=crop&w=400&q=80"
        ],
        advertisedRent: 1100,
        size: 45,
        rooms: 1,
        wwsPoints: 125,
        maxLegalRent: 850.20,
        description: "Bright and efficiently designed studio apartment, perfect for a young professional or student. Located minutes away from Rotterdam Centraal station, offering excellent connectivity. The studio is fully furnished and includes a compact kitchen and a modern bathroom.",
        amenities: [
            { name: "Near Public Transport", icon: faBusAlt },
            { name: "Compact Kitchen", icon: faBlender },
            { name: "Elevator", icon: faSortAmountUpAlt },
            { name: "City Center", icon: faCity },
            { name: "Furnished", icon: faCouch }
        ],
        wwsBreakdown: [
            { item: "Surface Area (45 m&sup2;)", points: 40 },
            { item: "Energy Label (C)", points: 20 },
            { item: "Kitchenette", points: 10 },
            { item: "Bathroom Standard", points: 10 },
            { item: "WOZ Value (Rotterdam)", points: 40 },
            { item: "No Outdoor Space", points: 5 }
        ]
    },
    default: { 
        id: 0,
        title: "Beautiful Apartment in Great Location",
        location: "Netherlands",
        images: [
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGFwYXJ0bWVudCUyMGV4dGVyaW9yfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1615875605825-5eb9bbd5ce0d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8YXBhcnRtZW50JTIwa2l0Y2hlbnxlbnwwfHwwfHx8MA%3D&auto=format&fit=crop&w=400&q=80",
            "https://images.unsplash.com/photo-1582582494705-f8ce0b0c276d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGFwYXJ0bWVudCUyMGJhdGhyb29tfGVufDB8fDB8fHww&auto=format&fit=crop&w=400&q=80"
        ],
        advertisedRent: 1750,
        size: 80,
        rooms: 3,
        wwsPoints: 130,
        maxLegalRent: 950.00,
        description: "This is a sample description for a lovely apartment. It features modern amenities and is located in a desirable neighborhood. Enjoy comfortable living with easy access to public transport and local shops. The WWS point system helps ensure fair pricing.",
        amenities: [
            { name: "Balcony", icon: faWind },
            { name: "Dishwasher", icon: faSoap }, 
            { name: "Elevator", icon: faSortAmountUpAlt }, 
            { name: "Pet Friendly", icon: faPaw },
            { name: "Storage", icon: faArchive }
        ],
        wwsBreakdown: [
            { item: "Surface Area (80 m&sup2;)", points: 65 },
            { item: "Energy Label (C)", points: 20 },
            { item: "Sanitary Facilities", points: 12 },
            { item: "Kitchen Standard", points: 13 },
            { item: "WOZ Value Factor", points: 20 }
        ]
    }
};

const ListingDetailPage = () => {
    const { id } = useParams();
    const [listing, setListing] = useState(null);
    const [contactMessage, setContactMessage] = useState("This is a prototype. Contact functionality is for demonstration.");
    const [contactButtonDisabled, setContactButtonDisabled] = useState(false);

    useEffect(() => {
        // Simulate API call or data fetching
        const fetchedListing = listingsData[id] || listingsData.default;
        setListing(fetchedListing);
        document.title = `${fetchedListing.title} - RentRightNL`;
    }, [id]);

    if (!listing) {
        return <div className="container py-10 text-center mx-auto">Loading listing details...</div>;
    }

    let rentDifference = listing.advertisedRent - listing.maxLegalRent;
    let comparisonClass = '';
    let comparisonText = '';
    // const liberalisationThresholdRent = 879.66; // Example for 2024, currently unused in logic
    const liberalisationPointsThreshold = 136; // Example for 2024

    if (listing.wwsPoints >= liberalisationPointsThreshold) {
        comparisonClass = 'neutral';
        comparisonText = `Likely in liberalized sector (WWS points: ${listing.wwsPoints} &ge; ${liberalisationPointsThreshold}). Max legal rent is indicative.`;
    } 
    else if (listing.advertisedRent > listing.maxLegalRent) {
         comparisonClass = 'overpriced';
         comparisonText = `This is &#8364;${rentDifference.toFixed(2)} above the max legal rent.`;
    } else if (listing.advertisedRent < listing.maxLegalRent) {
        comparisonClass = 'fair';
        comparisonText = `This is &#8364;${Math.abs(rentDifference).toFixed(2)} below the max legal rent. Good deal!`;
    } else { 
        comparisonClass = 'fair';
        comparisonText = `Priced exactly at the max legal rent.`;
    }

    const handleContactLister = () => {
        setContactMessage("Thank you! Your (mock) inquiry has been sent.");
        setContactButtonDisabled(true);
    };

    const renderGallery = () => {
        if (!listing.images || listing.images.length === 0) {
            return <img src="https://placehold.co/800x500/007bff/white?text=Apartment+Image&font=poppins" alt={listing.title} className="w-full h-auto max-h-[500px] object-cover rounded-lg" />;
        }
        if (listing.images.length === 1) {
            return <img src={listing.images[0]} alt={listing.title} className="w-full h-auto max-h-[500px] object-cover rounded-lg" />;
        }
        // Grid for 2 or more images
        return (
            <div className="grid grid-cols-2 md:grid-cols-gallery_detail_page_layout grid-rows-gallery_detail_page_layout_rows gap-2 max-h-[500px] rounded-lg overflow-hidden">
                {listing.images.slice(0, 5).map((img, index) => (
                    <img 
                        key={index} 
                        src={img} 
                        alt={`${listing.title} - View ${index + 1}`}
                        className={`w-full h-full object-cover ${index === 0 ? 'md:row-span-2 md:col-span-2' : ''}`}
                    />
                ))}
            </div>
        );
    }

    return (
        <main className="listing-detail-section py-8 bg-gray-50">
            <div className="container max-w-5xl mx-auto px-4">
                <div className="listing-title-bar mb-6">
                    <h1 className="font-secondary text-3xl md:text-4xl font-bold text-text-dark mb-1">{listing.title}</h1>
                    <p className="location text-lg text-text-light flex items-center">
                        <FontAwesomeIcon icon={faMapMarkerAlt} className="mr-2 text-primary" /> {listing.location}
                    </p>
                </div>

                <div className="listing-gallery mb-8 shadow-md bg-secondary rounded-lg overflow-hidden">
                    {renderGallery()}
                </div>

                <div className="listing-main-content grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="listing-content-column lg:col-span-2 space-y-6">
                        <div className="listing-info listing-description bg-white p-6 rounded-md shadow-sm border border-border-color">
                            <h2 className="font-secondary text-2xl font-semibold mb-4 pb-2 border-b border-border-color text-text-dark">About this Apartment</h2>
                            <p className="mb-3 text-base">
                                <strong className="font-semibold"><FontAwesomeIcon icon={faRulerCombined} className="mr-1 text-primary" /> {listing.size} m&sup2;</strong>  |  
                                <strong className="font-semibold"><FontAwesomeIcon icon={faDoorOpen} className="mr-1 text-primary" /> {listing.rooms} room(s)</strong>
                            </p>
                            <p className="text-text-dark leading-relaxed">{listing.description}</p>
                        </div>

                        <div className="listing-info amenities bg-white p-6 rounded-md shadow-sm border border-border-color">
                            <h2 className="font-secondary text-2xl font-semibold mb-4 pb-2 border-b border-border-color text-text-dark">Amenities</h2>
                            <ul className="amenities-list grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-3">
                                {listing.amenities.map((amenity, index) => (
                                    <li key={index} className="flex items-center text-sm p-2 bg-secondary rounded border border-border-color">
                                        <FontAwesomeIcon icon={amenity.icon} className="text-primary mr-3 w-5 text-center" /> {amenity.name}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        
                        <div className="map-placeholder h-72 bg-secondary rounded-md flex flex-col items-center justify-center text-text-light text-center border border-border-color shadow-sm">
                            <FontAwesomeIcon icon={faMapMarkedAlt} size="3x" className="mb-3" />
                            <p className="text-xl">Map Area (Placeholder)</p>
                            <p className="text-sm"><small>Interactive map coming soon!</small></p>
                        </div>
                    </div>

                    <aside className="listing-sidebar lg:col-span-1">
                        <div className="sticky top-24 space-y-6">
                            <div className="price-summary-box bg-white p-6 rounded-md shadow-md border border-border-color">
                                <div className="advertised-rent text-3xl font-bold text-text-dark mb-1">&#8364;{listing.advertisedRent.toLocaleString('nl-NL')} <span className="text-base font-normal text-text-light">/month</span></div>
                                <div className="max-legal-rent text-base mb-3">
                                    Max Legal Rent (WWS): <strong className="text-accent font-bold">&#8364;{listing.maxLegalRent.toLocaleString('nl-NL', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong>
                                </div>
                                <div className={`rent-comparison-detail font-semibold text-sm p-3 rounded text-center border ${comparisonClass === 'fair' ? 'bg-green-100 text-accent border-accent' : comparisonClass === 'overpriced' ? 'bg-red-100 text-error border-error' : 'bg-gray-100 text-text-light border-border-color'}`}>
                                    {comparisonText}
                                </div>
                            </div>

                            <div className="wws-details bg-white p-6 rounded-md shadow-md border border-border-color">
                                <h2 className="font-secondary text-xl font-semibold mb-3 pb-2 border-b border-border-color text-text-dark">WWS Points Breakdown</h2>
                                <div className="wws-points-total text-xl font-bold text-primary text-center mb-4 p-2 bg-secondary rounded">
                                    {listing.wwsPoints} <span className="block text-sm font-medium text-text-dark">Total WWS Points</span>
                                </div>
                                <ul className="wws-breakdown-list space-y-2 text-sm">
                                    {listing.wwsBreakdown.map((item, index) => (
                                        <li key={index} className="flex justify-between pb-1 border-b border-dashed border-border-color last:border-b-0">
                                            <span>{item.item}</span>
                                            <span className="points font-semibold text-primary">{item.points} pts</span>
                                        </li>
                                    ))}
                                </ul>
                                <Link to="/about-wws" className="wws-explanation-link block text-right mt-4 text-sm text-primary hover:underline font-medium">
                                    How is this calculated? <FontAwesomeIcon icon={faInfoCircle} />
                                </Link>
                            </div>

                            <div className="contact-box bg-white p-6 rounded-md shadow-md border border-border-color">
                                <h2 className="font-secondary text-xl font-semibold mb-4 text-text-dark">Interested?</h2>
                                <button 
                                    type="button" 
                                    id="contactListerBtn" 
                                    onClick={handleContactLister}
                                    disabled={contactButtonDisabled}
                                    className={`w-full py-3 px-4 bg-accent text-white-color rounded-md text-lg font-semibold cursor-pointer transition-colors duration-300 flex items-center justify-center ${contactButtonDisabled ? 'bg-text-light cursor-not-allowed' : 'hover:bg-green-700'}`}
                                >
                                    <FontAwesomeIcon icon={faEnvelope} className="mr-2" /> Contact Lister
                                </button>
                                <p id="contactMessage" className={`text-xs text-center mt-3 ${contactButtonDisabled ? 'text-accent' : 'text-text-light'}`}>{contactMessage}</p>
                            </div>
                        </div>
                    </aside>
                </div>
            </div>
        </main>
    );
};

export default ListingDetailPage;
