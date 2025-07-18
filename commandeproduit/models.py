from django.db import models

# Mon modele commandeProduit pour gerer les commandes avec plusieurs produits

class Commandeproduit(models.Model):
    commande = models.ForeignKey('Commande',on_delete=models.CASCADE,related_name='commande_produits')
    produit = models.ForeignKey('Produit',on_delete=models.CASCADE)
    quantite = models.PositiveBigIntegerField()
    
    def __str__(self) :
        return f"{self.produit.nom}x{self.quantite} (Commande #{self.commande.id})"
    def get_total(self): # Calcul automatique du prix total du produit dans la commande
        return self.produit.prix * self.quantite
