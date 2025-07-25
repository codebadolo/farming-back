from rest_framework.routers import DefaultRouter
from .views import MethodePaiementViewSet, PaiementViewSet

router = DefaultRouter()
router.register(r"methodes", MethodePaiementViewSet)
router.register(r"paiements", PaiementViewSet)
urlpatterns = router.urls