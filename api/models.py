from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

# Model de l'app api

class APIConfiguration(models.Model):
    """Configuration spécifique à l'API"""
    api_name = models.CharField(max_length=100, default="Ecommerce API")
    is_active = models.BooleanField(default=True)
    rate_limit = models.PositiveIntegerField(default=1000)  # Requêtes/heure
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.api_name


class APIAccessToken(models.Model):
    """Gestion des tokens d'accès à l'API"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Modifiez ici aussi
        on_delete=models.CASCADE
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.token = self.generate_token() # type: ignore
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=365) # type: ignore
        super().save(*args, **kwargs)
   

class APIRequestLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Modifiez ici aussi
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.PositiveIntegerField()
    response_time = models.FloatField()
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status_code}"


class APIVersion(models.Model):
    """Gestion des versions de l'API"""
    version = models.CharField(max_length=10, unique=True)
    is_current = models.BooleanField(default=False)
    release_date = models.DateField()
    changelog = models.TextField()

    def save(self, *args, **kwargs):
        if self.is_current:
            # S'assurer qu'une seule version est marquée comme actuelle
            APIVersion.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"API v{self.version}"
