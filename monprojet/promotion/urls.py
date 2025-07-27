from rest_framework.routers import DefaultRouter
from .views import (
PromotionViewSet,
ProduitPromoViewSet,
CouponViewSet,
CouponCommandeViewSet,
)
router = DefaultRouter()
router.register(r"promotions", PromotionViewSet)
router.register(r"produit-promos", ProduitPromoViewSet)
router.register(r"coupons", CouponViewSet)
router.register(r"coupon-commandes", CouponCommandeViewSet)

urlpatterns = router.urls