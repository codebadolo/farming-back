from django.db import models

from monprojet.produit.models import Produit
from monprojet.utilisateur.models import CustomUser

# Modele reserver pour le panier.

class Panier(models.Model):
    utilisateur = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveIntegerField(default=1)

class PanierItem(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)