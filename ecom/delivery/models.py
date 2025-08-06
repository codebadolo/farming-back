from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from decimal import Decimal


class Adresse(models.Model):
    """Modèle pour les adresses de livraison et facturation"""
    
    class TypeAdresse(models.TextChoices):
        LIVRAISON = 'LIVRAISON', 'Livraison'
        FACTURATION = 'FACTURATION', 'Facturation'
    
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='adresses'
    )
    type_adresse = models.CharField(
        max_length=15,
        choices=TypeAdresse.choices
    )
    nom_complet = models.CharField(max_length=200)
    rue = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20)
    pays = models.CharField(max_length=100, default='Burkina Faso')
    telephone = models.CharField(max_length=20, blank=True)
    par_defaut = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'
        ordering = ['-par_defaut', '-date_creation']
    
    def __str__(self):
        return f"{self.nom_complet} - {self.ville}"
    
    def save(self, *args, **kwargs):
        # Si cette adresse est définie par défaut, retirer le défaut des autres
        if self.par_defaut:
            Adresse.objects.filter(
                utilisateur=self.utilisateur,
                type_adresse=self.type_adresse
            ).update(par_defaut=False)
        super().save(*args, **kwargs)


class Livraison(models.Model):
    """Modèle pour la gestion des livraisons"""
    
    class ModeLivraison(models.TextChoices):
        STANDARD = 'STANDARD', 'Standard (3-5 jours)'
        EXPRESS = 'EXPRESS', 'Express (1-2 jours)'
        RETRAIT = 'RETRAIT', 'Retrait en magasin'
    
    class StatusLivraison(models.TextChoices):
        EN_PREPARATION = 'EN_PREPARATION', 'En préparation'
        EXPEDIE = 'EXPEDIE', 'Expédié'
        EN_TRANSIT = 'EN_TRANSIT', 'En transit'
        LIVRE = 'LIVRE', 'Livré'
        ECHEC = 'ECHEC', 'Échec de livraison'
    
    commande = models.OneToOneField(
        'orders.Commande',
        on_delete=models.CASCADE,
        related_name='livraison'
    )
    adresse_livraison = models.ForeignKey(
        Adresse,
        on_delete=models.PROTECT,
        related_name='livraisons'
    )
    mode_livraison = models.CharField(
        max_length=15,
        choices=ModeLivraison.choices,
        default=ModeLivraison.STANDARD
    )
    status_livraison = models.CharField(
        max_length=15,
        choices=StatusLivraison.choices,
        default=StatusLivraison.EN_PREPARATION
    )
    date_envoi = models.DateTimeField(null=True, blank=True)
    date_livraison_estimee = models.DateTimeField(null=True, blank=True)
    date_livraison_reelle = models.DateTimeField(null=True, blank=True)
    numero_suivi = models.CharField(max_length=100, blank=True)
    transporteur = models.CharField(max_length=100, blank=True)
    frais_livraison = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00')
    )
    notes_livraison = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Livraison'
        verbose_name_plural = 'Livraisons'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Livraison {self.commande.numero_commande}"
    
    @property
    def est_livree(self):
        return self.status_livraison == self.StatusLivraison.LIVRE
    
    def calculer_frais_livraison(self):
        """Calcule les frais de livraison selon le mode"""
        if self.mode_livraison == self.ModeLivraison.RETRAIT:
            return Decimal('0.00')
        elif self.mode_livraison == self.ModeLivraison.EXPRESS:
            return Decimal('15.00')
        else:  # STANDARD
            return Decimal('5.00')


class SuiviLivraison(models.Model):
    """Modèle pour le suivi détaillé des livraisons"""
    
    livraison = models.ForeignKey(
        Livraison,
        on_delete=models.CASCADE,
        related_name='suivi'
    )
    status = models.CharField(max_length=50)
    description = models.TextField()
    localisation = models.CharField(max_length=200, blank=True)
    date_evenement = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Suivi Livraison'
        verbose_name_plural = 'Suivis Livraisons'
        ordering = ['-date_evenement']
    
    def __str__(self):
        return f"{self.livraison.commande.numero_commande} - {self.status}"