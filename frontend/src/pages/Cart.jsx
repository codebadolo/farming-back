import React, { useState, useEffect } from 'react';
import { api } from '../services/api.jsx';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);

  useEffect(() => {
    fetchCartItems();
  }, []);

   const fetchCartItems = async () => {
    try {
      const response = await apiService.getPanier();
      setCartItems(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement du panier:', error);
    } finally {
      setLoading(false);
    }
  };
 const updateQuantity = async (itemId, newQuantity) => {
    try {
      await apiService.updatePanier(itemId, { qte_produit: newQuantity });
      fetchCartItems();
    } catch (error) {
      console.error('Erreur lors de la mise à jour:', error);
    }
  };

  const removeItem = async (itemId) => {
    try {
      await apiService.supprimerDuPanier(itemId);
      fetchCartItems();
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
    }
  };

  const calculateTotal = () => {
    return cartItems.reduce((total, item) => total + (item.produit.prix * item.qte_produit), 0);
  };

  if (loading) {
    return <div className="flex justify-center items-center min-h-screen">Chargement...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Mon Panier</h1>
        
        {cartItems.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-gray-500 text-lg">Votre panier est vide</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              {cartItems.map((item) => (
                <div key={item.id} className="bg-white rounded-lg shadow-md p-6 mb-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <img 
                        src={item.produit.image || '/placeholder.jpg'} 
                        alt={item.produit.nom}
                        className="w-20 h-20 object-cover rounded"
                      />
                      <div>
                        <h3 className="font-semibold text-lg">{item.produit.nom}</h3>
                        <p className="text-gray-600">{item.produit.prix} FCFA</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        <button 
                          onClick={() => updateQuantity(item.id, item.qte_produit - 1)}
                          className="bg-gray-200 px-2 py-1 rounded"
                          disabled={item.qte_produit <= 1}
                        >
                          -
                        </button>
                        <span className="px-4">{item.qte_produit}</span>
                        <button 
                          onClick={() => updateQuantity(item.id, item.qte_produit + 1)}
                          className="bg-gray-200 px-2 py-1 rounded"
                        >
                          +
                        </button>
                      </div>
                      <button 
                        onClick={() => removeItem(item.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        Supprimer
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6 h-fit">
              <h2 className="text-xl font-semibold mb-4">Résumé de la commande</h2>
              <div className="space-y-2 mb-4">
                <div className="flex justify-between">
                  <span>Sous-total:</span>
                  <span>{calculateTotal()} FCFA</span>
                </div>
                <div className="flex justify-between">
                  <span>Livraison:</span>
                  <span>Gratuite</span>
                </div>
                <div className="border-t pt-2">
                  <div className="flex justify-between font-semibold">
                    <span>Total:</span>
                    <span>{calculateTotal()} FCFA</span>
                  </div>
                </div>
              </div>
              <button className="w-full bg-faso-purple text-white py-3 rounded-lg hover:bg-opacity-90">
                Procéder au paiement
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Cart;
