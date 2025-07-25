from django.db import models
from django.conf import settings
from produit.models import Produit
from commande.models import Commande

# Modele promotion

class Promotion(models.Model):
      nom = models.CharField(max_length=255)
      type_promotion = models.CharField(max_length=50) # ex: POURCENTAGE,MONTANT
      description = models.TextField(blank=True, null=True)
      valeur = models.DecimalField(max_digits=10, decimal_places=2)
      date_debut = models.DateField()
      date_fin = models.DateField()
      statut = models.BooleanField(default=True)
      
      def __str__(self):
        return self.nom
    
class ProduitPromo(models.Model):
       produit = models.ForeignKey(Produit, on_delete=models.CASCADE,
       related_name="promotions")
       promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE,
       related_name="produits")
       
       class Meta:
         unique_together = ("produit", "promotion")
         
class Coupon(models.Model):
       code = models.CharField(max_length=100, unique=True)
       description = models.TextField(blank=True, null=True)
       type = models.CharField(max_length=50) # ex: POURCENTAGE, MONTANT
       valeur = models.DecimalField(max_digits=10, decimal_places=2)
       debut = models.DateField()
       fin = models.DateField()
       nom_utilisation = models.PositiveIntegerField(default=1)
       nombre_utilise = models.PositiveIntegerField(default=0)
       statut = models.BooleanField(default=True)
       
       def __str__(self):
           return self.code
       
class CouponCommande(models.Model):
       commande = models.ForeignKey(Commande, on_delete=models.CASCADE,
       related_name="coupons")
       coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE,
       related_name="commandes")
       user = models.ForeignKey(settings.AUTH_USER_MODEL,
       on_delete=models.CASCADE)
       date_utilisation = models.DateTimeField(auto_now_add=True)
       
       class Meta:
           unique_together = ("commande", "coupon")