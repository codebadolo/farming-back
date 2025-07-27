from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class MethodePaiement(models.Model):
    """Modèle pour les méthodes de paiement"""
    
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    frais_transaction = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='methodes_paiement/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Méthode de Paiement'
        verbose_name_plural = 'Méthodes de Paiement'
    
    def __str__(self):
        return self.nom


class Paiement(models.Model):
    """Modèle pour les paiements"""
    
    class Statut(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", "En attente"
        VALIDE = "VALIDE", "Validé"
        REFUSE = "REFUSE", "Refusé"
        REMBOURSE = "REMBOURSE", "Remboursé"
    
    reference_transaction = models.CharField(max_length=255, unique=True, blank=True)
    commande = models.OneToOneField(
        'orders.Commande', 
        on_delete=models.CASCADE,
        related_name="paiement"
    )
    methode_paiement = models.ForeignKey(
        MethodePaiement,
        on_delete=models.PROTECT, 
        related_name="paiements"
    )
    montant = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    statut = models.CharField(
        max_length=20, 
        choices=Statut.choices,
        default=Statut.EN_ATTENTE
    )
    date_paiement = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-date_paiement']
    
    def save(self, *args, **kwargs):
        if not self.reference_transaction:
            self.reference_transaction = f"PAY-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Paiement {self.reference_transaction} - {self.commande.numero_commande}"
    
    def valider(self):
        """Valide le paiement"""
        from django.utils import timezone
        self.statut = self.Statut.VALIDE
        self.date_validation = timezone.now()
        self.save()
        
        # Mettre à jour le statut de la commande
        if self.commande.status == 'EN_ATTENTE':
            self.commande.status = 'CONFIRMEE'
            self.commande.save()
    
    def refuser(self, raison=""):
        """Refuse le paiement"""
        self.statut = self.Statut.REFUSE
        if raison:
            self.notes = raison
        self.save()
        
        # Annuler la commande si nécessaire
        if self.commande.status in ['EN_ATTENTE', 'CONFIRMEE']:
            self.commande.annuler()