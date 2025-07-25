from django.contrib import admin
from .models import Commande, ProduitCommande

# Modele pour les commandes.
admin.site.register(Commande)
admin.site.register(ProduitCommande)
