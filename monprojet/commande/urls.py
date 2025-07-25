from rest_framework.routers import DefaultRouter
from .views import CommandeViewSet, ProduitCommandeViewSet

router = DefaultRouter()
router.register(r"commandes", CommandeViewSet)
router.register(r"produits", ProduitCommandeViewSet)
urlpatterns = router.urls