import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="site-footer bg-text-dark text-secondary-color py-10 text-center mt-auto">
      <div className="container mx-auto px-4">
        <p className="mb-2 text-sm">&copy; {new Date().getFullYear()} RentRightNL. Empowering renters with transparency.</p>
        <p className="mb-2 text-sm">This is a design prototype. Not a functional service.</p>
        <p className="text-sm">
          <Link to="/about-wws" className="text-primary-color hover:underline">
            Learn more about the WWS
          </Link>
        </p>
      </div>
    </footer>
  );
};

export default Footer;
