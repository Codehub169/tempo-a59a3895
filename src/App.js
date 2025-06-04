import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

// Placeholder for future Page components
const HomePage = () => <div className="container mx-auto p-4">HomePage Placeholder</div>;
const ListingDetailPage = () => <div className="container mx-auto p-4">ListingDetailPage Placeholder</div>;
const AboutWWSPage = () => <div className="container mx-auto p-4">AboutWWSPage Placeholder</div>;

// Placeholder for Header and Footer components
const Header = () => (
  <header className="bg-primary-color text-white-color p-4 shadow-md">
    <div className="container mx-auto flex justify-between items-center">
      <h1 className="text-2xl font-bold font-secondary">RentRight<span className="text-accent-color">NL</span></h1>
      <nav>
        {/* Basic navigation links - will be expanded in Header.js */}
        <a href="/" className="px-2 hover:text-secondary-color">Home</a>
        <a href="/about-wws" className="px-2 hover:text-secondary-color">About WWS</a>
      </nav>
    </div>
  </header>
);

const Footer = () => (
  <footer className="bg-text-dark text-secondary-color p-4 text-center mt-8">
    <div className="container mx-auto">
      <p>&copy; 2024 RentRightNL. Empowering renters with transparency.</p>
      <p>This is a React application. Styling with Tailwind CSS.</p>
    </div>
  </footer>
);

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Header />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<HomePage />} />
            {/* Example route for listing detail page - will be dynamic */}
            <Route path="/listing/:id" element={<ListingDetailPage />} />
            <Route path="/about-wws" element={<AboutWWSPage />} />
            {/* Default route for non-matching paths (optional) */}
            {/* <Route path="*" element={<NotFoundPage />} /> */}
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
