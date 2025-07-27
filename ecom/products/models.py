from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Categorie(models.Model):
    """Modèle pour les catégories de produits avec support des sous-catégories"""
    
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='sous_categories'
    )
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['ordre', 'nom']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.nom} > {self.nom}"
        return self.nom
    
    @property
    def niveau(self):
        """Retourne le niveau de la catégorie (0 pour racine, 1 pour sous-catégorie, etc.)"""
        niveau = 0
        parent = self.parent
        while parent:
            niveau += 1
            parent = parent.parent
        return niveau
    
    def get_descendants(self):
        """Retourne toutes les sous-catégories (récursif)"""
        descendants = []
        for child in self.sous_categories.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants


class Produit(models.Model):
    """Modèle pour les produits"""
    
    class Status(models.TextChoices):
        BROUILLON = 'BROUILLON', 'Brouillon'
        PUBLIE = 'PUBLIE', 'Publié'
        ARCHIVE = 'ARCHIVE', 'Archivé'
        RUPTURE = 'RUPTURE', 'Rupture de stock'
    
    nom = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    categorie = models.ForeignKey(
        Categorie, 
        on_delete=models.PROTECT, 
        related_name='produits'
    )
    vendeur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='produits'
    )
    prix = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    poids = models.DecimalField(
        max_digits=8, 
        decimal_places=3, 
        blank=True, 
        null=True,
        help_text="Poids en kg"
    )
    date_peremption = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=10, 
        choices=Status.choices, 
        default=Status.BROUILLON
    )
    featured = models.BooleanField(default=False, help_text="Produit mis en avant")
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['-date_ajout']
        indexes = [
            models.Index(fields=['status', 'categorie']),
            models.Index(fields=['vendeur', 'status']),
            models.Index(fields=['featured', 'status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.nom}-{self.vendeur.id}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} - {self.vendeur.username}"
    
    @property
    def image_principale(self):
        """Retourne la première image du produit"""
        return self.images.first()
    
    @property
    def prix_avec_promotion(self):
        """Retourne le prix avec promotion si applicable"""
        # Import dynamique pour éviter les imports circulaires
        try:
            from promotions.models import ProduitPromotion
            promotion_active = ProduitPromotion.objects.filter(
                produit=self,
                promotion__status='ACTIVE',
                promotion__date_debut__lte=models.functions.Now(),
                promotion__date_fin__gte=models.functions.Now()
            ).first()
            
            if promotion_active:
                return promotion_active.promotion.calculer_prix_reduit(self.prix)
        except ImportError:
            pass
        return self.prix


class ImageProduit(models.Model):
    """Modèle pour les images des produits"""
    
    produit = models.ForeignKey(
        Produit, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='produits/')
    alt_text = models.CharField(max_length=200, blank=True)
    ordre = models.PositiveIntegerField(default=0)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Image Produit'
        verbose_name_plural = 'Images Produits'
        ordering = ['ordre', 'date_ajout']
    
    def __str__(self):
        return f"Image de {self.produit.nom}"


class AttributProduit(models.Model):
    """Modèle pour les attributs des produits (couleur, taille, etc.)"""
    
    produit = models.ForeignKey(
        Produit, 
        on_delete=models.CASCADE, 
        related_name='attributs'
    )
    nom_attribut = models.CharField(max_length=100)
    valeur = models.CharField(max_length=200)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Attribut Produit'
        verbose_name_plural = 'Attributs Produits'
        unique_together = ['produit', 'nom_attribut']
    
    def __str__(self):
        return f"{self.produit.nom} - {self.nom_attribut}: {self.valeur}"


class AvisProduit(models.Model):
    """Modèle pour les avis sur les produits"""
    
    produit = models.ForeignKey(
        Produit, 
        on_delete=models.CASCADE, 
        related_name='avis'
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    note = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    modere = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Avis Produit'
        verbose_name_plural = 'Avis Produits'
        unique_together = ['produit', 'utilisateur']
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Avis de {self.utilisateur.username} sur {self.produit.nom} ({self.note}/5)"