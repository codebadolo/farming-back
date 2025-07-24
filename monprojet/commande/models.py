from django.db import models

from monprojet.Source import settings
from monprojet.produit.models import Produit
from monprojet.utilisateur.models import CustomUser

# Modele commande

class Adresse(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    TYPE_CHOIX = (('livraison', 'Livraison'), ('facturation', 'Facturation'))
    type_adresse = models.CharField(max_length=20, choices=TYPE_CHOIX)
    rue = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    pays = models.CharField(max_length=100)
class Commande(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    adresse_livraison = models.ForeignKey(Adresse, on_delete=models.SET_NULL, null=True)
    date_livraison_estimee = models.DateField()
class ProduitCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2) 
class ListeSouhait(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='souhaits'
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='souhaits'
    )
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'produit')  # éviter les doublons

    def __str__(self):
        return f"{self.utilisateur.username} - {self.produit.nom}"
