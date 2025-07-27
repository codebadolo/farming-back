from rest_framework.routers import DefaultRouter
from .views import (
CategorieViewSet,
ProduitViewSet,
AttributViewSet,
ListeSouhaitViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategorieViewSet)
router.register(r"produits", ProduitViewSet)
router.register(r"attributs", AttributViewSet)
router.register(r"souhaits", ListeSouhaitViewSet)

urlpatterns = router.urls