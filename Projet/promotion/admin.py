from django.contrib import admin
from .models import Promotion,ProduitPromo, Coupon, CouponCommande

# Modele pour mon application promotion.
admin.site.register(Promotion)
admin.site.register(ProduitPromo)
admin.site.register(Coupon)
admin.site.register(CouponCommande)