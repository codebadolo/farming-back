from django.db import models

# Modele couppon commande.

class Couponcommande(models.Model):
    commande = models.OneToOneField('Commande',on_delete=models.CASCADE)
    montant_reduction = models.DecimalField(max_digits=20,decimal_places=2)
def __str__(self):
    return f"Réduction sur commande #{self.commande.id} :{self.montant_reduction}"
