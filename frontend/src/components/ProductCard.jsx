import React, { useState } from 'react';

const ProductCard = ({ produit }) => {
  const [imageError, setImageError] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleAddToCart = async () => {
    setIsLoading(true);
    try {
      // Ici on pourrait ajouter la logique d'ajout au panier
      console.log('Ajout au panier:', produit.id);
      // Simulation d'une requête API
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error('Erreur lors de l\'ajout au panier:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('fr-FR').format(price);
  };

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
      {/* Image du produit */}
      <div className="relative aspect-w-16 aspect-h-9 bg-gray-100">
        {!imageError ? (
          <img 
            src={produit.image || '/placeholder-product.jpg'} 
            alt={produit.nom}
            className="w-full h-48 object-cover transition-transform duration-300 hover:scale-105"
            onError={() => setImageError(true)}
          />
        ) : (
          <div className="w-full h-48 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
            <div className="text-center">
              <svg className="w-12 h-12 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <p className="text-gray-500 text-sm">Image non disponible</p>
            </div>
          </div>
        )}
        
        {/* Badge de disponibilité */}
        <div className="absolute top-3 right-3">
          <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full font-semibold">
            Disponible
          </span>
        </div>
      </div>

      {/* Contenu de la carte */}
      <div className="p-6">
        {/* Nom du produit */}
        <h3 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2 hover:text-purple-700 transition-colors">
          {produit.nom}
        </h3>
        
        {/* Description */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-3 leading-relaxed">
          {produit.description}
        </p>
        
        {/* Prix et bouton */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-orange-600">
              {formatPrice(produit.prix)} CFA
            </span>
            {produit.prix_unitaire && (
              <span className="text-sm text-gray-500">
                {formatPrice(produit.prix_unitaire)} CFA/kg
              </span>
            )}
          </div>
          
          <button 
            onClick={handleAddToCart}
            disabled={isLoading}
            className="bg-purple-700 text-white px-4 py-2 rounded-lg hover:bg-purple-800 transition-all duration-200 font-medium flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Ajout...</span>
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5H19" />
                </svg>
                <span>Ajouter</span>
              </>
            )}
          </button>
        </div>
        
        {/* Informations supplémentaires */}
        <div className="border-t pt-4 space-y-2">
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-500">Vendeur:</span>
            <span className="font-medium text-gray-700">
              {produit.vendeur?.entreprise || 'Non spécifié'}
            </span>
          </div>
          
          {produit.poids && (
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-500">Poids:</span>
              <span className="font-medium text-gray-700">{produit.poids} kg</span>
            </div>
          )}
          
          {produit.categorie && (
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-500">Catégorie:</span>
              <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full text-xs font-medium">
                {produit.categorie.nom}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;