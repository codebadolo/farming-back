import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from '../pages/Home';
import Products from '../pages/Products';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/produits" element={<Products />} />
      <Route path="/categories" element={
        <div className="p-8 min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Catégories</h1>
            <p className="text-gray-600">Page des catégories en cours de développement</p>
          </div>
        </div>
      } />
      <Route path="/vendeurs" element={
        <div className="p-8 min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Vendeurs</h1>
            <p className="text-gray-600">Page des vendeurs en cours de développement</p>
          </div>
        </div>
      } />
      <Route path="/contact" element={
        <div className="p-8 min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Contact</h1>
            <p className="text-gray-600">Page de contact en cours de développement</p>
          </div>
        </div>
      } />
      <Route path="/panier" element={
        <div className="p-8 min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Panier</h1>
            <p className="text-gray-600">Page du panier en cours de développement</p>
          </div>
        </div>
      } />
      <Route path="/login" element={
        <div className="p-8 min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Connexion</h1>
            <p className="text-gray-600">Page de connexion en cours de développement</p>
          </div>
        </div>
      } />
      <Route path="*" element={
        <div className="p-8 min-h-screen bg-gray-50">
          <div className="max-w-7xl mx-auto text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">404</h1>
            <p className="text-gray-600">Page non trouvée</p>
          </div>
        </div>
      } />
    </Routes>
  );
};

export default AppRoutes;