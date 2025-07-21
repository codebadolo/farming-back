from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .models import Produit

# Les modeles de mon site

# -------------------------------
# UTILISATEURS & PROFILS
# -------------------------------

class CustomUser(AbstractUser):
    ROLES = (
        ('client', 'Client'),
        ('vendeur', 'Vendeur'),
        ('admin', 'Administrateur'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='client')
    date_inscription = models.DateTimeField(auto_now_add=True)
class VendeurProfile(models.Model):
    utilisateur = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nom_entreprise = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='logos/')
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    status_validation = models.BooleanField(default=False)
class AcheteurProfile(models.Model):
    utilisateur = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    adresse_defaut = models.CharField(max_length=255, blank=True)
# -------------------------------
# PRODUITS
# -------------------------------
class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nom
class Produit(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    poids = models.FloatField()
    date_peremption = models.DateField(null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    vendeur = models.ForeignKey(VendeurProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom
class ImageProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='produits/')
class AttributProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    nom_attribut = models.CharField(max_length=100)
    valeur = models.CharField(max_length=100)

# -------------------------------
# STOCK
# -------------------------------
class Stock(models.Model):
    produit = models.OneToOneField(Produit, on_delete=models.CASCADE)
    quantite_disponible = models.IntegerField()
    seuil_alerte = models.IntegerField()
    date_mise_a_jour = models.DateTimeField(auto_now=True)
class MouvementStock(models.Model):
    TYPES_MOUVEMENT = (
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
    )
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    type_mouvement = models.CharField(max_length=10, choices=TYPES_MOUVEMENT)
    quantite = models.IntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(null=True, blank=True)

# -------------------------------
# COMMANDE
# -------------------------------
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

# -------------------------------
# PROMOTION & COUPON
# -------------------------------

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

# -------------------------------
# LIVRAISON
# -------------------------------

class Livraison(models.Model):
    MODES = (('express', 'Express'), ('standard', 'Standard'), ('retrait', 'Retrait'))
    STATUS = (('preparation', 'En préparation'), ('expedie', 'Expédié'), ('livre', 'Livré'))
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    mode_livraison = models.CharField(max_length=20, choices=MODES)
    status_livraison = models.CharField(max_length=20, choices=STATUS)
    date_envoi = models.DateField(null=True, blank=True)
    date_livraison_estimee = models.DateField(null=True, blank=True)
    suivis_colis = models.TextField(null=True, blank=True)

# -------------------------------
# PAIEMENT
# -------------------------------

class MethodePaiement(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField()
    frais_transaction = models.DecimalField(max_digits=10, decimal_places=2)


class Paiement(models.Model):
    STATUS = (('attente', 'En attente'), ('valide', 'Validé'), ('refuse', 'Refusé'))
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode_paiement = models.ForeignKey(MethodePaiement, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS)
    reference_transaction = models.CharField(max_length=100)

# -------------------------------
# PANIER
# -------------------------------

class Panier(models.Model):
    utilisateur = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveIntegerField(default=1)

class PanierItem(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
