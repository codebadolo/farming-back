# ECOMMERCE - Plateforme E-commerce pour Produits d'Élevage

## Description

Application web e-commerce complète développée avec Django REST Framework pour le backend et React.js pour le frontend, spécialisée dans la vente de produits d'élevage.

## Fonctionnalités

### 🔐 Authentification et Gestion des Utilisateurs
- Inscription/Connexion avec email
- Trois types d'utilisateurs : Client, Vendeur, Administrateur
- Profils personnalisés pour vendeurs et acheteurs
- Gestion des permissions par rôle

### 🛍️ Gestion des Produits
- Catalogue de produits avec catégories et sous-catégories
- Images multiples par produit
- Attributs personnalisables (couleur, taille, etc.)
- Système d'avis et de notes
- Produits mis en avant

### 📦 Gestion du Stock
- Suivi en temps réel des quantités
- Alertes de stock faible
- Historique des mouvements de stock
- Gestion des pertes et ajustements

### 🛒 Panier et Commandes
- Panier persistant
- Processus de commande complet
- Suivi des statuts de commande
- Historique des commandes

### 💳 Paiements
- Intégration Orange Money
- Gestion des méthodes de paiement
- Suivi des transactions
- Gestion des remboursements

### 🚚 Livraison
- Gestion des adresses multiples
- Modes de livraison (Standard, Express, Retrait)
- Suivi des colis
- Calcul automatique des frais

### 🎯 Promotions et Marketing
- Système de promotions flexible
- Codes de réduction (coupons)
- Promotions par pourcentage ou montant fixe
- Livraison gratuite conditionnelle

## Technologies Utilisées

### Backend
- **Django 5.2.4** - Framework web Python
- **Django REST Framework** - API REST
- **MySQL** - Base de données
- **Pillow** - Traitement d'images
- **django-cors-headers** - Gestion CORS
- **django-filter** - Filtrage avancé

### Frontend (à développer)
- **React.js** - Interface utilisateur
- **Tailwind CSS** - Framework CSS
- **Axios** - Client HTTP

## Installation et Configuration

### Prérequis
- Python 3.8+
- MySQL 8.0+
- Node.js 16+ (pour le frontend)

### 1. Configuration du Backend

```bash
# Cloner le projet
git clone <repository-url>
cd ecom

# Créer et activer l'environnement virtuel
python -m venv myvir
# Windows
myvir\Scripts\activate
# Linux/Mac
source myvir/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configuration de la base de données
# Créer la base de données MySQL 'ferme-d'
mysql -u root -p
CREATE DATABASE `ferme-d` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver
```

### 2. Configuration du Frontend (React.js)

```bash
# Dans un nouveau terminal, créer l'application React
npx create-react-app frontend
cd frontend

# Installer les dépendances
npm install axios react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Lancer le serveur de développement
npm start
```

## Structure du Projet

```
ecom/
├── source/                 # Configuration Django
├── authentication/         # Gestion des utilisateurs
├── products/              # Gestion des produits
├── stock/                 # Gestion du stock
├── orders/                # Gestion des commandes
├── payments/              # Gestion des paiements
├── promotions/            # Promotions et coupons
├── delivery/              # Livraison et adresses
├── cart/                  # Panier d'achat
├── media/                 # Fichiers uploadés
├── static/                # Fichiers statiques
├── requirements.txt       # Dépendances Python
└── manage.py             # Script de gestion Django
```

## API Endpoints

### Authentification
- `POST /api/auth/register/` - Inscription
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/logout/` - Déconnexion
- `GET /api/auth/profile/` - Profil utilisateur

### Produits
- `GET /api/products/` - Liste des produits
- `GET /api/products/{slug}/` - Détail d'un produit
- `GET /api/products/categories/` - Liste des catégories
- `GET /api/products/featured/` - Produits mis en avant

### Commandes
- `GET /api/orders/` - Mes commandes
- `POST /api/orders/` - Créer une commande
- `GET /api/orders/{id}/` - Détail d'une commande

### Panier
- `GET /api/cart/` - Contenu du panier
- `POST /api/cart/add/` - Ajouter au panier
- `DELETE /api/cart/remove/{id}/` - Retirer du panier

## Configuration de Production

### Variables d'Environnement
Créer un fichier `.env` :

```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_NAME=ferme-d
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=localhost
DATABASE_PORT=3306
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Déploiement
1. Configurer un serveur web (Nginx/Apache)
2. Utiliser Gunicorn comme serveur WSGI
3. Configurer les fichiers statiques et médias
4. Mettre en place SSL/HTTPS
5. Configurer les sauvegardes de base de données

## Tests

```bash
# Lancer les tests
python manage.py test

# Tests avec couverture
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Support

Pour toute question ou support, contactez : support@ferme-d.com

## Roadmap

- [ ] Interface d'administration avancée
- [ ] Application mobile (React Native)
- [ ] Intégration de plus de méthodes de paiement
- [ ] Système de chat en temps réel
- [ ] Analytics et rapports avancés
- [ ] API publique pour partenaires