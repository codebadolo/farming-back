
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import ProductCard from '../components/ProductCard.jsx';
import apiService from '../services/api';

const Home = () => {
  const [produits, setProduits] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [produitsRes, categoriesRes] = await Promise.all([
          apiService.getProduits(),
          apiService.getCategories()
        ]);
        setProduits(produitsRes.data.slice(0, 8)); // Afficher les 8 premiers
        setCategories(categoriesRes.data.slice(0, 6)); // Afficher 6 catégories
      } catch (error) {
        console.error('Erreur lors du chargement:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-faso-purple"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-faso-purple to-faso-orange text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Bienvenue chez FASO FARM SHOP
            </h1>
            <p className="text-xl md:text-2xl mb-8">
              Votre boutique en ligne pour les meilleurs produits d'élevage
            </p>
            <Link 
              to="/produits" 
              className="bg-white text-faso-purple px-8 py-3 rounded-lg font-bold text-lg hover:bg-gray-100 transition-colors inline-block"
            >
              Découvrir nos produits
            </Link>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Nos Catégories
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories.map((categorie) => (
              <Link 
                key={categorie.id} 
                to={`/categories/${categorie.id}`}
                className="text-center group"
              >
                <div className="bg-white rounded-full w-20 h-20 mx-auto mb-4 flex items-center justify-center shadow-lg hover:shadow-xl transition-shadow group-hover:scale-105 transform duration-200">
                  <span className="text-2xl">🐄</span>
                </div>
                <h3 className="font-semibold text-gray-900 group-hover:text-faso-purple transition-colors">
                  {categorie.nom}
                </h3>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900">
              Produits Populaires
            </h2>
            <Link 
              to="/produits" 
              className="text-faso-purple hover:text-faso-orange font-semibold"
            >
              Voir tous les produits →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {produits.map((produit) => (
              <ProductCard key={produit.id} produit={produit} />
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-faso-purple text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-6">
            Rejoignez notre communauté d'éleveurs
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Découvrez des produits de qualité directement des fermes locales et soutenez l'agriculture durable.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/vendeurs" 
              className="bg-faso-orange text-white px-8 py-3 rounded-lg font-bold hover:bg-orange-600 transition-colors"
            >
              Devenir Vendeur
            </Link>
            <Link 
              to="/contact" 
              className="border-2 border-white text-white px-8 py-3 rounded-lg font-bold hover:bg-white hover:text-faso-purple transition-colors"
            >
              Nous Contacter
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;