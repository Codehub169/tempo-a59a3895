import axios from 'axios';

// Determine the base URL based on the environment
// For development (npm start), React runs on port 3000 and the backend on 9000.
// For production-like serving (via startup.sh after npm run build), both are on port 9000.
// REACT_APP_API_URL can override this.
// The default 'http://localhost:9000/api' ensures 'npm start' works without a proxy,
// aligning with backend CORS settings. For 'npm run build' served by FastAPI,
// REACT_APP_API_URL could be set to '/api' or this default will also work.
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:9000/api';

/**
 * Fetches all listings from the backend.
 * @returns {Promise<Array<Object>>} A promise that resolves to an array of listing objects.
 */
export const getListings = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/listings`);
    return response.data;
  } catch (error) {
    console.error('Error fetching listings:', error);
    // In a real app, you might want to throw the error or return a specific error object
    // For this project, returning an empty array or the cached mock data could be a fallback
    // For now, let's re-throw to make it clear if the API is down during development
    throw error;
  }
};

/**
 * Fetches a single listing by its ID from the backend.
 * @param {string|number} id The ID of the listing to fetch.
 * @returns {Promise<Object>} A promise that resolves to a single listing object.
 */
export const getListingById = async (id) => {
  if (!id && id !== 0) { // Allow ID 0 if it's a valid identifier
    console.error('Error: Listing ID is required.');
    throw new Error('Listing ID is required.');
  }
  try {
    const response = await axios.get(`${API_BASE_URL}/listings/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching listing with ID ${id}:`, error);
    throw error;
  }
};

// Example of how you might add other API calls in the future:
// export const submitContactForm = async (listingId, contactData) => {
//   try {
//     const response = await axios.post(`${API_BASE_URL}/listings/${listingId}/contact`, contactData);
//     return response.data;
//   } catch (error) {
//     console.error(`Error submitting contact form for listing ${listingId}:`, error);
//     throw error;
//   }
// };
