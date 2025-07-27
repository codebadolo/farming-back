from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "CLIENT", "Client"
        VENDEUR = "VENDEUR", "Vendeur"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    telephone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Adresse(models.Model):
    class TypeAdresse(models.TextChoices):
        LIVRAISON = "LIVRAISON", "Livraison"
        FACTURATION = "FACTURATION", "Facturation"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adresses")
    type_adresse = models.CharField(max_length=20, choices=TypeAdresse.choices)
    rue = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.type_adresse} - {self.rue} ({self.user})"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")
    profile = models.CharField(max_length=255, blank=True, null=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Client {self.user.username}"


class Vendeur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendeur")
    entreprise = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=100, blank=True, null=True)
    statu_validation = models.BooleanField(default=False)

    def __str__(self):
        return f"Vendeur {self.entreprise} ({self.user.username})"