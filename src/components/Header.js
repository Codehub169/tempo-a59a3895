import React, { useState, useEffect } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars, faTimes } from '@fortawesome/free-solid-svg-icons';

const Header = () => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const location = useLocation();

    const toggleMobileMenu = () => {
        setIsMobileMenuOpen(!isMobileMenuOpen);
    };

    // Close mobile menu on route change
    useEffect(() => {
        setIsMobileMenuOpen(false);
    }, [location]);

    const navLinkClasses = ({ isActive }) => 
        `py-2 px-1 font-medium transition-colors duration-300 hover:text-primary ${isActive ? 'text-primary border-b-2 border-primary' : 'text-text-dark'}`;

    return (
        <header className="site-header bg-white-color py-4 border-b border-border-color sticky top-0 z-50 shadow-sm">
            <div className="container mx-auto px-4 flex justify-between items-center">
                <Link to="/" className="logo font-secondary text-2xl md:text-3xl font-bold text-primary">
                    RentRight<span className="text-accent">NL</span>
                </Link>
                
                {/* Mobile Menu Toggle Button */}
                <button 
                    className="mobile-nav-toggle md:hidden text-2xl text-text-dark bg-transparent border-none cursor-pointer"
                    onClick={toggleMobileMenu}
                    aria-label="Toggle navigation"
                    aria-expanded={isMobileMenuOpen}
                >
                    <FontAwesomeIcon icon={isMobileMenuOpen ? faTimes : faBars} />
                </button>

                {/* Desktop Navigation */}
                <nav className="main-nav hidden md:flex md:items-center">
                    <ul className="flex gap-6 items-center">
                        <li><NavLink to="/" className={navLinkClasses} end>Home</NavLink></li>
                        <li><NavLink to="/about-wws" className={navLinkClasses}>About WWS</NavLink></li>
                    </ul>
                </nav>
            </div>

            {/* Mobile Navigation Menu */}
            {isMobileMenuOpen && (
                <nav className="main-nav-mobile md:hidden bg-white-color shadow-md absolute top-full left-0 right-0 border-t border-border-color py-4 z-40">
                    <ul className="flex flex-col items-center gap-4">
                        <li><NavLink to="/" className={navLinkClasses} onClick={toggleMobileMenu} end>Home</NavLink></li>
                        <li><NavLink to="/about-wws" className={navLinkClasses} onClick={toggleMobileMenu}>About WWS</NavLink></li>
                    </ul>
                </nav>
            )}
        </header>
    );
};

export default Header;
