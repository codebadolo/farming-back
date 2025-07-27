# Structure Frontend React.js

## Architecture Recommandée

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/           # Composants réutilisables
│   │   ├── common/          # Composants communs
│   │   │   ├── Header.js
│   │   │   ├── Footer.js
│   │   │   ├── Navbar.js
│   │   │   ├── Loading.js
│   │   │   └── Modal.js
│   │   ├── auth/            # Composants d'authentification
│   │   │   ├── LoginForm.js
│   │   │   ├── RegisterForm.js
│   │   │   └── ProfileForm.js
│   │   ├── products/        # Composants produits
│   │   │   ├── ProductCard.js
│   │   │   ├── ProductList.js
│   │   │   ├── ProductDetail.js
│   │   │   ├── ProductForm.js
│   │   │   └── CategoryTree.js
│   │   ├── cart/            # Composants panier
│   │   │   ├── CartItem.js
│   │   │   ├── CartSummary.js
│   │   │   └── Checkout.js
│   │   ├── orders/          # Composants commandes
│   │   │   ├── OrderList.js
│   │   │   ├── OrderDetail.js
│   │   │   └── OrderStatus.js
│   │   └── dashboard/       # Tableaux de bord
│   │       ├── VendorDashboard.js
│   │       ├── AdminDashboard.js
│   │       └── ClientDashboard.js
│   ├── pages/               # Pages principales
│   │   ├── Home.js
│   │   ├── Products.js
│   │   ├── ProductDetail.js
│   │   ├── Cart.js
│   │   ├── Checkout.js
│   │   ├── Profile.js
│   │   ├── Orders.js
│   │   ├── Login.js
│   │   ├── Register.js
│   │   └── Dashboard.js
│   ├── services/            # Services API
│   │   ├── api.js           # Configuration Axios
│   │   ├── authService.js   # Services d'authentification
│   │   ├── productService.js # Services produits
│   │   ├── cartService.js   # Services panier
│   │   ├── orderService.js  # Services commandes
│   │   └── paymentService.js # Services paiement
│   ├── hooks/               # Hooks personnalisés
│   │   ├── useAuth.js
│   │   ├── useCart.js
│   │   ├── useProducts.js
│   │   └── useOrders.js
│   ├── context/             # Contextes React
│   │   ├── AuthContext.js
│   │   ├── CartContext.js
│   │   └── ThemeContext.js
│   ├── utils/               # Utilitaires
│   │   ├── constants.js
│   │   ├── helpers.js
│   │   ├── validators.js
│   │   └── formatters.js
│   ├── styles/              # Styles
│   │   ├── globals.css
│   │   ├── components.css
│   │   └── tailwind.css
│   ├── App.js               # Composant principal
│   ├── App.css
│   ├── index.js             # Point d'entrée
│   └── index.css
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

## Configuration Tailwind CSS

### tailwind.config.js
```javascript
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        secondary: {
          50: '#f8fafc',
          500: '#64748b',
          600: '#475569',
        }
      }
    },
  },
  plugins: [],
}
```

## Composants Principaux

### 1. App.js
```javascript
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import Home from './pages/Home';
import Products from './pages/Products';
import ProductDetail from './pages/ProductDetail';
import Cart from './pages/Cart';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/auth/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Router>
          <div className="min-h-screen bg-gray-50">
            <Header />
            <main className="container mx-auto px-4 py-8">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/products" element={<Products />} />
                <Route path="/products/:slug" element={<ProductDetail />} />
                <Route path="/cart" element={<Cart />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route 
                  path="/dashboard" 
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  } 
                />
              </Routes>
            </main>
            <Footer />
          </div>
        </Router>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;
```

### 2. Services API

#### api.js
```javascript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
```

#### authService.js
```javascript
import api from './api';

export const authService = {
  login: async (email, password) => {
    const response = await api.post('/auth/login/', { email, password });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  register: async (userData) => {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    return api.post('/auth/logout/');
  },

  getCurrentUser: () => {
    return JSON.parse(localStorage.getItem('user'));
  },

  getProfile: () => {
    return api.get('/auth/profile/');
  }
};
```

### 3. Contextes

#### AuthContext.js
```javascript
import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const userData = authService.getCurrentUser();
      setUser(userData);
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const data = await authService.login(email, password);
    setUser(data.user);
    return data;
  };

  const register = async (userData) => {
    return await authService.register(userData);
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
```

## Installation et Configuration

### 1. Créer l'application React
```bash
npx create-react-app frontend
cd frontend
```

### 2. Installer les dépendances
```bash
npm install axios react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 3. Configuration des variables d'environnement
Créer `.env` dans le dossier frontend :
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_MEDIA_URL=http://localhost:8000/media
```

### 4. Lancer le serveur de développement
```bash
npm start
```

## Fonctionnalités à Implémenter

### Phase 1 - Core
- [x] Configuration de base
- [ ] Authentification (Login/Register)
- [ ] Navigation et routing
- [ ] Affichage des produits
- [ ] Panier d'achat

### Phase 2 - Avancé
- [ ] Profils utilisateurs
- [ ] Gestion des commandes
- [ ] Système de paiement
- [ ] Dashboard vendeur
- [ ] Interface d'administration

### Phase 3 - Optimisations
- [ ] Optimisation des performances
- [ ] Tests unitaires
- [ ] PWA (Progressive Web App)
- [ ] SEO et métadonnées