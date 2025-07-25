from rest_framework import serializers
from .models import Promotion, ProduitPromo, Coupon, CouponCommande

class PromotionSerializer(serializers.ModelSerializer):
    
         class Meta:
            model = Promotion
            fields = "__all__"
            
class ProduitPromoSerializer(serializers.ModelSerializer):
    
          class Meta:
              model = ProduitPromo
              fields = "__all__"
              
class CouponSerializer(serializers.ModelSerializer):
    
          class Meta:
              model = Coupon
              fields = "__all__"
              
class CouponCommandeSerializer(serializers.ModelSerializer):
    
           class Meta:
              model = CouponCommande
              fields = "__all__"