
import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-faso-purple text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">FASO FARM SHOP</h3>
            <p className="text-sm text-gray-300">
              Votre boutique en ligne pour les produits d'élevage de qualité.
            </p>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Liens rapides</h3>
            <ul className="text-sm space-y-2">
              <li><a href="/" className="hover:text-faso-orange">Accueil</a></li>
              <li><a href="/products" className="hover:text-faso-orange">Produits</a></li>
              <li><a href="/about" className="hover:text-faso-orange">À propos</a></li>
              <li><a href="/contact" className="hover:text-faso-orange">Contact</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <p className="text-sm text-gray-300">
              Email: maxyax99@gmail.com<br />
              Téléphone: +226 79015091
            </p>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-sm text-gray-300">
          <p>&copy; 2024 FASO FARM SHOP. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
