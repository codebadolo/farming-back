from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Modele utilisateurs

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
