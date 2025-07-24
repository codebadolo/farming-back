from django.db import models

from monprojet.produit.models import Produit

# Mon modele pour les stocks

class Stock(models.Model):
    produit = models.OneToOneField(Produit, on_delete=models.CASCADE)
    quantite_disponible = models.IntegerField()
    seuil_alerte = models.IntegerField()
    date_mise_a_jour = models.DateTimeField(auto_now=True)
class MouvementStock(models.Model):
    TYPES_MOUVEMENT = (
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
    )
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    type_mouvement = models.CharField(max_length=10, choices=TYPES_MOUVEMENT)
    quantite = models.IntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(null=True, blank=True)
