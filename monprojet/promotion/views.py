from django.shortcuts import render
from rest_framework import viewsets
from .models import Promotion, ProduitPromo, Coupon, CouponCommande
from .serializers import (
PromotionSerializer,
ProduitPromoSerializer,
CouponSerializer,
CouponCommandeSerializer,
)

# Ma vue pour l'application promotion.

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    
class ProduitPromoViewSet(viewsets.ModelViewSet):
    queryset = ProduitPromo.objects.all().select_related("produit",
    "promotion")
    serializer_class = ProduitPromoSerializer
    
class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    
class CouponCommandeViewSet(viewsets.ModelViewSet):
    queryset = CouponCommande.objects.all().select_related("commande",
    "coupon", "user")
    serializer_class = CouponCommandeSerializer