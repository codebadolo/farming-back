from django.contrib import admin
from .models import MethodePaiement, Paiement

# Modele pour les paiements.
admin.site.register(Paiement)
admin.site.register(MethodePaiement)