from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Catégories
    path('categories/', views.CategorieListView.as_view(), name='categories-list'),
    path('categories/tree/', views.categories_tree_view, name='categories-tree'),
    path('categories/<slug:slug>/', views.CategorieDetailView.as_view(), name='categorie-detail'),
    
    # Produits
    path('', views.ProduitListView.as_view(), name='produits-list'),
    path('featured/', views.produits_featured_view, name='produits-featured'),
    path('mes-produits/', views.MesProduitsView.as_view(), name='mes-produits'),
    path('create/', views.ProduitCreateView.as_view(), name='produit-create'),
    path('<slug:slug>/', views.ProduitDetailView.as_view(), name='produit-detail'),
    path('<slug:slug>/update/', views.ProduitUpdateView.as_view(), name='produit-update'),
    path('<slug:slug>/delete/', views.ProduitDeleteView.as_view(), name='produit-delete'),
    path('<int:produit_id>/similaires/', views.produits_similaires_view, name='produits-similaires'),
    
    # Images et attributs
    path('<int:produit_id>/images/', views.upload_image_produit_view, name='upload-image'),
    path('<int:produit_id>/attributs/', views.add_attribut_produit_view, name='add-attribut'),
    
    # Avis
    path('<int:produit_id>/avis/', views.AvisProduitListCreateView.as_view(), name='avis-list-create'),
]