from django.db import models

from monprojet.utilisateur.models import VendeurProfile
from .models import Produit

# Modele pour les produits

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nom
class Produit(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    poids = models.FloatField()
    date_peremption = models.DateField(null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    vendeur = models.ForeignKey(VendeurProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom
class ImageProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='produits/')
class AttributProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    nom_attribut = models.CharField(max_length=100)
    valeur = models.CharField(max_length=100)
