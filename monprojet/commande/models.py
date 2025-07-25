from email.policy import default
from django.db import models
from django.conf import settings
from produit.models import Produit
from utilisateur.models import Adresse

# Modele commande

class Commande(models.Model):
   class Statut(models.TextChoices):
      EN_COURS = "EN_COURS", "En cours"
      PAYEE = "PAYEE", "Payée"
      LIVREE = "LIVREE", "Livrée"
      ANNULEE = "ANNULEE", "Annulée"
   client = models.ForeignKey(settings.AUTH_USER_MODEL,
   on_delete=models.CASCADE, related_name="commandes")
   date_commande = models.DateTimeField(auto_now_add=True)
   statut = models.CharField(max_length=20, choices=Statut.choices,
   default=Statut.EN_COURS)
   montant_total = models.DecimalField(max_digits=12, decimal_places=2,
   default=0) # type: ignore
   adresse_livraison = models.ForeignKey(Adresse, on_delete=models.SET_NULL,
   null=True, blank=True, related_name="commandes_livraison")
   date_livraison = models.DateField(blank=True, null=True)
   commande_id=models.CompositePrimaryKey() 
def __str__(self): # type: ignore
   return f"Commande #{self.id} ({self.client})"

class ProduitCommande(models.Model):
   commande = models.ForeignKey(Commande, on_delete=models.CASCADE,
   related_name="lignes")
   produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
   qte = models.PositiveIntegerField()
   prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
def sous_total(self):
   return self.qte * self.prix_unitaire

def __str__(self):
   return f"{self.produit} x {self.qte}"