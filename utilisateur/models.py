from django.db import models
from django.contrib.auth.models import AbstractUser

# Mon modèle utilisateur


class Utilisateur(AbstractUser):
   role_choix = (
       ('client','Client'),
       ('vendeur','Vendeur'),
       ('admin','Admin'),
   )
   role = models.CharField(max_length=50, choices=role_choix)
   telephone = models.CharField(max_length=20, blank=True, null=True)