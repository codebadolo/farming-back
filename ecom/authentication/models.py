from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """Modèle utilisateur personnalisé"""
    
    class Role(models.TextChoices):
        CLIENT = 'CLIENT', 'Client'
        VENDEUR = 'VENDEUR', 'Vendeur'
        ADMIN = 'ADMIN', 'Administrateur'
    
    class Status(models.TextChoices):
        ACTIF = 'ACTIF', 'Actif'
        INACTIF = 'INACTIF', 'Inactif'
        SUSPENDU = 'SUSPENDU', 'Suspendu'
    
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIF)
    date_inscription = models.DateTimeField(auto_now_add=True)
    telephone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        blank=True,
        null=True
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nom', 'prenom']
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class VendeurProfile(models.Model):
    """Profil vendeur avec informations business"""
    
    class StatusValidation(models.TextChoices):
        EN_ATTENTE = 'EN_ATTENTE', 'En attente'
        VALIDE = 'VALIDE', 'Validé'
        REJETE = 'REJETE', 'Rejeté'
        SUSPENDU = 'SUSPENDU', 'Suspendu'
    
    utilisateur = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='profil_vendeur'
    )
    nom_entreprise = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='logos_vendeurs/', blank=True, null=True)
    adresse = models.TextField()
    telephone_entreprise = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )
    status_validation = models.CharField(
        max_length=15, 
        choices=StatusValidation.choices, 
        default=StatusValidation.EN_ATTENTE
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Profil Vendeur'
        verbose_name_plural = 'Profils Vendeurs'
    
    def __str__(self):
        return f"{self.nom_entreprise} - {self.utilisateur.nom_complet}"


class AcheteurProfile(models.Model):
    """Profil acheteur avec préférences"""
    
    utilisateur = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='profil_acheteur'
    )
    date_naissance = models.DateField(blank=True, null=True)
    preferences_notifications = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Profil Acheteur'
        verbose_name_plural = 'Profils Acheteurs'
    
    def __str__(self):
        return f"Profil de {self.utilisateur.nom_complet}"