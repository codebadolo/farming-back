from django.db import models
from commande.models import Commande

# Modele pour les paiements.

class MethodePaiement(models.Model):
     nom_methode = models.CharField(max_length=100)
     description = models.TextField(blank=True, null=True)
     frais_transaction = models.DecimalField(max_digits=10, decimal_places=2,
     default =0) # type: ignore
     
     def __str__(self):
      return self.nom_methode
  
class Paiement(models.Model):
     class Statut(models.TextChoices):
       INITIE = "INITIE", "Initié"
       SUCCES = "SUCCES", "Succès"
       ECHEC = "ECHEC", "Échec"
     reference_transac = models.CharField(max_length=255, unique=True)
     nom_methode = models.ForeignKey(MethodePaiement,
     on_delete=models.PROTECT, related_name="paiements")
     montant = models.DecimalField(max_digits=12, decimal_places=2)
     commande = models.OneToOneField(Commande, on_delete=models.CASCADE,
     related_name="paiement")
     commande_id=models.ForeignKey(Commande,on_delete=models.CASCADE)
     statut = models.CharField(max_length=20, choices=Statut.choices,
     default=Statut.INITIE)
     date_paiement = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
      return f"Paiement {self.reference_transac} - {self.commande_id}"