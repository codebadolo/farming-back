from django.db import models
from django.conf import settings

class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="enfants")

    def __str__(self):
        return self.nom


class Produit(models.Model):
    vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="produits")
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name="produits")

    nom = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    poids = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    peremption = models.DateField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Attribut(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="attributs")
    nom_attribut = models.CharField(max_length=100)
    valeur = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nom_attribut}: {self.valeur}"


class ListeSouhait(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="souhaits")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "produit")