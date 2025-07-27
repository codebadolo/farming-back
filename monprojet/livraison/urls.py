from rest_framework.routers import DefaultRouter
from .views import LivraisonViewSet

router = DefaultRouter()
router.register(r"livraisons", LivraisonViewSet)
urlpatterns = router.urls