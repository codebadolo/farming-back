from django.contrib import admin
from .models import Panier, PanierItem

# Modele pour l'application panier.
admin.site.register(Panier)
admin.site.register(PanierItem)