from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Commande(models.Model):
    """Modèle pour les commandes"""
    
    class Status(models.TextChoices):
        EN_ATTENTE = 'EN_ATTENTE', 'En attente'
        CONFIRMEE = 'CONFIRMEE', 'Confirmée'
        EN_PREPARATION = 'EN_PREPARATION', 'En préparation'
        EXPEDIEE = 'EXPEDIEE', 'Expédiée'
        LIVREE = 'LIVREE', 'Livrée'
        ANNULEE = 'ANNULEE', 'Annulée'
    
    numero_commande = models.CharField(max_length=50, unique=True, blank=True)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commandes'
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.EN_ATTENTE
    )
    montant_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    frais_livraison = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00')
    )
    montant_reduction = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00')
    )
    date_commande = models.DateTimeField(auto_now_add=True)
    date_livraison_estimee = models.DateTimeField(null=True, blank=True)
    date_livraison_reelle = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-date_commande']
    
    def save(self, *args, **kwargs):
        if not self.numero_commande:
            self.numero_commande = f"CMD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Commande {self.numero_commande} - {self.client.username}"
    
    @property
    def montant_final(self):
        """Montant final après réductions et frais de livraison"""
        return self.montant_total + self.frais_livraison - self.montant_reduction
    
    @property
    def nombre_articles(self):
        """Nombre total d'articles dans la commande"""
        return sum(item.quantite for item in self.items.all())
    
    def calculer_total(self):
        """Calcule le montant total de la commande"""
        total = sum(item.prix_unitaire * item.quantite for item in self.items.all())
        self.montant_total = total
        self.save()
        return total
    
    def peut_etre_annulee(self):
        """Vérifie si la commande peut être annulée"""
        return self.status in [self.Status.EN_ATTENTE, self.Status.CONFIRMEE]
    
    def annuler(self):
        """Annule la commande et remet les stocks"""
        if self.peut_etre_annulee():
            # Remettre les stocks
            for item in self.items.all():
                try:
                    stock = item.produit.stock
                    stock.ajouter_stock(item.quantite, f"Annulation commande {self.numero_commande}")
                except:
                    pass
            
            self.status = self.Status.ANNULEE
            self.save()
            return True
        return False


class ProduitCommande(models.Model):
    """Modèle pour les produits dans une commande"""
    
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='items'
    )
    produit = models.ForeignKey(
        'products.Produit',
        on_delete=models.CASCADE
    )
    quantite = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Produit Commande'
        verbose_name_plural = 'Produits Commandes'
        unique_together = ['commande', 'produit']
    
    def __str__(self):
        return f"{self.produit.nom} x{self.quantite} - {self.commande.numero_commande}"
    
    @property
    def sous_total(self):
        """Sous-total pour cet item"""
        return self.prix_unitaire * self.quantite
    
    def save(self, *args, **kwargs):
        # Sauvegarder le prix actuel du produit si pas déjà défini
        if not self.prix_unitaire:
            self.prix_unitaire = self.produit.prix
        super().save(*args, **kwargs)


class HistoriqueCommande(models.Model):
    """Modèle pour l'historique des changements de statut des commandes"""
    
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='historique'
    )
    ancien_status = models.CharField(max_length=15, blank=True)
    nouveau_status = models.CharField(max_length=15)
    commentaire = models.TextField(blank=True)
    date_changement = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Historique Commande'
        verbose_name_plural = 'Historiques Commandes'
        ordering = ['-date_changement']
    
    def __str__(self):
        return f"{self.commande.numero_commande}: {self.ancien_status} → {self.nouveau_status}"