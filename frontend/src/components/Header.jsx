import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-600 via-purple-700 to-orange-500 rounded-full flex items-center justify-center mr-3 relative overflow-hidden">
                {/* Sacs shopping stylisés */}
                <div className="relative">
                  <div className="w-8 h-10 bg-gradient-to-b from-orange-400 to-orange-600 rounded-lg transform -rotate-12 relative">
                    <div className="absolute top-1 left-1 right-1 h-2 bg-orange-300 rounded-t-lg"></div>
                    <div className="absolute top-0 left-2 w-4 h-1 bg-orange-500 rounded-full"></div>
                  </div>
                  <div className="absolute -top-1 -right-1 w-6 h-8 bg-gradient-to-b from-pink-500 to-purple-600 rounded-lg transform rotate-12">
                    <div className="absolute top-1 left-1 right-1 h-2 bg-pink-400 rounded-t-lg"></div>
                    <div className="absolute top-0 left-1 w-3 h-1 bg-pink-600 rounded-full"></div>
                  </div>
                </div>
                {/* Orbite dorée */}
                <div className="absolute inset-0 border-2 border-yellow-400 rounded-full transform rotate-45"></div>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-purple-700">FASO FARM SHOP</h1>
                <p className="text-sm text-gray-600">Votre Boutique Votre Magasin</p>
              </div>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            <Link 
              to="/" 
              className="text-gray-700 hover:text-purple-700 font-medium transition-colors duration-200"
            >
              Accueil
            </Link>
            <Link 
              to="/produits" 
              className="text-gray-700 hover:text-purple-700 font-medium transition-colors duration-200"
            >
              Produits
            </Link>
            <Link 
              to="/categories" 
              className="text-gray-700 hover:text-purple-700 font-medium transition-colors duration-200"
            >
              Catégories
            </Link>
            <Link 
              to="/vendeurs" 
              className="text-gray-700 hover:text-purple-700 font-medium transition-colors duration-200"
            >
              Vendeurs
            </Link>
            <Link 
              to="/contact" 
              className="text-gray-700 hover:text-purple-700 font-medium transition-colors duration-200"
            >
              Contact
            </Link>
          </nav>

          {/* Actions */}
          <div className="flex items-center space-x-4">
            {/* Bouton recherche */}
            <button className="text-gray-700 hover:text-purple-700 transition-colors duration-200">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
            
            {/* Panier */}
            <Link to="/panier" className="text-gray-700 hover:text-purple-700 relative transition-colors duration-200">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5H19" />
              </svg>
              <span className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-semibold">
                0
              </span>
            </Link>
            
            {/* Bouton connexion */}
            <Link 
              to="/login" 
              className="bg-purple-700 text-white px-6 py-2 rounded-lg hover:bg-purple-800 transition-colors duration-200 font-medium"
            >
              Connexion
            </Link>
          </div>

          {/* Menu mobile */}
          <div className="md:hidden">
            <button className="text-gray-700 hover:text-purple-700">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
