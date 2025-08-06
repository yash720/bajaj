import React, { useState } from "react";
import { Menu, X } from "lucide-react";
import bajajLogoPath from "@assets/bajaj-auto-bike-logo-11549750548dzky3ovjqc_1754502098000.png";

export default function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="bg-white shadow-lg border-b-2 border-bajaj-blue">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0 flex items-center">
            <img 
              src={bajajLogoPath} 
              alt="Bajaj Logo" 
              className="h-10 w-auto"
            />
          </div>

          {/* Center Title */}
          <div className="flex-1 flex justify-center">
            <h1 className="text-xl font-semibold text-bajaj-blue">
              Bajaj Intelligent Claims Assistant
            </h1>
          </div>

          {/* Desktop Navigation Links */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <a 
                href="#" 
                className="text-bajaj-blue hover:bg-bajaj-blue hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
              >
                Home
              </a>
              <a 
                href="#" 
                className="text-gray-700 hover:bg-bajaj-blue hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
              >
                About
              </a>
              <a 
                href="#" 
                className="text-gray-700 hover:bg-bajaj-blue hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
              >
                Contact
              </a>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-gray-700 hover:text-bajaj-blue"
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-gray-50">
              <a 
                href="#" 
                className="text-bajaj-blue block px-3 py-2 rounded-md text-base font-medium"
              >
                Home
              </a>
              <a 
                href="#" 
                className="text-gray-700 hover:text-bajaj-blue block px-3 py-2 rounded-md text-base font-medium"
              >
                About
              </a>
              <a 
                href="#" 
                className="text-gray-700 hover:text-bajaj-blue block px-3 py-2 rounded-md text-base font-medium"
              >
                Contact
              </a>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
