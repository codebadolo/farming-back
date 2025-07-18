from django.db import models

# Modele pour categorie de produit

class Categorie(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self) :
        return self.nom
