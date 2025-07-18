from django.db import models

# Modele pour la metode de paiement

class Methodepaiement(models.Model):
    nom = models.CharField(max_length=40,unique=True)
def __str__(self):
    return self.nom
    
