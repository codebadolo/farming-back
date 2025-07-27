from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Promotion(models.Model):
    """Modèle pour les promotions"""
    
    class TypePromotion(models.TextChoices):
        POURCENTAGE = 'POURCENTAGE', 'Pourcentage'
        MONTANT_FIXE = 'MONTANT_FIXE', 'Montant fixe'
        LIVRAISON_GRATUITE = 'LIVRAISON_GRATUITE', 'Livraison gratuite'
    
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        EXPIREE = 'EXPIREE', 'Expirée'
        SUSPENDUE = 'SUSPENDUE', 'Suspendue'
    
    nom = models.CharField(max_length=200)
    description = models.TextField()
    type_promotion = models.CharField(
        max_length=20,
        choices=TypePromotion.choices
    )
    valeur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.nom} ({self.type_promotion})"
    
    def calculer_prix_reduit(self, prix_original):
        """Calcule le prix après application de la promotion"""
        if self.type_promotion == self.TypePromotion.POURCENTAGE:
            reduction = prix_original * (self.valeur / 100)
            return prix_original - reduction
        elif self.type_promotion == self.TypePromotion.MONTANT_FIXE:
            return max(prix_original - self.valeur, Decimal('0.00'))
        return prix_original


class ProduitPromotion(models.Model):
    """Modèle pour associer des produits aux promotions"""
    
    produit = models.ForeignKey(
        'products.Produit',
        on_delete=models.CASCADE,
        related_name='promotions'
    )
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='produits'
    )
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Produit Promotion'
        verbose_name_plural = 'Produits Promotions'
        unique_together = ['produit', 'promotion']
    
    def __str__(self):
        return f"{self.produit.nom} - {self.promotion.nom}"


class Coupon(models.Model):
    """Modèle pour les coupons de réduction"""
    
    class TypeCoupon(models.TextChoices):
        MONTANT_FIXE = 'MONTANT_FIXE', 'Montant fixe'
        POURCENTAGE = 'POURCENTAGE', 'Pourcentage'
        LIVRAISON_GRATUITE = 'LIVRAISON_GRATUITE', 'Livraison gratuite'
    
    class Status(models.TextChoices):
        ACTIF = 'ACTIF', 'Actif'
        EXPIRE = 'EXPIRE', 'Expiré'
        SUSPENDU = 'SUSPENDU', 'Suspendu'
    
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    type_coupon = models.CharField(
        max_length=20,
        choices=TypeCoupon.choices
    )
    valeur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    nombre_utilisation_max = models.PositiveIntegerField(
        default=1,
        help_text="Nombre maximum d'utilisations du coupon"
    )
    nombre_utilise = models.PositiveIntegerField(default=0)
    montant_minimum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Montant minimum de commande pour utiliser le coupon"
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Si défini, le coupon n'est utilisable que par cet utilisateur"
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIF
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Coupon {self.code}"
    
    @property
    def est_utilisable(self):
        """Vérifie si le coupon peut encore être utilisé"""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.status == self.Status.ACTIF and
            self.date_debut <= now <= self.date_fin and
            self.nombre_utilise < self.nombre_utilisation_max
        )
    
    def peut_etre_utilise_par(self, utilisateur, montant_commande):
        """Vérifie si le coupon peut être utilisé par un utilisateur pour un montant donné"""
        if not self.est_utilisable:
            return False, "Coupon non utilisable"
        
        if self.utilisateur and self.utilisateur != utilisateur:
            return False, "Coupon réservé à un autre utilisateur"
        
        if montant_commande < self.montant_minimum:
            return False, f"Montant minimum requis: {self.montant_minimum}€"
        
        return True, "Coupon valide"
    
    def calculer_reduction(self, montant_commande):
        """Calcule la réduction appliquée par le coupon"""
        if self.type_coupon == self.TypeCoupon.POURCENTAGE:
            return min(montant_commande * (self.valeur / 100), montant_commande)
        elif self.type_coupon == self.TypeCoupon.MONTANT_FIXE:
            return min(self.valeur, montant_commande)
        return Decimal('0.00')
    
    def utiliser(self):
        """Marque le coupon comme utilisé"""
        self.nombre_utilise += 1
        if self.nombre_utilise >= self.nombre_utilisation_max:
            self.status = self.Status.EXPIRE
        self.save()


class CouponCommande(models.Model):
    """Modèle pour l'utilisation des coupons dans les commandes"""
    
    commande = models.ForeignKey(
        'orders.Commande',
        on_delete=models.CASCADE,
        related_name='coupons_utilises'
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name='utilisations'
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    montant_reduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    date_utilisation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Coupon Commande'
        verbose_name_plural = 'Coupons Commandes'
        unique_together = ['commande', 'coupon']
    
    def __str__(self):
        return f"Coupon {self.coupon.code} utilisé dans {self.commande.numero_commande}"