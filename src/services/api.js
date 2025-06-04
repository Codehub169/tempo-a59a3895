import axios from 'axios';

// Determine the base URL based on the environment
// For development, React typically runs on port 3000 and the backend on 8000 (or as configured).
// For production, both might be served from the same origin or a configured API URL.
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Fetches all listings from the backend.
 * @returns {Promise<Array>} A promise that resolves to an array of listing objects.
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
