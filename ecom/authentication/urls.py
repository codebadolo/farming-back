from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Authentification
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profils
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/vendeur/', views.VendeurProfileView.as_view(), name='vendeur-profile'),
    path('profile/acheteur/', views.AcheteurProfileView.as_view(), name='acheteur-profile'),
    
    # Utilitaires
    path('change-password/', views.change_password_view, name='change-password'),
    
    # Vendeurs publics
    path('vendeurs/', views.VendeurListView.as_view(), name='vendeurs-list'),
    path('vendeurs/<int:vendeur_id>/', views.vendeur_detail_view, name='vendeur-detail'),
]