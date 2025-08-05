
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import apiService from '../services/api';

const Product = () => {
  const { id } = useParams();
  const [produit, setProduit] = useState(null);
  const [produitsLies, setProduitsLies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [quantite, setQuantite] = useState(1);
  const [activeImage, setActiveImage] = useState(0);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await apiService.getProduit(id);
        setProduit(response.data);
        
        // Charger les produits liés de la même catégorie
        if (response.data.categorie) {
          const produitsLiesRes = await apiService.getProduitsParCategorie(response.data.categorie.id);
          setProduitsLies(produitsLiesRes.data.filter(p => p.id !== parseInt(id)).slice(0, 4));
        }
      } catch (error) {
        console.error('Erreur lors du chargement du produit:', error);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchProduct();
    }
  }, [id]);

  const ajouterAuPanier = async () => {
    try {
      await apiService.ajouterAuPanier({
        produit_id: produit.id,
        quantite: quantite
      });
      alert('Produit ajouté au panier avec succès!');
    } catch (error) {
      console.error('Erreur lors de l\'ajout au panier:', error);
      alert('Erreur lors de l\'ajout au panier');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-faso-purple"></div>
      </div>
    );
  }

  if (!produit) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Produit non trouvé</h2>
        <Link to="/produits" className="text-faso-purple hover:text-faso-orange">
          Retour aux produits
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Breadcrumb */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <nav className="flex" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-4">
              <li>
                <Link to="/" className="text-gray-500 hover:text-faso-purple">
                  Accueil
                </Link>
              </li>
              <li>
                <span className="text-gray-500">/</span>
              </li>
              <li>
                <Link to="/produits" className="text-gray-500 hover:text-faso-purple">
                  Produits
                </Link>
              </li>
              <li>
                <span className="text-gray-500">/</span>
              </li>
              <li>
                <span className="text-gray-900 font-medium">{produit.nom}</span>
              </li>
            </ol>
          </nav>
        </div>
      </div>

      {/* Product Details */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Images */}
          <div className="space-y-4">
            <div className="aspect-w-1 aspect-h-1 bg-gray-200 rounded-lg overflow-hidden">
              <img
                src={produit.image || '/api/placeholder/600/600'}
                alt={produit.nom}
                className="w-full h-full object-center object-cover"
              />
            </div>
            {/* Gallery thumbnails could go here */}
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{produit.nom}</h1>
              <p className="text-sm text-gray-500 mt-2">
                Catégorie: {produit.categorie?.nom} | Vendeur: {produit.vendeur?.nom}
              </p>
            </div>

            <div className="flex items-center space-x-4">
              <span className="text-3xl font-bold text-faso-purple">
                {produit.prix_unitaire} FCFA
              </span>
              {produit.prix_promo && (
                <span className="text-xl text-gray-500 line-through">
                  {produit.prix_promo} FCFA
                </span>
              )}
            </div>

            <div className="prose max-w-none">
              <h3 className="text-lg font-medium text-gray-900">Description</h3>
              <p className="text-gray-600">{produit.description}</p>
            </div>

            {/* Stock Status */}
            <div className="flex items-center space-x-2">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                produit.stock > 0 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {produit.stock > 0 ? `En stock (${produit.stock})` : 'Rupture de stock'}
              </span>
            </div>

            {/* Add to Cart */}
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <label htmlFor="quantite" className="text-sm font-medium text-gray-700">
                  Quantité:
                </label>
                <select
                  id="quantite"
                  value={quantite}
                  onChange={(e) => setQuantite(parseInt(e.target.value))}
                  className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-faso-purple focus:border-faso-purple"
                >
                  {[...Array(Math.min(produit.stock, 10))].map((_, i) => (
                    <option key={i + 1} value={i + 1}>
                      {i + 1}
                    </option>
                  ))}
                </select>
              </div>

              <button
                onClick={ajouterAuPanier}
                disabled={produit.stock === 0}
                className="w-full bg-faso-purple text-white py-3 px-6 rounded-lg font-semibold hover:bg-faso-purple/90 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                {produit.stock > 0 ? 'Ajouter au panier' : 'Rupture de stock'}
              </button>
            </div>

            {/* Additional Info */}
            <div className="border-t pt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Informations supplémentaires</h3>
              <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Unité</dt>
                  <dd className="mt-1 text-sm text-gray-900">{produit.unite}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Poids</dt>
                  <dd className="mt-1 text-sm text-gray-900">{produit.poids || 'Non spécifié'}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Date d'ajout</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {new Date(produit.date_creation).toLocaleDateString('fr-FR')}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Vendeur</dt>
                  <dd className="mt-1 text-sm text-gray-900">{produit.vendeur?.nom}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>

        {/* Related Products */}
        {produitsLies.length > 0 && (
          <div className="mt-16">
            <h2 className="text-2xl font-bold text-gray-900 mb-8">Produits similaires</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {produitsLies.map((produitLie) => (
                <Link
                  key={produitLie.id}
                  to={`/produit/${produitLie.id}`}
                  className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
                >
                  <div className="aspect-w-1 aspect-h-1 bg-gray-200 rounded-t-lg overflow-hidden">
                    <img
                      src={produitLie.image || '/api/placeholder/300/300'}
                      alt={produitLie.nom}
                      className="w-full h-48 object-center object-cover"
                    />
                  </div>
                  <div className="p-4">
                    <h3 className="text-lg font-semibold text-gray-900 truncate">
                      {produitLie.nom}
                    </h3>
                    <p className="text-faso-purple font-bold mt-2">
                      {produitLie.prix_unitaire} FCFA
                    </p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Product;