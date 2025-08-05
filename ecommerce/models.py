from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

from django.utils import timezone

# Les modèles du projet basé sur le diagramme de classe

class Utilisateur(AbstractUser):
    """Modèle utilisateur personnalisé"""
    identifiant = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    telephone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=[
        ('acheteur', 'Acheteur'),
        ('vendeur', 'Vendeur')
    ])
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateur_groups',  # Nom personnalisé
        blank=True,
        verbose_name='groupes',
        help_text='Les groupes auxquels appartient l’utilisateur.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateur_permissions',  # Nom personnalisé
        blank=True,
        verbose_name='permissions utilisateur',
        help_text='Permissions spécifiques à cet utilisateur.',
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nom', 'prenom']
    
class Meta:
    db_table = 'utilisateur'  # Optionnel : pour éviter les conflits de noms de tables

class Adresse(models.Model):
    """Modèle pour les adresses"""
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='adresses')
    type_adresse = models.CharField(max_length=20, choices=[
        ('livraison', 'Livraison'),
        ('facturation', 'Facturation')
    ])
    rue = models.CharField(max_length=200)
    pays = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=100)

class Vendeur(models.Model):
    """Profil vendeur"""
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    id_vendeur = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    entreprise = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True)
    adresse = models.CharField(max_length=300)
    numero = models.CharField(max_length=20)
    statut_validation = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé')
    ], default='en_attente')

class Client(models.Model):
    """Profil client"""
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    id_client = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    profile = models.TextField(blank=True)
    localisation = models.CharField(max_length=200, blank=True)

class Categorie(models.Model):
    """Catégories de produits"""
    id_categorie = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sous_categories')
    
    def __str__(self):
        return self.nom

class Produit(models.Model):
    """Modèle produit"""
    id_produit = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    poids = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    peremption = models.DateField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE, related_name='produits')
    id_attribut = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.nom

class Image(models.Model):
    """Images des produits"""
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='produits/')
    alt_text = models.CharField(max_length=200, blank=True)
    est_principale = models.BooleanField(default=False)

class Stock(models.Model):
    """Gestion du stock"""
    id_stock = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    produit = models.OneToOneField(Produit, on_delete=models.CASCADE)
    qte_disponible = models.IntegerField(validators=[MinValueValidator(0)])
    seuil_alerte = models.IntegerField(validators=[MinValueValidator(0)], default=5)
    date_maj = models.DateTimeField(auto_now=True)

class Attribut(models.Model):
    """Attributs des produits"""
    id_attribut = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_attribut = models.CharField(max_length=100)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='attributs')
    valeur = models.CharField(max_length=200)

class Panier(models.Model):
    """Panier d'achats"""
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte_produit = models.IntegerField(validators=[MinValueValidator(1)])
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de {self.client.utilisateur.email} - {self.produit.nom}"
    
class Methode_Paiement(models.Model):
    METHODES_CHOICES = [
        ('orange_money', 'Orange Money'),
        ('carte_bancaire', 'Carte Bancaire'),
        ('especes', 'Espèces'),
        ('virement', 'Virement bancaire'),
    ]
    
    nom_methode = models.CharField(max_length=50, choices=METHODES_CHOICES)
    description = models.TextField()
    frais_transaction = models.DecimalField(max_digits=5, decimal_places=2)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return dict(self.METHODES_CHOICES).get(self.nom_methode, self.nom_methode)

class Paiement(models.Model):
    """Modèle de paiement général"""
    id_paiement = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commande = models.OneToOneField('Commande', on_delete=models.CASCADE, related_name='paiement')
    methode_paiement = models.ForeignKey(Methode_Paiement, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('reussi', 'Réussi'),
        ('echec', 'Échec'),
        ('rembourse', 'Remboursé')
    ], default='en_attente')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Paiement pour Commande {self.commande.id_commande} - {self.montant} {self.statut}"


class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traitee', 'Traitée'),
        ('livree', 'Livrée'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)

class Produit_Commande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

class PaiementOrangeMoney(models.Model):
    paiement = models.OneToOneField(Paiement, on_delete=models.CASCADE)
    numero_telephone = models.CharField(max_length=15)
    code_transaction = models.CharField(max_length=50)
    statut_orange = models.CharField(max_length=20, choices=[
        ('pending', 'En attente'),
        ('success', 'Succès'),
        ('failed', 'Échec'),
        ('cancelled', 'Annulé')
    ])
    message_retour = models.TextField(blank=True)
    date_traitement = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Orange Money: {self.numero_telephone} - {self.statut_orange}"

class PaiementCarteBancaire(models.Model):
    paiement = models.OneToOneField(Paiement, on_delete=models.CASCADE)
    numero_carte_masque = models.CharField(max_length=20)  # Ex: ****-****-****-1234
    type_carte = models.CharField(max_length=20, choices=[
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('american_express', 'American Express')
    ])
    token_paiement = models.CharField(max_length=100)  # Token sécurisé
    code_autorisation = models.CharField(max_length=10, blank=True)
    statut_banque = models.CharField(max_length=20, choices=[
        ('pending', 'En attente'),
        ('authorized', 'Autorisé'),
        ('captured', 'Capturé'),
        ('declined', 'Refusé'),
        ('cancelled', 'Annulé')
    ])
    message_banque = models.TextField(blank=True)
    date_autorisation = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Carte {self.type_carte}: {self.numero_carte_masque} - {self.statut_banque}"

class Liste_Souhait(models.Model):
    """Liste de souhaits"""
    id_produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)

class MouvementStock(models.Model):
    """Mouvements de stock"""
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='mouvements')
    type_mouvement = models.CharField(max_length=20, choices=[
        ('entree', 'Entrée'),
        ('sortie', 'Sortie')
    ])
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qte = models.IntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True)

class Promotion(models.Model):
    """Promotions"""
    id_promotion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    type_promotion = models.CharField(max_length=20, choices=[
        ('pourcentage', 'Pourcentage'),
        ('montant', 'Montant fixe')
    ])
    description = models.TextField(blank=True)
    valeur = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expiree', 'Expirée')
    ])

class Produit_Promo(models.Model):
    """Association produit-promotion"""
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

class Coupon(models.Model):
    """Coupons de réduction"""
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=[
        ('pourcentage', 'Pourcentage'),
        ('montant', 'Montant fixe')
    ])
    valeur = models.DecimalField(max_digits=10, decimal_places=2)
    debut = models.DateTimeField()
    fin = models.DateTimeField()
    nombre_utilisation = models.IntegerField(default=1)
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=[
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('expire', 'Expiré')
    ])

class CouponCommande(models.Model):
    """Utilisation des coupons"""
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_utilisation = models.DateTimeField(auto_now_add=True)