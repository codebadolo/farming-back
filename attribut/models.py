from django.db import models

# Modele attribut

class Attribut(models.Model):
    produit = models.ForeignKey('Produit',on_delete=models.CASCADE,related_name='attribut')
    nom = models.CharField(max_length=100)
    valeur =models.CharField(max_length=100)
def __str__(self):
    return f"{self.nom}: {self.valeur} ({self.produit.nom})"

