from django.db import models

# Mon modele livraison


class Livraison(models.Model):
    
    commande = models.OneToOneField('Commande', on_delete=models.CASCADE)
    
    mode_livraison = models.CharField(max_length=100)
    
    statut = models.CharField(max_length=50)
    
    date_livraison = models.DateField(null=True, blank=True)
    
    date_envoie = models.DateField(null=True, blank=True)
    
    suivi_colis = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Livraison commande {self.commande.id}"