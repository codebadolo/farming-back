from django.contrib import admin
from .models import Categorie, Produit, Attribut, ListeSouhait

# Modele pour les produits.
admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(Attribut)
admin.site.register(ListeSouhait)