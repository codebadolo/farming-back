import axios from 'axios';

// Configuration de l'URL de base pour l'API Django
const API_BASE_URL = 'http://localhost:3000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Intercepteur pour les requêtes
api.interceptors.request.use(
  (config) => {
    // Vous pouvez ajouter ici des tokens d'authentification si nécessaire
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour les réponses
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Gérer l'expiration du token
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // Produits
  getProduits: () => api.get('/produits/'),
  getProduit: (id) => api.get(`/produits/${id}/`),
  createProduit: (data) => api.post('/produits/', data),
  updateProduit: (id, data) => api.put(`/produits/${id}/`, data),
  deleteProduit: (id) => api.delete(`/produits/${id}/`),
  
  // Catégories
  getCategories: () => api.get('/categories/'),
  getCategorie: (id) => api.get(`/categories/${id}/`),
  createCategorie: (data) => api.post('/categories/', data),
  updateCategorie: (id, data) => api.put(`/categories/${id}/`, data),
  deleteCategorie: (id) => api.delete(`/categories/${id}/`),
 
  getProduitsVendeur: (vendeurId) => api.get(`/produits/vendeur/${vendeurId}/`),
  ajouterAuPanier: (data) => api.post('/panier/ajouter/', data),
  rechercherProduits: (query) => api.get(`/rechercher/?q=${query}`),


  // Vendeurs
  getVendeurs: () => api.get('/vendeurs/'),
  getVendeur: (id) => api.get(`/vendeurs/${id}/`),
  createVendeur: (data) => api.post('/vendeurs/', data),
  updateVendeur: (id, data) => api.put(`/vendeurs/${id}/`, data),
  
  // Clients
  getClients: () => api.get('/clients/'),
  getClient: (id) => api.get(`/clients/${id}/`),
  createClient: (data) => api.post('/clients/', data),
  updateClient: (id, data) => api.put(`/clients/${id}/`, data),
  
  // Commandes
  getCommandes: () => api.get('/commandes/'),
  getCommande: (id) => api.get(`/commandes/${id}/`),
  createCommande: (data) => api.post('/commandes/', data),
  updateCommande: (id, data) => api.put(`/commandes/${id}/`, data),
  deleteCommande: (id) => api.delete(`/commandes/${id}/`),
  
  // Stock
  getStocks: () => api.get('/stocks/'),
  getStock: (id) => api.get(`/stocks/${id}/`),
  updateStock: (id, data) => api.put(`/stocks/${id}/`, data),
  
  // Paiements
  getMethodesPaiement: () => api.get('/paiements/methodes/'),
  initierPaiementOrangeMoney: (data) => api.post('/paiements/orange-money/initier/', data),
  initierPaiementCarteBancaire: (data) => api.post('/paiements/carte-bancaire/initier/', data),
  verifierStatutPaiement: (transactionId) => api.get(`/paiements/statut/${transactionId}/`),
  
  // Promotions
  getPromotions: () => api.get('/promotions/'),
  getPromotion: (id) => api.get(`/promotions/${id}/`),
  createPromotion: (data) => api.post('/promotions/', data),
  updatePromotion: (id, data) => api.put(`/promotions/${id}/`, data),
  deletePromotion: (id) => api.delete(`/promotions/${id}/`),
  
  // Coupons
  getCoupons: () => api.get('/coupons/'),
  getCoupon: (code) => api.get(`/coupons/${code}/`),
  createCoupon: (data) => api.post('/coupons/', data),
  updateCoupon: (code, data) => api.put(`/coupons/${code}/`, data),
  deleteCoupon: (code) => api.delete(`/coupons/${code}/`),
  
  // Panier
  getPanier: () => api.get('/panier/'),
  ajouterAuPanier: (data) => api.post('/panier/ajouter/', data),
  updatePanier: (itemId, data) => api.put(`/panier/${itemId}/`, data),
  supprimerDuPanier: (itemId) => api.delete(`/panier/${itemId}/`),
  viderPanier: () => api.delete('/panier/vider/'),
  
  // Fonctions spéciales
  getProduitsParCategorie: (categorieId) => api.get(`/produits/categorie/${categorieId}/`),
  getProduitsVendeur: (vendeurId) => api.get(`/produits/vendeur/${vendeurId}/`),
  rechercherProduits: (query) => api.get(`/rechercher/?q=${encodeURIComponent(query)}`),
  getProduitsPopulaires: () => api.get('/produits/populaires/'),
  getProduitsEnPromotion: () => api.get('/produits/promotions/'),
  
  // Authentification
  login: (data) => api.post('/auth/login/', data),
  register: (data) => api.post('/auth/register/', data),
  logout: () => api.post('/auth/logout/'),
  refreshToken: () => api.post('/auth/refresh/'),
  
  // Profil utilisateur
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (data) => api.put('/auth/profile/', data),
  changePassword: (data) => api.post('/auth/change-password/', data),
  
  // Contact
  sendContactMessage: (data) => api.post('/contact/', data),
  
  // Statistiques (pour les vendeurs/admin)
  getStatistiques: () => api.get('/statistiques/'),
  getVentesParMois: () => api.get('/statistiques/ventes-mois/'),
  getProduitsVendus: () => api.get('/statistiques/produits-vendus/'),
};

// Export par défaut de l'instance axios pour les cas spéciaux
export default api;