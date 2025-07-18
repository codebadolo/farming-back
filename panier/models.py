from django.db import models

# Modele panier pour stocker les produits ajoutes par un utilisateur

class Panier(models.Model):
    utilisateur = models.ForeignKey('Utilisateur',on_delete=models.CASCADE,related_name='panier')
    produit = models.ForeignKey('Produit',on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)
class Meta:
    unique_together = ('utilisateur','produit') # Evite d'avoir deux lignes avec le meme produit pour un meme utilisateur
def __str__(self):
    return f"{self.produit.nom}x{self.quantite} (panier de {self.utilisateur.email})"
def get_total(self):
    return self.produit.prix * self.quantite

