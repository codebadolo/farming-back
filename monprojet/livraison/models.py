from django.db import models

from monprojet.commande.models import Commande

# Mon modele livraison

class Livraison(models.Model):
    MODES = (('express', 'Express'), ('standard', 'Standard'), ('retrait', 'Retrait'))
    STATUS = (('preparation', 'En préparation'), ('expedie', 'Expédié'), ('livre', 'Livré'))
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    mode_livraison = models.CharField(max_length=20, choices=MODES)
    status_livraison = models.CharField(max_length=20, choices=STATUS)
    date_envoi = models.DateField(null=True, blank=True)
    date_livraison_estimee = models.DateField(null=True, blank=True)
    suivis_colis = models.TextField(null=True, blank=True)

