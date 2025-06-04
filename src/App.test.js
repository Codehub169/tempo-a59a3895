import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

// Mock react-router-dom to prevent errors during testing of components that use Link/NavLink
// jest.mock('react-router-dom', () => ({
//   ...jest.requireActual('react-router-dom'), // import and retain default behavior
//   useNavigate: () => jest.fn(),
//   useLocation: () => ({ pathname: '/' }),
// }));

test('renders RentRightNL logo in header', () => {
  render(<App />); 
  // The logo text is 'RentRightNL', with 'NL' in a span. 
  // We can look for part of it or use a more robust selector if needed.
  const logoElement = screen.getByText(/RentRight/i);
  expect(logoElement).toBeInTheDocument();
});

test('renders footer text', () => {
  render(<App />);
  const footerElement = screen.getByText(/© \d{4} RentRightNL. Empowering renters with transparency./i);
  expect(footerElement).toBeInTheDocument();
});

// Basic smoke test for rendering main page components (if needed, could be more specific)
test('renders Home link in header', () => {
  render(<App />);
  // Check for a link that would typically be in the Header
  const homeLink = screen.getAllByRole('link', { name: /home/i });
  expect(homeLink.length).toBeGreaterThan(0);
  expect(homeLink[0]).toBeInTheDocument();
});

// Add more tests as components and functionality are built out.
// For example, testing navigation, page content rendering based on routes, etc.
