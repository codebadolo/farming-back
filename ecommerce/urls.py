
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'ecommerce'

urlpatterns = [
    # API
    path('api/test/', views.api_test, name='api_test'),
    # Produits
    path('api/produits/', views.ProduitListView.as_view(), name='produit-list'),
    path('api/produits/<uuid:pk>/', views.ProduitDetailView.as_view(), name='produit-detail'),
    path('api/recherche/', views.rechercher_produits, name='recherche-produits'),

    # Catégories
    path('api/categories/', views.CategorieListView.as_view(), name='categorie-list'),
    path('api/categories/<uuid:pk>/', views.CategorieDetailView.as_view(), name='categorie-detail'),
    path('api/rechercher/', views.rechercher_produits, name='rechercher-produits'),

    # URLs de paiement
    path('api/paiements/orange-money/initier/', views.initier_paiement_orange_money, name='initier_orange_money'),
    path('api/paiements/carte-bancaire/initier/', views.initier_paiement_carte_bancaire, name='initier_carte_bancaire'),
    path('api/paiements/statut/<str:transaction_id>/', views.verifier_statut_paiement, name='verifier_statut_paiement'),
    path('api/paiements/orange-money/notification/', views.notification_orange_money, name='notification_orange_money'),
]

router = DefaultRouter()
router.register(r'livraisons', views.LivraisonViewSet)
router.register(r'paiements', views.PaiementViewSet)

urlpatterns += router.urls
