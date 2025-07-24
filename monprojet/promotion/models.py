from django.db import models

from monprojet.commande.models import Commande
from monprojet.produit.models import Produit
from monprojet.utilisateur.models import CustomUser

# Modele promotin

class Promotion(models.Model):
    TYPE_PROMO = (('pourcentage', 'Pourcentage'), ('montant_fixe', 'Montant fixe'), ('livraison_gratuite', 'Livraison gratuite'))
    nom = models.CharField(max_length=100)
    description = models.TextField()
    type_promotion = models.CharField(max_length=20, choices=TYPE_PROMO)
    valeur = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut = models.DateField()
    date_fin = models.DateField()
    status = models.CharField(max_length=20)


class ProduitPromotion(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)


class Coupon(models.Model):
    TYPE_COUPON = (('pourcentage', 'Pourcentage'), ('montant_fixe', 'Montant fixe'), ('livraison_gratuite', 'Livraison gratuite'))
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    type_coupon = models.CharField(max_length=20, choices=TYPE_COUPON)
    valeur = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut = models.DateField()
    date_fin = models.DateField()
    nom_utilisation = models.IntegerField()
    nombre_utiliser = models.IntegerField(default=0)
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20)


class CouponCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_utilisation = models.DateTimeField(auto_now_add=True)
