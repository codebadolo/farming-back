from django.db import models
from django.core.validators import MinValueValidator
from products.models import Produit


class Stock(models.Model):
    """Modèle pour la gestion du stock des produits"""
    
    produit = models.OneToOneField(
        Produit, 
        on_delete=models.CASCADE, 
        related_name='stock'
    )
    quantite_disponible = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    seuil_alerte = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(0)],
        help_text="Seuil en dessous duquel une alerte est déclenchée"
    )
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
    
    def __str__(self):
        return f"Stock de {self.produit.nom}: {self.quantite_disponible}"
    
    @property
    def en_rupture(self):
        """Vérifie si le produit est en rupture de stock"""
        return self.quantite_disponible == 0
    
    @property
    def alerte_stock(self):
        """Vérifie si le stock est en dessous du seuil d'alerte"""
        return self.quantite_disponible <= self.seuil_alerte
    
    def peut_vendre(self, quantite):
        """Vérifie si on peut vendre une certaine quantité"""
        return self.quantite_disponible >= quantite
    
    def retirer_stock(self, quantite, commentaire="Vente"):
        """Retire du stock et crée un mouvement"""
        if self.peut_vendre(quantite):
            self.quantite_disponible -= quantite
            self.save()
            
            MouvementStock.objects.create(
                produit=self.produit,
                type_mouvement=MouvementStock.TypeMouvement.SORTIE,
                quantite=quantite,
                commentaire=commentaire
            )
            return True
        return False
    
    def ajouter_stock(self, quantite, commentaire="Réapprovisionnement"):
        """Ajoute du stock et crée un mouvement"""
        self.quantite_disponible += quantite
        self.save()
        
        MouvementStock.objects.create(
            produit=self.produit,
            type_mouvement=MouvementStock.TypeMouvement.ENTREE,
            quantite=quantite,
            commentaire=commentaire
        )


class MouvementStock(models.Model):
    """Modèle pour l'historique des mouvements de stock"""
    
    class TypeMouvement(models.TextChoices):
        ENTREE = 'ENTREE', 'Entrée'
        SORTIE = 'SORTIE', 'Sortie'
        AJUSTEMENT = 'AJUSTEMENT', 'Ajustement'
        PERTE = 'PERTE', 'Perte'
    
    produit = models.ForeignKey(
        Produit, 
        on_delete=models.CASCADE, 
        related_name='mouvements_stock'
    )
    type_mouvement = models.CharField(
        max_length=15, 
        choices=TypeMouvement.choices
    )
    quantite = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    commentaire = models.TextField(blank=True)
    date_mouvement = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(
        'authentication.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Utilisateur qui a effectué le mouvement"
    )
    
    class Meta:
        verbose_name = 'Mouvement de Stock'
        verbose_name_plural = 'Mouvements de Stock'
        ordering = ['-date_mouvement']
    
    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom}: {self.quantite}"


class AlerteStock(models.Model):
    """Modèle pour les alertes de stock"""
    
    class TypeAlerte(models.TextChoices):
        RUPTURE = 'RUPTURE', 'Rupture de stock'
        SEUIL = 'SEUIL', 'Seuil d\'alerte atteint'
        PEREMPTION = 'PEREMPTION', 'Produit bientôt périmé'
    
    class StatusAlerte(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        RESOLUE = 'RESOLUE', 'Résolue'
        IGNOREE = 'IGNOREE', 'Ignorée'
    
    produit = models.ForeignKey(
        Produit, 
        on_delete=models.CASCADE, 
        related_name='alertes_stock'
    )
    type_alerte = models.CharField(
        max_length=15, 
        choices=TypeAlerte.choices
    )
    message = models.TextField()
    status = models.CharField(
        max_length=10, 
        choices=StatusAlerte.choices, 
        default=StatusAlerte.ACTIVE
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_resolution = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Alerte de Stock'
        verbose_name_plural = 'Alertes de Stock'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Alerte {self.type_alerte} - {self.produit.nom}"
    
    def resoudre(self):
        """Marque l'alerte comme résolue"""
        from django.utils import timezone
        self.status = self.StatusAlerte.RESOLUE
        self.date_resolution = timezone.now()
        self.save()