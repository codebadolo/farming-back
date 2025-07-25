from rest_framework.routers import DefaultRouter
from .views import PanierViewSet, PanierItemViewSet

router = DefaultRouter()
router.register(r"paniers", PanierViewSet)
router.register(r"items", PanierItemViewSet)
urlpatterns = router.urls