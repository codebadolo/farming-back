from django.db import models
from django.conf import settings
from produit.models import Produit

# Modele reserver pour le panier.

class Panier(models.Model):
   id = models.CompositePrimaryKey()
   user = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE, related_name="paniers")
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   actif = models.BooleanField(default=True) # fermé après commande
    
   def __str__(self):
      return f"Panier #{self.id} ({self.user})"
   
@property
def total(self):
   return sum([item.sous_total for item in self.items.all()])

class PanierItem(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE,
    related_name="items")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte_produit = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
class Meta:
    unique_together = ("panier", "produit")
    
@property
def prix_unitaire(self):
   return self.produit.prix

@property
def sous_total(self):
   return self.prix_unitaire * self.qte_produit