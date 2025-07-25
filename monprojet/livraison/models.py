from django.db import models
from commande.models import Commande

# Mon modele livraison

class Livraison(models.Model):
    class Mode(models.TextChoices):
      STANDARD = "STANDARD", "Standard"
      EXPRESS = "EXPRESS", "Express"
      
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE,
      related_name="livraison")
    commande_id=models.ForeignKey(Commande,on_delete=models.CASCADE)
    mode_livraison = models.CharField(max_length=20, choices=Mode.choices,
    default=Mode.STANDARD)
    date_livraison = models.DateField(blank=True, null=True)
    date_envoi = models.DateField(blank=True, null=True)
    suivi_colis = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
      return f"Livraison commande #{self.commande_id}"

