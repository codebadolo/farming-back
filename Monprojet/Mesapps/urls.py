from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path
from . import views

# Urls : routes pour accéder à l'API du site avec connexion aux viewsets via le routeur DefaultRouter

router = DefaultRouter()

# Utilisateurs & Profils
router.register(r'utilisateurs', UtilisateurViewSet)
router.register(r'vendeurs', VendeurProfileViewSet)
router.register(r'acheteurs', AcheteurProfileViewSet)

# Produits
router.register(r'produits', ProduitViewSet)
router.register(r'produits-images', ProduitImageViewSet)
router.register(r'categories', CategorieViewSet)
router.register(r'attributs', AttributViewSet)

# Stock
router.register(r'stocks', StockViewSet)
router.register(r'mouvements-stock', MouvementStockViewSet)

# Commandes
router.register(r'commandes', CommandeViewSet)
router.register(r'produits-commandes', ProduitCommandeViewSet)

# Promotions
router.register(r'promotions', PromotionViewSet)
router.register(r'produits-promotions', ProduitPromotionViewSet)
router.register(r'coupons', CouponViewSet)
router.register(r'coupons-commandes', CouponCommandeViewSet)

# Livraison
router.register(r'adresses', AdresseViewSet)
router.register(r'livraisons', LivraisonViewSet)

# Paiement
router.register(r'paiements', PaiementViewSet)
router.register(r'methodes-paiement', MethodePaiementViewSet)

# Panier
router.register(r'paniers', PanierViewSet)

urlpatterns = [
    path('', include(router.urls)),
     path('', views.home, name='home'),
    path('produit/<int:produit_id>/', views.produit_detail, name='produit_detail'),
    path('panier/ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/update/<int:produit_id>/', views.update_panier, name='update_panier'),
    path('panier/modify/', views.modify_panier, name='modify_panier'),
    path('panier/delete/<int:produit_id>/', views.delete_produit_panier, name='delete_produit_panier'),
    path('souhait/ajouter/<int:produit_id>/', views.ajouter_liste_souhait, name='ajouter_liste_souhait'),
    path('boutique/', boutique, name='boutique'),
    
]
