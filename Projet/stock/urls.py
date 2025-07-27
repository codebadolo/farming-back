from rest_framework.routers import DefaultRouter
from .views import StockViewSet, MouvementStockViewSet

router = DefaultRouter()
router.register(r"stocks", StockViewSet)
router.register(r"mouvements", MouvementStockViewSet)
urlpatterns = router.urls