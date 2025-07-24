from django.db import models

from monprojet.commande.models import Commande

# Modele pour les paiements.

class MethodePaiement(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField()
    frais_transaction = models.DecimalField(max_digits=10, decimal_places=2)


class Paiement(models.Model):
    STATUS = (('attente', 'En attente'), ('valide', 'Validé'), ('refuse', 'Refusé'))
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode_paiement = models.ForeignKey(MethodePaiement, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS)
    reference_transaction = models.CharField(max_length=100)
