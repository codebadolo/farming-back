from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Panier(models.Model):
    """Modèle pour le panier d'achat"""
    
    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='panier'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Panier'
        verbose_name_plural = 'Paniers'
    
    def __str__(self):
        return f"Panier de {self.utilisateur.username}"
    
    @property
    def nombre_articles(self):
        """Nombre total d'articles dans le panier"""
        return sum(item.quantite for item in self.items.all())
    
    @property
    def total(self):
        """Total du panier"""
        return sum(item.sous_total for item in self.items.all())
    
    def vider(self):
        """Vide le panier"""
        self.items.all().delete()
    
    def ajouter_produit(self, produit, quantite=1):
        """Ajoute un produit au panier ou met à jour la quantité"""
        item, created = ItemPanier.objects.get_or_create(
            panier=self,
            produit=produit,
            defaults={'quantite': quantite}
        )
        
        if not created:
            item.quantite += quantite
            item.save()
        
        return item
    
    def retirer_produit(self, produit):
        """Retire un produit du panier"""
        try:
            item = self.items.get(produit=produit)
            item.delete()
            return True
        except ItemPanier.DoesNotExist:
            return False
    
    def peut_etre_commande(self):
        """Vérifie si le panier peut être transformé en commande"""
        if not self.items.exists():
            return False, "Panier vide"
        
        for item in self.items.all():
            try:
                stock = item.produit.stock
                if not stock.peut_vendre(item.quantite):
                    return False, f"Stock insuffisant pour {item.produit.nom}"
            except:
                return False, f"Produit {item.produit.nom} non disponible"
        
        return True, "Panier valide"


class ItemPanier(models.Model):
    """Modèle pour les articles dans le panier"""
    
    panier = models.ForeignKey(
        Panier,
        on_delete=models.CASCADE,
        related_name='items'
    )
    produit = models.ForeignKey(
        'products.Produit',
        on_delete=models.CASCADE
    )
    quantite = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Article Panier'
        verbose_name_plural = 'Articles Panier'
        unique_together = ['panier', 'produit']
    
    def __str__(self):
        return f"{self.produit.nom} x{self.quantite}"
    
    @property
    def prix_unitaire(self):
        """Prix unitaire du produit (avec promotions éventuelles)"""
        return self.produit.prix_avec_promotion
    
    @property
    def sous_total(self):
        """Sous-total pour cet article"""
        return self.prix_unitaire * self.quantite
    
    def peut_augmenter_quantite(self, nouvelle_quantite=None):
        """Vérifie si on peut augmenter la quantité"""
        if nouvelle_quantite is None:
            nouvelle_quantite = self.quantite + 1
        
        try:
            stock = self.produit.stock
            return stock.peut_vendre(nouvelle_quantite)
        except:
            return False
    
    def save(self, *args, **kwargs):
        # Vérifier le stock avant de sauvegarder
        if not self.peut_augmenter_quantite(self.quantite):
            from django.core.exceptions import ValidationError
            raise ValidationError(f"Stock insuffisant pour {self.produit.nom}")
        
        super().save(*args, **kwargs)


class PanierSauvegarde(models.Model):
    """Modèle pour sauvegarder les paniers abandonnés"""
    
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='paniers_sauvegardes'
    )
    contenu = models.JSONField()
    date_sauvegarde = models.DateTimeField(auto_now_add=True)
    restaure = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Panier Sauvegardé'
        verbose_name_plural = 'Paniers Sauvegardés'
        ordering = ['-date_sauvegarde']
    
    def __str__(self):
        return f"Panier sauvegardé de {self.utilisateur.username}"
    
    @classmethod
    def sauvegarder_panier(cls, panier):
        """Sauvegarde le contenu d'un panier"""
        contenu = []
        for item in panier.items.all():
            contenu.append({
                'produit_id': item.produit.id,
                'quantite': item.quantite,
                'prix_unitaire': str(item.prix_unitaire)
            })
        
        return cls.objects.create(
            utilisateur=panier.utilisateur,
            contenu=contenu
        )
    
    def restaurer_panier(self):
        """Restaure le panier sauvegardé"""
        panier, created = Panier.objects.get_or_create(
            utilisateur=self.utilisateur
        )
        
        # Vider le panier actuel
        panier.vider()
        
        # Restaurer les articles
        from products.models import Produit
        for item_data in self.contenu:
            try:
                produit = Produit.objects.get(id=item_data['produit_id'])
                panier.ajouter_produit(produit, item_data['quantite'])
            except Produit.DoesNotExist:
                continue
        
        self.restaure = True
        self.save()
        
        return panier