from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import ( # type: ignore
    TokenObtainPairView,
    TokenRefreshView,
)

"""
URL configuration for monprojet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
# Authentification
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
# Urls pour les applications

path("api/utilisateur/", include("utilisateur.urls")),
path("api/produit/", include("produit.urls")),
path("api/stock/", include("stock.urls")),
path("api/panier/", include("panier.urls")),
path("api/commande/", include("commande.urls")),
path("api/livraison/", include("livraison.urls")),
path("api/paiement/", include("paiement.urls")),
path("api/promotions/", include("promotions.urls")),
]
