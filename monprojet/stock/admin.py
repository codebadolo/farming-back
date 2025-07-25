from django.contrib import admin
from .models import Stock, MouvementStock

# Modele pour les stocks.
admin.site.register(Stock)
admin.site.register(MouvementStock)
