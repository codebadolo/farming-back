from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AdresseViewSet, ClientViewSet, VendeurViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"adresses", AdresseViewSet)
router.register(r"clients", ClientViewSet)
router.register(r"vendeurs", VendeurViewSet)

urlpatterns = router.urls