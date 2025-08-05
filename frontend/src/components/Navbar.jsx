
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-faso-purple text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0">
              <img className="h-10 w-auto" src="/logo.png" alt="FASO FARM SHOP" />
            </Link>
            <div className="ml-4">
              <h1 className="text-xl font-bold">FASO FARM SHOP</h1>
              <p className="text-xs text-faso-orange">Votre Boutique Votre Magasin</p>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <Link to="/" className="hover:bg-faso-orange px-3 py-2 rounded-md text-sm font-medium">Accueil</Link>
              <Link to="/products" className="hover:bg-faso-orange px-3 py-2 rounded-md text-sm font-medium">Produits</Link>
              <Link to="/cart" className="hover:bg-faso-orange px-3 py-2 rounded-md text-sm font-medium">Panier</Link>
              <Link to="/contact" className="hover:bg-faso-orange px-3 py-2 rounded-md text-sm font-medium">Contact</Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
